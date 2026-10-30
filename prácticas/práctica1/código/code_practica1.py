import WebGUI
import HAL
import Frequency
import time

#--Variables constantes del programa
velocity = 0.5 #--> Velocidad lineal/angular del robot
MAX_DISTANCE = 0.45 #--> Distancia límite a la que el robot se puede acercar a un obstáculo
estado = "RECTO" #--> Para gestionar el movimiento del robot por estados (movimientos)
obstaculo = False #--> Para comprobar si el robot está muy cerca del obstáculo


#--Bucle que se ejecutará continuamente
while True:
    Frequency.tick(50)

    #--Variable el laser del robot
    laser_data = HAL.getLaserData()

    #--Nos aseguramos de que todos los láseres estén activos
    #  Si hay alguno no activo, se pasará a la siguiente iteración del bucle
    if len(laser_data.values) != 180:
        continue


    HAL.setV(velocity) #--> Ir recto al principio


    #--Comprobar si cada laser sobrepasa el límite de distancia
    for laser in laser_data.values:
        if laser <= MAX_DISTANCE:
            obstaculo = True #--> El robot está a punto de colisionar
            break

    
    #--MÁQUINA DE ESTADOS, MOVIMIENTOS DEL ROBOT
    if estado == "RECTO": #--> Ir RECTO

        inicio = time.time()
        #--El robot debe mantenerse en ese movimiento 2 segundos
        while time.time() - inicio < 2:
            HAL.setV(velocity)
            if obstaculo == True: #--> Cada vez que se detecte un obstáculo se activará la máquina de estados
                estado = "RETROCEDER"
                obstaculo = False #--> Reset de la variable
                break #--> Se sale del bucle para cambiar de movimiento


    if estado == "RETROCEDER": #--> RETROCEDER

        #--> En este estado no validaremos if obstaculo == True ya que los láseres se encuentran únicamente en la parte delantera del robot

        inicio = time.time()
        #--El robot debe mantenerse en ese movimiento 1 segundos
        while time.time() - inicio < 1:
            HAL.setV(-velocity)
        estado = "DERRECHA"


    if estado == "DERRECHA": #--> Girar a la DERRECHA
        
        inicio = time.time()
        #--El robot debe mantenerse en ese movimiento 2 segundos
        while time.time() - inicio < 2:
            HAL.setW(velocity)
            if obstaculo == True: #--> Cada vez que se detecte un obstáculo se activará la máquina de estados
                estado = "IZQUIERDA"
                obstaculo = False #--> Reset de la variable
                break #--> Se sale del bucle para cambiar de movimiento


    if estado == "IZQUIERDA": #--> Girar a la IZQUIERDA

        inicio = time.time()
        #--El robot debe mantenerse en ese movimiento 2 segundos
        while time.time() - inicio < 2:
            HAL.setW(-velocity)
            if obstaculo == True: #--> Cada vez que se detecte un obstáculo se activará la máquina de estados
                estado = "RECTO"
                obstaculo = False #--> Reset de la variable
                break #--> Se sale del bucle para cambiar de movimiento
