# Estado del Arte

#### Bloque 4 — Fundamentos de *Machine Learning*.

###### 4.1.  Formulación del problema de aprendizaje supervisado.
El ***Machine Learning*** (**ML**) es el subcampo de la inteligencia artificial que estudia el diseño de algoritmos capaces de aprender patrones a partir de datos sin ser programados explícitamente para cada tarea.  En el contexto del presente TFG, la predicción de RUL se formula como un problema de **regresión supervisada**: dado un conjunto de ejemplos de entrenamiento $$\{(x_i, y_i)\}_{i=1}^{N}$$ donde $$x_i \in \mathbb{R}^d$$  es el vector de características extraídas de los sensores y $$y_i \in \mathbb{R}$$ es el valor de RUL correspondiente, el objetivo es aprender una función $$f:\mathbb{R}^d \rightarrow \mathbb{R}$$ que minimice el error de predicción sobre datos no vistos durante el entrenamiento.

La calidad del modelo se mide mediante una **función de pérdida** $$\mathcal{L}(\hat{y},y)$$ que cuantifica la discrepancia entre las predicciones $$\hat{y}=f(x)$$ y los valores reales $$y$$. Para problemas de regresión, la función de pérdida más utilizada durante el entrenamiento es el **Error Cuadrático Medio** (**MSE**, ***Mean Squared Error***):

$$\mathcal{L}_{MSE} = \frac{1}{N} \sum_{i=1}^{N} (\hat{y}_i - y_i)^2$$

La diferenciabilidad continua del MSE lo hace adecuado para la optimización mediante descenso de gradiente. Su raíz cuadrada, el **RMSE**, es la métrica de evaluación estándar en el campo de la predicción de RUL por expresar el error en las mismas unidades que la variable objetivo (ciclos de vuelo).



###### 4.2. El problema del sesgo-varianza (*Bias-Variance Tradeoff*).
El error de generalización de cualquier modelo de ML puede descomponerse en tres términos independientes:

$$\mathbb{E}[(\hat{y} - y)^2] = \text{Bias}^2 + \text{Varianza} + \text{Ruido irreducible}$$

El **sesgo** (*bias*) cuantifica el error sistemático introducido por las simplificaciones del modelo respecto al proceso real que genera los datos. Un modelo con sesgo elevado no captura la complejidad subyacente del fenómeno (***underfitting***). La **varianza** cuantifica la sensibilidad del modelo a las fluctuaciones del conjunto de entrenamiento. Un modelo con varianza elevada memoriza los datos de entrenamiento incluyendo su ruido, perdiendo capacidad de generalización a datos nuevos (***overfitting***).

En el contexto de predicción de RUL sobre el N-CMAPSS 2, este compromiso presenta especial relevancia: el dataset ofrece alta variabilidad operativa entre subconjuntos y entre unidades de entrenamiento y test, por lo que los modelos deben ser suficientemente complejos para capturar los patrones de degradación no lineales pero debidamente regulados para generalizar fuera de la distribución de entrenamiento.

Con objeto de gestionar dicho compromiso, aplicamos técnicas de control destacando la **regularización** (penalización de complejidad del modelo), ***dropout*** (desactivación aleatoria de neuronas durante el entrenamiento) y ***early stopping*** (detención del entrenamiento en caso de estancamiento del error de validación).



###### 4.3. Pipeline de preprocesado para series temporales multivariantes.
Los datos de motores *turbofan* son series temporales multivariantes: secuencias ordenadas de vectores de observación $$x^{(t)} \in \mathbb{R}^d$$ siendo el índice $$t$$ esencial para la predicción. El *pipeline* estándar de preprocesado en la literatura de predicción de RUL sobre C-MAPSS y N-CMAPSS comprende las siguientes etapas [@wang2021remaining]:

**Selección de características.** Cabe diferenciar las señales de estimación de RUL verdaderamente **informativas** de aquéllas típicas de ruido de entrada, como valores constantes o variaciones irregulares atípicas a las tendencias de degradación. La selección puede realizarse mediante **análisis de correlación** con la variable objetivo, métricas de calidad del HI (monotonicidad, tendencialidad) o métodos de importancia de características como *Random Forest* [@fan2024advancing].

**Normalización.** Técnicas estándar que garantizan la contribución equitativa de todas las variables al aprendizaje del modelo pese a la heterogeneidad de rangos de magnitud presente en N-CMAPSS. Dichas técnicas corresponden a normalización *Min-Max* y estandarización *Z-Score*:

$$x_{norm} = \frac{x - x_{min}}{x_{max} - x_{min}}$$   (*Min-Max*)

$$x_{std} = \frac{x - \mu}{\sigma}$$  (*Z-Score*)

donde $$\mu$$ y $$\sigma$$ son la media y desviación típica del conjunto de entrenamiento respectivamente. Tanto el escalador *Min-Max* como el *Z-score* se ajustan exclusivamente sobre los datos de entrenamiento y se aplican posteriormente al conjunto de test, evitando así la **fuga de datos** (*data leakage*): la filtración de información del conjunto de test al proceso de entrenamiento constituye uno de los errores metodológicos más frecuentes en la literatura y produce estimaciones de rendimiento artificialmente optimistas [@chen2023changepoint].

**Generación de ventanas temporales deslizantes.** Las redes neuronales recurrentes y convolucionales requieren que los datos de series temporales se transformen en secuencias de longitud fija. El método estándar es la **ventana deslizante** (*sliding window*): dado un parámetro de tamaño de ventana $$w$$, generamos secuencias solapadas $$[x^{(t-w+1)},...,x^{(t)}]$$ etiquetadas con el valor de RUL en el instante $$t$$ [@zhou2020automatic]. El tamaño de ventana es un hiperparámetro que determina la cantidad de historia temporal que el modelo puede utilizar para hacer su predicción.

$$\text{Muestra}_t = \{[x^{(t-w+1)}, \ldots, x^{(t)}], \; RUL(t)\}$$

**Partición ***train/validation/test***.** La partición de los datos debe realizarse por unidad de motor, no por ciclo, para garantizar que el modelo se evalúa sobre trayectorias de degradación completas no vistas durante el entrenamiento. La práctica estándar utiliza el conjunto de validación para la selección de hiperparámetros y *early stopping*, y el conjunto *test* exclusivamente para la evaluación final.



###### 4.4. Optimización: descenso de gradiente y el optimizador Adam.
El entrenamiento de modelos de *Deep Learning* consiste en minimizar la función de pérdida $$\mathcal{L}$$ respecto a los parámetros del modelo $$\theta$$ mediante **descenso de gradiente estocástico (SGD)**:

$$\theta_{t+1} = \theta_t - \eta \nabla_\theta \mathcal{L}(\theta_t)$$

donde $$\eta$$ es la **tasa de aprendizaje** (*learning rate*), el hiperparámetro más crítico del proceso de entrenamiento. El optimizador más utilizado en la literatura de predicción de RUL es **Adam** (*Adaptive Moment Estimation*), que combina dos mecanismos: el uso de momentos de primer orden (media del gradiente) para acelerar la convergencia, y el uso de momentos de segundo orden (varianza del gradiente) para adaptar la tasa de aprendizaje de forma individual para cada parámetro:

$$m_t = \beta_1 m_{t-1} + (1-\beta_1)\nabla_\theta \mathcal{L}$$

$$v_t = \beta_2 v_{t-1} + (1-\beta_2)(\nabla_\theta \mathcal{L})^2$$

$$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$

donde $$\beta_1 = 0.9$$ y $$\beta_2 = 0.999$$ son los hiperparámetros de decaimiento de los momentos; $$\hat{m}_t$$ y $$\hat{v}_t$$ son las estimaciones corregidas por sesgo de los momentos; y $$\epsilon$$ es una constante de estabilidad numérica [@kingma2015adam]. La principal ventaja de Adam sobre SGD estándar en el contexto de la predicción de RUL es su robustez frente a gradientes dispersos y su menor sensibilidad a la elección de la tasa de aprendizaje inicial.



###### 4.5. Regularización y técnicas de control del sobreajuste.
En modelos de *Deep Learning* aplicados a datasets de tamaño moderado como N-CMAPSS 2, el sobreajuste constituye un riesgo real. Presentamos las técnicas de regularización adoptadas en la literatura de predicción de RUL:

***Dropout***. Durante el entrenamiento, cada neurona se desactiva de forma aleatoria con probabilidad $$p$$ en cada paso de actualización. Impide la dependencia excesiva del modelo con características individuales y fuerza el aprendizaje de representaciones más robustas. En la fase de inferencia, todas las neuronas permanecen activas y sus pesos se escalan por $$(1-p)$$.

***Early stopping.*** Detención del entrenamiento cuando el error de validación deja de decrecer durante un número predefinido de épocas consecutivas (***patience***). Previene el sobreajuste sin necesidad de definir *a priori* el número de épocas de entrenamiento.

**Regularización L2 (***weight decay***).** Añade un término de penalización a la función de pérdida proporcional a la norma cuadrada de los parámetros del modelo, desincentivando pesos de gran magnitud que suelen asociarse a sobreajuste:

$$\mathcal{L}_{reg} = \mathcal{L}_{MSE} + \lambda \|\theta\|_2^2$$

donde $$\lambda$$ es el coeficiente de regularización.