# Estado del Arte

#### Bloque 8 — Interpretabilidad: *Permutation Importance* y SHAP.

###### 8.1. El problema de la interpretabilidad en modelos de *Deep Learning* para PHM.
Los modelos de *Deep Learning* de mayor rendimiento predictivo en la estimación de RUL —LSTM, Bi-LSTM, CNN-LSTM— son arquitecturas de elevada complejidad paramétrica cuyo proceso de decisión interno no es directamente accesible ni auditable. Esta opacidad constituye una barrera crítica para su adopción en entornos operacionales regulados como la aviación, donde las decisiones de mantenimiento requieren justificación técnica verificable ante las autoridades competentes (EASA, FAA) [@sun2020shap_rul]. La disciplina de la **Inteligencia Artificial Explicable** (*Explainable Artificial Intelligence*, **XAI**) ha emergido como respuesta a esta limitación, desarrollando métodos capaces de atribuir las predicciones de modelos opacos a contribuciones individuales de las características de entrada.

En el contexto del PHM para motores *turbofan*, la interpretabilidad tiene además un valor técnico más allá del regulatorio: identificar qué señales de sensor respaldan la predicción de RUL permite establecer la correspondencia entre la respuesta del modelo y los mecanismos físicos de degradación conocidos, validando que el modelo ha aprendido representaciones físicamente coherentes en lugar de correlaciones espurias del dataset de entrenamiento.



###### 8.2. Importancia por permutación (*Permutation Feature Importance*).
La **importancia por permutación** (*Permutation Feature Importance*, **PFI**) es un método de interpretabilidad global agnóstico al modelo, introducido originalmente por Breiman en 2001 en el contexto de *Random Forest* [@breiman2001random]. Su principio fundamental consiste en medir la degradación del rendimiento predictivo del modelo tras destruirse la relación entre una característica y la variable objetivo vía permutación aleatoria de sus valores.

Formalmente, dado un modelo entrenado $$\hat{f}$$, una matriz de características $$X$$ y un vector objetivo $$y$$, el algoritmo PFI procede como sigue. Primero se estima el error original del modelo: $$e_{orig} = L(y, \hat{f}(X))$$. A continuación, para cada característica $$j$$, se genera la matriz perturbada $$X_{perm_j}$$ permutando aleatoriamente los valores de la columna $$j$$, rompiendo su asociación con $$y$$. El error perturbado se estima como $$e_{perm_j} = L(y, \hat{f}(X_{perm_j}))$$. La importancia por permutación de la característica $$j$$ se define como:

$$FI_j = \frac{e_{perm_j}}{e_{orig}}$$

o alternativamente como la diferencia absoluta:

$$FI_j = e_{perm_j} - e_{orig}$$

Una característica es **importante** si su permutación incrementa significativamente el error del modelo, lo que indica que el modelo dependía de ella para realizar sus predicciones. Una característica es **no informativa** si su permutación deja el error invariante, lo que indica que el modelo la ignoraba.

La PFI presenta ventajas significativas respecto al MDI de *Random Forest* en este contexto: es completamente agnóstica al modelo, puede aplicarse indistintamente a *Random Forest*, LSTM, Bi-LSTM y CNN-LSTM sobre el mismo conjunto de test, y no presenta el sesgo hacia características de alta cardinalidad característico del MDI. Su principal limitación es la subestimación de la importancia de características correladas: cuando dos características contienen información redundante, permutar una de ellas no degrada el rendimiento porque el modelo puede compensar con la otra, produciendo importancias artificialmente bajas para ambas.



###### 8.3. SHAP: fundamento teórico en la teoría de juegos cooperativos.
**SHAP** (*SHapley Additive exPlanations*) fue introducido por Lundberg y Lee en 2017 como un *framework* unificado de interpretabilidad *post-hoc* fundamentado en los valores de Shapley de la teoría de juegos cooperativos, introducidos originalmente por Lloyd Shapley en 1953 [@lundberg2017shap]. La idea central es trasladar al aprendizaje automático el problema de la distribución justa del beneficio en un juego cooperativo: los jugadores son las características del modelo, el juego es la predicción y el *payoff* a distribuir es la diferencia entre la predicción para una instancia concreta y la predicción media del modelo.

El valor de Shapley de la característica $$j$$ para la instancia $$x$$ mide su contribución marginal promediada sobre todas las posibles coaliciones $$S$$ de las $$d - 1$$ características restantes:

$$\phi_j(x) = \sum_{S \subseteq D \setminus \{j\}} \frac{|S|!(d-|S|-1)!}{d!} \left[ v(S \cup \{j\}) - v(S) \right]$$

donde $$D$$ es el conjunto completo de características, $$d = |D|$$, y $$v(S)$$ es la función de valor que mide la predicción del modelo cuando sólo están disponibles las características del subconjunto $$S$$:

$$v_{f,x}(S) = \mathbb{E}[f(X) \mid X_S = x_S]$$

El modelo de explicación de SHAP es una función lineal aditiva de los valores de Shapley:

$$g(z') = \phi_0 + \sum_{j=1}^{d} \phi_j z_j'$$

donde $$z' \in \{0,1\}^d$$ es el vector de características simplificado (1 si la característica está presente en la coalición, 0 si está ausente); $$\phi_0 = \mathbb{E}[f(X)]$$ es el valor base (predicción media del modelo); y $$\phi_j$$ es el valor SHAP de la característica $$j$$.

Lundberg y Lee demostraron que los valores de Shapley son la **única solución** que satisface simultáneamente tres propiedades axiomáticas fundamentales para un método de atribución aditivo:

**Precisión local (*local accuracy*)**. La suma de los valores SHAP de todas las características más el valor base reproduce exactamente la predicción del modelo para la instancia explicada: $$g(z') = f(x)$$.

**Ausencia (*missingness*)**. Las características ausentes (con valor $$z_j' = 0$$) reciben contribución SHAP nula.

**Consistencia (*consistency*)**. Si el modelo cambia de forma que la contribución marginal de una característica aumenta o permanece igual, su valor SHAP no disminuye.



###### 8.4. Variantes computacionales de SHAP.
El cálculo exacto de los valores de Shapley tiene complejidad combinatoria $$O(2^d)$$, lo que lo hace computacionalmente inviable para datasets de alta dimensionalidad. Lundberg et al. desarrollaron tres variantes computacionales especializadas que reducen esta complejidad:

**KernelSHAP.** Método agnóstico al modelo que aproxima los valores de Shapley mediante regresión lineal ponderada sobre un conjunto muestreado de coaliciones. Aplicable a cualquier modelo, con complejidad $$O(TKd)$$ donde $$T$$ es el número de muestras de coalición y $$K$$ el número de instancias a explicar. Es la variante utilizada para los modelos de *Deep Learning* (LSTM, Bi-LSTM, CNN-LSTM) del presente TFG.

**TreeSHAP.** Variante específica para modelos de árbol (*Random Forest*, *Gradient Boosting*) que explota la estructura jerárquica de los árboles para calcular los valores de Shapley de forma exacta en tiempo polinomial $$O(TLD^2)$$, donde $$T$$ es el número de árboles, $$L$$ el número máximo de hojas y $$D$$ la profundidad máxima [@lundberg2020treeshap_global]. Es la variante aplicada a *Random Forest* del presente TFG, donde la eficiencia computacional es crítica dado el volumen del N-CMAPSS 2. TreeSHAP reduce la complejidad de $$O(TL2^M)$$ para KernelSHAP exacto a $$O(TLD^2)$$. [@lundberg2018treeshap]

**DeepSHAP.** Variante para redes neuronales profundas basada en una versión modificada del método DeepLIFT, que retropropaga las contribuciones a través de las capas de la red hasta las entradas. Más eficiente que KernelSHAP para arquitecturas de *Deep Learning* pero produce aproximaciones en lugar de valores exactos.



###### 8.5. Interpretabilidad local y global mediante SHAP en predicción de RUL.
SHAP proporciona dos niveles complementarios de interpretabilidad que son especialmente valiosos en el contexto de la predicción de RUL sobre el N-CMAPSS 2:

**Interpretabilidad local.** Para cada instancia individual (motor $$i$$, ciclo $$t$$), los valores SHAP descomponen la predicción $$\hat{RUL}^i(t)$$ en contribuciones atribuibles a cada sensor: $$\hat{RUL}^i(t) = \phi_0 + \sum_{j=1}^{d} \phi_j^{i,t}$$. Esto permite identificar qué señales de sensor están impulsando la predicción de RUL en un instante concreto del ciclo de vida del motor, con implicaciones directas para el diagnóstico operacional.

**Interpretabilidad global.** Agregando los valores SHAP locales sobre todas las instancias del conjunto de test mediante la media de los valores absolutos, se obtiene la importancia global de cada característica:

$$\bar{\phi}_j = \frac{1}{N} \sum_{i=1}^{N} |\phi_j^i|$$

Esta métrica permite comparar la relevancia de cada sensor entre los distintos modelos del TFG (*Random Forest*, LSTM, Bi-LSTM, CNN-LSTM) y entre los distintos modos de fallo, respondiendo a la pregunta de si arquitecturas con rendimiento predictivo similar están apoyando sus predicciones en las mismas señales físicas o en conjuntos de sensores distintos. [@alomari2024shap_aerospace]

La aplicación de SHAP sobre el N-CMAPSS 2 tiene además una dimensión temporal que no está presente en datasets estáticos: al ser los datos series temporales procesadas mediante ventana deslizante, los valores SHAP pueden analizarse en función de la posición dentro del ciclo de vida del motor, permitiendo detectar si la relevancia de cada sensor varía entre la fase saludable, la fase de transición y la fase de degradación avanzada del motor. [@alomari2023network_shap]