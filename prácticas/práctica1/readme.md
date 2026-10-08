# PRÁCTICA 1: Navegación pseudoaleatoria con FSM en una aspiradora de gama baja

## OBJETIVO DE LA PRÁCTICA

En esta práctica debemos programar una aspiradora para que recorra el mayor porcentaje de la casa. Esta estará configurada mediante una máquina de estados la cual contendrá una serie de movimientos que se ejecutarán de forma aleatoria.

## MÁQUINA DE ESTADOS

<img width="542" height="362" alt="practica1_maquinaEstados" src="https://github.com/user-attachments/assets/6c467213-7661-4d88-b3b3-5646cde84df8" />


## DETALLES DEL CÓDIGO
Al inicio del programa se deberá comprobar que todos los láseres del robot están activos, si así es, comenzará su ejecución. Cuando el robot llega a una distancia límite de 0.45 contra un obstáculo, procede a cambiar de estado, se mantendrá en ese estado durante 1-2 segundos y luego automáticamente cambiará al siguiente. Va a 0.5 de velocidad.

## PROBLEMAS ENCONTRADOS
Cuando comencé a programar mezclé los movimientos y no se detectaban como estados independientes, es decir, al principio el robot iba recto, pero luego giraba a la vez que retrocedía y así sucesivamente, por lo que no entendía como separarlos correctamente.
Corregí el error detectando cada estado por separado tratándolo como un movimiento independiente, como hemos dicho previamente cada movimiento se ejecutará durante 1-2 segundos y posteriormente se activará el siguiente estado.

Por otro lado, es cierto que no se mueve tan aleatoriamente ya que la estructura del código respecto a la máquina de estados sigue un patrón: recto --> atrás --> derecha --> izquierda, pero consigue avanzar igual.

## VÍDEO
[screencast-from-2026-10-08-12-25-58_x5ITNrzt.webm](https://github.com/user-attachments/assets/e21fe8a5-8437-4efe-b71e-464589ff70fe)

Como podemos comprobar la aspiradora funciona correctamente y acaba recorriendo más del 60% de la casa, pero al final del video observamos que se queda pillada, exceptuando eso, recorre bastante superficie.
