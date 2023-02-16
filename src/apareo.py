from typing import TextIO

MAX = 999999
CAMPOS = 3
PADRON = 0
NOMBRE = 1
APELLIDO = 2
TIPO_NOVEDAD = 3
ALTA = 'A'
BAJA = 'B'
MODIFICACION = 'M'


def esEntero(numero: str) -> bool:
    """
    PRE:
    POST: Devuelve True si el número es entero. False de lo contrario.
    """
    try:
        int(numero)
        return True
    except ValueError:
        return False


def procesarValores(campos: int, valores: list) -> tuple:
    """
    PRE: Los valores deben ser de una línea valida.
    POST: Devuelve una tupla con toda la información, dependiendo de si la línea es del archivo maestro o de novedades.
    """
    # Funcion auxiliar para reutilizar leer().
    if campos == CAMPOS:
        return int(valores[PADRON]), valores[NOMBRE], valores[APELLIDO]
    else:
        return int(valores[PADRON]), valores[NOMBRE], valores[APELLIDO], valores[TIPO_NOVEDAD]


def leer(archivo: TextIO, errores: TextIO, campos: int) -> tuple:
    """
    PRE:
    POST: Devuelve la información de la primera línea correcta en una tupla. Guarda las líneas incorrectas.
    """
    informacion = None
    lineaValida = False
    while not lineaValida and (linea := archivo.readline()):
        valores = linea.rstrip().split(',')
        # Capaz estaria bueno hacer una funcion que filtre dependiendo de los campos pasados por parametro.
        # Si son 3, revisa tal cual está declarado.
        # Sin son 4, revisa lo mismo y si la letra es una de las declaradas (A, B, M).
        if not len(valores) == campos or not esEntero(valores[PADRON]):
            generarError(errores, linea)
        else:
            informacion = procesarValores(campos, valores)
            lineaValida = True
    return informacion if informacion else (MAX,)


def procesarInformacion(informacion: tuple) -> str:
    """
    PRE: La información debe contar con los tres datos: Padron, Nombre y Apellido.
    POST: Devuelve un string con formato, incluyendo la información.
    """
    return f"{informacion[PADRON]},{informacion[NOMBRE]},{informacion[APELLIDO]}\n"


def procesarLineaErronea(informacion: tuple) -> str:
    """
    PRE: La información debe contar con los cuatro datos: Padron, Nombre, Apellido y Tipo de Actualizacion.
    POST: Devuelve un string con formato, incluyendo la información.
    """
    return f"{informacion[PADRON]},{informacion[NOMBRE]},{informacion[APELLIDO]},{informacion[TIPO_NOVEDAD]}\n"


def guardarInformacion(archivo: TextIO, informacion: tuple) -> None:
    """
    PRE: La información debe contar con los tres datos: Padron, Nombre y Apellido.
    POST: Guarda la información en el archivo deseado.
    """
    archivo.write(procesarInformacion(informacion))


def generarError(archivo: TextIO, linea: str) -> None:
    """
    PRE:
    POST: Guarda la línea incorrecta en el archivo. Si la línea es vacia, guarda un mensaje acorde.
    """
    if linea == '\n':
        archivo.write(f"/LINEA VACIA/\n")
    else:
        archivo.write(f"{linea}")


def hayCoincidencia(padron1: int, padron2: int) -> bool:
    """
    PRE:
    POST: Devuelve True si hay coincidencia y ninguno de los padrones es MAX. False de lo contrario.
    """
    return padron1 == padron2 and padron1 != MAX and padron2 != MAX


def resolverNovedad(archivo: TextIO, errores: TextIO, informacion: tuple) -> None:
    """
    PRE: La información debe ser completa, incluyendo el tipo de novedad a resolver.
    POST: Resuelve la novedad. Si no es posible procesarla, guarda la información en el archivo de errores.
    """
    if informacion[TIPO_NOVEDAD] == ALTA:
        guardarInformacion(archivo, informacion)
    else:
        generarError(errores, procesarLineaErronea(informacion))


def resolverCoincidencia(archivo: TextIO, errores: TextIO, informacion1: tuple, informacion2: tuple) -> None:
    """
    PRE: La información debe ser completa, incluyendo el tipo de novedad a resolver.
    POST: Resuelve la coincidencia. Si no es posible procesarla, guarda la información en el archivo de errores.
    """
    if informacion2[TIPO_NOVEDAD] == MODIFICACION:
        guardarInformacion(archivo, informacion2)
    elif not informacion2[TIPO_NOVEDAD] == BAJA:
        guardarInformacion(archivo, informacion1)
        generarError(errores, procesarLineaErronea(informacion2))


def apareo(nombreArchivo1: str, nombreArchivo2: str, nombreApareo: str, nombreErrores: str) -> None:
    """
    PRE: Los archivos indicados a leer deben existir. El archivo nombreArchivo2 debe ser de novedades.
    POST: Genera un archivo nombreApareo.txt como resultado de la operacion entre ambos archivos. Las líneas que sean
    incorrectas seran guardadas en un archivo nombreErrores.txt.
    """
    with open(nombreArchivo1, "r") as archivo1, \
            open(nombreArchivo2, "r") as archivo2, \
            open(nombreApareo, "w") as archivoApareo, \
            open(nombreErrores, "w") as errores:
        informacion1 = leer(archivo1, errores, CAMPOS)
        informacion2 = leer(archivo2, errores, CAMPOS + 1)
        while informacion1[PADRON] < MAX or informacion2[PADRON] < MAX:
            minimo = min(informacion1[PADRON], informacion2[PADRON])
            while hayCoincidencia(informacion1[PADRON], informacion2[PADRON]):
                resolverCoincidencia(archivoApareo, errores, informacion1, informacion2)
                informacion1 = leer(archivo1, errores, CAMPOS)
                informacion2 = leer(archivo2, errores, CAMPOS + 1)
            while informacion1[PADRON] == minimo:
                guardarInformacion(archivoApareo, informacion1)
                informacion1 = leer(archivo1, errores, CAMPOS)
            while informacion2[PADRON] == minimo:
                resolverNovedad(archivoApareo, errores, informacion2)
                informacion2 = leer(archivo2, errores, CAMPOS + 1)


def main():
    # Precondicion de archivos: no se repiten padrones en ninguno de los archivos. De esta forma, se simplifican mucho
    # los distintos casos:
    # 1. Si hay una coincidencia, resolver hasta que no haya coincidencia. La unica operacion que no es posible en este
    # caso es dar de alta.
    # 2. Si no hay coincidencia, guardar las líneas del archivo maestro.
    # 3. Cuando se procese el archivo de novedades, estamos seguros de que no hay una coincidencia. Por lo tanto, lo
    # unico posible en este caso es dar de alta.
    apareo("archivo1.txt", "archivo3.txt", "apareo.txt", "erroresApareo.txt")


main()
