# Programa analise_nodal_modificada.py
# Autora: Karen dos Anjos Arcoverde
# Data: 12/09/2020
#
# Descrição de um circuito por uma "netlist",
# obtem tensões nodais de um circuito resistivo linear com fontes DC 
# pela análise sistemática nodal
#


import numpy as np


#def resultado_final (m):
	

def montar_q(lista_componentes,q,index):
	
	print(lista_componentes[index + 2])
	print(lista_componentes[index + 1])
	
	if (lista_componentes[index + 1] == 0):
		(q[int(lista_componentes[index + 2]) - 1][0]) += (lista_componentes[index + 3])	
		
	
	if (lista_componentes[index + 2] == 0):
		(q[int(lista_componentes[index + 1]) - 1][0]) += -(lista_componentes[index + 3])
		
		

	elif ((lista_componentes[index + 1] != 0) and (lista_componentes[index + 2] != 0)):
		(q[int(lista_componentes[index + 1]) - 1][0]) += -(lista_componentes[index + 3])
		(q[int(lista_componentes[index + 2]) - 1][0]) += (lista_componentes[index + 3])
		
		
	return q
	
	
	



#def montar_m (yn,q):
	#inv_yn = np.linalg.inv(yn)
	#m = np.multiply(inv_yn, q)


def montar_yn(lista_componentes, yn, index):

	
	
	if (lista_componentes[index + 1] == 0): #corrente entrando no nó
		##R
		if (lista_componentes[index][0] == 'R'):
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 2]) - 1]) += (1/(lista_componentes[index + 3])) 
		##G
		if (lista_componentes[index][0] == 'G'):
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 3]) - 1]) += -(lista_componentes[index + 5])
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 4]) - 1]) += (lista_componentes[index + 5])
			
			if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 4]) - 1]) += (lista_componentes[index + 5])	
		
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 3]) - 1]) += -(lista_componentes[index + 5])
		##V
		if (lista_componentes[index][0] == 'V'):
			(yn[yn.shape[0]-1][int(lista_componentes[index + 2]) - 1]) += -1
			
			
	
	if (lista_componentes[index + 2] == 0): #corrente saindo do nó
		## R
		if (lista_componentes[index][0] == 'R'):
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 1]) - 1]) += (1/(lista_componentes[index + 3])) 
		## G
		if (lista_componentes[index][0] == 'G'):
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] != 0):
				(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 3]) - 1]) += (lista_componentes[index + 5])
				(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 4]) - 1]) += -(lista_componentes[index + 5])
			
			if (lista_componentes[index + 3] == 0 and lista_componentes[index + 4] != 0):
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 4]) - 1]) += -(lista_componentes[index + 5])	
		
			if (lista_componentes[index + 3] != 0 and lista_componentes[index + 4] == 0):
				(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 3]) - 1]) += (lista_componentes[index + 5])
		##V
		if (lista_componentes[index][0] == 'V'):
			(yn[yn.shape[0]-1][int(lista_componentes[index + 1]) - 1]) += 1
			
		
		
		

	elif ((lista_componentes[index + 1] != 0) and (lista_componentes[index + 2] != 0)):
		##R
		if (lista_componentes[index][0] == 'R'):
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 1]) - 1]) += (1/(lista_componentes[index + 3]))
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 2]) - 1]) += (1/(lista_componentes[index + 3]))
			(yn[int(lista_componentes[index + 1]) - 1][int(lista_componentes[index + 2]) - 1]) += -(1/(lista_componentes[index + 3]))
			(yn[int(lista_componentes[index + 2]) - 1][int(lista_componentes[index + 1]) - 1]) += -(1/(lista_componentes[index + 3]))
		##G
		if (lista_componentes[index][0] == 'G'):		
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
		if (lista_componentes[index][0] == 'V'):
			(yn[yn.shape[0]-1][int(lista_componentes[index + 1]) - 1]) += 1
			(yn[yn.shape[0]-1][int(lista_componentes[index + 2]) - 1]) += -1
			
		
	return yn













##################### Programa Principal #####################
def menu():
	componente = ""
	indice = 0
	index = 0
	maior_valor_nó = 0
	lista_componentes = []
	
	
	print("INSTRUÇÕES")
	print("Digite:")      
	print("PARA RESISTÊNCIA: R+ÍNDICE DO COMPONENTE     Nó k     Nó i    valor da resistência")
	print("PARA FONTE DE CORRENTE INDEPENDENTE: I+ÍNDICE DO COMPONENTE     Nó k     Nó i    valor da fonte de corrente")
	print("PARA FONTE DE TENSÃO INDEPENDENTE: V+ÍNDICE DO COMPONENTE     Nó k     Nó i    valor da fonte de tensão")
	print("PARA FONTE DE TENSÃO INDEPENDENTE: V+ÍNDICE DO COMPONENTE     Nó k     Nó i    valor da fonte de tensão")
	print("PARA FONTE DE CORRENTE CONTROLADA POR TENSÃO: G+ÍNDICE DO COMPONENTE     Nó k     Nó i         Nó f  Nó g      valor do G")
	print("PARA FONTE DE CORRENTE CONTROLADA POR CORRENTE: B+ÍNDICE DO COMPONENTE     Nó k              Nó i  Nó f  Nó g     valor do B")
	print("PARA FONTE DE TENSÃO CONTROLADA POR TENSÃO: A+ÍNDICE DO COMPONENTE     Nó k     Nó i         Nó f  Nó g       valor do A")
	print("PARA FONTE DE TENSÃO CONTROLADA POR CORRENTE: H+ÍNDICE DO COMPONENTE     Nó k     Nó i         Nó f  Nó g       valor do H")
	print()
	print("IMPORTANTE: RESPEITAR A POLARIDADE DAS FONTES DE TENSÃO E CORRENTE. CONSIDERAR NÓ k e NÓ f (POLO POSITIVO), NÓ i e Nó g (POLO NEGATIVO)") 
	print("Digite 0 para SAIR")
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
	print(q)
	
	
	
	while ((index) < (len(lista_componentes))):
		if (type(lista_componentes[index]) is float):
			index += 1
		else:
			if (lista_componentes[index][0] == 'R'): #resistência
				yn = montar_yn(lista_componentes,yn, index)
				
			if (lista_componentes[index][0] == 'I'): #fonte de corrente independente 
				q = montar_q(lista_componentes,q, index)
				
			if (lista_componentes[index][0] == 'G'): #fonte de corrente controlada por tensão 
				yn = montar_yn(lista_componentes,yn, index)
			
			if (lista_componentes[index][0] == 'V'): #fonte de tensão independente
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
				yn = montar_yn(lista_componentes,yn, index)
				
				
				
			index += 1
			
	#print(yn)	
	#print(q)
	# yn*m = q
	# m = inv(yn)*q
	#montar_m (yn,q)
			
	print(yn)	
	#print(q)
	
	#print(m)
	
	#resultado_final(m)
				
		
	
	







######## chamada ao menu
menu()