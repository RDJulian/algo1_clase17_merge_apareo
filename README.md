# Clase 17: Merge y Apareo

Ambos algoritmos se pueden resumir en el siguiente pseudocódigo:

```
def mezcla (suc1, suc2, unificado):
    fecha1, vendedor1, monto1 = leer(suc1)
    fecha2, vendedor2, monto2 = leer(suc2)
    while (fecha1 < MAX) or (fecha2 < MAX):
        minimo = min(fecha1, fecha2)
        while (fecha1 == mínimo):
            guardar(fecha1, vendedor1, monto1, unificado)
            fecha1, vendedor1, monto1 = leer(suc1)
        while (fecha2 == mínimo):
            guardar(fecha2, vendedor2, monto2, unificado)
            fecha2, vendedor2, monto2 = leer(suc2)
```

Donde suc1, suc2 son archivos de texto que serán leídos; unificado es el archivo final.<br>
Lo crucial es que al finalizar un archivo, la función leer() devuelva un dato "hardcodeado" igualado a MAX.<br>
MAX es una constante de valor muy alto para asegurarnos de que mínimo nunca sea MAX. Por lo tanto, evitamos leer
el archivo que ya fue totalmente recorrido.<br><br>
Se propone realizar un merge y un apareo de dos archivos con el formato (PADRON, NOMBRE, APELLIDO) y (PADRON, NOMBRE, 
APELLIDO, NOVEDAD) para un archivo de novedades. Considerar las siguientes precondiciones:
1. Los archivos están ordenados por el valor a comparar.
2. Los archivos no repiten padrón.

De esta forma, se simplifican mucho los casos de conflicto al ejecutar el apareo.

Al resolver el apareo, es importante pensar qué casos no son correctos. Si en el archivo de novedades agregamos un carácter
A, B o M para indicar la novedad, entonces:
1. No se puede dar de alta un padrón que ya existe.
2. No se puede modificar o dar de baja un padrón que no existe.