# Programa analise_nodal_sistematica.py
# Autora: Karen dos Anjos Arcoverde
# Data: 12/09/2020
#
# Descrição de um circuito por uma "netlist",
# obtem tensões nodais de um circuito resistivo linear com fontes DC 
# pela análise sistemática nodal
#


#importando bibliotecas numpy e scipy para matrizes 
import numpy as np
from scipy import linalg
from numpy import *


##################################################################### Funcoes #####################################################################

def resultado_final (m,maior_valor_nó,dimensoes_extras):
	indice = 0
	
	for indice in range (maior_valor_nó):
		print("e"+ str(indice + 1),'= {:.2f}'.format(m[indice][0]))
		
	indice = 0
	if (dimensoes_extras != 0):
		indice += maior_valor_nó
		for (indice) in range (indice,(dimensoes_extras + maior_valor_nó)):
			print("j"+ str(indice + 1),'= {:.2f}'.format(m[indice][0]))
		

	
def montar_q(lista_componentes,q,index):
	
	
	##I
	if (lista_componentes[index][0] == 'I' or lista_componentes[index][0] == 'i'):
		if (lista_componentes[index + 3] == "DC" or lista_componentes[index + 3] == "dc"):
			if (lista_componentes[index + 1] == 0):
				(q[int(lista_componentes[index + 2]) - 1][0]) += (lista_componentes[index + 4])	
		
	
			if (lista_componentes[index + 2] == 0):
				(q[int(lista_componentes[index + 1]) - 1][0]) += -(lista_componentes[index + 4])
		
			elif ((lista_componentes[index + 1] != 0) and (lista_componentes[index + 2] != 0)):
				(q[int(lista_componentes[index + 1]) - 1][0]) += -(lista_componentes[index + 4])
				(q[int(lista_componentes[index + 2]) - 1][0]) += (lista_componentes[index + 4])
		
		
	##V
	if (lista_componentes[index][0] == 'V' or lista_componentes[index][0] == 'v'):
		if (lista_componentes[index + 3] == "DC" or lista_componentes[index + 3] == "dc"):
			(q[q.shape[0]-1][0]) += (lista_componentes[index + 4])
		
		
	return q
	
def montar_m (yn,q):
	inv_yn = np.linalg.inv(yn)
	m = np.dot(inv_yn, q)
	
	return m

def montar_yn(lista_componentes, yn, index, corrente,w):

	
	
	if (lista_componentes[index + 1] == 0): #corrente entrando no nó
		##R
		if (lista_componentes[index][0] == 'R' or lista_componentes[index][0] == 'r'):
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 2]) - 1]) += (1/(lista_componentes[index + 3])) 
		##G
		if (lista_componentes[index][0] == 'G' or lista_componentes[index][0] == 'g'):
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 3]) - 1]) += -(lista_componentes[index + 5])
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 4]) - 1]) += (lista_componentes[index + 5])
			
			if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 4]) - 1]) += (lista_componentes[index + 5])	
		
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 3]) - 1]) += -(lista_componentes[index + 5])
		##V
		if (lista_componentes[index][0] == 'V' or lista_componentes[index][0] == 'v'):
			(yn[yn.shape[0]-1][int(lista_componentes[index + 2]) - 1]) += -1
			(yn[int(lista_componentes[index + 2]) - 1][yn.shape[1]-1]) += -1
		
		##B
		if (lista_componentes[index][0] == 'B' or lista_componentes[index][0] == 'b'):
			(yn[int(lista_componentes[index + 2]) - 1][yn.shape[1]-1]) += -(lista_componentes[index + 5])
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += 1
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -1
				(yn[int(lista_componentes[index + 3]) - 1][yn.shape[1]-1]) += 1
				(yn[int(lista_componentes[index + 4]) - 1][yn.shape[1]-1]) += -1
			
			if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -1
				(yn[int(lista_componentes[index + 4]) - 1][yn.shape[1]-1]) += -1
			
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += 1
				(yn[int(lista_componentes[index + 3]) - 1][yn.shape[1]-1]) += 1
				
		
		##A
		if (lista_componentes[index][0] == 'A' or lista_componentes[index][0] == 'a'):
			(yn[int(lista_componentes[index + 2]) - 1][yn.shape[1]-1]) += -1
			(yn[yn.shape[0]-1][int(lista_componentes[index + 2]) - 1]) += 1
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += (lista_componentes[index + 5])
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -(lista_componentes[index + 5])			
			
			if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -(lista_componentes[index + 5])
					
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += (lista_componentes[index + 5])
				
		##H
		if (lista_componentes[index][0] == 'H' or lista_componentes[index][0] == 'h'):
			if (corrente == "jx"):
				(yn[int(lista_componentes[index + 3]) - 1][yn.shape[1]-1]) += 1
				(yn[int(lista_componentes[index + 4]) - 1][yn.shape[1]-1]) += -1		
				if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
					(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += -1
					(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += 1
					
				if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
					(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += 1	
			
				if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
					(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += -1
					
			if (corrente == "jy"):
				(yn[int(lista_componentes[index + 2]) - 1][yn.shape[1]-1]) += -1
				(yn[yn.shape[0]-1][int(lista_componentes[index + 2]) - 1]) += 1
			
				(yn[yn.shape[0]-1][yn.shape[1]-2]) += (lista_componentes[index + 5])
				
		##C		
		if (lista_componentes[index][0] == 'C' or lista_componentes[index][0] == 'c'): 
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 2]) - 1]) += j*w*(lista_componentes[index + 3]))
			
		##X	
		if (lista_componentes[index][0] == 'X' or lista_componentes[index][0] == 'x'): 
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 2]) - 1]) += 1/(j*w*(lista_componentes[index + 3]))
			
	
	if (lista_componentes[index + 2] == 0): #corrente saindo do nó
		## R
		if (lista_componentes[index][0] == 'R' or lista_componentes[index][0] == 'r'):
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 1]) - 1]) += (1/(lista_componentes[index + 3])) 
		## G
		if (lista_componentes[index][0] == 'G' or lista_componentes[index][0] == 'g'):
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
				(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 3]) - 1]) += (lista_componentes[index + 5])
				(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 4]) - 1]) += -(lista_componentes[index + 5])
			
			if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 4]) - 1]) += -(lista_componentes[index + 5])	
		
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 3]) - 1]) += (lista_componentes[index + 5])
		##V
		if (lista_componentes[index][0] == 'V' or lista_componentes[index][0] == 'v'):
			(yn[yn.shape[0]-1][int(lista_componentes[index + 1]) - 1]) += 1
			(yn[int(lista_componentes[index + 1]) - 1][yn.shape[1]-1]) += 1
		
		##B
		if (lista_componentes[index][0] == 'B' or lista_componentes[index][0] == 'b'):
			(yn[int(lista_componentes[index + 1]) - 1][yn.shape[1]-1]) += (lista_componentes[index + 5])
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += 1
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -1
				(yn[int(lista_componentes[index + 3]) - 1][yn.shape[1]-1]) += 1
				(yn[int(lista_componentes[index + 4]) - 1][yn.shape[1]-1]) += -1
			
			if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -1
				(yn[int(lista_componentes[index + 4]) - 1][yn.shape[1]-1]) += -1
			
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += 1
				(yn[int(lista_componentes[index + 3]) - 1][yn.shape[1]-1]) += 1
		
		##A
		if (lista_componentes[index][0] == 'A' or lista_componentes[index][0] == 'a'):		
			(yn[int(lista_componentes[index + 1]) - 1][yn.shape[1]-1]) += 1
			(yn[yn.shape[0]-1][int(lista_componentes[index + 1]) - 1]) += -1
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += (lista_componentes[index + 5])
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -(lista_componentes[index + 5])				
			
			if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -(lista_componentes[index + 5])	
			
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += (lista_componentes[index + 5])
				
		##H
		if (lista_componentes[index][0] == 'H' or lista_componentes[index][0] == 'h'):
			if (corrente == "jx"):
				(yn[int(lista_componentes[index + 3]) - 1][yn.shape[1]-1]) += 1
				(yn[int(lista_componentes[index + 4]) - 1][yn.shape[1]-1]) += -1		
				if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
					(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += -1
					(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += 1
					
				if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
					(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += 1	
			
				if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
					(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += -1
					
			if (corrente == "jy"):
				(yn[int(lista_componentes[index + 1]) - 1][yn.shape[1]-1]) += 1
				(yn[yn.shape[0]-1][int(lista_componentes[index + 1]) - 1]) += -1
			
				(yn[yn.shape[0]-1][yn.shape[1]-2]) += (lista_componentes[index + 5])
				
		##C		
		if (lista_componentes[index][0] == 'C' or lista_componentes[index][0] == 'c'): 
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 1]) - 1]) += j*w*(lista_componentes[index + 3]))
			
		##X	
		if (lista_componentes[index][0] == 'X' or lista_componentes[index][0] == 'x'): 
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 1]) - 1]) += 1/(j*w*(lista_componentes[index + 3]))
			
			
				
		
		

	elif ((lista_componentes[index + 1] != 0) and (lista_componentes[index + 2] != 0)):
		##R
		if (lista_componentes[index][0] == 'R' or lista_componentes[index][0] == 'r'):
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 1]) - 1]) += (1/(lista_componentes[index + 3]))
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 2]) - 1]) += (1/(lista_componentes[index + 3]))
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 2]) - 1]) += -(1/(lista_componentes[index + 3]))
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 1]) - 1]) += -(1/(lista_componentes[index + 3]))
		##G
		if (lista_componentes[index][0] == 'G' or lista_componentes[index][0] == 'g'):		
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
				(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 3]) - 1]) += (lista_componentes[index + 5])
				(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 4]) - 1]) += -(lista_componentes[index + 5])
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 3]) - 1]) += -(lista_componentes[index + 5])
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 4]) - 1]) += (lista_componentes[index + 5])
			
			if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
				(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 4]) - 1]) += -(lista_componentes[index + 5])
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 4]) - 1]) += (lista_componentes[index + 5])
		
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
				(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 3]) - 1]) += (lista_componentes[index + 5])		
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 3]) - 1]) += -(lista_componentes[index + 5])
		##V
		if (lista_componentes[index][0] == 'V' or lista_componentes[index][0] == 'v'):
			(yn[yn.shape[0]-1][int(lista_componentes[index + 1]) - 1]) += 1
			(yn[yn.shape[0]-1][int(lista_componentes[index + 2]) - 1]) += -1
			(yn[int(lista_componentes[index + 1]) - 1][yn.shape[1]-1]) += 1
			(yn[int(lista_componentes[index + 2]) - 1][yn.shape[1]-1]) += -1
		
		
		##B
		if (lista_componentes[index][0] == 'B' or lista_componentes[index][0] == 'b'):
			(yn[int(lista_componentes[index + 1]) - 1][yn.shape[1]-1]) += (lista_componentes[index + 5])
			(yn[int(lista_componentes[index + 2]) - 1][yn.shape[1]-1]) += -(lista_componentes[index + 5])
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += 1
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -1
				(yn[int(lista_componentes[index + 3]) - 1][yn.shape[1]-1]) += 1
				(yn[int(lista_componentes[index + 4]) - 1][yn.shape[1]-1]) += -1
			
			if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -1
				(yn[int(lista_componentes[index + 4]) - 1][yn.shape[1]-1]) += -1
			
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += 1
				(yn[int(lista_componentes[index + 3]) - 1][yn.shape[1]-1]) += 1
		
		
		##A
		if (lista_componentes[index][0] == 'A' or lista_componentes[index][0] == 'a'):
			(yn[int(lista_componentes[index + 1]) - 1][yn.shape[1]-1]) += 1
			(yn[int(lista_componentes[index + 2]) - 1][yn.shape[1]-1]) += -1		
			(yn[yn.shape[0]-1][int(lista_componentes[index + 1]) - 1]) += -1
			(yn[yn.shape[0]-1][int(lista_componentes[index + 2]) - 1]) += 1
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += (lista_componentes[index + 5])
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -(lista_componentes[index + 5])
					
			if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -(lista_componentes[index + 5])	
			
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += (lista_componentes[index + 5])
			
			
		##H
		if (lista_componentes[index][0] == 'H' or lista_componentes[index][0] == 'h'):
			if (corrente == "jx"):
				(yn[int(lista_componentes[index + 3]) - 1][yn.shape[1]-1]) += 1
				(yn[int(lista_componentes[index + 4]) - 1][yn.shape[1]-1]) += -1		
				if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
					(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += -1
					(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += 1
					
				if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
					(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += 1	
			
				if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
					(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += -1
					
			if (corrente == "jy"):
				(yn[int(lista_componentes[index + 1]) - 1][yn.shape[1]-1]) += 1
				(yn[int(lista_componentes[index + 2]) - 1][yn.shape[1]-1]) += -1		
				if (lista_componentes[index + 1] != 0 and lista_componentes[index + 2] != 0):
					(yn[yn.shape[0]-1][int(lista_componentes[index + 1]) - 1]) += -1
					(yn[yn.shape[0]-1][int(lista_componentes[index + 2]) - 1]) += 1
					
				if (lista_componentes[index + 1] == 0 and lista_componentes[index + 2] != 0):
					(yn[yn.shape[0]-1][int(lista_componentes[index + 1]) - 1]) += 1	
			
				if (lista_componentes[index + 1] != 0 and lista_componentes[index + 2] == 0):
					(yn[yn.shape[0]-1][int(lista_componentes[index + 1]) - 1]) += -1	
					
				(yn[yn.shape[0]-1][yn.shape[1]-2]) += (lista_componentes[index + 5])
				
		##C		
		if (lista_componentes[index][0] == 'C' or lista_componentes[index][0] == 'c'): 
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 1]) - 1]) += j*w*(lista_componentes[index + 3])
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 2]) - 1]) += j*w*(lista_componentes[index + 3])
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 2]) - 1]) += -j*w*(lista_componentes[index + 3])
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 1]) - 1]) += -j*w*(lista_componentes[index + 3])
			
		##X	
		if (lista_componentes[index][0] == 'X' or lista_componentes[index][0] == 'x'): 
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 1]) - 1]) += 1/(j*w*(lista_componentes[index + 3]))
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 2]) - 1]) += 1/(j*w*(lista_componentes[index + 3]))
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 2]) - 1]) += -1/(j*w*(lista_componentes[index + 3]))
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 1]) - 1]) += -1/(j*w*(lista_componentes[index + 3]))
				
		
			
	return yn

##################################################################### Programa Principal #####################################################################
def menu():
	componente = ""
	dimensoes_extras = 0 
	indice = 0
	index = 0
	corrente = ""
	w = 0
	maior_valor_nó = 0
	lista_componentes = []
	print()
	print("##################################################################################################################################################################################")
	print("## -------------------------------------------------------------------------- INSTRUÇÕES -------------------------------------------------------------------------------------- ##")
	print("## Digite:                                                                                                                                                                      ##")       
	print("## PARA RESISTÊNCIA: <R+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <valor da resistência>                                                                                              ##")
	print("## PARA FONTE DE CORRENTE INDEPENDENTE: <I+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <tipo de fonte (DC)> <valor da fonte de corrente>                                                ##")
	print("## PARA FONTE DE TENSÃO INDEPENDENTE: <V+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <tipo de fonte (DC)> <valor da fonte de tensão>                                                    ##")
	print("## PARA FONTE DE CORRENTE CONTROLADA POR TENSÃO: <G+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <Nó f> <Nó g> <valor do G>                                                              ##")
	print("## PARA FONTE DE CORRENTE CONTROLADA POR CORRENTE: <B+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <Nó f> <Nó g> <valor do B>                                                            ##")
	print("## PARA FONTE DE TENSÃO CONTROLADA POR TENSÃO: <A+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <Nó f> <Nó g> <valor do A>                                                                ##")
	print("## PARA FONTE DE TENSÃO CONTROLADA POR CORRENTE: <H+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <Nó f> <Nó g> <valor do H>	                                                           ##")
	print("## PARA INDUTOR: <X+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <indutância(L)>                                       	                                                               ##")
	print("## PARA CAPACITOR: <C+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <indutância(C)>                                       	                                                               ##")
	print("## PARA INDUTÂNCIA MÚTUA: <K+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <indutância(L1)> <Nó f> <Nó g> <indutância(L2)> <indutância mútua(M)>                                          ##")
	print("## PARA FONTE DE TENSÃO SENOIDAL: <V+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <tipo de fonte (SIN)> <nível contínuo> <amplitude> <frequência> <atraso> <atenuação> <ângulo> <ciclos> ##")
	print("##################################################################################################################################################################################")
	print()
	print("##################################################################################################################################################################################")
	print("## IMPORTANTE: RESPEITAR A POLARIDADE DAS FONTES DE TENSÃO E CORRENTE. CONSIDERAR NÓ k e NÓ f (POLO POSITIVO), NÓ i e Nó g (POLO NEGATIVO)                                      ##")
	print("##################################################################################################################################################################################")
	print()
	print("########################")
	print("## Digite 0 para SAIR ##")
	print("########################")
	print()
	
	
	while (componente != '0'):
		componente = input()
		
		
		componente_descricao = componente.split()
		
		
		if (componente != '0'):
			lista_componentes.append (componente_descricao[0])
		
			indice += 1
			while ( (indice) <= (len(componente_descricao) - 1)):
				componente_descricao_inteiro = float(componente_descricao[indice])
				
				if (indice == 1):
					if (componente_descricao_inteiro > maior_valor_nó):
						maior_valor_nó = int(componente_descricao_inteiro)
				
				if (indice == 2):
					if (componente_descricao_inteiro > maior_valor_nó):
						maior_valor_nó = int(componente_descricao_inteiro)
							
				
			
				lista_componentes.append (componente_descricao_inteiro)
				indice += 1
			
			indice = 0
	
	
	
	yn = np.zeros((maior_valor_nó, maior_valor_nó))
	q = np.zeros((maior_valor_nó,1))
	
	while ((index) < (len(lista_componentes))):
		if (type(lista_componentes[index]) is float):
			index += 1
		elif (lista_componentes[index] == "SIN" or lista_componentes[index] == "sin"):
			w = lista_componentes[index + 1]   
	
	while ((index) < (len(lista_componentes))):
		if (type(lista_componentes[index]) is float):
			index += 1
		else:
			if (lista_componentes[index][0] == 'R' or lista_componentes[index][0] == 'r'): #resistência
				yn = montar_yn(lista_componentes,yn, index,corrente,w)
				
				
			if (lista_componentes[index][0] == 'I' or lista_componentes[index][0] == 'i'): #fonte de corrente independente 		
				q = montar_q(lista_componentes,q, index)
				
				
				
			if (lista_componentes[index][0] == 'G' or lista_componentes[index][0] == 'g'): #fonte de corrente controlada por tensão 
				yn = montar_yn(lista_componentes,yn, index,corrente,w)
				
			
			if (lista_componentes[index][0] == 'V' or lista_componentes[index][0] == 'v'): #fonte de tensão independente
				#adiciona linha e coluna em yn
				dimensao_yn = (yn.shape)
				b = np.zeros((dimensao_yn[0] + 1,dimensao_yn[1] + 1))
				b[:-1,:-1] = yn
				yn = b
				#adiciona linha em q
				dimensao_q = (q.shape)
				b = np.zeros((dimensao_yn[0] + 1,1))
				b[:-1,:] = q
				q = b
				yn = montar_yn(lista_componentes,yn, index,corrente,w)
				q = montar_q(lista_componentes,q, index)
				dimensoes_extras += 1
				
			if (lista_componentes[index][0] == 'B' or lista_componentes[index][0] == 'b'): #fonte de corrente controlada por corrente
				#adiciona linha e coluna em yn
				dimensao_yn = (yn.shape)
				b = np.zeros((dimensao_yn[0] + 1,dimensao_yn[1] + 1))
				b[:-1,:-1] = yn
				yn = b
				#adiciona linha em q
				dimensao_q = (q.shape)
				b = np.zeros((dimensao_yn[0] + 1,1))
				b[:-1,:] = q
				q = b
				yn = montar_yn(lista_componentes,yn, index, corrente,w)
				dimensoes_extras += 1
				
				
			if (lista_componentes[index][0] == 'A' or lista_componentes[index][0] == 'a'): #fonte de tensão controlada por tensão
				#adiciona linha e coluna em yn
				dimensao_yn = (yn.shape)
				b = np.zeros((dimensao_yn[0] + 1,dimensao_yn[1] + 1))
				b[:-1,:-1] = yn
				yn = b
				#adiciona linha em q
				dimensao_q = (q.shape)
				b = np.zeros((dimensao_yn[0] + 1,1))
				b[:-1,:] = q
				q = b
				yn = montar_yn(lista_componentes,yn, index, corrente,w)
				dimensoes_extras += 1
				
			if (lista_componentes[index][0] == 'H' or lista_componentes[index][0] == 'h'): #fonte de tensão controlada por corrente
				##jx
				#adiciona linha e coluna em yn
				dimensao_yn = (yn.shape)
				b = np.zeros((dimensao_yn[0] + 1,dimensao_yn[1] + 1))
				b[:-1,:-1] = yn
				yn = b	
				#adiciona linha em q
				dimensao_q = (q.shape)
				b = np.zeros((dimensao_yn[0] + 1,1))
				b[:-1,:] = q
				q = b
				corrente = "jx"
				yn = montar_yn(lista_componentes,yn, index, corrente,w)
				dimensoes_extras += 1
				
				##jy
				#adiciona linha e coluna em yn
				dimensao_yn = (yn.shape)
				b = np.zeros((dimensao_yn[0] + 1,dimensao_yn[1] + 1))
				b[:-1,:-1] = yn
				yn = b	
				#adiciona linha em q
				dimensao_q = (q.shape)
				b = np.zeros((dimensao_yn[0] + 1,1))
				b[:-1,:] = q
				q = b
				corrente = "jy"
				yn = montar_yn(lista_componentes,yn, index, corrente,w)
				dimensoes_extras += 1
				
			if (lista_componentes[index][0] == 'C' or lista_componentes[index][0] == 'c'): #capacitor		
				yn = montar_yn(lista_componentes,yn, index, corrente,w)
			
			if (lista_componentes[index][0] == 'X' or lista_componentes[index][0] == 'x'): #indutor		
				yn = montar_yn(lista_componentes,yn, index, corrente,w)
			
			if (lista_componentes[index][0] == 'K' or lista_componentes[index][0] == 'k'): #indutância mútua	
				yn = montar_yn(lista_componentes,yn, index, corrente,w)
				
				
			index += 1
			
	#print(yn)	
	#print(q)
	# yn*m = q
	# m = inv(yn)*q
	m = montar_m (yn,q)
			
	#print(yn)	
	#print(q)
	
	#print(m)
	resultado_final(m,maior_valor_nó,dimensoes_extras)
				
	
######## chamada ao menu
menu()
