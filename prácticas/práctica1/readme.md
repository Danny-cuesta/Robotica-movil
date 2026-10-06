# PRÁCTICA 2: Navegación pseudoaleatoria con FSM en una aspiradora de gama baja

## OBJETIVO DE LA PRÁCTICA

En esta práctica debemos programar una aspiradora para que recorra el mayor porcentaje de la casa. Esta estará configurada mediante una máquina de estados la cual contendrá una serie de movimientos que se ejecutarán de forma aleatoria.

## MÁQUINA DE ESTADOS
1- Recto 

2- Retroceder

3- Girar

## OBJETIVO DEL CÓDIGO
Al inicio del programa se deberá comprobar que todos los láseres del robot están activos, si así es, comenzará su ejecución. Cuando el robot llega a una distancia límite contral un obstáculo de 0,2, procede a cambiar de estado.

## PROBLEMAS ENCONTRADOS
Cuando comencé a programar mezcle los movimientos y no se detectaban como estados independientes, es decir, al principio el robot iba recto, pero luego giraba a la vez que retrocedía y así sucesivamente, por lo que no entendía como separarlos correctamente.
