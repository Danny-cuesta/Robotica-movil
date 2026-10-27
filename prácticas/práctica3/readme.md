# PRÁCTICA 3: Navegación local con VFF de un fórmula 1

## OBJETIVO DE LA PRÁCTICA
En esta práctica debemos implementar la lógica del algoritmo de navegación reactivo VFF (Campo de Fuerza Virtual), donde un coche de carreras, también formula 1, debe esquivar obstáculos en la carretera mientras se dirige a un objetivo.

El destino genera una fuerza de atracción que tira del robot hacia la meta, pero a su vez, los objetos generan una fuerza de repulsión que evita que el robot se choque con ellos.  
Para ello debemos calcular por separado ambas fuerzas, combinarlas (para que por ejemplo cuando el robot vaya hacia la meta y se encuentre un obstáculo, pueda esquivarlo sin perder el rumbo obteniendo una fuerza intermedia) y controlar el movimiento.

## DETALLES DEL CÓDIGO

Debemos calcular por partes cada fuerza, para la **FUERZA ATRACTIVA** necesitamos previamente hallar la posición del coche (xr, yr) y la posición de la meta (xg, yg), de esta forma podremos calcular el vector hacia la meta, también tendremos en cuenta su intensidad que será un número CONSTANTE porque no nos interesa que vaya variando, el coche va con la misma intensidad hacia la meta en todo momento. Por tanto, el cálculo es: **F.atractiva = a * ((xg, yg) - (xr, yr))**.

Para la **FUERZA REPULSIVA** necesitamos la DIRECCIÓN DE LA FUERZA que podemos calcular con la posición del coche (xr, yr) y la del obstáculo (xo, yo), d.fuerza.repulsiva = (xr, yr) - (xo, yo), es negativa (por eso va al revés que la otra). Por otro lado necesitamos la INTENSIDAD DE LA FUERZA que será un número NO CONSTANTE, ya que queremos que varíe en función de si el coche se aleja o se acerca del objeto. Su cálculo será **F.repulsiva =  b * ((xr, yr) - (xo, yo))**.

Por último, hacemos el cálculo de la **FUERZA RESULTANTE: f.intermedia = α*F.atractiva + β*F.repulsiva**.  
(α y β son parámetros adicionales de ajuste que indican el peso y la prioridad de cada fuerza en cada momento, es decir, si por ejemplo nos encontramos un obstáculo de frente, la fuerza repulsiva tendrá más peso y daremos más prioridad a esquivar dicho obstáculo).

## PROBLEMAS ENCONTRADOS

Al principio al combinar ambas fuerzas, el coche iba como tambaleándose, no 100% recto.

## VIDEOS
