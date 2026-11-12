# PRÁCTICA 4: Navegación global con algoritmo GPP, plan como recurso


## OBJETIVO DE LA PRÁCTICA 

El objetivo de esta práctica es implementar un algoritmo de Planificación de Ruta de Gradiente (GPP). La idea es construir un campo de costes sobre el mapa y descender por su gradiente hasta el objetivo. Una vez seleccionado un destino, el algoritmo GPP se encarga de encontrar el camino más corto hacia él, evitando, en este nuestro caso, todo lo que no es camino. Una vez seleccionada la trayectoria, deberá seguirla y alcanzar el objetivo en el robot. 

## PARTES DEL ALGORITMO

### 1- Mapa discretizado

El mapa se convierte en una rejilla de celdas libres y ocupadas. Conviene inflar los obstáculos, es decir, hacerlo más grande de lo que es en realidad, añadiéndole un “margen” a su alrededor en el mapa, para poder tratar al robot como si fuera un punto, para que la ruta no pase pegada a las paredes.

### 2- Campo de costes (propagación de onda)
Es un mapa donde cada celda guarda un número: cuántos pasos hay desde esa celda hasta el objetivo, rodeando los obstáculos. Indica el coste que hay hasta la meta desde cada celda.

### 3- Descenso por gradiente
El concepto es: MOVERSE SIEMPRE EN LA DIRECCIÓN EN LA QUE EL COSTE BAJA MÁS RÁPIDO.  
Debemos tener en cuenta que el **vector gradiente ∇C** es aquel que indica hacia dónde sube el coste y con qué rapidez, es la pendiente, no la altura.  
El **coste C(x, y)** es un número en cada celda. Cuanto mayor es, más lejos se está del objetivo.  
Por ello, tenemos que tener en cuenta que si te nos movemos en la dirección del gradiente, el coste aumenta y nos alejamos del objetivo. Por eso el robot va en la dirección contraria, **−∇C**.


El vector gradiente tiene dos direcciones:  
·**gx: cuánto cambia el coste al moverte en x.**  
·**gy: cuánto cambia el coste al moverte en y** 


## DETALLES DEL CÓDIGO

## PROBLEMAS ENCONTRADOS

## VÍDEOS

