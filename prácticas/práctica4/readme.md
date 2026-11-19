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

### -FUERA DEL BUCLE PRINCIPAL:  
Lo primero que tenemos que hacer es cargar el mapa con WebGUI.getMap, esta función lee una imagen y la devuelve como una tabla de números, cada número representa el grado de brillo, que indica si hay obstáculos:  
--> 0: negro (representa muros)  
--> 255: blanco (representa celdas libres)

Luego crearemos otra tabla donde están definidos los muros para luego inflarlos.

Depués debemos inflar los muros para que se descarten las calles más estrechas y que solo se tengan en cuenta las calles por las que puede pasar un coche real (las más grandes).  

Posteriormente vamos definir parámetros para que el coche siga una ruta óptima.


### -En una FUNCIÓN A PARTE que llamaremos, cost_field:  
Construiremos el campo de costes comprobando que cada celda es válida y de esta forma aisgnamos un coste para cada celda del mapa.

### -En la FUNCIÓN A PARTE, build_path:  
Decribiremos la ruta que debe seguir el coche por el mapa donde construiremos el **vector gradiente**. Esta función recibirá el coste de cada celda para llegar al objetivo y el inicio, y si el coste del vecino es más bajo que el de la celda actual, debemos guardar esa celda del vecino en la ruta, para que de esta forma el coche avance priorizando el coste (el coste aumenta si se aleja del objetivo).


### -DENTRO DEL BUCLE PRINCIPAL:  
Al principio debemos PLANIFICAR LA RUTA. Vamos a definir el objetivo y la posición inicial a las coordenadas correspondientes, del mundo a rejilla y de rejilla al mundo, se realiza cada conversión cuando queremos "salir o entrar" del algoritmo:  
**--> Coordenadas del mundo (continuas) :** Posiciones en metros, como las que usa el simulador.  
**--> Coordenadas de rejilla (discretas):** Posiciones en celdas del array, es lo que entiende nuestro campo de costes, ya que la propagación de onda y el inflado necesitan un mapa discretizado.  

También llamaremos a las funciones que hemos creado previamente formando el campos de costes y la ruta al objetivo.

Posteriormente el coche debe SEGUIR LA RUTA marcada donde debe recorrer cada punto de la ruta verificando si ese es el objetivo, si no continuirá movimiendose con su ángulo de giro y velocidad.

## PROBLEMAS ENCONTRADOS

Al seleccionar el objetivo a veces aunque lo señale dentro de la calle, me lo marca como inalcanzable o que no puede acceder, puede que tenga que ver con un problema al inflar los muros. A parte, al principio el coche se chocaba o giraba sin motivo, he tenido que ajustar los parámetros para arreglarlo.

Aquí un ejemplo de ello:

https://github.com/user-attachments/assets/fc1947c3-3543-4f9e-8a46-6f3554321fe8

## VÍDEOS DE PRUEBA QUE FUNCIONAN

[prueba_objetivoInalcanzable.webm](https://github.com/user-attachments/assets/b14f04bc-f7ed-4328-bbfc-fb0efc9f448c) 

En general a veces cuesta marcar el objetivo por los muros hinchados, y en ocasiones hasta en los propios muros puede detectar un objetivo (en este caso gira algo mejor).

[coche_lineaRecta.webm](https://github.com/user-attachments/assets/19328217-90bd-43c1-b95f-2111c7a673b1)

Cumple un objetivo donde la ruta es una linea recta.

[cocheVolador_alcanzaObjetivo.webm](https://github.com/user-attachments/assets/b4656795-c02f-4105-abe0-cdef25b2bf3f)

Por alguna extraña razón el coche empieza a volar, pero por otra extraña razón más desconocida todavía alcanza su objetivo.

