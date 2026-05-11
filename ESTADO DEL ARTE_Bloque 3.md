# Estado del Arte.

#### BLOQUE 3 - Dataset NASA N-CMAPSS2.

###### 3.1. El simulador C-MAPSS: origen y contexto.
El dataset empleado en el presente proyecto proviene del simulador **C-MAPSS** (***Commercial Modular Aero-Propulsion System Simulation***), desarrollado por la NASA en su Centro de Investigación Ames. El C-MAPSS es un modelo termodinámico de alta fidelidad de un motor *turbofan* de dos ejes (**two-spool**) con configuración de alta derivación, cuya estructura refleja la de motores de la familia CFM56 o similar, ampliamente utilizados en aeronaves de pasajeros de fuselaje estrecho. [@chao2021ncmapss]

El C-MAPSS modela el motor mediante un sistema acoplado de ecuaciones no lineales. Sus entradas se dividen en dos grupos: las **condiciones operativas descriptoras de escenario** ($$w$$) y los **parámetros de salud del modelo** ($$\theta$$), no observables directamente. Las salidas del sistema son estimaciones de las **propiedades físicas medidas** ($$x_s$$, señales de sensores reales) y **propiedades no observadas** ($$x_v$$, sensores virtuales).  La perturbación aleatoria de ruido de sensor se añade a las señales de salida para reproducir las condiciones de medición reales.  



###### 3.2. El dataset C-MAPSS original (2008): descripción y limitaciones.
El dataset C-MAPSS original fue publicado en 2008 por Saxena, Goebel, Simon y Eklund en el contexto de *PHM Data Challenge* de 2008. Seis años después de su publicación, dicho dataset se consolidó como el *benchmark* estándar en la predicción de RUL de motores *turbofan* respaldando más de setenta publicaciones. [@ramasso2014benchmarking]

El C-MAPSS original se estructura en cuatro subconjuntos (FD001–FD004) que combinan condiciones operativas discretas y modos de fallo. El subconjunto FD001 tiene 100 trayectorias de entrenamiento bajo una única condición operativa y un único modo de fallo (degradación del HPC); FD004 llega a 248 trayectorias con seis condiciones operativas discretas y dos modos de fallo simultáneos. Cada fila corresponde a un ciclo operativo, con 3 parámetros de ajuste operativo y 21 mediciones de sensores. [@saxena2008damage]

No obstante, el C-MAPSS original presenta dos limitaciones estructurales fundamentales que motivaron el desarrollo del N-CMAPSS:

**Primera limitación — Condiciones operativas discretas y simplificadas.** El C-MAPSS original define hasta seis condiciones operativas como estados discretos predefinidos, sin reproducir la variabilidad continua del espacio de vuelo real. Un motor comercial opera bajo un espacio continuo de altitud, número de Mach, ajuste del acelerador y temperatura de entrada que varía en cada vuelo y entre rutas.

**Segunda limitación — Independencia de la degradación respecto al historial operativo.** El modelo de propagación de daño del C-MAPSS original trata la degradación como un proceso independiente del historial de operación de cada motor. En la realidad, dos motores con el mismo número de ciclos pueden estar en estados de degradación radicalmente distintos en función de sus condiciones de operación y actividad.



###### 3.3. El dataset N-CMAPSS2 (2021): motivación y generación.
El dataset **N-CMAPSS** (*New CMAPSS*) fue desarrollado por Manuel Arias Chao, Chetan Kulkarni, Kai Goebel y Olga Fink, y publicado en enero de 2021 en la revista Data (MDPI) con DOI 10.3390/data6010005. El desarrollo de modelos de pronóstico orientados a datos requiere datasets con **trayectorias de funcionamiento hasta el fallo**. Sin embargo, los grandes datasets representativos de run-to-failure son frecuentemente inaccesibles en aplicaciones reales porque los fallos son raros en sistemas críticos para la seguridad. Para fomentar el desarrollo de métodos de pronóstico, se desarrolló un nuevo dataset realista de trayectorias de funcionamiento hasta el fallo para una flota de motores de aeronave bajo condiciones de vuelo reales. [@chao2021ncmapss]

El N-CMAPSS incorpora dos nuevos niveles de fidelidad respecto al C-MAPSS original: en primer lugar, simula vuelos completos tal y como se registran a bordo de un avión comercial, cubriendo condiciones de vuelo de ascenso, crucero y descenso correspondientes a diferentes rutas de vuelo comerciales. En segundo lugar, aumenta la fidelidad del modelado de la degradación relacionando el inicio del proceso de degradación con el historial de operación.

El proceso de generación del dataset sigue cuatro etapas secuenciales:

**1. Definición de las condiciones de vuelo.** Las condiciones de vuelo reales registradas a bordo de aviones comerciales procedentes del repositorio *NASA DASHlink* se toman como entrada al simulador C-MAPSS.

**2. Imposición de degradación.** La degradación de los componentes del motor se impone en cada vuelo de forma acumulativa.

**3. Simulación del vuelo degradado.** El vuelo completo se simula con el motor en estado degradado.

**4. Evaluación del estado de salud.** El HI se evalúa y la unidad continúa operando con degradación creciente hasta que HI=0, que define el final de vida. Finalmente se añade ruido de sensor a la respuesta simulada del motor.



###### 3.4. Estructura del dataset: variables y categorías.
Cada fichero de datos del N-CMAPSS proporciona dos conjuntos: el dataset de desarrollo y el dataset de test. Ambos contienen **seis categorías de variables** almacenadas en formato HDF5 (.h5):

**Descriptores de escenario — $$w$$ (4 variables).** Condiciones de vuelo reales que definen el punto de operación del motor en cada instante:

| Variable | Símbolo | Descripción |
|---|---|---|
| Altitud | `alt` | Altitud de vuelo (ft) |
| Número de Mach | `XM` | Número de Mach de vuelo |
| Ángulo de acelerador | `TRA` | *Throttle Resolver Angle* (deg) |
| Temperatura de entrada al fan | `T2` | Temperatura total en la entrada del fan (°R) |

**Señales de sensores medidos — $$x_s$$ (14 variables).** Mediciones físicas del *gas path* accesibles en sistemas de monitorización reales: temperaturas y presiones en distintas estaciones del motor (compresor, cámara de combustión, turbina y tobera), velocidades de rotación de los ejes de alta y baja presión, y gasto de combustible. Estas son las variables de entrada principales para los modelos de predicción de RUL.

**Sensores virtuales — $$x_v$$.** Variables del modelo no directamente medibles en operación real, proporcionadas en el dataset para facilitar el desarrollo de modelos híbridos física+datos. [@chao2020fusing]

**Parámetros de salud del modelo — $$\theta$$.** Modificadores de flujo y eficiencia de cada componente rotativo, equivalentes a los índices de degradación $$SF_{x,p}$$ definidos en el Bloque 1. Representan la verdad fundamental (***ground truth***) del estado de degradación de cada componente.

**Variables auxiliares — $$A$$ (4 variables).** Número de unidad, número de ciclo de vuelo, clase de vuelo y condición de salud binaria (sano/fallo).

**Variable objetivo — $$RUL$$.** Vida Útil Restante en ciclos de vuelo para cada instante de cada unidad del dataset de desarrollo.



###### 3.5. Modos de fallo y subconjuntos.
El N-CMAPSS define siete modos de fallo que afectan a la eficiencia y/o capacidad de flujo de los subsistemas rotativos del motor (fan, LPC, HPC, HPT, LPT) de forma individual o combinada. El dataset completo se distribuye en ocho subconjuntos (DS01–DS08), cada uno caracterizado por un modo de fallo específico, un número de unidades y unas clases de vuelo determinadas:

| Subconjunto | Unidades | Modo de fallo | Fan | LPC | HPC | HPT | LPT |
|---|---|---|---|---|---|---|---|
| DS01 | 10 | 1 | No | No | No | Sí | No |
| DS03 | 15 | 2 | No | No | No | Sí | Sí |
| DS04 | 10 | 3 | Sí | No | No | No | No |
| DS05 | 10 | 4 | No | No | Sí | No | No |
| DS06 | 10 | 5 | No | Sí | Sí | No | No |
| DS07 | 10 | 6 | No | No | No | No | Sí |
| DS08a/c | 15 | 7 | Sí | Sí | Sí | Sí | Sí |

Para el presente TFG resultan especialmente relevantes los subconjuntos **DS01** (fallo aislado de HPT) y **DS03** (fallo combinado HPT+LPT), que constituyen los dos modos de degradación sobre los que se realizará el análisis de selección de características diferenciada mediante Random Forest.  [@chao2021phm]

La escala del dataset completo es significativa desde el punto de vista computacional. El subconjunto DS03 contiene 9,8 millones de instancias y 47 características, y el dataset completo suma más de 63 millones de instancias, lo que requiere **estrategias específicas de preprocesado** y **reducción de dimensionalidad** antes del entrenamiento de los modelos. [@chatterjee2021eda]



###### 3.6. Clases de vuelo y distribución operativa.
Cada unidad del dataset opera exclusivamente bajo una de **tres clases de vuelo** (***flight classes***), que corresponden a distintos perfiles de misión: vuelos de corto radio a baja altitud (clase 1), vuelos de medio radio (clase 2) y vuelos de largo radio a alta altitud en crucero (clase 3). La asignación de clase de vuelo a cada unidad se realiza una única vez y permanece constante durante toda su vida operativa.

Esta estructura introduce un elemento de variabilidad operativa deliberada: las unidades de test 14 y 15 presentan una distribución de operación significativamente diferente a la de las unidades de entrenamiento; concretamente, operan vuelos más cortos y a menor altitud que otras unidades. Este desplazamiento de distribución (***distribution shift***) entre las unidades de entrenamiento y test replica una **condición real de generalización** fuera de la distribución entrenada. [@chao2021phm]



###### 3.7. El N-CMAPSS como benchmark para el problema de RUL.
La formulación formal del problema de pronóstico propuesta en el N-CMAPSS establece lo siguiente: dadas las series temporales multivariantes de lecturas de sensores de condición $$X_s^i = [x^{(1)}, \ldots, x^{(t)}]$$ para la unidad $$i$$, el objetivo es estimar la RUL en el instante actual $$t$$:

$$\hat{RUL}^i(t) = f(X_s^i(1:t), w^i(1:t))$$

donde $$f$$ es la función de pronóstico a aprender, $$X_s^i$$ son las señales de sensores medidos y $$w^i$$ son los descriptores de escenario operativo. La dependencia explícita de $$f$$ respecto a $$w$$ distingue formalmente el problema del N-CMAPSS del C-MAPSS original, donde las condiciones operativas se trataban como variables de normalización en lugar de como entradas informativas del modelo. [@chao2020fusing]