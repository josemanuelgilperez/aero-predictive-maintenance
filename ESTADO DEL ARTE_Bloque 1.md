# Estado del Arte

#### BLOQUE 1 - Mantenimiento de aeronaves y motores turbofan.
###### 1.1. El motor turbofan: ciclo termodinámico y arquitectura.
El motor ***turbofan*** se ha convertido en la solución propulsiva predominante en el ámbito de la aviación comercial subsónica moderna. Fundamentado en el **ciclo de Brayton** como principio básico de funcionamiento, un motor *turbofan* queda regido por los siguientes cuatro procesos termodinámicos establecidos en serie: compresión isentrópica mediante la utilización de compresores de alta y baja presión (**HPC** y **LPC** respectivamente), adición de calor a presión constante (**isóbaro**) en el interior de la cámara de combustión, expansión isentrópica mediante la utilización de turbinas de alta y baja presión (**HPT** y **LPT** respectivamente) montadas sobre ejes concéntricos independientes y expulsión de calor al exterior, acelerando el flujo másico de gases de escape gracias a la implantación de toberas en su última etapa. En la práctica real, los procesos no son perfectamente isentrópicos ni isóbaros, y las irreversibilidades introducen pérdidas caloríficas, mecánicas y aerodinámicas, siendo la eficiencia isentrópica el parámetro que cuantifica la desviación respecto al ciclo ideal.

Los motores *turbofan* modifican el balance del ciclo de Brayton mediante la adición de un ***fan*** canalizado accionado por la etapa de turbina adicional de baja presión **LPT**. El trabajo generado por dicha etapa de turbina facilita el accionamiento del *fan*, incrementando así el gasto másico y provocando una reducción de velocidad de escape de gases de combustión. La redistribución de potencia disponible de turbina incrementa la eficiencia propulsiva en regímenes subsónicos. 

El parámetro fundamental de caracterización de diseño de motores *turbofan* se conoce como **relación de derivación** (*Bypass Ratio*, **BPR**), definida como:

$$BPR = \frac{\dot{m}_{bypass}}{\dot{m}_{core}}$$

Las elevadas relaciones de derivación aumentan la eficiencia propulsiva y reducen drásticamente el consumo específico de combustible por unidad de empuje (**TSFC**), puesto que la aceleración pequeña de una gran masa de aire mejora la efectividad respecto de mayores aceleraciones de masas menos significativas. Rolls-Royce obtiene eficiencias propulsivas del 72%-82% y eficiencias térmicas entre el 42%-49% para valores de TSFC de 0,49 y 0,63 lb/lbf/h a Mach 0,8, buscando alcanzar límites teóricos del 95% y 60% para eficiencia propulsiva en rotor abierto y eficiencia térmica respectivamente. 

La arquitectura típica de un ***turbofan de doble eje*** (***two-spool***) se organiza en cinco módulos principales:

**Fan**. Primera etapa de compresor, de diámetro muy superior al resto de etapas. Divide el flujo entrante en dos corrientes: una **corriente de derivación** aislada del *core* y expandida en una tobera separada, suponiendo ésta hasta el 80% de la capacidad propulsiva del motor en motores modernos de alta derivación; y la **corriente de** ***core***, que alimenta el proceso de combustión.

**Compresor de baja presión (LPC) y de alta presión (HPC)**. Combinación de álabes rotativos (**rotores**) y paletas estacionarias (**estátores**), facilita la compresión de flujo axial gracias a un incremento de presión en etapa con relaciones de compresión globales (**OPR**) que alcanzan valores de hasta 40:1 en motores modernos. El HPC es el componente más susceptible a degradación por ***fouling*** y **erosión** debido a la radicalidad de temperatura y presión en sus condiciones de operación.

**Cámara de combustión**. Temperaturas cercanas a los 1400 ºC, requiere avances en sistemas de  refrigeración y recubrimientos térmicos para operar en condiciones superiores al punto de fusión de los materiales.

**Turbina de alta presión (HPT) y de baja presión (LPT)**.La HPT extrae la energía necesaria para accionar el HPC; la LPT acciona el LPC y el fan. Quedan expuestas a condiciones extremadamente agresivas, ometidas a los mayores gradientes térmicos y centrífugos del motor.

**Tobera**. Convierte la entalpía residual de los gases en energía cinética, generando el empuje del *core* mediante el tercer principio de Newton.


###### 1.2. Parámetros de salud y monitorización del gas path.
La degradación de un motor *turbofan* no se manifiesta directamente en los parámetros observables —temperaturas, presiones, velocidades de giro— sino que se origina en la variación de los **parámetros de salud** (***health parameters***) de los componentes del *gas path*: la **eficiencia isentrópica** y la **capacidad de flujo** de cada módulo rotativo, infiriendo así el estado real de cada componente.

Existen tres índices de degradación capaces de caracterizar el estado del compresor. Dichos índices quedan definidos como el ratio entre el valor del parámetro en estado degradado y su valor en motor limpio. Sendos índices son **índice de capacidad de flujo** (**$$SF_{c,FC}$$**), **índice de relación de compresión** (**$$SF_{c,PR}$$**) e **índice de eficiencia isentrópica** (**$$SF_{c,eff}$$**).

$$SF_{c,FC} = \frac{W_{c,deg}}{W_{c,clean}}$$ ; $$SF_{c,PR} = \frac{PR_{c,deg}}{PR_{c,clean}}$$ ; $$SF_{c,eff} = \frac{\eta_{c,deg}}{\eta_{c,clean}}$$

Los parámetros más utilizados en la literatura para determinar el deterioro del rendimiento en motores de turbina de gas incluyen velocidades del *fan*, vibración, presión y temperatura del aceite, temperatura de gases de escape (EGT) y gasto de combustible. De todos ellos, **EGT** (***Exhaust Gas Temperature***) es el indicador global de salud más utilizado operacionalmente: un incremento sostenido en EGT a potencia constante es síntoma inequívoco de degradación acumulada, ya que el sistema **FADEC** incrementa el gasto de combustible para compensar la pérdida de eficiencia del compresor y mantener el nivel de empuje requerido.

Respecto a la degradación de rendimiento en turbina, ésta puede ser **temporal** o **permanente**, pudiendo recuperarse parcialmente durante el mantenimiento y operación. En caso de permanencia, cabe efectuar una reparación completa. Ejemplo más notorio de degradación temporal reside en el *fouling*; la distorsión de perfiles aerodinámicos recalcaría la degradación permanente.


###### 1.3. Mecanismos de degradación en componentes rotativos.
Los mecanismos de degradación son múltiples y actúan simultáneamente sobre distintas partes del motor:

***Fouling*** **(ensuciamiento)**. Causado por la adherencia de contaminantes sobre la superficie de los componentes del motor. Produce un cambio en la geometría de los perfiles aerodinámicos y un aumento de la rugosidad superficial, resultando en un deterioro del rendimiento. El *fouling* del compresor reduce la capacidad de flujo y la eficiencia isentrópica. Es la forma de degradación más frecuente y la única mayoritariamente recuperable mediante lavado del compresor, tanto en línea como fuera de línea.

**Erosión**. Mecanismo de desgaste que actúa principalmente sobre superficies de presión y succión de álabes, pudiendo provocar a su vez reducción de cuerda, deformación de bordes de ataque y salida, variación del ángulo de escalonamiento y ampliación de las holguras en punta de álabe. Sus efectos se correlacionan típicamente de forma lineal o regresiva con el tiempo de operación y afectan negativamente a la eficiencia del compresor y al acoplamiento entre componentes.

**Aumento de holgura en punta de álabe** ***(Tip Clearance Increase)***. La holgura entre la punta del álabe y la carcasa aumenta progresivamente por dilatación térmica diferencial, desgaste mecánico y deformación plástica de los materiales. Los efectos acumulativos de fouling, erosión, corrosión y desgaste por rozamiento causan deterioro que puede impedir al motor satisfacer los requisitos de diseño. El incremento de holgura en la HPT es particularmente crítico porque incrementa el flujo de fuga no productivo, reduciendo directamente la eficiencia de extracción de trabajo.

**Degradación térmica en componentes de la zona caliente.** El *fouling* del compresor reduce la tasa de flujo de aire y su eficiencia, reduciendo a su vez el empuje del motor. El sistema de control de combustible suministra el combustible requerido correspondiente al ajuste de potencia, creando una relación combustible-aire rica que resulta en una alta temperatura de entrada a la turbina y la consiguiente erosión de los álabes. Este mecanismo de realimentación —fouling del compresor →  enriquecimiento de la mezcla → sobretemperatura en turbina → erosión de álabes de turbina— explica la propagación del daño entre módulos y la naturaleza no lineal de la degradación avanzada.

La modelización de propagación de daño —tasa, distribución entre componentes y dependencia del perfil de misión—resultante en incrementos progresivos de EGT y TSFC que limitan los márgenes de empuje disponible del motor, es precisamente el problema que aborda el simulador C-MAPSS de la NASA y, por extensión, el dataset N-CMAPSS 2 sobre el que desarrollaremos posteriormente nuestro proyecto.


###### 1.4. Marco regulatorio: aeronavegabilidad continua.
Las normativas **EASA Part 145** y **FAA Part 43 y Part 145** establecen los marcos regulatorios de **aeronavegabilidad continua** como obligación del operador en Europa y Estados Unidos respectivamente. Dicho concepto establece el cumplimiento de los requisitos del certificado tipo de cada aeronave en todo momento.

El programa de mantenimiento de cada aeronave se estructura en torno al ***Maintenance Planning Document*** (**MPD**), derivado del ***Maintenance Review Board Report*** (**MRBR**), que a su vez aplica la metodología **MSG-3** (***Maintenance Steering Group - 3rd Task Force***) para determinar las tareas de mantenimiento necesarias y sus intervalos. Este sistema divide el mantenimiento en revisiones de línea —alta frecuencia, realizadas en aeropuertos *in situ*— y revisiones de base —de menor frecuencia, en instalaciones especializadas— permitiendo minimizar interrupciones operativas y garantizando la aeronavegabilidad.

La jerarquía de inspecciones, conocida como checks A/B/C/D, estructura las intervenciones de menor a mayor profundidad:

| Check | Intervalo típico | Duración | Horas-hombre | Categoría |
|---|---|---|---|---|
| Línea | 24–60 h vuelo | Horas | Mínimas | Línea |
| A | 400–600 h vuelo / 200–300 ciclos | 10–20 h | 50–70 | Línea |
| B | 6–8 meses | 1–3 días | 160–180 | Línea/Base |
| C | 20–24 meses / ~6.000 FH | 1–4 semanas | Hasta 6.000 | Base |
| D (HMV) | 6–10 años / ~20.000 FH | 6–12 meses | Hasta 50.000 | Base |



###### 1.5. El motor como componente crítico: impacto económico.
El mantenimiento de motores representa **entre el 35% y el 40% de los costes totales de mantenimiento** de una aeronave, convirtiéndolo en el subsistema de mayor impacto económico dentro del ciclo de vida operativo.

El tiempo de inactividad no planificado cuesta a la aviación global más de **33.000 millones de dólares anuales**, de los cuales hasta un **20%** están directamente ligados a **retrasos en el mantenimiento y falta de disponibilidad de piezas**. El mantenimiento no planificado puede costar entre **3 y 4 veces más** que las intervenciones programadas, dado que las reparaciones de emergencia generan mayores costes de mano de obra, envío urgente de piezas y logística acelerada. Esta asimetría de costes es la principal **justificación económica** del mantenimiento predictivo: **anticipación del fallo** con suficiente horizonte temporal para planificar la intervención y **transformación de costes de emergencia** en costes programados, con un factor de reducción de entre 3 y 4 sobre el mismo evento.