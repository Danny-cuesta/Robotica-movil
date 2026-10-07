# PRÁCTICA 1: Navegación pseudoaleatoria con FSM en una aspiradora de gama baja

## OBJETIVO DE LA PRÁCTICA

En esta práctica debemos programar una aspiradora para que recorra el mayor porcentaje de la casa. Esta estará configurada mediante una máquina de estados la cual contendrá una serie de movimientos que se ejecutarán de forma aleatoria.

## MÁQUINA DE ESTADOS

<img width="542" height="362" alt="practica1_maquinaEstados" src="https://github.com/user-attachments/assets/6c467213-7661-4d88-b3b3-5646cde84df8" />


## OBJETIVO DEL CÓDIGO
Al inicio del programa se deberá comprobar que todos los láseres del robot están activos, si así es, comenzará su ejecución. Cuando el robot llega a una distancia límite de 0.2 contra un obstáculo, procede a cambiar de estado, se mantendrá en ese estado durante 2 segundos y luego automáticamente cambiará al siguiente.

## PROBLEMAS ENCONTRADOS
Cuando comencé a programar mezclé los movimientos y no se detectaban como estados independientes, es decir, al principio el robot iba recto, pero luego giraba a la vez que retrocedía y así sucesivamente, por lo que no entendía como separarlos correctamente.
Corregí el error detectando cada estado por separado tratándolo como un movimiento independiente, como hemos dicho previamente cada movimiento se ejecutará durante 2 segundos y posteriormente se activará el siguiente estado, pero al finalizar el programa, al principio de la ejecución tarda demasiado en detectar el obstáculo, pero no se cómo arreglarlo, exceptuando eso funciona correctamente.

## VÍDEO
