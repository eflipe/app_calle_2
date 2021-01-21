import re
import os

file_txt = 'calles_text.txt'

basedir = os.path.abspath(os.path.dirname(__file__))
ruta = os.path.join(basedir, file_txt)

# PINO, VIRREY DEL
nombres = 'doctor luis agote'#'Doctor Eleodoro Lobos'


def sin_tilde(nombre_calle):
    return nombre_calle.translate(str.maketrans("ÁÉÍÓÚ", "AEIOU"))


def clean_txt(nombre_calle):

    nombre_calle = nombre_calle.lower()
    if 'doctor' in nombre_calle:
        long = len('doctor ')
        return nombre_calle[long:]

    return nombre_calle

def search_calle(nombre_calle=None):
    file_txt = ruta
    calle_info = []

    print(nombre_calle)
    nombre_calle = (' ').join(nombre_calle.split('_'))
    nombre_calle = clean_txt(nombre_calle)
    nombre_calle = f'{nombre_calle.upper()}'
    print("DOC BIEN", nombre_calle)
    nombre_calle_sin_tilde = sin_tilde(nombre_calle)

    pattern = re.compile(r"({0}.*\(calle\)|{1}.*\(calle\)|{0}.*\(avenida\)|{1}.*\(avenida\))".format(nombre_calle_sin_tilde, nombre_calle))

    with open(file_txt, encoding='latin1') as openfile:
        index_1 = 0

        for linea in openfile:
            linea = sin_tilde(linea)
            if pattern.search(linea) is not None:
                index_1 = 1
                continue

            if index_1 == 1:
                if nombre_calle_sin_tilde.lower().title() or nombre_calle.lower().title() in linea:
                    linea = linea.replace('- ', '')
                    linea = linea.replace('', '"').replace('', '"')
                    calle_info.append(linea.strip())
                    break

    if calle_info:
        print("INFO CALLE", calle_info[0])
        return calle_info[0]

    return [calle_info, nombre_calle_sin_tilde]


# search_calle(nombres)
# print(clean_txt(nombres))
