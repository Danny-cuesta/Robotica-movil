# PRÁCTICA 4: Navegación global con algoritmo GPP, plan como recurso


## OBJETIVO DE LA PRÁCTICA 

El objetivo de esta práctica es implementar un algoritmo de Planificación de Ruta de Gradiente (GPP). La idea es construir un campo de costes sobre el mapa y descender por su gradiente hasta el objetivo. Una vez seleccionado un destino, el algoritmo GPP se encarga de encontrar el camino más corto hacia él, evitando, en este nuestro caso, todo lo que no es camino. Una vez seleccionada la trayectoria, deberá seguirla y alcanzar el objetivo en el robot. 

## PARTES DEL ALGORITMO

### 1- Mapa discretizado

### 2- Campo de costes (propagación de onda)

### 3- Descenso por gradiente
El concepto es: moverse siempre en la dirección en la que el coste baja más rápido.  
Debemos tener en cuenta que el **vector gradiente** es aquel que indica hacia dónde sube el coste y con qué rapidez, es la pendiente, no la altura.  
El **coste** es un número en cada celda. Cuanto mayor es, más lejos se está ddel objetivo.  
Por ello, tenemos que tener en cuenta que si te nos movemos en la dirección del gradiente, el coste aumenta y nos alejamos del objetivo. Por eso el robot va en la dirección contraria (−∇C).


## DETALLES DEL CÓDIGO

## PROBLEMAS ENCONTRADOS

## VÍDEOS

