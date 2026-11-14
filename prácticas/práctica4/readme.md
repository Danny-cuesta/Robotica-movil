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
**- gx: cuánto cambia el coste al moverte en x.**  
**- gy: cuánto cambia el coste al moverte en y** 


## DETALLES DEL CÓDIGO

**-FUERA DEL BUCLE PRINCIPAL:**  
Lo primero que tenemos que hacer es cargar el mapa con WebGUI.getMap, esta función lee una imagen y la devuelve como una tabla de números, cada número representa el grado de brillo, que indica si hay obstáculos:  
--> 0: negro (representa muros)  
--> 255: blanco (representa celdas libres)

Luego crearemos otra tabla donde están defidos los muros para luego inflarlos.

Depués debemos inflar los muros para que se descarten las calles más estrechas y que solo se tengan en cuenta las calles por las que puede pasar un coche real (las más grandes). 


**-DENTRO DEL BUCLE PRINCIPAL:**  
Vamos a definir el objetivo y realizar la conversión de coordenadas correspondientes, del mundo a rejilla y de rejilla al mundo, se realiza cada conversión cuando queremos "salir y entrar" del algoritmo:  
**Coordenadas del mundo (continuas) :** Posiciones en metros, como las que usa el simulador.  
**Coordenadas de rejilla (discretas):** Posiciones en celdas del array, es lo que entiende nuestro campo de costes, ya que la propagación de onda y el inflado necesitan un mapa discretizado.


**-En una FUNCIÓN A PARTE que llamaremos build_path:**  
Decribiremos la ruta que debe seguir el coche por el mapa donde construiremos el **vector gradiente**. Esta función recibirá el coste de cada celda para llegar al objetivo y el inicio.

## PROBLEMAS ENCONTRADOS

## VÍDEOS

