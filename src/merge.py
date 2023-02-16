from typing import TextIO

MAX = 999999
CAMPOS = 3
PADRON = 0
NOMBRE = 1
APELLIDO = 2


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


def leer(archivo: TextIO, errores: TextIO) -> tuple:
    """
    PRE:
    POST: Devuelve la información de la primera línea correcta en una tupla. Guarda las líneas incorrectas.
    """
    informacion = None
    lineaValida = False
    while not lineaValida and (linea := archivo.readline()):
        valores = linea.rstrip().split(',')
        if not len(valores) == CAMPOS or not esEntero(valores[PADRON]):
            generarError(errores, linea)
        else:
            informacion = (int(valores[PADRON]), valores[NOMBRE], valores[APELLIDO])
            lineaValida = True
    return informacion if informacion else (MAX,)


def procesarInformacion(informacion: tuple) -> str:
    """
    PRE: La información debe contar con los tres datos: Padron, Nombre y Apellido.
    POST: Devuelve un string con formato, incluyendo la información.
    """
    return f"{informacion[PADRON]},{informacion[NOMBRE]},{informacion[APELLIDO]}\n"


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


def merge(nombreArchivo1: str, nombreArchivo2: str, nombreMerge: str, nombreErrores: str) -> None:
    """
    PRE: Los archivos indicados a leer deben existir.
    POST: Genera un archivo nombreMerge.txt como resultado de la operacion entre ambos archivos. Las líneas que sean
    incorrectas seran guardadas en un archivo nombreErrores.txt.
    """
    with open(nombreArchivo1, "r") as archivo1, \
            open(nombreArchivo2, "r") as archivo2, \
            open(nombreMerge, "w") as archivoMerge, \
            open(nombreErrores, "w") as errores:
        informacion1 = leer(archivo1, errores)
        informacion2 = leer(archivo2, errores)
        while informacion1[PADRON] < MAX or informacion2[PADRON] < MAX:
            minimo = min(informacion1[PADRON], informacion2[PADRON])
            while informacion1[PADRON] == minimo:
                guardarInformacion(archivoMerge, informacion1)
                informacion1 = leer(archivo1, errores)
            while informacion2[PADRON] == minimo:
                guardarInformacion(archivoMerge, informacion2)
                informacion2 = leer(archivo2, errores)


def main() -> None:
    merge("archivo1.txt", "archivo2.txt", "merge.txt", "erroresMerge.txt")


main()
