# Estado del Arte

#### BLOQUE 2 - PHM, RUL y Mantenimiento Predictivo.

###### 2.1. Prognostics and Health Management (PHM): definición y arquitectura funcional.
El **PHM** desempeña un papel fundamental en la garantía de la seguridad y fiabilidad de los sistemas de aeronave. El proceso implica vigilancia proactiva y evaluación del estado y efectividad funcional de los subsistemas críticos. El objetivo principal del PHM es predecir la **Vida Útil Restante** (**RUL**) de los subsistemas y mitigar proactivamente los fallos futuros con el fin de minimizar sus consecuencias.

La utilización del PHM proporciona al usuario un análisis exhaustivo de los estados actual y futuro de un sistema, maximizando la **disponibilidad operativa** y fiabilidad y facilitando la reducción de costes, todo ello con objeto de garantizar los estándares de seguridad predefinidos. 

Desde el punto de vista funcional, un sistema PHM completo se articula en **cinco módulos en cascada**: [@fu2023phm]

**Adquisición y preprocesado de datos.** Captación continua de señales de sensores instalados en el motor —temperaturas, presiones, velocidades de giro, gasto de combustible— y su posterior acondicionamiento para eliminar ruido de medida, valores atípicos y efectos de las condiciones operativas.

**Extracción de características.** Identificación y aislamiento de datos relevantes procedentes de sensores indicativos del estado de salud del sistema o componente de interés. En el dominio de motores *turbofan*, dichas señales exhiben cuatro tipos de tendencia de degradación: monótona creciente, monótona decreciente, variación irregular y valor constante. Únicamente las señales con tendencia monótona creciente o decreciente son informativas para la estimación de RUL, ya que reflejan procesos de degradación irreversibles y acumulativos sin oscilaciones que podrían confundirse con recuperaciones del estado de salud o ruido de medida.

**Evaluación del estado de salud.** Estimación del *Health Index* (**HI**), una representación escalar del estado de degradación del motor derivada de la fusión de múltiples señales de sensores. Para la construcción del HI se requiere un conjunto de **métricas** que describan su calidad, incluyendo monotonicidad, tendencialidad (trendability) y prognosabilidad (prognosability). La monotonicidad representa la tendencia positiva o negativa de las características; asumiendo que el sistema no recibe mantenimiento, las características degradadas deben ser monótonas en el eje temporal.

**Pronóstico.** Predicción de la evolución futura del proceso de degradación y estimación de RUL con un horizonte temporal operacionalmente útil.

**Soporte a la decisión.** Generación de recomendaciones de mantenimiento accionables a partir de estimaciones del pronóstico, incluyendo ventanas temporales óptimas de intervención y la severidad de la acción requerida.  



###### 2.2. Métricas de calidad de *Health Index*.   
Definimos *Health Index* (**HI**) como la representación escalar y normalizada del estado de degradación de un sistema, construida mediante la fusión de las señales de múltiples sensores. Su objetivo es sintetizar en un único valor la información distribuida entre los distintos canales de monitorización, de modo que su evolución temporal refleje de forma continua y cuantificable el proceso de deterioro del componente. Un HI ideal parte de un valor correspondiente al estado nominal del sistema y evoluciona monótonamente hasta alcanzar un umbral predefinido que indica el fallo. [@zhang2023unsupervised]

Las tres métricas estándar de calidad de un *Health Index* en la literatura PHM son:

**Monotonicidad** **(***Monotonicity***)**. Medición de tendencias positiva o negativa del HI a lo largo del ciclo de vida del motor. Asumiendo que el sistema no recibe mantenimiento, un HI de calidad debe ser **monótono** en el eje temporal para reflejar un proceso de degradación irreversible y acumulativa. Se define formalmente como:

$$Mon = \left| \frac{\text{número de diferencias positivas} - \text{número de diferencias negativas}}{\text{número total de diferencias}} \right|$$

Su valor oscila entre 0 y 1. Cuanto más próximo a 1, más monótono es el indicador y más adecuado para la predicción de RUL. Cabe evitar confusiones entre valores de HI y monotonicidad de HI, puesto que ambos oscilan entre 0 y 1, representando el primero el estado de degradación del motor y el segundo la calidad de monotonicidad aplicada a la predicción/validación del mismo HI.

**Tendencialidad** **(***Trendability**)***. Mide la similitud entre las trayectorias de degradación de múltiples motores. Un HI con alta tendencialidad presenta patrones de degradación consistentes entre distintas unidades de la flota, lo que indica que el indicador captura el **comportamiento de degradación común** del sistema y no artefactos específicos de cada unidad. Se cuantifica habitualmente mediante el **coeficiente de correlación de Spearman** entre el HI y el tiempo de operación.

$$Tre = \left| \frac{1}{N} \sum_{i=1}^{N} \rho_s(HI_i, t_i) \right|$$

donde $$\rho_s$$ es el coeficiente de correlación de Spearman para la unidad $$i$$.

**Prognosabilidad** **(***Prognosability***)**. Mide la variabilidad del valor del HI en el momento del fallo entre distintas unidades. Un HI con alta prognosabilidad presenta valores similares en el punto de fallo para todos los motores, lo que facilita la definición de un umbral de fallo consistente y reproducible. Puede definirse como:

$$Pro = e^{-\frac{\sigma(HI_{fallo})}{\mu(HI_{fallo})}}$$

donde $$\sigma(HI_{fallo})$$ y $$\mu(HI_{fallo})$$ son la desviación típica y la media del HI en el instante de fallo respectivamente. Su valor oscila entre 0 y 1, siendo 1 el caso ideal de variabilidad nula en el punto de fallo.



###### 2.3. Remaining Useful Life (RUL): definición formal y modelización.
El concepto RUL queda definido como la longitud temporal de un componente desde el instante actual hasta el final de su vida útil. El objeto principal de su utilización reside en la monitorización del estado de salud del equipo, pudiendo conocer en tiempo real el estado operativo actual de los sistemas e implementar así estrategias de mantenimiento predictivo basadas en condición, posibilitando la reducción de costes de intervención de emergencia debidos a fallos no contemplados.

Formalmente, para un motor con *N* ciclos de vida total, definimos RUL para un ciclo *t* cualquiera como:

$$RUL(t) = N - t$$

La definición lineal expuesta presenta múltiples limitaciones en modelizaciones de datasets *run-to-failure*, sustituyéndose el etiquetado lineal por tramos (***Piecewise Linear***, **PwL**).[@chen2023changepoint]  Comenzando con un valor inicial constante de RUL típico de la fase de operación saludable, el nuevo modelo asume la inexistencia de degradación notoria en dicha fase inicial, asumiendo que la degradación comienza de forma abrupta a partir de un punto de cambio predefinido (***change point***). La formulación matemática de PwL quedaría de la siguiente forma:

$$RUL_{PwL}(t) = \begin{cases} RUL_{max} & \text{si } t \leq t_{cp} \\ N - t & \text{si } t > t_{cp} \end{cases}$$

donde $$t_{cp}$$ es *change point* a partir del cual comienza la fase de degradación efectiva y $$RUL_{max}$$ el valor máximo de RUL asignado durante la fase saludable. La determinación del punto de inicio de degradación, también conocido como RUL inicial, impacta significativamente en la precisión de las predicciones de RUL. Valores excesivos de $$RUL_{max}$$ introducen demasiados ciclos de etiquetado con un mismo valor constante durante la fase saludable, provocando **ruido supervisado**: el modelo aprende a asociar señales de sensor prácticamente idénticas con valores de RUL distintos, generando inconsistencias en el entrenamiento y degradando la capacidad de aprendizaje de la tendencia de degradación real; por ende, valores demasiado bajos asumen inicios de degradación excesivamente tempranos, **truncando  la fase de transición** entre operación nominal y degradación incipiente, donde los patrones más sutiles de deterioro son detectables.  [@elsherif2025deeplearning]



###### 2.4. Métricas de evaluación estándar en predicción de RUL.
La evaluación del rendimiento de los modelos de predicción de RUL en la literatura queda sujeta a dos métricas complementarias definidas por la NASA en el contexto del ***PHM Data Challenge de 2008*** (PHM'08):

***Root Mean Square Error*** **(**RMSE**)**. Métrica simétrica estándar que penaliza sin diferenciación aparente las predicciones tempranas y tardías:

$$RMSE = \sqrt{\frac{1}{N}\sum_{i=1}^{N}(\hat{RUL}_i - RUL_i)^2}$$

**Función de puntuación asimétrica** **(***NASA Score***)**. La función de puntuación es asimétrica y penaliza más las predicciones tardías sobre las tempranas, debido a las graves consecuencias de fallo del sistema. Su formulación introduce una penalización exponencial diferenciada según el signo del error:

$$S = \sum_{i=1}^{N} \begin{cases} e^{-d_i/13} - 1 & \text{si } d_i < 0 \\ e^{d_i/10} - 1 & \text{si } d_i \geq 0 \end{cases}$$

donde $$d_i = \hat{RUL}_i - RUL_i$$ es el error de predicción para un motor cualquiera $$i$$. La asimetría de la función —penalización con denominador 13 para predicciones tempranas frente a denominador 10 para predicciones tardías— refleja la diferencia de consecuencias operacionales: una predicción tardía (**sobreestimación de RUL**) puede resultar en un fallo no anticipado en vuelo, mientras que una predicción temprana (**subestimación**) implica únicamente un mantenimiento prematuro planificable. Esta métrica incorpora conocimiento de dominio a través de penalizaciones asimétricas, reflejando el mayor riesgo de los fallos inesperados en entornos industriales. [@saxena2008damage]



###### 2.5. Taxonomía de enfoques para predicciones de RUL.
Los algoritmos básicos diseñados para predecir RUL pueden clasificarse en dos categorías: enfoques basados en modelos físicos y enfoques basados en modelos de orientación a datos. La combinación de ambos paradigmas puede originar un tercer enfoque híbrido.

**Enfoques basados en modelos físicos (** ***Physics-Based Models*** **).** Descripción mediante modelos matemáticos fundamentados en mecánicas de daño y procesos termodinámicos del motor de los procesos de degradación. Aunque los modelos basados en física pueden mejorar la precisión en la predicción de RUL, las simplificaciones y supuestos inherentes a los modelos adoptados pueden incrementar las limitaciones en implementaciones prácticas. Característicos por la interpretabilidad física de los resultados ofrecida, sucumben ante la dificultad de modelizar con precisión todos los mecanismos de degradación simultáneos en un sistema complejo, como un *turbofan*.

**Enfoques orientados a datos** **(***Data-Driven Models***)**. Aprendizaje de patrones de degradación directamente del historial de datos de sensores sin requerir conocimiento explícito de los mecanismos físicos subyacentes.Incrementan la precisión de las predicciones sacrificando robustez en la cuantificación de incertidumbre y adaptabilidad de condiciones operativas variables.

**Enfoques híbridos** **(***Hybrid Models***)**. Representación del estado del arte más reciente, combinando la interpretabilidad física con la capacidad de generalización de modelos de *Deep Learning*.



###### 2.6. Del TBM al CBM: el mantenimiento basado en condición como marco del PHM.
La decisión de ejecución de tareas de mantenimiento queda fundamentada por las siguientes metodologías:  mantenimiento basado en tiempo (**TBM**) y mantenimiento basado en condición (**CBM**). TBM programa el mantenimiento basándose únicamente en intervalos de tiempo estimados, apoyándose en datos históricos de fallo; en cambio CBM se centra en la monitorización en tiempo real y el análisis predictivo basado en las condiciones del equipo, lo que permite acciones de mantenimiento adaptadas y potencialmente previene fallos inesperados.

El CBM puede eliminar **entre el 25% y el 30%** de los costes de mantenimiento y reduce el tiempo de inactividad no planificado al realizar el trabajo únicamente cuando los datos de monitorización de condición indican una **necesidad real**.  [@elgendy2025ai]

La predicción de RUL es la pieza central del CBM: proporciona el horizonte temporal que permite transformar una intervención reactiva en una planificada. Sin una estimación fiable de RUL con suficiente antelación, el CBM degenera en un sistema de alarma de umbral que sólo detecta la degradación cuando ya está en fase avanzada, sin margen de planificación de logística de repuestos ni programación de hangar.