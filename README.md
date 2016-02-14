Programa de parseo de un archivo con registros de UniProt

Script basado en Python 2.7

Usage: 

  $python BigData_JAL.py Nombre-archivo-entrada Fichero-salida-1 Fichero-salida-2
  
El nombre de archivo de entrada (que contiene los registros de Uniprot) debe especificar la ruta del mismo si no está en el directorio de trabajo

El fichero de salida 1 es de texto, con campos tabulados, contiene información 
  - Accession Number Principal
  - Nombre del gen
  - Identificador taxonómico NCBI
  - Anotación GO (Gene Ontology)
 
El fichero de salida 2 es de texto, formato fasta, con campos delimitados por '|'. Contiene:
  - Accession Number Principal
  - Nombre del gen
  - Identificador taxonómico NCBI
  - Secuencia de la proteína

Los ficheros de salida se almacenan, por defecto, en el directorio de trabajo y SOBRE-ESCRIBEN ficheros pre-existentes con el mismo nombre
