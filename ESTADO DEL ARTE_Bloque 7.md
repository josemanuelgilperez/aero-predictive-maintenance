# Estado del Arte

#### Bloque 7 — Sistemas Híbridos Jerárquicos: Clasificación de Modo de Fallo y Modelos Especializados.

###### 7.1. Motivación: insuficiencia de los modelos universales de RUL.
Los modelos de predicción de RUL descritos en el Bloque 6 —LSTM, Bi-LSTM y CNN-LSTM— se entrenan habitualmente sobre el conjunto completo del dataset, asumiendo implícitamente que una única función de mapeo $$f: X_s \rightarrow RUL$$ es suficiente para capturar la heterogeneidad de los patrones de degradación presentes en todos los modos de fallo. Esta asunción es cuestionable en el contexto del N-CMAPSS 2, cuyos ocho subconjuntos representan siete modos de fallo con estructuras de degradación intrínsecamente distintas: un fallo aislado de HPT (DS01) genera una firma de sensores cualitativamente diferente a un fallo combinado HPT+LPT (DS03) o a un fallo de fan (DS04).

Los modelos de pronóstico existentes para sistemas con múltiples modos de fallo típicamente siguen un enfoque en dos etapas: primero, la clasificación o identificación de los modos de fallo a partir de las señales de degradación; segundo, la construcción de un modelo de pronóstico específico para cada modo de fallo identificado con objeto de predecir la RUL. Sin embargo, este método encuentra varios desafíos prácticos en aplicaciones reales: la primera dificultad es el solapamiento de las señales de degradación debido a fuentes de deterioro ambiguas. [@li2024rul_uncertain]

Esta observación fundamenta la arquitectura del sistema híbrido jerárquico implementado en el presente TFG: en lugar de un único modelo universal, se propone una estructura en dos niveles que clasifica primero el modo de fallo y aplica después el modelo de predicción de RUL más adecuado para ese modo específico.



###### 7.2. Paradigma de Mezcla de Expertos (*Mixture of Experts*).
El fundamento teórico del sistema híbrido jerárquico reside en el paradigma de **Mezcla de Expertos** (*Mixture of Experts*, **MoE**), introducido formalmente por Jacobs, Jordan, Nowlan y Hinton en 1991 [@jacobs1991moe]. El principio central es la sustitución de un único modelo generalista por un conjunto de modelos especializados (*expertos*), cada uno de los cuales aprende a manejar un subconjunto del espacio de entrada, gobernados por una **red de enrutamiento** (*gating network*) que determina qué experto activar para cada instancia de entrada.

La salida del sistema MoE se formula como la combinación ponderada de las predicciones de los $$K$$ expertos:

$$\hat{y}_{MoE} = \sum_{k=1}^{K} g_k(x) \cdot E_k(x)$$

donde $$E_k(x)$$ es la predicción del $$k \text {-ésimo}$$ experto y $$g_k(x)$$ es el peso asignado por la red de enrutamiento, con la restricción: 

$$\sum_{k=1}^{K} g_k(x) = 1, \quad g_k(x) \geq 0 \quad \forall k$$

La red de enrutamiento se implementa habitualmente mediante una capa densa de activación ***softmax***:

$$g(x) = \text{softmax}(W_g x + b_g)$$

donde $$W_b$$ y $$b_g$$ son los parámetros entrenables de la red de enrutamiento. En el caso de enrutamiento ***hard routing***, la red selecciona el experto con mayor peso $$k^*=\text{arg max}_k g_k(x)$$ y descarta la contribución del resto:

$$\hat{y}_{hard} = E_{k^*}(x)$$

Esta variante es la adoptada en el sistema híbrido jerárquico del presente TFG: el clasificador de modo de fallo actúa como red de enrutamiento duro que dirige cada instancia al modelo de RUL especializado en el modo de fallo identificado.



###### 7.3. El clasificador de modo de fallo como red de enrutamiento.
El primer nivel del sistema jerárquico es un clasificador de modo de fallo cuya función es asignar cada trayectoria de degradación a uno de los $$K$$ modos de fallo definidos en el N-CMAPSS 2. Formalmente, dado el vector de señales de sensores $$X_s^i$$ de la unidad $$i$$, el clasificador aprende la función:

$$\hat{m}^i = c(X_s^i) \in \{1, 2, \ldots, K\}$$

donde $$\hat{m}^i$$ es el modo de fallo predicho. La calidad del clasificador se evalúa mediante precisión (*accuracy*), precisión por clase (*precision*), exhaustividad (*recall*) y puntuación F1 (*F1-score*) sobre un conjunto de test balanceado entre modos de fallo.

La característica fundamental del N-CMAPSS 2 que hace viable esta clasificación es la afectación de diferentes modos de fallo a componentes distintos del motor, generando **firmas de sensor** diferenciadas. Un fallo de HPT se manifiesta preferentemente en el incremento de la EGT y en la variación de la relación de expansión de la turbina; un fallo de LPT impacta en la velocidad del eje de baja presión y en la eficiencia de la turbina de baja; un fallo de fan modifica las presiones y temperaturas en la entrada del motor. Esta discriminabilidad física entre modos de fallo es la que sustenta la viabilidad de la clasificación a partir de señales de sensores. [@liu2023deeplearning_fdp]

Un modelo híbrido CNN-Transformer aplicado al dataset CMAPSS para identificación de fallos logra precisiones superiores al 97% bajo condiciones de operación únicas y múltiples, demostrando la robustez y adaptabilidad de las arquitecturas híbridas para la clasificación de modos de fallo a partir de señales de sensores multivariantes. [@chen2023faultid]



###### 7.4. Modelos especializados por modo de fallo.
El segundo nivel del sistema jerárquico está compuesto por siete **modelos de predicción de RUL**, cada uno entrenado exclusivamente sobre el subconjunto del N-CMAPSS 2 correspondiente a su modo de fallo asignado (DS01, DS03–DS08), cuyas estructuras de degradación quedan completamente descritas en la sección 3.5. Cada modelo aprende la función de mapeo:

$$f_m: X_s^i \rightarrow \hat{RUL}^i, \quad m \in \{1, 2, \ldots, 7\}$$

específica para la geometría de degradación de su componente afectado, permitiendo que las representaciones internas capturen la dinámica particular de cada modo de fallo sin interferencia de los patrones de degradación de los demás modos.

La justificación de esta especialización reside en la heterogeneidad física de los procesos de degradación entre subconjuntos. Cada modo de fallo afecta a un subconjunto diferente de componentes rotativos del motor, generando firmas de sensor cualitativamente distintas que un modelo universal no puede capturar simultáneamente con la misma precisión que un modelo especializado [@wei2024star]. Un modelo entrenado sobre el conjunto completo del dataset queda expuesto a la interferencia entre patrones de degradación de naturaleza física distinta, lo que introduce sesgo en las estimaciones de RUL para cada modo individual.

La especialización por modo de fallo tiene además una implicación directa sobre la **selección de características**: el conjunto óptimo de sensores para predecir RUL no es idéntico entre modos de fallo. El análisis de importancia mediante *Random Forest* aplicado independientemente sobre cada subconjunto permite identificar qué sensores son más informativos para cada tipo de degradación, aportando conocimiento técnico accionable sobre la relación entre la instrumentación del motor y el componente en fallo. [@baptista2022semisuper]

El entrenamiento de cada modelo especializado se realiza de forma independiente sobre su subconjunto correspondiente, utilizando el mismo pipeline de preprocesado, normalización y ventana deslizante descrito en el ***Capítulo 3 (Metodología)***, garantizando así la comparabilidad directa entre los siete modelos especializados y los modelos de referencia entrenados sobre el dataset completo.



###### 7.5. Arquitectura integrada del sistema jerárquico.
La arquitectura completa del sistema híbrido jerárquico sigue el flujo:

$$X_s^i \xrightarrow{\text{Clasificador}} \hat{m}^i \xrightarrow{\text{Enrutamiento}} \text{Modelo}_{{\hat{m}^i}} \xrightarrow{} \hat{RUL}^i$$

El proceso de inferencia para una nueva unidad $$i$$ procede en tres etapas secuenciales:

**Etapa 1 — Clasificación del modo de fallo.** El clasificador procesa las señales de sensores de los primeros $$t_0$$ ciclos de la unidad y genera una estimación del modo de fallo $$\hat{m}^i$$. El parámetro $$t_0$$ representa el horizonte mínimo de observación necesario para que las señales de degradación sean suficientemente discriminativas.

**Etapa 2 — Enrutamiento al modelo especializado.** La estimación $$\hat{m}^i$$ determina qué modelo de predicción de RUL se activa para esa unidad. En el caso de enrutamiento duro, se selecciona el modelo $$\text{Modelo}_{\hat{m}^i}$$ con exclusión del resto.

**Etapa 3 — Predicción de RUL especializada.** El modelo seleccionado genera la estimación $$\hat{RUL}^i(t)$$ para cada instante $$t > t_0$$ de la trayectoria de la unidad.

La función de pérdida durante el entrenamiento del sistema integrado combina la pérdida de clasificación y la pérdida de regresión en un objetivo conjunto:

$$\mathcal{L}_{total} = \alpha \cdot \mathcal{L}_{clf} + (1 - \alpha) \cdot \mathcal{L}_{RUL}$$

donde $$\mathcal{L}_{clf}$$ es la entropía cruzada del clasificador, $$\mathcal{L}_{RUL}$$ es el MSE del modelo de RUL especializado activado y  $$\alpha \in [0,1]$$ es el hiperparámetro de ponderación entre ambos objetivos.



###### 7.6. Desafíos y limitaciones del enfoque jerárquico.
Pese a sus ventajas, el sistema híbrido jerárquico presenta desafíos técnicos que deben reconocerse explícitamente:

**Propagación de errores de clasificación.** Un error en la etapa de clasificación del modo de fallo conduce al enrutamiento de la unidad hacia el modelo incorrecto, generando predicciones de RUL sistemáticamente sesgadas. Este efecto de *error cascading* es la limitación estructural más crítica del enfoque en dos etapas y justifica la necesidad de un clasificador de alta precisión en el primer nivel.

**Señales de degradación solapadas**. Las señales de degradación suelen originarse en sensores instalados en el exterior de las máquinas, que pueden capturar efectos de degradación solapados de múltiples componentes internos. Por ejemplo, un sensor de vibración en una caja de engranajes podría detectar señales influenciadas tanto por engranajes como por rodamientos, complicando la tarea de atribuir la degradación a una fuente específica. En motores *turbofan*, sensores instalados en posiciones intermedias del *gas path* pueden reflejar **simultáneamente** la degradación de componentes aguas arriba y aguas abajo, dificultando la discriminación entre modos de fallo.[@li2024rul_uncertain]

**Disponibilidad de etiquetas de modo de fallo.** En el N-CMAPSS 2 las etiquetas de modo de fallo están disponibles en las variables auxiliares del *dataset* de desarrollo pero no en el de *test*, obligando al clasificador a ser completamente autónomo en producción y sólo poder ser evaluado indirectamente a través del rendimiento del sistema completo.