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
import sympy as sp
from sympy import *




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

	
	##O
	if (lista_componentes[index][0] == 'O' or lista_componentes[index][0] == 'o'): #amplificador operacional real
		if (lista_componentes[index + 1] == 0 and lista_componentes[index + 2] != 0):
			(yn[int(lista_componentes[index + 2]) - 1][yn.shape[1]-1]) += -1
			
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += 1
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -1
			
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += 1
				
			if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -1
					
		if (lista_componentes[index + 1] != 0 and lista_componentes[index + 2] == 0):
			(yn[int(lista_componentes[index + 1]) - 1][yn.shape[1]-1]) += 1
			
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += 1
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -1
			
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += 1
				
			if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -1
					
		elif ((lista_componentes[index + 1] != 0) and (lista_componentes[index + 2] != 0)):
			(yn[int(lista_componentes[index + 1]) - 1][yn.shape[1]-1]) += 1
			(yn[int(lista_componentes[index + 2]) - 1][yn.shape[1]-1]) += -1
			
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += 1
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -1
			
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += 1
				
			if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -1
			
		elif ((lista_componentes[index + 1] == 0) and (lista_componentes[index + 2] == 0)):
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += 1
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -1
			
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 3]) - 1]) += 1
				
			if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
				(yn[yn.shape[0]-1][int(lista_componentes[index + 4]) - 1]) += -1			
		return yn
				

	
	
	if (lista_componentes[index + 1] == 0):#corrente entrando no nó
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
			(yn[int(lista_componentes[index + 2]) - 1][yn.shape[1]-1]) += -1		
			(yn[yn.shape[0]-1][int(lista_componentes[index + 2]) - 1]) += 1
			([yn.shape[0]-1][yn.shape[1]-1]) += 1j*w*(lista_componentes[index + 3])
			
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
			(yn[int(lista_componentes[index + 1]) - 1][yn.shape[1]-1]) += 1		
			(yn[yn.shape[0]-1][int(lista_componentes[index + 1]) - 1]) += -1
			([yn.shape[0]-1][yn.shape[1]-1]) += 1j*w*(lista_componentes[index + 3])
			
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
			(yn[int(lista_componentes[index + 1]) - 1][yn.shape[1]-1]) += 1
			(yn[int(lista_componentes[index + 2]) - 1][yn.shape[1]-1]) += -1		
			(yn[yn.shape[0]-1][int(lista_componentes[index + 1]) - 1]) += -1
			(yn[yn.shape[0]-1][int(lista_componentes[index + 2]) - 1]) += 1	
			(yn[yn.shape[0]-1][yn.shape[1]-1]) += 1j*w*(lista_componentes[index + 3])
			
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
	opcao_linear = ""
	print()
	print("##################################################################################################################################################################################################")
	print("## ---------------------------------------------------------------------------------- INSTRUÇÕES ---------------------------------------------------------------------------------------------- ##")
	print("## Digite:                                                                                                                                                                                      ##")       
	print("## PARA RESISTÊNCIA: <R+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <valor da resistência>                                                                                                              ##")
	print("## PARA FONTE DE CORRENTE INDEPENDENTE: <I+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <tipo de fonte (DC)> <valor da fonte de corrente>                                                                ##")
	print("## PARA FONTE DE TENSÃO INDEPENDENTE: <V+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <tipo de fonte (DC)> <valor da fonte de tensão>                                                                    ##")
	print("## PARA FONTE DE CORRENTE CONTROLADA POR TENSÃO: <G+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <Nó f> <Nó g> <valor do G>                                                                              ##")
	print("## PARA FONTE DE CORRENTE CONTROLADA POR CORRENTE: <B+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <Nó f> <Nó g> <valor do B>                                                                            ##")
	print("## PARA FONTE DE TENSÃO CONTROLADA POR TENSÃO: <A+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <Nó f> <Nó g> <valor do A>                                                                                ##")
	print("## PARA FONTE DE TENSÃO CONTROLADA POR CORRENTE: <H+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <Nó f> <Nó g> <valor do H>                                                                              ##")
	print("## PARA INDUTOR: <X+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <indutância(L)>                                                                                                                         ##")
	print("## PARA CAPACITOR: <C+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <indutância(C)>                                                                                                                       ##")
	print("## PARA INDUTÂNCIA MÚTUA: <K+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <indutância(L1)> <Nó f> <Nó g> <indutância(L2)> <indutância mútua(M)>                                                          ##")
	print("## PARA FONTE DE TENSÃO/CORRENTE SENOIDAL: <(V OU I)+ÍNDICE DO COMPONENTE> <Nó k> <Nó i> <tipo de fonte (SIN)> <nível contínuo> <amplitude> <frequência> <atraso> <atenuação> <ângulo> <ciclos> ##")
	print("## PARA AMPLIFICADOR OPERACIONAL REAL: <O+ÍNDICE DO COMPONENTE> <Nó de Saída 1> <Nó de Saída 2> <Nó de Entrada 1 POSITIVO> <Nó de Entrada 2 NEGATIVO>                                           ##")	
	print("##################################################################################################################################################################################################")
	print()
	print("##################################################################################################################################################################################")
	print("## IMPORTANTE: RESPEITAR A POLARIDADE DAS FONTES DE TENSÃO E CORRENTE. CONSIDERAR NÓ k e NÓ f (POLO POSITIVO), NÓ i e Nó g (POLO NEGATIVO)                                      ##")
	print("##################################################################################################################################################################################")
	print()
	print("##################################################################################################################################################################################")
	print("## IMPORTANTE: PARA VER O RESULTADO DA MATRIZ JACOBIANA DOS 3 CIRCUITOS ESCOLHIDOS DIGITE: nao linear                                                                           ##")
	print("##################################################################################################################################################################################")
	print()
	print("########################")
	print("## Digite 0 para SAIR ##")
	print("########################")
	print()
	
	
	opcao_linear = input()
	if (opcao_linear == "nao linear"):
	
		########### circuito 1
		e1 = sp.symbols("e1",real=True)
		e2 = sp.symbols("e2",real=True)
		a11 = Derivative(-1 +2*(e1-e2)**2 +3*(e2)**2,e1)
		a12 = Derivative(-1 +2*(e1-e2)**2 +3*(e2)**2,e2)
		a21 = Derivative(e2 -2*(e1-e2)**2 -3*(e2)**2,e1)
		a22 = Derivative(e2 -2*(e1-e2)**2 -3*(e2)**2,e2)
		
		jacobiano_circuito1 = [[a11.doit(),a12.doit()],[a21.doit(),a22.doit()]]
		print("Circuito 1:")
		print(jacobiano_circuito1)
		print()
		
		
		e1n = sp.symbols("e1n",real=True)
		e2n = sp.symbols("e2n",real=True)
		
		yn = np.zeros((2,2))
		I = np.zeros((2,1))
		
	
		
		
		##resistencia
		G1 = Derivative(2*(e1n-e2n)**2,e1n).doit()
		
		nova_resistencia = 1/G1 #resistencia
		I1 = 2*(e1n-e2n)**2 -G1*(e1n-e2n) #fonte de corrente
		
		##fonte de corrente controlada por tensao
		Gm2 = Derivative(3*(e2n)**2,e2n).doit() #fonte de corrente
		I2 = 3*(e2n)**2 -Gm2*(e2n) #fonte de corrente
		
		
		
		
		G1 = G1.subs(e1n,0.1)
		G1 = G1.subs(e2n,0.05)
		I1 = I1.subs(e1n,0.1)
		I1 = I1.subs(e2n,0.05)
		Gm2 = Gm2.subs(e1n,0.1)
		Gm2 = Gm2.subs(e2n,0.05)
		I2 = I2.subs(e1n,0.1)
		I2 = I2.subs(e2n,0.05)
		
		
	
		
		#construindo a matriz
		I[0,0] = I1 - I2 +1
		I[1,0] = -I1 +I2
		yn[0,0] = G1
		yn[1,1] = 1 +G1 -Gm2
		yn[0,1] = -G1 +Gm2
		yn[1,0] = -G1 
		
		
		inv_yn = np.linalg.inv(yn)
		e_n_mais_um = np.dot(inv_yn, I)
		
		p = 0
	
		e1n = e1n.subs(e1n,0.1)
		e2n = e2n.subs(e2n,0.05)
		
		
		while (p < 100):

			
			if (e_n_mais_um [0,0] == e1n and e_n_mais_um[1,0] == e2n):
				print ("e1 = ", e_n_mais_um[0,0])
				print ("e2 = ", e_n_mais_um[1,0])
				break
				
				
			
			else:
				e1n = sp.symbols("e1n",real=True)
				e2n = sp.symbols("e2n",real=True)
				##resistencia
				G1 = Derivative(2*(e1n-e2n)**2,e1n).doit()
		
				nova_resistencia = 1/G1 #resistencia
				I1 = 2*(e1n-e2n)**2 -G1*(e1n-e2n) #fonte de corrente
		
				##fonte de corrente controlada por tensao
				Gm2 = Derivative(3*(e2n)**2,e2n).doit() #fonte de corrente
				I2 = 3*(e2n)**2 -Gm2*(e2n) #fonte de corrente
				
				G1 = G1.subs(e1n, e_n_mais_um[0,0])
				G1 = G1.subs(e2n, e_n_mais_um[1,0])
				I1 = I1.subs(e1n, e_n_mais_um[0,0])
				I1 = I1.subs(e2n, e_n_mais_um[1,0])
				Gm2 = Gm2.subs(e1n, e_n_mais_um[0,0])
				Gm2 = Gm2.subs(e2n, e_n_mais_um[1,0])
				I2 = I2.subs(e1n, e_n_mais_um[0,0])
				I2 = I2.subs(e2n, e_n_mais_um[1,0])
				
				
				I[0,0] = I1 - I2 +1
				I[1,0] = -I1 +I2
				yn[0,0] = G1
				yn[1,1] = 1 +G1 -Gm2
				yn[0,1] = -G1 +Gm2
				yn[1,0] = -G1 
				
				e1n = e1n.subs(e1n, e_n_mais_um[0,0])
				e2n = e2n.subs(e2n, e_n_mais_um[1,0])
				
				
				
				inv_yn = np.linalg.inv(yn)
				e_n_mais_um = np.dot(inv_yn, I)
				
				if (p == 98):
					print ("e1 = ", e_n_mais_um[0,0])
					print ("e2 = ", e_n_mais_um[1,0])
				
				if (p == 99):
					print ("e1 = ", e_n_mais_um[0,0])
					print ("e2 = ", e_n_mais_um[1,0])
			
			
			p+=1
		
		print()
		
		########### circuito 2
		e1 = sp.symbols("e1",real=True)
		e2 = sp.symbols("e2",real=True)
		e3 = sp.symbols("e3",real=True)
		
		a11 = Derivative(2*e2*e1 +e1 -2,e1)
		a12 = Derivative(2*e2*e1 +e1 -2,e2)
		a13 = Derivative(2*e2*e1 +e1 -2,e3)
		a21 = Derivative(e3/2 +2 -2*e2*e1 +e2,e1)
		a22 = Derivative(e3/2 +2 -2*e2*e1 +e2,e2)
		a23 = Derivative(e3/2 +2 -2*e2*e1 +e2,e3)
		a31 = Derivative(e2-e3 -2,e1)
		a32 = Derivative(e2-e3 -2,e2)
		a33 = Derivative(e2-e3 -2,e3)
		
		
		jacobiano_circuito2 = [[a11.doit(),a12.doit(),a13.doit()],[a21.doit(),a22.doit(),a23.doit()],[a31.doit(),a32.doit(),a33.doit()]]
		print("Circuito 2:")
		print(jacobiano_circuito2)
		print()
		
		
	
		e1n = sp.symbols("e1n",real=True)
		e2n = sp.symbols("e2n",real=True)
		
		yn = np.zeros((4,4))
		I = np.zeros((4,1))
		
		##fonte de corrente controlada por duas tensoes
		Gm1 = Derivative(2*e2n*e1n,e2n).doit() #fonte de corrente controlada
		Gm2 = Derivative(2*e2n*e1n,e1n).doit() #fonte de corrente controlada
		I1 = 2*e2n*e1n -Gm1*e2n -Gm2*e1n #fonte de corrente 
		
		I1 = I1.subs(e1n,0)
		I1 = I1.subs(e2n,0)
		Gm1 = Gm1.subs(e1n,0)
		Gm1 = Gm1.subs(e2n,0)
		Gm2 = Gm2.subs(e1n,0)
		Gm2 = Gm2.subs(e2n,0)
		
		
		
		#construindo a matriz
		I[0,0] = -I1 +2
		I[1,0] = -2
		I[2,0] = I1
		I[3,0] = -2
		yn[0,0] = 1 +Gm1
		yn[0,1] = Gm2
		yn[0,2] = 0
		yn[0,3] = 0
		yn[1,0] = 0
		yn[1,1] = 1
		yn[1,2] = 0
		yn[1,3] = 1
		yn[2,0] = -Gm1
		yn[2,1] = -Gm2
		yn[2,2] = 1/2
		yn[2,3] = -1
		yn[3,0] = 0
		yn[3,1] = -1
		yn[3,2] = 1
		yn[3,3] = 0
		
	
		
		inv_yn = np.linalg.inv(yn)
		e_n_mais_um = np.dot(inv_yn, I)
		
		
		
		p = 0
	
		e1n = e1n.subs(e1n,0)
		e2n = e2n.subs(e2n,0)
		
	
		
		while (p < 50):

			
			if (e_n_mais_um [0,0] == e1n and e_n_mais_um[1,0] == e2n):
				print ("e1 = ", e_n_mais_um[0,0])
				print ("e2 = ", e_n_mais_um[1,0])
				print ("e3 = ", e_n_mais_um[2,0])
				break
				
				
			
			else:
				e1n = sp.symbols("e1n",real=True)
				e2n = sp.symbols("e2n",real=True)
				##fonte de corrente controlada por duas tensoes
				Gm1 = Derivative(2*e2n*e1n,e1n).doit() #fonte de corrente controlada
				Gm2 = Derivative(2*e2n*e1n,e2n).doit() #fonte de corrente controlada
				I1 = 2*e2n*e1n -Gm1*e1n -Gm2*e2n #fonte de corrente 
				
				I1 = I1.subs(e1n,e_n_mais_um[0,0])
				I1 = I1.subs(e2n,e_n_mais_um[1,0])
				Gm1 = Gm1.subs(e1n,e_n_mais_um[0,0])
				Gm1 = Gm1.subs(e2n,e_n_mais_um[1,0])
				Gm2 = Gm2.subs(e1n,e_n_mais_um[0,0])
				Gm2 = Gm2.subs(e2n,e_n_mais_um[1,0])
				
				#construindo a matriz
				I[0,0] = -I1 +2
				I[1,0] = -2
				I[2,0] = I1
				I[3,0] = -2
				yn[0,0] = 1
				yn[0,1] = 0
				yn[0,2] = 0
				yn[0,3] = 0
				yn[1,0] = Gm1
				yn[1,1] = 1 +Gm2
				yn[1,2] = 0
				yn[1,3] = 1
				yn[2,0] = -Gm1
				yn[2,1] = -Gm2
				yn[2,2] = 1/2
				yn[2,3] = -1
				yn[3,0] = 0
				yn[3,1] = -1
				yn[3,2] = 1
				yn[3,3] = 0 
				
				e1n = e1n.subs(e1n, e_n_mais_um[0,0])
				e2n = e2n.subs(e2n, e_n_mais_um[1,0])
				
				
				
				inv_yn = np.linalg.inv(yn)
				e_n_mais_um = np.dot(inv_yn, I)
				
				
				
				
				if(math.isnan(e_n_mais_um[0,0])):
					print("Solução divergente!")
					break
				
				else:
					if (p == 48):
						print ("e1 = ", e_n_mais_um[0,0])
						print ("e2 = ", e_n_mais_um[1,0])
						print ("e3 = ", e_n_mais_um[2,0])
				
					if (p == 49):
						print ("e1 = ", e_n_mais_um[0,0])
						print ("e2 = ", e_n_mais_um[1,0])
						print ("e3 = ", e_n_mais_um[2,0])
			
			
			
			p+=1
		
		print()
		
		
		########### circuito 3
		
		
		e2 = sp.symbols("e2",real=True)
		e3 = sp.symbols("e3",real=True)
		
		a11 = Derivative(5*e2**2 -7*e2*e3 +58*e2 +2*e3**2 -24*e3,e2)
		a12 = Derivative(5*e2**2 -7*e2*e3 +58*e2 +2*e3**2 -24*e3,e3)
		a21 = Derivative(-2*e2**2 +5*e2*e3 -48*e2 -3*e3**2 +54*e3 -200,e2)
		a22 = Derivative(-2*e2**2 +5*e2*e3 -48*e2 -3*e3**2 +54*e3 -200,e3)
		
		
		jacobiano_circuito3 = [[a11.doit(),a12.doit()],[a21.doit(),a22.doit()]]
		print("Circuito 3:")
		print(jacobiano_circuito3)
		
		print()
		
		Ixn = sp.symbols("Ixn",real=True)
		Iyn = sp.symbols("Iyn",real=True)
		
		yn = np.zeros((6,6))
		I = np.zeros((6,1))
		
		##fonte de corrente controlada por duas correntes
		B0 = Derivative((2*Ixn)/Iyn,Ixn).doit() #fonte de corrente controlada
		B1 = Derivative((2*Ixn)/Iyn,Iyn).doit() #fonte de corrente controlada
		I0 = (2*Ixn)/Iyn -B0*Ixn -B1*Iyn #fonte de corrente 
		
		
		I0 = I0.subs(Ixn,0.1)
		I0 = I0.subs(Iyn,0.05)
		B0 = B0.subs(Ixn,0.1)
		B0 = B0.subs(Iyn,0.05)
		B1 = B1.subs(Ixn,0.05)
		B1 = B1.subs(Iyn,0.05)
		
		
		
		#construindo a matriz
		I[0,0] = -I0
		I[1,0] = 0
		I[2,0] = 10
		I[3,0] = I0
		I[4,0] = 0
		I[5,0] = 0
		yn[0,0] = 1/2
		yn[0,1] = 0
		yn[0,2] = 0
		yn[0,3] = 0
		yn[0,4] = B0 +1
		yn[0,5] = B1
		yn[1,0] = 0
		yn[1,1] = 2
		yn[1,2] = -1
		yn[1,3] = 0
		yn[1,4] = -1
		yn[1,5] = 0
		yn[2,0] = 0
		yn[2,1] = -1
		yn[2,2] = 1
		yn[2,3] = 0
		yn[2,4] = 0
		yn[2,5] = 1
		yn[3,0] = 0
		yn[3,1] = 0
		yn[3,2] = 0
		yn[3,3] = 1/2
		yn[3,4] = -B0
		yn[3,5] = -B1-1
		yn[4,0] = -1
		yn[4,1] = 1
		yn[4,2] = 0
		yn[4,3] = 0
		yn[4,4] = 0
		yn[4,5] = 0
		yn[5,0] = 0
		yn[5,1] = 0
		yn[5,2] = -1
		yn[5,3] = 1
		yn[5,4] = 0
		yn[5,5] = 0
		
		
	
		
		inv_yn = np.linalg.inv(yn)
		e_n_mais_um = np.dot(inv_yn, I)
		
		
		
		p = 0
	
		Ixn = Ixn.subs(Ixn,0.1)
		Iyn = Iyn.subs(Iyn,0.05)
		
	
		
		while (p < 100):

			
			if (e_n_mais_um [4,0] == Ixn and e_n_mais_um[5,0] == Iyn):
				print ("e1 = ", e_n_mais_um[0,0])
				print ("e2 = ", e_n_mais_um[1,0])
				print ("e3 = ", e_n_mais_um[2,0])
				print ("e4 = ", e_n_mais_um[3,0])
				break
				
				
			
			else:
				Ixn = sp.symbols("Ixn",real=True)
				Iyn = sp.symbols("Iyn",real=True)
				##fonte de corrente controlada por duas correntes
				B0 = Derivative((2*Ixn)/Iyn,Ixn).doit() #fonte de corrente controlada
				B1 = Derivative((2*Ixn)/Iyn,Iyn).doit() #fonte de corrente controlada
				I0 = (2*Ixn)/Iyn -B0*Ixn -B1*Iyn #fonte de corrente 
				
				
				I0 = I0.subs(Ixn,e_n_mais_um[4,0])
				I0 = I0.subs(Iyn,e_n_mais_um[5,0])
				B0 = B0.subs(Ixn,e_n_mais_um[4,0])
				B0 = B0.subs(Iyn,e_n_mais_um[5,0])
				B1 = B1.subs(Ixn,e_n_mais_um[4,0])
				B1 = B1.subs(Iyn,e_n_mais_um[5,0])
				
				
				#construindo a matriz
				I[0,0] = -I0
				I[1,0] = 0
				I[2,0] = 10
				I[3,0] = I0
				I[4,0] = 0
				I[5,0] = 0
				yn[0,0] = 1/2
				yn[0,1] = 0
				yn[0,2] = 0
				yn[0,3] = 0
				yn[0,4] = B0 +1
				yn[0,5] = B1
				yn[1,0] = 0
				yn[1,1] = 2
				yn[1,2] = -1
				yn[1,3] = 0
				yn[1,4] = -1
				yn[1,5] = 0
				yn[2,0] = 0
				yn[2,1] = -1
				yn[2,2] = 1
				yn[2,3] = 0
				yn[2,4] = 0
				yn[2,5] = 1
				yn[3,0] = 0
				yn[3,1] = 0
				yn[3,2] = 0
				yn[3,3] = 1/2
				yn[3,4] = -B0
				yn[3,5] = -B1-1
				yn[4,0] = -1
				yn[4,1] = 1
				yn[4,2] = 0
				yn[4,3] = 0
				yn[4,4] = 0
				yn[4,5] = 0
				yn[5,0] = 0
				yn[5,1] = 0
				yn[5,2] = -1
				yn[5,3] = 1
				yn[5,4] = 0
				yn[5,5] = 0
				
				Ixn = Ixn.subs(Ixn, e_n_mais_um[4,0])
				Iyn = Iyn.subs(Iyn, e_n_mais_um[5,0])
				
				
				
				inv_yn = np.linalg.inv(yn)
				e_n_mais_um = np.dot(inv_yn, I)
				
				
				
				
				if(math.isnan(e_n_mais_um[0,0])):
					print("Solução divergente!")
					break
				
				else:
				
					if (p == 99):
						print ("e1 = ", e_n_mais_um[0,0])
						print ("e2 = ", e_n_mais_um[1,0])
						print ("e3 = ", e_n_mais_um[2,0])
						print ("e4 = ", e_n_mais_um[3,0])
			
			
			
			p+=1
		
		print()
		
		
		
		
		
		
	
	
	else:
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
				
				if (lista_componentes[index][0] == 'K' or lista_componentes[index][0] == 'k'): #indutância mútua
					#criando matriz de indutâncias e autoindutâncias
					
					matriz_L[0][0] = (lista_componentes[index + 3])
					matriz_L[0][1] = (lista_componentes[index + 7])
					matriz_L[1][0] = (lista_componentes[index + 7])
					matriz_L[1][1] = (lista_componentes[index + 6])
					
					gama = np.linalg.inv(matriz_L)
					
					yn = montar_yn(lista_componentes,yn, index, corrente,w,gama)
					
					
				if (lista_componentes[index][0] == 'O' or lista_componentes[index][0] == 'o'): #amplificador operacional real 	
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
					
				index += 1
	
	if(opcao_linear != "nao linear"):
		# yn*m = q
		# m = inv(yn)*q
		m = montar_m (yn,q)
		resultado_final(m,maior_valor_nó,dimensoes_extras,w)
				
######## chamada ao menu
menu()