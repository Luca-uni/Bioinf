#Trimming with minimum QS of "qs" and minimum length of "read_length"
import sys
import os
import networkx as nx
import matplotlib.pyplot as plt

#MAIN



#-------------------------------------------

#Funzione di estrazione dei valori associati ai caratteri per il formato FastQ
def ascii_to_Qs(a):
  return (ord(a)-33)

def trim_read(read, quality, qs, read_length):
#Questa funzione non agisce correttamente se accettiamo read_length==1 perchè non ritorna l'ultimo char se esso è "buono" e il penultumo non lo è
  sequences = []
  start = 0
  found_start = false
  for c in quality: # c = current_char
    if(ascii_to_Qs(c) >= qs):
      if(found_start == false):
        start = quality.charAt(c)
        found_start = true

      elif(quality.charAt(c) == len(quality) and found_start):  ##per ottimizzare rimuovi il controllo su found_start dato che lo controlli sopra
        if(((len(quality)-1)-start) >= read_length):
          sequences.append(read[start:(len(quality)-1)])

    elif (found_start == true) :
      if((quality.charAt(c-1)-start) >= read_length):
        sequences.append(read[start:quality.charAt(c-1)])
      found_start = false

    


def trim_read_equalQuality(read, quality, qs, read_length):
  #...

def trimmer():
  #Configura qui i parametri per l'operazione di trimming!
  qs = 58           #qualità minima per l'inclusione di una base
  read_length = 20  #qualità minima per mantenere una read/sequenza
  f = open("dataset.txt", "r") #Configurare qui il file di input
  
  lines = f.readlines()
  curr_line_counter = 0
  curr_read = ""
  curr_quality = ""

  for x in lines:
    #Significa che la riga corrente è una read
    if ((curr_line_counter % 4) == 2): 
      curr_read = x

    #Significa che la riga corrente è il QS dell'ultima read
    elif ((curr_line_counter % 4) == 0): 
      curr_quality = x

    if(curr_read != "" and curr_quality != ""):
      trim_read(curr_read, curr_quality, qs, read_length)
    elif(curr_read == ""):
      print("Read riga {} non valida!".format(x))
    else:
      print("Quality riga {} non valida!".format(x))

    curr_line_counter += 1
	
#-------------------------------------------------------------------------
#--- Costruzione del grafo di de Brujin ---

#Fase 1, generare k-mer dalle reads senza duplicati e poi ordinalo con obj.sort()
def k_mer(reads, k):
	k_mers = []
	for x in reads:
		if(len(x) > k ):
			for(i=0, i<len(x)-k, i++):
				for y in k_mers:
					if(x[i:i+k-1] != y):
						k_mers.append(x[i:i+k-1])
	k_mers.sort()	#se si dovessero avere problemi di efficienza, seortare a mano nei cicli durante l'inserimento dei k_mers
	
#Fase 2, creazione del grafo
def de_brujin_builder(k_mers):
	G = nx.Graph()
	for x in k_mers:
		G.add_node(x[0:len(x)-1])
	for x in k_mers:
		G.add_edge(x[0:len(x)-1], x[1:len(x)])
	nx.draw(G)
