# Estado del Arte

#### Bloque 6 — Arquitecturas de Deep Learning: LSTM, Bi-LSTM y CNN-LSTM.

###### 6.1. Redes Neuronales Recurrentes y el problema del gradiente evanescente.
Las **Redes Neuronales Recurrentes** (*Recurrent Neural Networks*, **RNN**) son arquitecturas diseñadas para procesar secuencias de datos manteniendo un estado oculto $$h_t$$ que encapsula la información de los pasos temporales anteriores. En cada instante $$t$$, el estado oculto se actualiza como:

$$h_t = \tanh(W_h h_{t-1} + W_x x_t + b)$$

donde $$W_h$$ y $$W_x$$ son matrices de pesos y $$b$$ es el vector de sesgo. El entrenamiento se realiza mediante **retropropagación a través del tiempo** (*Backpropagation Through Time*, BPTT), que consiste en desenrollar la red en el eje temporal y aplicar la regla de la cadena hacia atrás. El gradiente de la función de pérdida respecto a los parámetros de un paso temporal $$k$$ pasos atrás involucra el producto de $$k$$ matrices jacobianas [@ghojogh2023rnn]:

$$\frac{\partial \mathcal{L}_t}{\partial h_k} = \frac{\partial \mathcal{L}_t}{\partial h_t} \prod_{i=k+1}^{t} \frac{\partial h_i}{\partial h_{i-1}}$$

Cuando los valores propios dominantes de estas matrices son sistemáticamente menores que 1, el gradiente decae exponencialmente con la distancia temporal: este es el **problema del gradiente evanescente** (*vanishing gradient*), identificado formalmente por Bengio, Simard y Frasconi en 1994. Las RNN estándar son incapaces de aprender dependencias de largo alcance en secuencias extensas, inadecuándolas en el modelo del proceso de degradación acumulativa de un motor *turbofan*, donde su estado actual depende del historial operativo previo. [@bengio1994vanishing]



###### 6.2. *Long Short-Term Memory* (LSTM).
La arquitectura LSTM fue introducida por Hochreiter y Schmidhuber en 1997 como solución estructural al problema del gradiente evanescente. Su innovación fundamental es la introducción de una **celda de estado $$C_t$$** que actúa como memoria a largo plazo protegida por tres puertas de información, cuyas conexiones aditivas garantizan el flujo de gradiente sin atenuación exponencial [@hochreiter1997lstm].

###### 6.2.1. Ecuaciones de celda LSTM.
Dado el vector de entrada $$x_t \in \mathbb{R}^d$$ en el instante $$t$$ y el estado oculto previo $$h_{t-1}$$, la celda LSTM computa secuencialmente:

**Puerta de olvido (***forget gate***).** Determina qué fracción de la celda de estado anterior se retiene:

$$f_t = \sigma(W_f [h_{t-1}, x_t] + b_f)$$

**Puerta de entrada (***input gate***).** Controla qué nueva información se escribe en la celda de estado:

$$i_t = \sigma(W_i [h_{t-1}, x_t] + b_i)$$

$$\tilde{C}_t = \tanh(W_C [h_{t-1}, x_t] + b_C)$$

**Actualización de la celda de estado.** Combinación de la memoria retenida con la nueva información mediante conexiones aditivas:

$$C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$$

**Puerta de salida (***output gate***).** Determina qué parte de la celda de estado se expone como estado oculto:

$$o_t = \sigma(W_o [h_{t-1}, x_t] + b_o)$$

$$h_t = o_t \odot \tanh(C_t)$$

donde $$\sigma(\cdot)$$ es la función sigmoide, $$\tanh(\cdot)$$ es la tangente hiperbólica y $$\odot$$ denota el producto elemento a elemento (*Hadamard product*). El mecanismo de celda de estado con conexiones aditivas —en lugar de multiplicativas como en las RNN estándar— es el que resuelve el gradiente evanescente: el gradiente puede fluir hacia atrás a través de la celda sin atenuación exponencial.

###### 6.2.2. Aplicación a la predicción de RUL.
LSTM es especialmente adecuadas para modelar la degradación de motores *turbofan* gracias a las dependencias temporales de largo alcance: el estado actual del motor no depende únicamente de los ciclos inmediatamente anteriores sino de toda la historia acumulada de condiciones de operación. LSTM procesa la secuencia de vectores de sensores generada por la ventana deslizante, produciendo en el estado oculto final $$h_T$$ una representación del estado de degradación acumulado, que se proyecta al espacio escalar de RUL mediante capas densas (*fully connected*).

No obstante, LSTM presenta limitaciones reconocidas en la literatura específica de predicción de RUL: su elevado coste computacional y requerimiento de memoria la hacen ineficiente para aplicaciones en tiempo real, y puede seguir sufriendo atenuación del gradiente para secuencias de ciclos operativos extremadamente largas, dificultando la captura de patrones de degradación complejos en horizontes de predicción extendidos [@ayodeji2024lstm].



###### 6.3. *Bidirectional LSTM* (Bi-LSTM).
La arquitectura **Bi-LSTM** fue propuesta por Schuster y Paliwal en 1997, extendiéndola al procesado simultáneo de la secuencia en dos direcciones: una LSTM directa (*forward*) que procesa de $$t=1$$ a $$t=T$$ y una LSTM inversa (*backward*) de $$t=T$$ a $$t=1$$. Los estados ocultos de ambas direcciones se concatenan en cada instante:

$$\overrightarrow{h_t} = \text{LSTM}_{fwd}(x_t, \overrightarrow{h_{t-1}})$$

$$\overleftarrow{h_t} = \text{LSTM}_{bwd}(x_t, \overleftarrow{h_{t+1}})$$

$$h_t^{Bi} = [\overrightarrow{h_t}\, ;\, \overleftarrow{h_t}]$$

La justificación del procesado bidireccional en el contexto de predicción de RUL reside en la causalidad (la historia pasada determina el estado presente) y contextualidad (patrones observados en ciclos posteriores de la ventana pueden informar la interpretación de estados anteriores, especialmente en la detección de puntos de inflexión de la trayectoria de degradación) de patrones de degradación de ventanas de observación fijas [@sherifi2024blstm]. 

Bi-LSTM ha demostrado mejoras consistentes sobre la LSTM unidireccional en condiciones operativas variables, con una mejora del 27,8% en la predicción de RUL respecto a modelos de *Deep Learning* convencionales en evaluaciones sobre el *dataset* C-MAPSS bajo condiciones de cambio de punto [@chen2025bilstm]. Su principal limitación es el coste computacional y paramétrico aproximadamente doble respecto a la LSTM unidireccional, pudiendo dificultar el entrenamiento en *datasets* de escala moderada sin técnicas adecuadas de regularización.



###### 6.4. *Convolutional Neural Network — LSTM* (CNN-LSTM).
La arquitectura CNN-LSTM combina en una **estructura híbrida secuencial** las capacidades de extracción de características locales de las redes convolucionales con la modelización de dependencias temporales de largo alcance de las LSTM, superando las limitaciones individuales de cada paradigma: las CNN capturan bien las correlaciones locales multivariantes pero no modelan dependencias de largo alcance; las LSTM procesan la secuencia completa pero pueden no capturar eficientemente las correlaciones locales entre sensores.

###### 6.4.1. Bloque convolucional 1D.
Las redes convolucionales unidimensionales (1D-CNN) aplican filtros a lo largo del eje temporal, extrayendo patrones locales y correlaciones entre sensores en ventanas reducidas [@liu2022tddn]. Para una secuencia $$X \in \mathbb{R}^{w×d}$$ y el filtro $$k \text{-ésimo}$$ $$F_k \in \mathbb{R}^{l×d}$$ de longitud $$l$$, la operación de convolución produce el mapa de características:

$$z_k^{(t)} = \text{ReLU}\left(\sum_{j=0}^{l-1} X_{t+j} \cdot F_k^{(j)} + b_k\right)$$

La capa de ***max-pooling*** temporal reduce la dimensionalidad reteniendo el valor máximo en cada ventana, proporcionando invariancia traslacional local y comprimiendo la representación antes de la LSTM.

###### 6.4.2. Arquitectura integrada y flujo de información.
El flujo en la arquitectura CNN-LSTM sigue el patrón secuencial:

$$X \xrightarrow{\text{Conv1D}} Z \xrightarrow{\text{MaxPool}} Z' \xrightarrow{\text{LSTM}} h_T \xrightarrow{\text{Dense}} \hat{RUL}$$

El bloque convolucional actúa como extractor de características automático que aprende representaciones de los patrones locales de degradación multi-sensor, eliminando la necesidad de ingeniería de características manual. La LSTM subsiguiente modela las dependencias temporales entre estas representaciones a lo largo de la secuencia. Este modelo híbrido representa actualmente el paradigma más extendido en la literatura de predicción de RUL sobre datasets C-MAPSS y N-CMAPSS, con reducciones de RMSE del orden del 17% y mejoras del 25% en la función de puntuación respecto a modelos CNN o LSTM puros [@li2022cnnlstm]. Un estudio comparativo sobre el C-MAPSS reporta para la CNN-LSTM con mecanismo de atención valores de RMSE de 15,98, 14,45, 13,91 y 16,64 sobre los cuatro subconjuntos FD001-FD004, ilustrando los beneficios del aprendizaje jerárquico de características combinado con modelado temporal [@kim2021cnnlstm].