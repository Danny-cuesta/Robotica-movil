import WebGUI
import HAL
import Frequency
import cv2 #--> Librería que proporciona herramientas para procesar la imagen 
import numpy as np #--> Permite analizar los datos de los píxeles y realizar cálculos con ellos


#--VARIABLES GLOBALES
k = 0.005 #--> Ganancia (valor random de prueba)
    #Si K es pequeña: el coche gira poco, por lo que corrige su trayectoria lentamente.
    #Si K es grande: el coche gira más, por lo que corrige su trayectoria con mayor intensidad.

velocity = 5 #--> Velocidad por defecto del coche

#--Definimos el rango de color del rojo (los límites)
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])

lower_red2 = np.array([170, 100, 100])
upper_red2 = np.array([180, 255, 255])

#--Primero debemos imprimir las dimensiones de la imagen
image = HAL.getImage()
print("\nDimensiones de la imagen: ", image.shape, "\n")

ancho_imagen = image.shape[1] #--> Obtenemos el ancho de la imagen
centro_imagen = image.shape[1]/2 #--> Obtenemos el centro de la imagen para posteriormente centrar el coche


#--Bucle que se ejecutará constantemente
while True:

    Frequency.tick(50)

    #--En este ejercicio LA VELOCIDAD NO ES CONSTANTE


    #--Obtenemos los datos de la cámara (aunque no cargue)
    image = HAL.getImage()

    #--Converitmos BGR a HSV, trabajando en un formato más
    #  cómodo para detectar colores
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 
        # H--> Tono
        # S--> Saturación
        # V--> valor


    #--Detectar los píxeles rojos (definimos arrays bidimensionales)
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        # Examina los píxeles de la imagen y comprueba si sus valores están dentro del intervalo especificado.
        # --> Si un píxel ESTÁ DENTRO del intervalo, en la máscara recibe el 
        #     valor 255 (BLANCO).
        # --> Si ESTÁ FUERA, recibe el valor 0 (NEGRO).

    #--Unimos las dos máscaras (los dos intervalos del rojo)
    mask = cv2.bitwise_or(mask1, mask2) #--> Máscara principal para detectar el color rojo


    #--Ahora debemos calcular la posición donde se encuentra el rojo, es decir,
    #  el centro de la carretera
    ys, xs = np.where(mask == 255) #--> Define las coordenadas donde mask detecta el rojo

    #--Sabemos que xs contiene los píxeles horizontales donde está el rojo, por tanto:

    HAL.setV(velocity) #--> Primero avanzar recto

    if len(xs) > 0: #--> Si hay al menos 1 elemento en xs
        centro_linea = np.mean(xs) #--> Calcula la media de todas las  
                                   #    posiciones horizontales guardadas en xs

        #--Calculamos el error para saber si vamos centrados o no                        
        error = centro_imagen - centro_linea 
        
            #--> centro linea < 320 --> Linea a la izquierda
            #--> centro linea > 320 --> Linea a la derecha
            #--> centro linea = 320 --> Centrado (linea recta)

        HAL.setW(k * error) #--> Giramos en función del error (si es 0, seguimos recto)

    else:
        HAL.setV(0) #--> No tiene nada que seguir, se para
