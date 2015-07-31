graph = {'a':'bc', 'b':'de', 'e':'h', 'c':'fg'}

def seen_all(visited, graph):
	return len(set(graph) ^ set(visited)) == 0

def dfs(g, v, visited=None):
	if visited == None:
		visited = []
	visited.append(v)
	if v in g:
		for child in g[v]:
			if child not in visited:
				dfs(g, child, visited)
	return visited

def bfs(g, v):
	discovered = [v]
	queue = [v]
	while queue:
		v = queue.pop()
		if v in graph:
			for neighbor in graph[v]:
				print neighbor
				queue.append(neighbor)
				discovered.append(neighbor)
	return discovered

def components(g):
	found_components = set()
	found_verts = set()
	for vertex in g:
		if vertex not in found_verts:
			component = dfs(g,vertex)
			found_verts = found_verts.union(set(dfs(g, vertex)))
			found_components.add(frozenset(component))
	return found_components

if __name__ == '__main__':
	g = {'a':'bc', 'b':'a', 'c':'a', 'd':'ef', 'e': 'df', 'f':'de','g':'hi', 'h':'gi', 'i': 'gh'}
	print components(g)