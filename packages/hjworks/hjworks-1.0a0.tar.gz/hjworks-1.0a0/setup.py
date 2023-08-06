import pathlib
from setuptools import find_packages, setup

RUTA = pathlib.Path(__file__).parent

VERSION = '1.0.a'
NOMBRE_PAQUETE = 'hjworks' 
AUTORES = 'Hector Jimenez'
CONTACTO = 'hectorjjmch@gmail.com' 
URL = 'https://trabajodepanas.com' 

LICIENCIA = 'Copyright'
DESCRIPCION = 'libreria de juegos ligeros y sencillos de python'
TIPO_DESCRIPCION = "text/markdown"


#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
REQUERIMIENTOS = ["colorama"]

setup(
    name=NOMBRE_PAQUETE,
    version=VERSION,
    description=DESCRIPCION,
    long_description_content_type=TIPO_DESCRIPCION,
    author=AUTORES,
    author_email=CONTACTO,
    url=URL,
    install_requires=REQUERIMIENTOS,
    license=LICIENCIA,
    packages=find_packages(),
    include_package_data=True
)