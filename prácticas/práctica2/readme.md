
# PRÁCTICA 2: Control Visual con PID de un Fórmula 1

## OBJETIVO DE LA PRÁCTICA

Esta práctica se basa en programar un control reactivo PID, es decir, un sistema que hace que un robot reaccione continuamente a lo que está detectando, ajustando su movimiento para ejecutar un comportamiento deseado. Este control que irá implementado en un coche de carreras fórmula 1, debe seguir una línea roja constantemente en medio de la carretera.

## DETALLES DEL CÓDIGO

El coche identificará la línea roja mediante píxeles, detectando el color rojo en el rango correcto, utilizando las librerías cv2 y numpy para el procesamiento y el manejo de la imagen y de arrays.

Para ello hemos tenido que imprimir las dimensiones de la imagen para ver cual era el ancho de esta, después lo dividiremos entre 2 para obtener su mitad y en función de ese valor mantendremos centrado el coche. Entre esto último y detectando los píxeles del color rojo, calcularemos también el error, si el coche se desvía un poco de la linea roja, girará a la derecha o a la izquierda en función del valor de dicho error y la ganancia para mantenerse en el centro de la carretera.

## PROBLEMAS ENCONTRADOS

Durante toda la práctica, no me ha cargado la imagen de la cámara del vehículo, por lo que en ningún momento he podido ver lo que el coche veía, pero aun así he podido procesar los valores y manejar el coche.

<img width="728" height="323" alt="Screenshot from 2026-10-14 12-30-59" src="https://github.com/user-attachments/assets/eb848f7c-0d51-4352-a1a9-bc062d21bb62" />


## VÍDEOS
### Simple circuit:



### Montreal circuit:



### Montmelo circuit:



### Si el coche está fuera de la línea roja al inicio:

[Screencast from 2026-10-15 12-11-09.webm](https://github.com/user-attachments/assets/6df9e2fe-d052-48c2-8b3f-d15e3be2eab5)

Observamos que se coloca rápidamente en el centro siguiendo la línea.
