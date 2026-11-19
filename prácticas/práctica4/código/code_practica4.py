import WebGUI
import HAL
import Frequency
import numpy as np
import cv2 #--> Para poder inflar el mapa
from collections import deque
import math


#--CONSTANTES necesarias
directions = [(1,0), (-1,0), (0,1), (0,-1)]


#--Cargamos el mapa
array = WebGUI.getMap('/resources/exercises/global_navigation/images/cityLargenBin.png')
# --> Genera una función que lee una imagen y la devuelve como una
#     tabla de números

#--Definimos los muros del mapa (sabiendo que 0 = negro)
ocupado = np.where(array == 0, 255, 0).astype(np.uint8)

radio_celdas = 4 #--> Cuanto más radio, más se inflarán los muros

#--Plantilla que define cuánto y con qué forma engordar los muros
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                   (2*radio_celdas + 1, 2*radio_celdas + 1))
#--> Esta función: getStructuringElement, recibe (forma, tamaño) donde se define la plantilla para poder dilatar los obstáculos
#--> Con MORPH_ELLIPSE, los muros crecen igual en todas direcciones

#--Inflamos los obstáculos
ocupado_inflado = cv2.dilate(ocupado, kernel)
#--> Con dilate se recorre el mapa y, en cada píxel, coloca esa plantilla que hemos definido antes por encima

objetivo_anterior = None #--> Sirve para detectar si el usuario ha elegido un objetivo nuevo
path_global = [] #--> Ruta actual, inicialmente vacía. Se rellena cuando se calcula la ruta para un objetivo

idx_actual = 0 #--> Índice por el que va el coche dentro de la ruta


#--PARÁMETROS del seguimiento de la ruta (se ajustan probando)
LOOKAHEAD = 5 #--> Cuántos puntos de la ruta por delante apunta el coche
V_LINEAL = 10.0 #--> Velocidad lineal
V_LENTA = 3.0 #--> Velocidad cuando va mal orientado
K_GIRO = 1.0 #--> Ganancia del giro
DIST_LLEGADA = 1.0 #--> Metros al destino para parar


#_________________________________________________________________________
#_________________________________________________________________________



#--Función que fabrica el CAMPO DE COSTES
def cost_field(mapa_inflado, goal):

    #--Definimos las dimensiones del mapa engordado (mapa_inflado.shape es una matriz entera)
    alto, ancho = mapa_inflado.shape

    #--Definimos el CAMPO DE COSTES donde irán todos los costes e los inicializamos todos en un inicio a infinito para diferenciarlo bien de un coste real
    cost = np.full((alto, ancho), np.inf) 

    #--Definir objetivo y su coste
    gx, gy = goal
    cost[gx, gy] = 0

    #--Creamos una cola donde en un inicio se introducirá el objetivo como punto de partida y luego se irán añadiendo las celdas pendientes por asignar coste
    cola = deque([(gx, gy)]) 

    while cola:
        x, y = cola.popleft() #--> Saca de la cola la celda que toca

        #--Recorremos cada dirección
        for dx, dy in directions: 
            nx, ny = x + dx, y + dy #--> Definimos la dirección del vecino

            #--Comprobamos que las coordenadas del vecino están en el rango correcto (los límites de las dimensiones del mapa)
            x_valida = 0 <= nx < alto
            y_valida = 0 <= ny < ancho
                #--> Estas variables son de COMPROBACIÓN, devuelven true si la condición de dentro se cumple
            dentro = x_valida and y_valida #--> Unimos las variables

            #--Si las coordenadas del vecino son válidas (dentro = True), es una celda libre (0 = no está ocupado) y aun está sin explorar...
            if dentro and mapa_inflado[nx, ny] == 0 and cost[nx, ny] == np.inf:
                cost[nx, ny] = cost[x, y] + 1 #--> Asignar coste en la celda nueva (está cada vez más lejos del objetivo)
                cola.append((nx, ny)) #--> Añadimos a la cola el vecino con el coste YA ASIGNADO

    return cost #--> Retornar todo el campo de coste con dicho coste en cada celda



#_________________________________________________________________________
#_________________________________________________________________________


 
#--Función donde se DEFINE LA RUTA en función del coste y el inicio
#  Aquí es donde vamos a calcular el GRADIENTE 
def build_path(cost, start):

    #--Variables que simbolizan las coordendas en la que está el coche (la celda) y la ruta que debe seguir
    fila, col = start
    path_local = [[fila, col]] #--> Lista de celdas

    #--Si el coste de la ruta es infinito, es inalcanzable, retornar lista vaía
    if cost[fila, col] == np.inf:
        return [] 

    #--Por el contrario, mientras la celda tenga algún coste, definir ruta
    while cost[fila, col] > 0:
        mejor_celda = (fila, col) #--> De momento la mejor opción es la misma celda

        #--Recorremos todas las direcciones que puede realizar el coche
        for df, dc in directions:

            #--Definir nuevas posiciones
            nf, nc = fila + df, col + dc #--> Calcula el vecino que toca mirar

            #--Comprobamos que las coordenadas están en el rango correcto
            fila_valida = 0 <= nf < cost.shape[0]
            col_valida = 0 <= nc < cost.shape[1]
            dentro = fila_valida and col_valida
            
            #--Comprobamos que el coste del vecino es mejor que el que ya teniamos (Y QUE LA FILA Y LA COLUMNA SON VÁLIDAS, dentro = True)
            if dentro and cost[nf, nc] < cost[mejor_celda]:
                mejor_celda = (nf, nc) #--> Actualizamos

        #--Comprobar si no hay vecino y en ese caso salir del bucle
        if mejor_celda == (fila, col):
            break 

        fila, col = mejor_celda #--> Actulizar coordenadas a la del vecino elegido (y de esta forma vamos avanzando, del inicio al objetivo)
        path_local.append([fila, col]) #--> Añadir celda a la que deberíamos ir a la ruta 

    
    return path_local #--> Retornamos la lista con toda la ruta hecha



#_________________________________________________________________________
#_________________________________________________________________________



#--Función de BUCLE PRINCIPAL
while True:
    Frequency.tick(50)


    #---------------------------PLANIFICAR RUTA---------------------------


    #--Seleccionar objetivo
    target = WebGUI.getTargetPose() #--> Devuelve las coordenadas de la desición elegida en el mundo (el objetivo)

    #--Si aun no hay objetos, pasar a la siguiente iteración
    if target is None:
        continue

    #--Solo recalcular si el objetivo ha cambiado
    if target != objetivo_anterior:
        objetivo_anterior = target

        #--CONVERTIR COORDENADAS del mundo en coordenadas de cuadrícula de mapa, MUNDO --> REJILLA (para el objetivo y el inicio)
        pose = HAL.getPose3d() #--> Para la posicion inicial
        obj_f, obj_c = WebGUI.worldToGrid([target[0], target[1]]) #--> Objetivo convertido
        ini_f, ini_c = WebGUI.worldToGrid([pose.x, pose.y]) #--> Inicio convertido
        #--Convertimos a int porque al estar en rejilla necesitamos valores discretos
        obj_f, obj_c = int(obj_f), int(obj_c)
        ini_f, ini_c = int(ini_f), int(ini_c)

        #--Imprimir objetivo y posición inicial
        print("\nPosición inicial: ", ini_f, ini_c, "\n")
        print("Objetivo: ", obj_f, obj_c, "\n")

        #--Construir CAMPO DE COSTES
        field = cost_field(ocupado_inflado, [obj_f, obj_c])


        #--Calcular RUTA
        ruta_rejilla = build_path(field, [ini_f, ini_c])


        #--Objetivo inalcanzable, devolver ruta vacía
        if not ruta_rejilla:
            print("Objetivo inalcanzable (o dentro de una zona inflada)")
            path_global = []
            idx_actual = 0
            HAL.setV(0)
            HAL.setW(0)
            #--> El coche no se mueve

        else:
            #--CONVERTIR COORDENADAS, REJILLA --> MUNDO para que el coche se pueda mover
            path_global = [WebGUI.gridToWorld(p) for p in ruta_rejilla]
            #--> Para cada celda p de ruta_rejilla, calcula su posición en metros con grid_to_world(p) (vuelve a convertirlo a las coordenadas en las que estaban) y guarda todos los resultados en path_global
            idx_actual = 0 #--> Ruta nueva: se empieza por el principio



        #---------------------------SEGUIR RUTA---------------------------


        
    #--AHORA EL COCHE DEBE SEGUIR EL OBJETIVO
    if path_global: #--> Todo el camino hasta el objetivo está en la ruta
        poseCar = HAL.getPose3d()#--> Posicion inicial del coche

        #--Comprobar en qué parte de la ruta está el coche ahora:
        #  Calcular distancia al cuadrado entre ese punto y el coche
        #  --> (x_punto - x_coche)² + (y_punto - y_coche)²
        idx = min(range(len(path_global)),
        key=lambda i: (path_global[i][0] - poseCar.x)**2 + (path_global[i][1] - poseCar.y)**2)

        #--Elegir el punto al que apuntar
        idx_obj = min(idx + LOOKAHEAD, len(path_global) - 1)
        tx, ty = path_global[idx_obj][0], path_global[idx_obj][1]

        #--Calcular ángulo de giro, normalizado entre -pi y pi
        ang = math.atan2(ty - poseCar.y, tx - poseCar.x)
        err = math.atan2(math.sin(ang - poseCar.yaw), math.cos(ang - poseCar.yaw))

        #--Comprobar si se ha llegado el objetivo
        final_x, final_y = path_global[-1][0], path_global[-1][1]
        #--> Definimos el ultimo elemento de la lista (el objetivo)
        #           Desde el principio:  0   1   2   3
        #           Desde el final:     -4  -3  -2  -1  <--
        #--Calcular la hipotenusa del vector resta entre el objetivo y la posicion del coche para verificar si ya ha llegado
        if math.hypot(final_x - poseCar.x, final_y - poseCar.y) < DIST_LLEGADA:
            #--Parar coche
            HAL.setV(0)
            HAL.setW(0)
            path_global = [] #--> Ya no hay más ruta
            print("Objetivo alcanzado\n")

        else: #--> El coche debe seguir avanzando

            #--Comprobar si el coche va bien orientado (el error es pequeño)
            if abs(err) < 0.5: #--> abs() devuelve el valor absoluto de un nº
                velocidad = V_LINEAL #--> Avanzar como de costumbre

            else:
                velocidad = V_LENTA #--> Si va mal, disminuir la velocidad (el error es más grande de los que debería)

            #--Mover el coche en función de los valores propuestos
            HAL.setV(velocidad)
            HAL.setW(K_GIRO * err)


