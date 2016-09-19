from collections import deque

words=[]

for line in open('u1.txt'):
	words.extend(line.split())

#print (words)

algo=words[0]
start=words[1]
goal=words[2]
live_lines=int(words[3])
ll=live_lines*3
sl=ll+4
sunday_lines=int(words[sl])
#sl=int(sunday_lines)
graph1={}
graph2={}
sun={}
for i in range(sl+1,sl+1+sunday_lines*2,2):
    sun[words[i]]=int(words[i+1])

#print sun

def distBetween(graph, current,neighbor):
    list1=graph[current]
    if neighbor in list1:
        return int(list1[neighbor])
    else:
        return 999999

def heuristicEstimate(start,goal):
    return int(sun[start])

def neighborNodes(graph,current):
    if current in graph:
        list1=graph[current]
        return list1.keys()
    else:
        return None
    
def reconstructPath(cameFrom,goal):
    path = deque()
    node = goal
    path.appendleft(node)
    while node in cameFrom:
        node = cameFrom[node]
        path.appendleft(node)
    return path
    
def getLowest(openSet,fScore):
    lowest = float("inf")
    lowestNode = None
    for node in openSet:
        if fScore[node] < lowest:
            lowest = fScore[node]
            lowestNode = node
    return lowestNode

def aStar(graph, start,goal):
    cameFrom = {}
    openSet = set([start])
    closedSet = set()
    gScore = {}
    fScore = {}
    gScore[start] = 0
    fScore[start] = gScore[start] + heuristicEstimate(start,goal)
    while len(openSet) != 0:
        current = getLowest(openSet,fScore)
        if current == goal:
            return reconstructPath(cameFrom,goal)
        openSet.remove(current)
        closedSet.add(current)
        if neighborNodes(graph,current) is not None:
            for neighbor in neighborNodes(graph,current):
                tentative_gScore = gScore[current] + distBetween(graph,current,neighbor)
                if neighbor in closedSet and tentative_gScore >= gScore[neighbor]:
                    continue
                if neighbor not in closedSet or tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = gScore[neighbor] + heuristicEstimate(neighbor,goal)
                    if neighbor not in openSet:
                        openSet.add(neighbor)
        elif neighborNodes(graph,current) is None:
            pass
    return 0
    
def fill_graph():
	for v in range(4,ll+4,3):
		if words[v] not in graph1:
			graph1[words[v]]=[words[v+1],words[v+2]]
		elif words[v] in graph1:
			graph1[words[v]] = graph1.get(words[v], ()) + [words[v+1],words[v+2]]
#	print (graph1)


def readGraph():
    graph = {}
    for x in graph1:
        line = ''.join(x)
        for y in graph1[x]:
            line=line+" "
            y=''.join(y)
            line=line+y
            tokens = line.split()
            node = tokens[0]
            graph[node] = {}
        
            for i in range(1, len(tokens) - 1, 2):
                # print(node, tokens[i], tokens[i + 1])
                # graph.addEdge(node, tokens[i], int(tokens[i + 1]))
                graph[node][tokens[i]] = int(tokens[i + 1])
    #graph[goal]={}
    #graph[goal][goal]=0
    return graph


def main():
    fill_graph()
    graph = readGraph()
    path = aStar(graph, start, goal)
    path = list(path)
    #outfile=open('ou1.txt','w')
    #print path
    cost=0
    print(path[0]+' '+str(cost))
    for i in range(1,len(path)):
        cost=cost+int(graph[path[i-1]][path[i]])
        #print('\n')
        print(path[i]+' '+str(cost))

if __name__ == "__main__":
    main()