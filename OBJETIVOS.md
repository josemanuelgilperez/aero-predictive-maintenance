# Objetivos

Respondiendo a las limitaciones identificadas en la literatura, se procede al desarrollo de diferentes modelos de *Deep Learning* y *Machine Learning*, con objeto de satisfacer las necesidades actuales de **determinación de fallo** de componentes de turbofan. En consecuencia, se establecen los presentes objetivos, formulados en concordancia con los criterios ***SMART*** recomendados.

- **Objetivo 1 -** ***Revisión y selección de datos***. Revisión sistemática de datasets públicos disponibles en base a la predicción de ***RUL*** en motores turbofan, evaluando así su idoneidad en función de la representatividad de las condiciones reales de operación, volumen de datos, diversidad de modos de fallo y la disponibilidad pública de éstos, seleccionando el *benchmark* más adecuado para el correcto desarrollo del proyecto.

- **Objetivo 2 -** ***Análisis exploratorio y comprensión del dataset seleccionado.*** Estudio de la estructura, variables y posibles modos de fallo del dataset **NASA N-CMAPSS 2**, caracterizando las distribuciones de trayectorias de degradación, variabilidad operativa entre subconjuntos y relaciones establecidas entre señales de  sensores y  el proceso de deterioro de componentes rotativos.

- **Objetivo 3 -** ***Diseño e implementación del*** **pipeline** ***de procesado.*** Desarrollo de un *pipeline* reproducible de procesado, incluyendo limpieza y normalización de datos, generación de ventanas temporales y construcción de la variable objetivo ***RUL***, garantizando simultáneamente su aplicabilidad uniforme a los cuatro modelos comparados.

- **Objetivo 4 -** ***Selección de características diferenciadoras en función del modo de fallo.*** Identificación de relevancia informativa de los sensores para la estimación de ***RUL*** en función del modo de degradación consecuente (**HPT** y **HPT+LPT**), mediante la importancia de características del modelo Random Forest, determinando si el conjunto óptimo de sensores varía según el tipo de fallo.

- **Objetivo 5 -** ***Implementación y entrenamiento de los cuatro modelos.*** Desarrollo, entrenamiento y ajuste de los modelos de *Deep Learning* y *Machine Learning* ***Random Forest***, ***LSTM***, ***Bi-LSTM*** y ***CNN-LSTM*** sobre el dataset completo *N-CMAPSS 2*, documentándose las decisiones de diseño arquitectónico e hiperparámetros seleccionados en cada modelo.

- **Objetivo 6 -** ***Evaluación comparativa del rendimiento predictivo.*** Evaluación y comparación del rendimiento de los cuatro modelos aplicando métricas estándar de campo (***RMSE*** y ***función de puntuación asimétrica de la NASA***), pudiendo identificar la arquitectura con mayor precisión y robustez bajo condiciones de alta variabilidad operativa.

- **Objetivo 7 -** ***Análisis de interpretabilidad mediante*** **SHAP.** Aplicación de la metodología de análisis ***SHAP*** a los distintos modelos con objeto de identificar el respaldo proporcionado por cada sensor en función de la arquitectura implementada, comparando patrones de degradación capturados por cada enfoque y evaluando las variaciones de relevancia de cada sensor en base a la evolución de los ciclos de vida del motor.

Quedan exentos del alcance del proyecto la validación sobre datos de motores reales en operación, el despliegue del sistema integrado en un entorno productivo y el análisis de transferibilidad entre flotas de distinto perfil operativo. 






