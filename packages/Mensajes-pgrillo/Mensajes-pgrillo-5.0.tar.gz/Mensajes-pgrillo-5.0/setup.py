from setuptools import setup, find_packages

setup(
    name="Mensajes-pgrillo",
    version="5.0",
    description="Este es un paquete de ejemplo",
    long_description=open('README.md').read(), # Para que leea el el ridme 
    long_description_content_type='text/markdown',#para especificar el tipo de documento readme.me
    author="Pietro Grillo",
    author_email="yo@gmail.com",
    url="http://PGRi.info",
    license_files=['LICENSE'],#Licencia
    packages=find_packages(),#permite agregar todos los scrips, osea nos busca todas las def
    scripts=[],
    test_suite='test',
    install_requires=[i.strip() 
                      for i in open("requirements.txt").readlines()],#strip para quietarle los espacios por delante y por detras, el readlines para leer el txt
    #Los Clasificadores, las categorias

    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
    ]
    #Los clasificadores del programa los saco de https://pypi.org/pypi?%3Aaction=list_classifiers
    #Luego de haber realizado la busqueda de los clasificadores de mi programa instalo los paquetes 'build' & 'twine', con el sgte comando
    #pip install build twine --upgrade
    
    # Luego ejecuto el sgte comando en la terminal
    # python -m build 
    #Con esto creo el paquete o el redistribuible

    #Luego ejecutamos el sgte comando en la terminal
    #python -m twine check dist/*
    #Con esto verificaremos todos los paquetes estes corresctamente y listo para publicar
    #con esto si dice "PASSED" es porque esta todo correcto en caso de un "WARNING", ojo, revisar lo que pide revisar.
    #
)