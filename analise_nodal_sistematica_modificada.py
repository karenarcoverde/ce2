# Programa analise_nodal_sistematica_modificada.py
# Autora: Karen dos Anjos Arcoverde
# Data: 12/09/2020
#
# Descrição de um circuito por uma "netlist",
# obter tensões nodais de um circuito resistivo linear com fontes DC 
# pela análise sistemática nodal
# e
# Descrição de um circuito por uma "netlist",
# obter tensões nodais em regime permanente senoidal de um circuito linear 
# pela análise sistemática nodal
#
# o programa foi feito utilizando análise nodal modificada


#importando bibliotecas numpy e scipy para matrizes 
import numpy as np
from scipy import linalg
from numpy import *
import cmath
import math



##################################################################### Funcoes #####################################################################

def resultado_final (m,maior_valor_nó,dimensoes_extras,w):
	indice = 0
	t = 't'
	cosseno = 'cos'
	seno = 'sin'
	
	#se for regime permanente senoidal
	if (w != 0):
		for indice in range (maior_valor_nó):
			real = '{:.2f}'.format(m[indice][0].real)
			imaginaria = '{:.2f}'.format(-m[indice][0].imag)
		
			if (m[indice][0].real !=0 and m[indice][0].imag != 0):
				print("e"+ str(indice + 1),' = ' + real + cosseno + str(int(w)) + str(t) + " " + imaginaria + seno + str(int(w)) + str(t))
			elif (m[indice][0].real != 0 and m[indice][0].imag == 0):
				print("e"+ str(indice + 1),' = ' + real + cosseno + str(int(w)) + str(t))
			elif (m[indice][0].real == 0 and m[indice][0].imag!= 0):
				print("e"+ str(indice + 1),' = ' + imaginaria + seno + str(int(w)) + str(t))
			elif (m[indice][0].real == 0 and m[indice][0].imag == 0):
					print("e"+ str(indice + 1),' = ' + '0')
			
		indice = 0
		if (dimensoes_extras != 0):
			indice += maior_valor_nó
			for (indice) in range (indice,(dimensoes_extras + maior_valor_nó)):
				real = '{:.2f}'.format(m[indice][0].real)
				imaginaria = '{:.2f}'.format(-m[indice][0].imag)
				if (m[indice][0].real !=0 and m[indice][0].imag != 0):
					print("j"+ str(indice + 1),' = ' + real + cosseno + str(int(w)) + str(t) + " " + imaginaria + seno + str(int(w)) + str(t))
				elif (m[indice][0].real != 0 and m[indice][0].imag == 0):
					print("j"+ str(indice + 1),' = ' + real + cosseno + str(int(w)) + str(t))
				elif (m[indice][0].real == 0 and m[indice][0].imag != 0):
					print("j"+ str(indice + 1),' = ' + imaginaria + seno + str(int(w)) + str(t))	
				elif (m[indice][0].real == 0 and m[indice][0].imag == 0):
					print("j"+ str(indice + 1),' = ' + '0')
					
					
	#se for DC		
	if (w == 0):
		for indice in range (maior_valor_nó):
			real = '{:.2f}'.format(m[indice][0].real)
			imaginaria = '{:.2f}'.format(-m[indice][0].imag)
		
			if (m[indice][0].real != 0 or m[indice][0].real == 0 and m[indice][0].imag == 0):
				print("e"+ str(indice + 1),' = ' + real)
			
		indice = 0
		if (dimensoes_extras != 0):
			indice += maior_valor_nó
			for (indice) in range (indice,(dimensoes_extras + maior_valor_nó)):
				real = '{:.2f}'.format(m[indice][0].real)
				imaginaria = '{:.2f}'.format(-m[indice][0].imag)
				if (m[indice][0].real != 0 or m[indice][0].real == 0 and m[indice][0].imag == 0):
					print("j"+ str(indice + 1),' = ' + real)
				
			
		

	
def montar_q(lista_componentes,q,index):
	
	##I
	if (lista_componentes[index][0] == 'I' or lista_componentes[index][0] == 'i'):
		if (lista_componentes[index + 3] == 'DC' or lista_componentes[index + 3] == 'dc'):
			if (lista_componentes[index + 1] == 0):
				(q[int(lista_componentes[index + 2]) - 1][0]) += (lista_componentes[index + 4])	
		
	
			if (lista_componentes[index + 2] == 0):
				(q[int(lista_componentes[index + 1]) - 1][0]) += -(lista_componentes[index + 4])
		
			elif ((lista_componentes[index + 1] != 0) and (lista_componentes[index + 2] != 0)):
				(q[int(lista_componentes[index + 1]) - 1][0]) += -(lista_componentes[index + 4])
				(q[int(lista_componentes[index + 2]) - 1][0]) += (lista_componentes[index + 4])
			
		if (lista_componentes[index + 3] == 'SIN' or lista_componentes[index + 3] == 'sin'):	
			if (lista_componentes[index + 1] == 0):
				(q[int(lista_componentes[index + 2]) - 1][0]) += cmath.rect(lista_componentes[index + 5],lista_componentes[index + 9])
		
	
			if (lista_componentes[index + 2] == 0):
				(q[int(lista_componentes[index + 1]) - 1][0]) += -cmath.rect(lista_componentes[index + 5],lista_componentes[index + 9])
		
			elif ((lista_componentes[index + 1] != 0) and (lista_componentes[index + 2] != 0)):
				(q[int(lista_componentes[index + 1]) - 1][0]) += -cmath.rect(lista_componentes[index + 5],lista_componentes[index + 9])
				(q[int(lista_componentes[index + 2]) - 1][0]) += cmath.rect(lista_componentes[index + 5],lista_componentes[index + 9])
		
		
		
	##V
	if (lista_componentes[index][0] == 'V' or lista_componentes[index][0] == 'v'):
		if (lista_componentes[index + 3] == 'DC' or lista_componentes[index + 3] == 'dc'):
			(q[q.shape[0]-1][0]) += (lista_componentes[index + 4])
			
		if (lista_componentes[index + 3] == 'SIN' or lista_componentes[index + 3] == 'sin'):
			(q[q.shape[0]-1][0]) += cmath.rect(lista_componentes[index + 5],lista_componentes[index + 9])		
	return q
	
def montar_m (yn,q):
	inv_yn = np.linalg.inv(yn)
	m = np.dot(inv_yn, q)
	
	return m

def montar_yn(lista_componentes, yn, index, corrente,w,gama):

	
	
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
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 2]) - 1]) += 1j*w*(lista_componentes[index + 3])
			
		##X	
		if (lista_componentes[index][0] == 'X' or lista_componentes[index][0] == 'x'): 
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 2]) - 1]) += 1/(1j*w*(lista_componentes[index + 3]))
			
		##K
		if (lista_componentes[index][0] == 'K' or lista_componentes[index][0] == 'k'):
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 2]) - 1]) += (gama[0][0])/(1j*w)		
			if (lista_componentes[index + 4] != 0 and lista_componentes[index + 5] == 0):
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 5]) - 1]) += (gama[1][1])/(1j*w)
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 5]) - 1]) += (gama[0][1])/(1j*w)
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 2]) - 1]) += (gama[1][0])/(1j*w)
			if (lista_componentes[index + 4] == 0 and lista_componentes[index + 5] != 0):
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 4]) - 1]) += (gama[1][1])/(1j*w)
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 4]) - 1]) += -(gama[0][1])/(1j*w)
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 2]) - 1]) += -(gama[1][0])/(1j*w)
			if (lista_componentes[index + 4] != 0 and lista_componentes[index + 5] != 0):
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 5]) - 1]) += (gama[1][1])/(1j*w)
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 5]) - 1]) += (gama[0][1])/(1j*w)
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 2]) - 1]) += (gama[1][0])/(1j*w)
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 4]) - 1]) += (gama[1][1])/(1j*w)
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 4]) - 1]) += -(gama[0][1])/(1j*w)
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 2]) - 1]) += -(gama[1][0])/(1j*w)
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 4]) - 1]) += -(gama[1][1])/(1j*w)
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 5]) - 1]) += -(gama[1][1])/(1j*w)
				
			
	
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
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 1]) - 1]) += 1j*w*(lista_componentes[index + 3])
		
		##X	
		if (lista_componentes[index][0] == 'X' or lista_componentes[index][0] == 'x'):
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 1]) - 1]) += 1/(1j*w*(lista_componentes[index + 3]))
			
		##K
		if (lista_componentes[index][0] == 'K' or lista_componentes[index][0] == 'k'):
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 1]) - 1]) += (gama[0][0])/(1j*w)
			if (lista_componentes[index + 4] != 0 and lista_componentes[index + 5] == 0):
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 4]) - 1]) += (gama[1][1])/(1j*w)
				(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 4]) - 1]) += (gama[0][1])/(1j*w)
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 1]) - 1]) += (gama[1][0])/(1j*w)
			if (lista_componentes[index + 4] == 0 and lista_componentes[index + 5] != 0):
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 5]) - 1]) += (gama[1][1])/(1j*w)
				(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 5]) - 1]) += -(gama[0][1])/(1j*w)
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 1]) - 1]) += -(gama[1][0])/(1j*w)
			if (lista_componentes[index + 4] != 0 and lista_componentes[index + 5] != 0):
				(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 4]) - 1]) += (gama[0][1])/(1j*w)
				(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 5]) - 1]) += -(gama[0][1])/(1j*w)
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 1]) - 1]) += (gama[1][0])/(1j*w)
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 1]) - 1]) += -(gama[1][0])/(1j*w)
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 4]) - 1]) += (gama[1][1])/(1j*w)
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 5]) - 1]) += -(gama[1][1])/(1j*w)
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 4]) - 1]) += -(gama[1][1])/(1j*w)
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 5]) - 1]) += (gama[1][1])/(1j*w)
			
				
		
		

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
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 1]) - 1]) += 1j*w*(lista_componentes[index + 3])
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 2]) - 1]) += 1j*w*(lista_componentes[index + 3])
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 2]) - 1]) += -1j*w*(lista_componentes[index + 3])
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 1]) - 1]) += -1j*w*(lista_componentes[index + 3])
			
		##X	
		if (lista_componentes[index][0] == 'X' or lista_componentes[index][0] == 'x'): 
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 1]) - 1]) += 1/(1j*w*(lista_componentes[index + 3]))
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 2]) - 1]) += 1/(1j*w*(lista_componentes[index + 3]))
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 2]) - 1]) += -1/(1j*w*(lista_componentes[index + 3]))
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 1]) - 1]) += -1/(1j*w*(lista_componentes[index + 3]))
			
		##K
		if (lista_componentes[index][0] == 'K' or lista_componentes[index][0] == 'k'):
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 1]) - 1]) += (gama[0][0])/(1j*w)
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 2]) - 1]) += -(gama[0][0])/(1j*w)
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 1]) - 1]) += -(gama[0][0])/(1j*w)
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 2]) - 1]) += (gama[0][0])/(1j*w)		
			if (lista_componentes[index + 4] != 0 and lista_componentes[index + 5] == 0):
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 5]) - 1]) += (gama[1][1])/(1j*w)
				(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 5]) - 1]) += -(gama[0][1])/(1j*w)
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 5]) - 1]) += (gama[0][1])/(1j*w)
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 1]) - 1]) += -(gama[1][0])/(1j*w)
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 2]) - 1]) += (gama[1][0])/(1j*w)
			if (lista_componentes[index + 4] == 0 and lista_componentes[index + 5] != 0):
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 4]) - 1]) += (gama[1][1])/(1j*w)
				(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 4]) - 1]) += (gama[0][1])/(1j*w)
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 4]) - 1]) += -(gama[0][1])/(1j*w)
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 1]) - 1]) += (gama[1][0])/(1j*w)
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 2]) - 1]) += -(gama[1][0])/(1j*w)
			if (lista_componentes[index + 4] != 0 and lista_componentes[index + 5] != 0):
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 5]) - 1]) += (gama[1][1])/(1j*w)
				(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 5]) - 1]) += -(gama[0][1])/(1j*w)
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 5]) - 1]) += (gama[0][1])/(1j*w)
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 1]) - 1]) += -(gama[1][0])/(1j*w)
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 2]) - 1]) += (gama[1][0])/(1j*w)
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 4]) - 1]) += (gama[1][1])/(1j*w)
				(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 4]) - 1]) += (gama[0][1])/(1j*w)
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 4]) - 1]) += -(gama[0][1])/(1j*w)
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 1]) - 1]) += (gama[1][0])/(1j*w)
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 2]) - 1]) += -(gama[1][0])/(1j*w)
				(yn[int(lista_componentes[index + 5]) - 1][int(lista_componentes[index + 4]) - 1]) += -(gama[1][1])/(1j*w)
				(yn[int(lista_componentes[index + 4]) - 1][int(lista_componentes[index + 5]) - 1]) += -(gama[1][1])/(1j*w)							
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
	print("## PARA FONTE DE TENSÃO CONTROLADA POR CORRENTE: <H+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <Nó f> <Nó g> <valor do H>                                                              ##")
	print("## PARA INDUTOR: <X+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <indutância(L)>                                                                                                         ##")
	print("## PARA CAPACITOR: <C+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <indutância(C)>                                                                                                       ##")
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
			lista_componentes.append (float(componente_descricao[1]))
			lista_componentes.append (float(componente_descricao[2]))
			
			if (int(componente_descricao[1]) > maior_valor_nó):
				maior_valor_nó = int(componente_descricao[1])
				
			if (int(componente_descricao[2]) > maior_valor_nó):
				maior_valor_nó = int(componente_descricao[2])
			
			
			if (componente_descricao[3] == 'SIN' or componente_descricao[3] == 'sin' or componente_descricao[3] == 'DC' or componente_descricao[3] == 'dc'):
				lista_componentes.append (componente_descricao[3])	
				indice += 4
			else:
				indice += 3
				
			if (indice == 3):
				while ( (indice) <= (len(componente_descricao)-1)):
					componente_descricao_inteiro = float(componente_descricao[indice])				
					lista_componentes.append (componente_descricao_inteiro)
					indice += 1
			
			if (indice == 4):
				while ( (indice) <= (len(componente_descricao)-1)):
					componente_descricao_inteiro = float(componente_descricao[indice])
					lista_componentes.append (componente_descricao_inteiro)
					indice += 1
			
			indice = 0
	
	
	yn = np.zeros((maior_valor_nó, maior_valor_nó),dtype=complex)
	q = np.zeros((maior_valor_nó,1),dtype=complex)
	gama = np.zeros((2, 2),dtype=complex)
	matriz_L = np.zeros((2, 2),dtype=complex)
	
	
	while ((index) < (len(lista_componentes))):
		if (lista_componentes[index] == 'SIN' or lista_componentes[index] == 'sin'):
			w = lista_componentes[index + 3] 			
			index += 1
		else:
			index += 1
		
	
	index = 0
	while ((index) < (len(lista_componentes))):
		if (type(lista_componentes[index]) is float):
			index += 1
		else:
			if (lista_componentes[index][0] == 'R' or lista_componentes[index][0] == 'r'): #resistência
				yn = montar_yn(lista_componentes,yn, index,corrente,w,gama)
				
				
			if (lista_componentes[index][0] == 'I' or lista_componentes[index][0] == 'i'): #fonte de corrente independente 		
				q = montar_q(lista_componentes,q, index)
				
				
				
			if (lista_componentes[index][0] == 'G' or lista_componentes[index][0] == 'g'): #fonte de corrente controlada por tensão 
				yn = montar_yn(lista_componentes,yn, index,corrente,w,gama)
				
			
			if (lista_componentes[index][0] == 'V' or lista_componentes[index][0] == 'v'): #fonte de tensão independente
				#adiciona linha e coluna em yn
				dimensao_yn = (yn.shape)
				b = np.zeros((dimensao_yn[0] + 1,dimensao_yn[1] + 1),dtype=complex)
				b[:-1,:-1] = yn
				yn = b
				#adiciona linha em q
				dimensao_q = (q.shape)
				b = np.zeros((dimensao_yn[0] + 1,1),dtype=complex)
				b[:-1,:] = q
				q = b
				yn = montar_yn(lista_componentes,yn, index,corrente,w,gama)
				q = montar_q(lista_componentes,q, index)
				dimensoes_extras += 1
				
			if (lista_componentes[index][0] == 'B' or lista_componentes[index][0] == 'b'): #fonte de corrente controlada por corrente
				#adiciona linha e coluna em yn
				dimensao_yn = (yn.shape)
				b = np.zeros((dimensao_yn[0] + 1,dimensao_yn[1] + 1),dtype=complex)
				b[:-1,:-1] = yn
				yn = b
				#adiciona linha em q
				dimensao_q = (q.shape)
				b = np.zeros((dimensao_yn[0] + 1,1),dtype=complex)
				b[:-1,:] = q
				q = b
				yn = montar_yn(lista_componentes,yn, index, corrente,w,gama)
				dimensoes_extras += 1
				
				
			if (lista_componentes[index][0] == 'A' or lista_componentes[index][0] == 'a'): #fonte de tensão controlada por tensão
				#adiciona linha e coluna em yn
				dimensao_yn = (yn.shape)
				b = np.zeros((dimensao_yn[0] + 1,dimensao_yn[1] + 1),dtype=complex)
				b[:-1,:-1] = yn
				yn = b
				#adiciona linha em q
				dimensao_q = (q.shape)
				b = np.zeros((dimensao_yn[0] + 1,1),dtype=complex)
				b[:-1,:] = q
				q = b
				yn = montar_yn(lista_componentes,yn, index, corrente,w,gama)
				dimensoes_extras += 1
				
			if (lista_componentes[index][0] == 'H' or lista_componentes[index][0] == 'h'): #fonte de tensão controlada por corrente
				##jx
				#adiciona linha e coluna em yn
				dimensao_yn = (yn.shape)
				b = np.zeros((dimensao_yn[0] + 1,dimensao_yn[1] + 1),dtype=complex)
				b[:-1,:-1] = yn
				yn = b	
				#adiciona linha em q
				dimensao_q = (q.shape)
				b = np.zeros((dimensao_yn[0] + 1,1),dtype=complex)
				b[:-1,:] = q
				q = b
				corrente = "jx"
				yn = montar_yn(lista_componentes,yn, index, corrente,w,gama)
				dimensoes_extras += 1
				
				##jy
				#adiciona linha e coluna em yn
				dimensao_yn = (yn.shape)
				b = np.zeros((dimensao_yn[0] + 1,dimensao_yn[1] + 1),dtype=complex)
				b[:-1,:-1] = yn
				yn = b	
				#adiciona linha em q
				dimensao_q = (q.shape)
				b = np.zeros((dimensao_yn[0] + 1,1),dtype=complex)
				b[:-1,:] = q
				q = b
				corrente = "jy"
				yn = montar_yn(lista_componentes,yn, index, corrente,w,gama)
				dimensoes_extras += 1
				
			if (lista_componentes[index][0] == 'C' or lista_componentes[index][0] == 'c'): #capacitor		
				yn = montar_yn(lista_componentes,yn, index, corrente,w,gama)
			
			if (lista_componentes[index][0] == 'X' or lista_componentes[index][0] == 'x'): #indutor		
				yn = montar_yn(lista_componentes,yn, index, corrente,w,gama)
			
			if (lista_componentes[index][0] == 'K' or lista_componentes[index][0] == 'k'): #indutância mútua
				#criando matriz de indutâncias e autoindutâncias
				
				matriz_L[0][0] = (lista_componentes[index + 3])
				matriz_L[0][1] = (lista_componentes[index + 7])
				matriz_L[1][0] = (lista_componentes[index + 7])
				matriz_L[1][1] = (lista_componentes[index + 6])
				
				gama = np.linalg.inv(matriz_L)
				
				yn = montar_yn(lista_componentes,yn, index, corrente,w,gama)
							
			index += 1

	# yn*m = q
	# m = inv(yn)*q
	m = montar_m (yn,q)
	resultado_final(m,maior_valor_nó,dimensoes_extras,w)
				
######## chamada ao menu
menu()
