from pymongo import MongoClient
from collections import defaultdict
class Graph:
	def __init__(self):
		self.nodes = set()
		self.edges = defaultdict(list)
		self.distances = {}
	def add_node(self, value):
		self.nodes.add(value)
	def add_edge(self, from_node, to_node, distance):
		self.edges[from_node].append(to_node)
		self.distances[(from_node, to_node)] = distance

def dijkstra(graph, initial):
	visited = {initial: 0}
	path = defaultdict(list)
	nodes = set(graph.nodes)
	while nodes: 
		min_node = None
		for node in nodes:
			if node in visited:
				if min_node is None:
					min_node = node
				elif visited[node] < visited[min_node]:
					min_node = node
		if min_node is None:
			break
		nodes.remove(min_node)
		current_weight = visited[min_node]
		for edge in graph.edges[min_node]:
			weight = current_weight + graph.distances[(min_node, edge)]
			if edge not in visited or weight < visited[edge]:
				visited[edge] = weight
				path[edge].append(min_node)
	return [path,visited]

def getShortestPath(startNode,endNode):
	returnValue = dijkstra(g, startNode)
	shortest_path = returnValue[0]
	visited = returnValue[1]
	fullpath = [endNode]
	destReached = False
	i = 0
	while(not destReached):
		nextNode = shortest_path[fullpath[i]][0] 
		i += 1
		fullpath.append(nextNode)
		if(nextNode == startNode):
			destReached = True
	return [fullpath, visited]

def idToName(id):
	nodes = ss.find({'solarSystemID': int(id)},{'solarSystemID':1,'solarSystemName':1})
	for i in nodes:
		name = i['solarSystemName']
	return name

# Main code
client = MongoClient()
db = client.solarSystems
ssjumps  = db.ssjumps
ss = db.ss

g = Graph()

nodes = ss.find({},{'solarSystemID':1,'solarSystemName':1})
for node in nodes:
	g.add_node(str(node['solarSystemID']))
	#print(str(node['solarSystemName']))

for edge in ssjumps.find({},{'fromSolarSystemID':1,'toSolarSystemID':1}):
	g.add_edge(str(edge['fromSolarSystemID']), str(edge['toSolarSystemID']),1)


startNode = '30000142'
endNode = '30004623'
shortestPath = getShortestPath(startNode,endNode)[0]
jumpNumber = 0
nodes = ss.find({},{'solarSystemID':1,'solarSystemName':1})
for jump in shortestPath:
	print(idToName(jump))
	print(jump)
	print(jumpNumber)
	jumpNumber += 1

#nodes = ss.find({},{'solarSystemID':1,'solarSystemName':1})
#print(nodes)
#for x in nodes:
#	print(str(x['solarSystemName']))



# for n in g.nodes:
# 	if(n != startNode):
# 		returnValue = getShortestPath(startNode,n)
# 		print(returnValue[0])
# 		print(returnValue[1])