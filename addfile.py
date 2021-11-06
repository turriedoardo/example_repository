# importo le librerie

import csv
import os
import shutil
import argparse
import sys
import pandas as pd

parser = argparse.ArgumentParser() # inizializzo il parser
parser.add_argument('--file', help='Enter the name of the file to move', type= str) # aggiungo il file al parser come argomento
arg = parser.parse_args() # assegno il namespace dei parametri ad arg

file = arg.file # assegno a file il valore dell'argomento del parser
os.chdir('files') # cambio la directory di lavoro
filepath = os.path.abspath(file) # assegno il percorso di file a filepath

if not os.path.exists(filepath):
    sys.exit('The file does not exist or is in another path!!') # stampo messaggio di errore se inserito come argomento un file che non esiste o che non si trova nella cartella

# creo lista formato immagini
images_fmt = ['png', 'jpg', 'jpeg']

# creo lista formato testo
text_fmt = ['txt', 'odt']

# se non esiste, creo cartella per immagini
if not os.path.isdir('images'):
    os.mkdir('images')

# se non esiste, creo cartella per file audio
if not os.path.isdir('audio'):
    os.mkdir('audio')

# se non esiste, creo cartella per file di testo
if not os.path.isdir('doc'):
    os.mkdir('doc')

size = os.path.getsize(filepath) # assegno a size la dimensione del file
    
filename, ext = file.split('.') # assegno a filename il nome e a ext il formato del file

if ext in images_fmt: # seleziono le immagini
    file_type = 'image' # assegno a file_type il tipo di file
    shutil.move(filepath, 'images') # sposto l'immagine in images

# utilizzo lo stesso procedimento con file audio o di testo
elif ext == 'mp3':
    file_type = 'audio'
    shutil.move(filepath, 'audio')

elif ext in text_fmt:
    file_type = 'doc'
    shutil.move(filepath, 'doc')

# se è di un altro formato, avviso l'utente
else:
    print(f'I file di tipo {ext} non sono supportati!')

# se il recap non è presente, lo creo
if not os.path.isfile('recap.csv'): 
    new_recap = open('recap.csv', mode = 'w')
    writer = csv.writer(new_recap)
    writer.writerow(['filename', 'type', 'size'])   
    new_recap.close()

# importo il file di recap come dataframe
data = pd.read_csv('recap.csv')

# estraggo la colonna dei nomi dei file nel recap
filenames = data.filename.tolist()

# apro il recap per aggiungere info sul file spostato
recap = open('recap.csv', mode = 'a')
writer = csv.writer(recap)

# se è già presente nel recap un file con lo stesso nome, lo aggiungo solo se dimensione e formato sono diversi
if filename in filenames:
    
    if file_type != data.type[filenames.index(filename)] and f'{size}B' != data['size'][filenames.index(filename)]:

        writer.writerow([filename, file_type, f'{size}B'])
    
    else:
        print('The file was already in the recap!')
            
# se non è presente un file con quel nome, lo aggiungo al recap
else: 
    writer.writerow([filename, file_type, f'{size}B'])

# chiudo il file di recap
recap.close()

print(f'''{filename}  size: {size}B  type: {file_type}
File moved successfully!''') # stampo un messaggio di conferma
