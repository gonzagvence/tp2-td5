import json
import networkx as nx
import matplotlib.pyplot as plt

def main():
	filename = "instances/toy_instance.json"
	#filename = "instances/retiro-tigre-semana.json"

	with open(filename) as json_file: # Cargo data
		data = json.load(json_file)

	def crear_tupla(diccionario): # Creo tuplas a partir de cada evento, para crear nodos (tipo inmutable)
		return (diccionario['time'], diccionario['station'], diccionario['type'])
	
	def create_loop(lista): # Creo Loops en nodos del mismo lugar para agregar a las aristas
		return [[lista[i], lista[(i + 1) % len(lista)]] for i in range(len(lista))]
	retiro = [] # Guardo Nodos retiro
	tigre = [] # Guardo Nodos tigre
	nodos = [] # Guardo todos los nodos
	aristas_viaje = [] # Guardo aristas D -> A
	for service in data["services"]:
		temp = []
		for place in data["services"][service]["stops"]:
			temp.append(crear_tupla(place))
			nodos.append(crear_tupla(place))
			if place['station'] == 'Retiro':
				retiro.append(crear_tupla(place))
			else:
				tigre.append(crear_tupla(place))
		aristas_viaje.append(temp)
		#G.add_edge(temp[0],temp[1],service)
	def positions(retiro, tigre):
		vr = {}
		for i, k, p in zip(retiro, tigre, range(1,len(retiro)+1)):
			vr[i] = (0, p)
			vr[k] = (1, p)
		return vr		
	def ordenar_tuplas_por_numero(lista):
		return sorted(lista, key=lambda x: x[0]) # Ordeno listas de nodos, para que sea creaciente en Numero
	retiro = ordenar_tuplas_por_numero(retiro)  # Ordeno nodos 
	tigre = ordenar_tuplas_por_numero(tigre)  # Ordeno nodos
	pos = positions(retiro, tigre)
	G = nx.DiGraph()
	G.add_nodes_from(nodos)  #Agrego nodos 
	G.add_edges_from(create_loop(tigre)) # Creo aristas de tipo 'ciclo'
	G.add_edges_from(create_loop(retiro)) # Creo aristas de tipo 'ciclo'
	G.add_edges_from(aristas_viaje) # Creo aristas de D -> A
	nx.draw(G, with_labels=True, font_weight='bold', pos=pos)
	plt.show() # para mostrar el dibujo



if __name__ == "__main__":
	main()