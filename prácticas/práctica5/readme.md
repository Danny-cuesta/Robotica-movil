# PRÁCTICA 5: Robot que construye un mapa en un almacén industrial

## OBJETIVO DE LA PRÁCTICA

El objetivo de esta práctica es desarrollar un algoritmo de navegación que permita a un robot explorar de forma autónoma un entorno de almacén mientras genera un mapa 2D preciso del entorno utilizando datos de sensores LIDAR.

## DESCRIPCIÓN DEL ALGORITMO

1- Al empezar, el mapa está todo en gris (no sabes nada). El robot solo "ve" lo que tiene a su alrededor.  
2- El láser lanza muchos rayos en abanico y mide la distancia a lo que hay en cada dirección.  
3- Cada lectura actualiza el mapa: las casillas por las que pasa el rayo se vuelven más "libres" y la casilla donde choca se vuelve más "ocupada".  
4- El robot se mueve y vuelve a medir desde otro sitio. Así ve zonas nuevas y también confirma las que ya había visto.  
5- Se repite este proceso muchas veces y el mapa se va completando. 


<img width="772" height="394" alt="upscalemedia-transformed" src="https://github.com/user-attachments/assets/b4a9ce7e-947c-4358-9f0e-e0bf0a993edd" />


## DETALLES DEL CÓDIGO

## PROBLEMAS ENCONTRADOS

## VIDEOS
