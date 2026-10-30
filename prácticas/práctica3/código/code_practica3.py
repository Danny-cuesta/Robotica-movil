import WebGUI
import HAL
import Frequency
import numpy as np
import math


#--Función para calcular las coordenadas de cada obstáculo que detecta el robot
def parse_laser_data(laser_data):
    
    laser_xy = []  #--> Lista de los datos del laser en coordenadas cartesianas

    #--Recorremos cada laser
    for i in range(180):

        #--Obtener la distaancia de cada objeto que detecta
        dist = laser_data.values[i]

        #--Ignorar distancias inválidas
        if not np.isfinite(dist) or dist <= 0:
            continue

        #--Calcular el ángulo respecto a la detección frontal del robot
        angle = math.radians(i - 90)

        #-Formar coordenadas
        x = dist * math.cos(angle)
        y = dist * math.sin(angle)
        laser_xy += [(x, y)]

    return laser_xy




#--CONSTANTES necesarias
i_atractiva = 5.0 #--> Intensidad constante para la fuerza atractiva
k = 0.5 #--> Parámetro de la fórmula de la instensidad de la fuerza repulsiva

#--Parámetros de la fuerza total intermedia (en este caso, vamos a darle más valor a la fuerza atractiva ya que debería a toda costa llegar a la meta, aunque esquivar obstáculos también es importante)
alfa = 1.8
beta = 1.5
influence_distance = 2.0 #--> Distancia de referencia, para que el coche comience a esquivar el obstáculo a 2 m de distancia y no antes, para que no influya en su movimiento



#_________________________________________________________________________




#--BUCLE PRINCIPAL que se ejecuta constantemente
while True:
    Frequency.tick(50)


    #----------CALCULAR FUERZAS-----------


    #--FUERZA ATRACTIVA

    #--Primero debemos hallar la posición del robot constantemente
    robot_x = HAL.getPose3d().x
    robot_y = HAL.getPose3d().y
    posRobot = np.array([robot_x, robot_y])

    #--Hallar coordenadas del objetivo
    target = WebGUI.getNextTarget() #--> Guardar la variable objetivo

    meta_x = target.getPose().x
    meta_y = target.getPose().y
    posMeta = np.array([meta_x, meta_y])

    #--Hallar vector velocidad positiva ESPECTO AL MAPA
    v_atractiva = posMeta - posRobot

    norma = np.linalg.norm(v_atractiva) #--> Calculamos la NORMA de la velocidad atractiva

    if norma > 0:
        #--Definimos la fuerza atractiva normalizada
        f_atractiva = i_atractiva * v_atractiva / norma
    else:
        f_atractiva = np.array([0.0, 0.0]) #--> La norma no puede ser 0, la fuerza se anula, error

    

#-------------------------------------------------------------------------


    #--FUERZA REPULSIVA

    distances = [] #--> Definimos una lista donde guardaremos la distancia de cada objeto
    i_repulsiva_lista = [] #--> Definimos la lista de intensidades
    v_repulsiva_lista = [] #--> Lista de velocidades repulsivas
    f_repulsiva_lista = [] #--> Lista de fuerzas repulsivas

    #--Hallar coordenadas del objetivo (DEBEMOS DETECTARLO)
    laser_data = HAL.getLaserData()

    listObjects = parse_laser_data(laser_data) #--> Llamamos a la función para hallar  las coordenadas de cada obstáculo

    #--Recorrer la lista de las coordenadas de los objetos
    for coordsObject in listObjects:

        #--Guardamos las coordenadas de cada objeto
        obst_x = coordsObject[0]
        obst_y = coordsObject[1]

        distance = math.sqrt(obst_x ** 2 + obst_y ** 2)

        #--Si la distancia es mayor de 2.0, ignorar la fuerza repulsiva y centrarnos en la meta
        if distance >= influence_distance:
            continue

        #--Calculamos la velocidad repulsiva normalizada
        v_repulsiva = -np.array(coordsObject) / distance
            # (solo usamos la posición del obstáculo porque es RESPECTO AL ROBOT, la posición del robot es respecto al mapa, son SISTEMAS DE REFERENCIAS DISTINTOS)
        v_repulsiva_lista.append(v_repulsiva)

        distances.append(distance)

    #--Definir intensidad de la fuerza 
        # LA INTENSIDAD DE LA FUERZA REPULSIVA DEPENDE DE LA DISTANCIA DEL COCHE AL OBJETO

    #--Recorremos ahora las distancias guardadas para calcular la intensidad de cada OBJETO
    for distance in distances:
        #--Fórmula de la intensidad que depende de la distancia --> b = k/d²
        if distance > 0:
            i_repulsiva = k / distance ** 2
        else:
            i_repulsiva = 0.0 #--> (Ya se ha chocado)

        i_repulsiva_lista.append(i_repulsiva) #--> Metemos cada intensidad en la lista


    #--Ahora recorremos las listas de las velocidades y las intensidades para multiplicarlas y obtener la fuerza como tal
    for v_repulsiva, i_repulsiva in zip(v_repulsiva_lista, i_repulsiva_lista):

        #--Definimos la fuerza repulsiva 
        f_repulsiva = i_repulsiva * v_repulsiva
        f_repulsiva_lista.append(f_repulsiva)


    #--> YA TENEMOS EN LA LISTA TODAS LAS FUERZAS REPULSIVAS

    #--Ahora debemos sumar todas las fuerzas repulsivas, para tener en cuenta todos los láseres del coche y detectar objetos en cualquier dirección
    f_repulsiva_total = np.array([0.0, 0.0])  
    for f_repulsiva in f_repulsiva_lista:
        f_repulsiva_total += f_repulsiva



    #-------------------------------------------------------------------------


    #--COMBINAR FUERZAS

    # Debemos sumar la fuerza atractiva con la repulsiva
    # FÓRMULA: f.intermedia = αF.atractiva + βF.repulsiva
    # (α y β son parámetros adicionales de ajuste que indican el peso y la prioridad de cada fuerza en cada momento)


    #--Debemos CAMBIAR DE SISTEMA DE COORDENADAS de la fuerza repulsiva del robot AL MAPA

    #--Obtenemos la orientación del robot con respecto al mapa
    orientacion = HAL.getPose3d().yaw

    #--Construir matriz que permite girar un vector un ángulo determinado
    R = np.array([
        [math.cos(orientacion), -math.sin(orientacion)],
        [math.sin(orientacion),  math.cos(orientacion)]
    ])

    #--Transformar la fuerza repulsiva al sistema del MAPA 
    f_repulsiva_mapa = R @ f_repulsiva_total
        #--> El operador @ representa la multiplicación de matrices (de dos componentes)


    #--Aplicar fórmula
    f_intermedia = (alfa * f_atractiva) + (beta * f_repulsiva_mapa)


    #--MOVERLO OBEDECIENDO ESA FUERZA
    #--Hallar ángulo de giro
    angulo_deseado = math.atan2(f_intermedia[1], f_intermedia[0])
        #--> Esta función calcula el ángulo de un vector a partir de sus coordenadas X e Y

    #--Obtenemos la orientación del robot con respecto al mapa
    orientacion = HAL.getPose3d().yaw

    #--Calcular error para mayor precision
    error_angulo = math.atan2(
        math.sin(angulo_deseado - orientacion),
        math.cos(angulo_deseado - orientacion)
    )
        #--> Consigue que el error angular sea el giro más corto entre la orientación actual y la deseada

    #--Mover el robot
    kp = 0.5 #--> Ganancia

    HAL.setW(kp * error_angulo)
    HAL.setV(4.3) #--> Velocidad constante de momento
