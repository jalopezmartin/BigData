#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
	Máster en Bioinformática y Biología Computacional, ENS-ISCIII
	Curso: 2015-2016
	Memoria de Evaluación de la Asignatura: Big Data Parsing and Processing
	Script del ejercicio 2.
	Autor: José Antonio López Martín

El siguiente paso del trabajo es, mediante un programa escrito en Python 2, extraer para cada proteína
la siguiente información.

El programa reconocerá tres parámetros, siendo el
1.- primero el del fichero de entrada,
2.- el segundo el del fichero de salida de datos tabulares y el
3.- tercero el del fichero de salida de datos FASTA.

Tendréis que mirar qué campos contienen los datos a extraer en la documentación de UniProt,
http://web.expasy.org/docs/userman.html, y explicarlo en la memoria.

Los datos a extraer son:
   a) accession number principal
   b) El nombre de gen (y buscad en la documentación de UniProt qué campo lo contiene)
   c) Los identificadores de NCBI de los organismos en los que aparece esa proteína
   d) Las anotaciones de Gene Ontology que no sean inferidas de anotaciones electrónicas,
       (mirad http://geneontology.org/page/guide-go-evidence-codes).
   e) La secuencia de la proteína

El fichero tabular generado por el programa tiene que tener el siguiente formato:
    Q8IY21    DDX60   9606    GO:0005737
donde el primer elemento es el accession number principal, el segundo es el nombre de gen
(y si no tuviese, un guión), el tercero es el identificador taxonómico y el cuarto es un
término de gene ontology.

Deberán aparecer tantas líneas como anotaciones de Gene Ontology encontradas y tantas líneas como organismos.
Por ejemplo, si la proteína AAAAA está en dos organismos y tiene tres anotaciones, deberán aparecer 6 líneas
en el fichero de salida.

El fichero FASTA generado por el programa contendrá la secuencia de cada proteína, y usará el siguiente formato
en la línea de comentarios de cada secuencia:
    >sp|Q8IY21|DDX60|9606
mostrando el accession number principal, el nombre de gen (si no tuviera, se pondría un guión) y los
identificadores taxonómicos de los organismos, unidos por comas estos últimos.

'''

# Importamos los módulos que necesitaremos para algunas de las funciones del script

from __future__ import print_function
import sys
import io
import re

# Comprobamos el número de parámetros de entrada

if __name__ == '__main__':

    if len(sys.argv) == 4:

        entrada = sys.argv[1]
        salida_tab = sys.argv[2]
        salida_fasta = sys.argv[3]

        # Procesamiento del fichero de entrada

        try:

            # Estamos abriendo el fichero con el encoding 'latin-1'
            # Para text mining lo recomendable es el encoding 'utf-8'

            with io.open(entrada, 'r', encoding="latin-1") as infile:

                # El programa inicializa archivos del mismo nombre que los definidos como salida. Por eso avisa al
                # usuario

                print("\nSi existen los archivos " + salida_fasta + " y " + salida_tab + ", se sobre-escribirán\n")
                confirm = raw_input("\nEstá seguro (S/N)?\n")

                if confirm == "S":
                    print("\nProcesando fichero ", entrada, "\n")

                    # Inicialización de variables
                    # Los datos a extraer son:
                    # a) accn - accession number principal (campo AC de UniProt)
                    # b) genid -El nombre de gen (campo GN de UniProt)
                    # c) taxid - identificador taxonómico NCBI (campo OX de UniProt)
                    # d) goterm - Las anotaciones de Gene Ontology (excluiremos IEA - inferidas de
                    #    anotaciones electrónicas)
                    # e) seq - La secuencia de la proteína (campo SQ de UniProt)

                    accn = '' # creamos un string vacio para el accession number principal
                    genid = '-' # el string por defecto será un guión, porque podrá no existir nombre del gen
                    taxid = '' # creamos una cadena vacía para almacenar los identificadores taxonómicos
                    golist = [] # creamos una lista vacía porque podrán exstir varios términos GO
                    seq = '' # incluiremos la secuencia como string
                    readingseq = False # flag para indicar cuándo empieza la secuencia (cuando tome el valor 'True')
                    infofasta = "" # contendrá los datos extraidos por cada registro UniProt, en formato fasta
                    infotab = "" #contendrá los datos extraídos por cada registro UniProt, en formato tabular

                    # Inicializamos también los dos archivos de salida, para evitar que se añada a información previa

                    salidaf = open(salida_fasta, 'w')
                    salidaf.write('')
                    salidaf.close()
                    salidat = open(salida_tab, 'w')
                    salidat.write('')
                    salidat.close()



                    # Comenzamos a iterar sobre el manejador del fichero 'entrada'(sys.argv[1]), línea a línea,
                    # sin cargarlo entero en memoria

                    for linea in infile:

                        # para cada línea, eliminamos el carácter especial de salto de línea

                        linea = linea.rstrip('\n')

                        # Al llegar al final del registro (línea que sólo contiene '//') generamos la orden de añadir
                        # la información extraída a los archivos de salida fasta y tabular.

                        if re.search('^//', linea) is not None:

                            # Escribimos sobre el fichero fasta, ordenando la información extraída
                            # según los requerimientos del trabajo

                            with open(salida_fasta, 'a+') as fastafile:
                                infofasta = ">sp|%s|%s|%s\n%s\n" % (accn, genid, taxid, seq)
                                fastafile.write(infofasta + '\n')

                            # Escribimos las líneas correspondientes al fichero tabular, tantas como anotaciones GO.
                            # Tras revisar la información del formato de registros Uniprot, se constata que el
                            # identificador taxonómico ('taxid') es único, por lo que no creamos una segunda lista
                            # para iterar sobre él (ver memoria)

                            with open(salida_tab, 'a+') as tabfile:
                                for goterm in golist:
                                    infotab = "%s\t%s\t%s\t%s" % (accn, genid, taxid, goterm)
                                    tabfile.write(infotab + "\n")

                            # Tras la lectura, extracción de datos y su volcado a archivo, se restauran
                            # las variables referentes a cada registro Uniprot a sus valores por defecto

                            accn = ''
                            genid = '-'
                            # taxidlist = []
                            taxid = ''
                            golist = []
                            seq = ''
                            readingseq = False

                        # Si el programa está leyendo una secuencia (readingseq == True), extraemos la información
                        # de la misma para almacenarla en la variable 'seq'

                        elif readingseq:

                            # Quito todos los espacios intermedios

                            linea = re.compile(r"\s+").sub('', linea)

                            # Y concateno

                            seq += linea

                        # Mientras readingseq == False, no está leyendo secuencia, por lo que buscamos los patrones
                        # que identifican el resto de los campos que contienen la información solicitada

                        else:

                            # Primero, el inicio del campo de la secuencia (la línea empieza con 'SQ')

                            seqmatch = re.search(r"^SQ", linea)
                            if seqmatch is not None:

                                # El match indica que se ha detectado la primera línea del campo que contiene la
                                # información de secuencia

                                readingseq = True

                                # De detectar esta línea, iteraríamos sobre la/las siguientes con el flag "readingseq"
                                # convertido a 'True', por lo que extreríamos toda la información de la secuencia hasta
                                # detectar la línea que comienza con '//', tál y como se describe en los dos párrafos
                                # previos.
                                # De no detectarla, seguimos buscando otros patrones:
                                # Probamos con el que identifica el Accession Number Principal (ver Memoria). Esta
                                # expresión regular está recomendada en la propia documentación de Uniprot, y tiene la
                                # finalidad de capturar todos las versiones de formatos de Accession Number utilizados

                            else:
                                accnmatch = re.search(r"^AC +([OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2});", linea)
                                if accnmatch is not None:

                                    # Si hay match, extraemos el primer Accesion Number (grupo uno de la expresión
                                    # regular), que es el principal

                                    accn = accnmatch.group(1)

                                # Si no hay match, seguimos buscando otro patron en la misma línea,
                                # el del nombre del gen (si lo hubiera)

                                else:
                                    genidmatch = re.search(r"^GN +.*Name=([A-Za-z0-9]+);", linea)
                                    if genidmatch is not None:

                                        # Si hay match, extraemos el nombre del gen de la proteína
                                        # (grupo 1 de la expresión regular)

                                        genid = genidmatch.group(1)

                                    # Si no hay match, seguimos buscando patrones en la misma línea. En este caso el del
                                    # identificador taxonómico (que es único por registro, según explicamos en memoria)
                                    # De haber sido múltiple, habríamos extraído la información en una lista.

                                    else:
                                        taxidmatch = re.search(r"^OX +NCBI_TaxID=([0-9]+);", linea)
                                        if taxidmatch is not None:

                                            # Si hay match, se captura la información del grupo 1 de la expresión regular

                                            taxid = taxidmatch.group(1)

                                        # De no haber match, se busca la existencia de patrones que
                                        # reconozcan anotaciones GO

                                        else:
                                            gomatch = re.search(r"^DR +GO; (GO:[0-9]+)", linea)
                                            if gomatch is not None:

                                                # Si hay match estamos ante una línea que contiene una anotación GO,
                                                # de la que nos interesa el grupo (1). No obstante, siguiendo las
                                                # instrucciones, antes de extraer dicha información excluiremos las
                                                # líneas que contengan los caracteres IEA.

                                                excludematch = re.search(r" IEA:", linea)
                                                if excludematch is None:

                                                # Si no hay match, extraeremos el código de la anotación GO, a partir
                                                # del grupo 1 de la expresión regular. Puede haber más de una por
                                                # registro, pero siempre es una por línea.
                                                # Las añadiremos a la lista 'golist'

                                                    golist.append(gomatch.group(1))

                else:
                    print('Seleccione otros nombres de ficheros de salida. Adiós.')

        except IOError as e:
            print('Error de lectura de fichero {0}: {1}'.format(e.errno, e.strerror), file=sys.stderr)
        # raise
        except:
            print('Error inesperado: ', sys.exc_info()[0], file=sys.stderr)
            raise

    else:
        raise AssertionError("""

            Numero erróneo de argumentos.
            El comando tiene el siguiente formato:
            >>>python BigData_JAL.py fichero-de-entrada salida-tabular salida-fasta

            """)
