# Estado del Arte.

#### Bloque 5 — *Random Forest* y modelos de ensemble.

###### 5.1. Árboles de decisión: fundamentos de esemble.
El **árbol de decisión** es el bloque constructivo fundamental de *Random Forest*. Un árbol de decisión particiona recursivamente el espacio de características mediante reglas de división binarias en los nodos internos, hasta alcanzar nodos hoja donde se asigna una predicción. Para problemas de regresión, la calidad de cada división se evalúa **minimizando** el MSE en los subconjuntos resultantes. Dado un nodo $$t$$ con $$n_t$$ muestras, el criterio de división óptimo selecciona la característica $$j$$ y el umbral $$s$$ que resuelven:

$$\underset{j, s}{\arg\min} \left[ \frac{n_t^L}{n_t} \cdot MSE_L + \frac{n_t^R}{n_t} \cdot MSE_R \right]$$

donde $$n_t^L$$ y $$n_t^R$$ son el número de muestras de los subconjuntos de muestras respectivamente y $$MSE_L$$, $$MSE_R$$ sus respectivos errores cuadráticos medios. La predicción en cada nodo hoja es la media de los valores objetivo de las muestras contenidas en él.

Los árboles de decisión individuales presentan una limitación estructural crítica: son altamente propensos al **sobreajuste**. Al crecer sin restricciones, dichos árboles pueden memorizar perfectamente el conjunto de entrenamiento con varianza elevada y escasa capacidad de generalización. *Random Forest* surge precisamente para superar esta limitación.



###### 5.2. *Random Forest*: algoritmo y fundamento teórico.
***Random Forest***, formalizado por Leo Breiman en su trabajo seminal de 2001, se ha consolidado como uno de los algoritmos más citados y desplegados. Introduce dos mecanismos de aleatorización que generan diversidad entre los árboles individuales del ensemble y reducen la correlación entre ellos:

***Bootstrap aggregating (Bagging).*** Para cada árbol $$h_k$$ del ensemble, se extrae una muestra de entrenamiento $$D_k$$ del conjunto original $$D$$ mediante muestreo con reemplazamiento (***sampling with replacement***). El tamaño de $$D_k$$ es igual al de $$D$$, pero aproximadamente un tercio de las instancias originales quedan fuera de cada muestra (***Out-of-bag***, OOB). Esto garantiza el entrenamiento de cada árbol sobre una versión distinta del *dataset*, reduciendo la correlación entre ellos. La predicción final del ensemble para regresión es la media aritmética de las predicciones individuales:

$$\hat{y}_{RF}(x) = \frac{1}{B} \sum_{k=1}^{B} h_k(x)$$

donde $$B$$ es el número total de árboles del ensemble. [@breiman2001random]

**Selección aleatoria de características (***Random Feature Subspace***)**. En cada nodo de cada árbol, solo se considera un subconjunto aleatorio de $$m_{try}$$ características para determinar la división óptima, en lugar de evaluar todas las $$d$$ características disponibles. El valor estándar recomendado en la regresión es $$m_{try}=d/3$$. Esta aleatorización adicional decorrelaciona los árboles entre sí: aunque el *bagging* ya introduce diversidad a nivel de muestras, árboles entrenados sobre instancias diferentes pero con las mismas características dominantes tienden a producir estructuras similares.

La combinación de ambos mecanismos garantiza que la varianza del ensemble sea sistemáticamente inferior a la de cualquier árbol individual. Breiman demostró que el error de generalización del Random Forest converge a medida que aumenta el número de árboles $$B$$ sin incremenar riesgos de sobreajuste como consecuencia de aumento de tamaño.



###### 5.3. Estimación *out-of-bag* (OOB).
Una propiedad distintiva y valiosa de *Random Forest* es la posibilidad de obtener una **estimación insesgada** del error de generalización sin necesidad de un conjunto de validación separado. Dado que en cada árbol $$h_k$$ aproximadamente un tercio de las instancias quedan fuera de $$D_k$$ (las muestras OOB), estas instancias pueden usarse para evaluar el árbol $$h_k$$ k​ sin sesgo. El error OOB global se obtiene agregando las predicciones de todos los árboles para los que cada instancia fue OOB:

$$\hat{y}_{OOB}(x_i) = \frac{1}{|\{k : x_i \notin D_k\}|} \sum_{k: x_i \notin D_k} h_k(x_i)$$

El error OOB resultante es un estimador consistente del error de test real y permite la selección de hiperparámetros —número de árboles $$B$$, $$m_{try}$$, profundidad máxima— sin incurrir en fuga de datos.



###### 5.4. Importancia de características: MDI y su aplicación a la selección de sensores.
La importancia de características de *Random Forest* es una de sus propiedades más valiosas en el contexto del presente TFG. El método estándar es ***Mean Decrease Impurity*** (**MDI**), que cuantifica la contribución de cada característica a la reducción de impureza a lo largo de todos los árboles del ensemble. [@louppe2013understanding]

Para regresión, la impureza en el nodo $$t$$ se mide mediante la varianza de los valores objetivo en ese nodo. La importancia MDI de la característica $$j$$ se define como:

$$MDI(j) = \frac{1}{B} \sum_{k=1}^{B} \sum_{t \in T_k: v(t)=j} \frac{n_t}{N} \left[ Var(t) - \frac{n_t^L}{n_t} Var(t^L) - \frac{n_t^R}{n_t} Var(t^R) \right]$$

donde $$v(t)$$ es la característica usada para dividir en el nodo $$t$$, $$n_t$$ es el número de muestras en ese nodo, $$N$$es el número total de muestras, y $$Var(t)$$, $$Var(t^L)$$, $$Var(t^R)$$ son las varianzas del nodo padre e hijos respectivamente. Los valores MDI se normalizan para que su suma sea igual a 1.

Una limitación reconocida del MDI es su **sesgo hacia características de alta cardinalidad** o con muchos posibles puntos de división, que tienden a recibir importancias artificialmente elevadas incluso cuando no son genuinamente informativas [@alomari2023advancing]. Para mitigar este sesgo, en el presente TFG el MDI se complementa con la **importancia por permutación** (*Mean Decrease Accuracy*, MDA): la importancia de cada característica se estima midiendo la caída en el rendimiento del modelo cuando los valores de esa característica se permutan aleatoriamente en el conjunto de test, rompiendo su relación con la variable objetivo. [@strobl2008conditional]

En el contexto de la selección de sensores del N-CMAPSS 2, la aplicación diferenciada del MDI sobre los subconjuntos DS01 (fallo HPT) y DS03 (fallo HPT+LPT) permite determinar si el conjunto óptimo de sensores varía según el modo de degradación, aportando conocimiento técnico sobre la relación entre la instrumentación del motor y el tipo de fallo.



###### 5.5. *Random Forest* como modelo de referencia en predicción de RUL.
En la literatura de predicción de RUL sobre datasets C-MAPSS y N-CMAPSS, *Random Forest* se utiliza habitualmente como **modelo de referencia (***baseline***)** frente al que se contrasta el rendimiento de las arquitecturas de *Deep Learning*. Su utilización en este rol queda justificada por tres razones complementarias:

**Primera**, *Random Forest* es intrínsecamente robusto al sobreajuste gracias al promediado de múltiples árboles descorrelados, lo que lo convierte en un competidor sólido incluso frente a modelos de mayor complejidad cuando el dataset de entrenamiento es de tamaño moderado.

**Segunda**, su capacidad de importancia de características permite evaluar la selección de sensores de forma integrada en el mismo modelo que sirve como referencia, estableciendo un criterio consistente y reproducible para todos los modelos de la comparativa. [@wang2023remaining]

**Tercera**, a diferencia de los modelos de *Deep Learning*, *Random Forest* no requiere de la transformación de series temporales en ventanas deslizantes: puede operar directamente sobre vectores de características estadísticas extraídas de cada ciclo, convirtiéndolo en un punto de referencia metodológicamente diferenciado.