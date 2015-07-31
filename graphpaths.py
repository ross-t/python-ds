import itertools, random, time
import numpy as np

from heapq import heappush, heappop, heapify

# Graph: Adjacency list is a hash table where each vertex is associated with an array of tuples. The tuples
# represent edges and are in the format of (to_vertex, weight).
class DisjointSet:
	def __init__(self):
		self.sets = set()

	def make_set(self, label):
		self.sets.add(frozenset([label]))

	def find_label(self, label):
		for s in self.sets:
			if label in s:
				return s
		return label

	def join(self, elem1, elem2):
		setA = self.find_label(elem1)
		setB = self.find_label(elem2)
		if setA != setB:
			self.sets.remove(setA)
			self.sets.remove(setB)
			self.sets.add(setA.union(setB))

class Graph:
	def __init__(self):
		self.graph = dict()

	def add_vertex(self, vertex_label):
		if vertex_label not in self.graph:
			self.graph[vertex_label] = list()

	def add_edge(self, from_vertex, to_vertex, weight=1):
		# Add the vertices if they're not already in the graph
		if to_vertex not in self.graph:
			self.add_vertex(to_vertex)
		if from_vertex not in self.graph:
			self.add_vertex(from_vertex)
		
		# If that edge already exists, update its weight
		edges = self.graph[from_vertex]
		for edge in edges:
			if edge[0] == to_vertex:
				edge = (to_vertex, weight)
				return

		# Otherwise, just add it to the list of edges
		self.graph[from_vertex].append((to_vertex, weight))

	def dfs(self, v, visited=None):
		if visited == None:
			visited = []
		visited.append(v)
		for child in self.graph[v]:
			if child[0] not in visited:
				self.dfs(child[0], visited)
		return visited

	def is_weakly_connected(self):
		if len(self.graph.keys()) == 0:
			return True

		reachable = self.dfs(random.choice(self.graph.keys()))
		return len(reachable) == len(self.graph.keys())

	def components(self):
		found_components = set()
		found_verts = set()
		all_verts = self.graph.keys()

		for vert in all_verts:
			component = self.dfs(vert)
			found_verts = found_verts.union(set(component))
			found_components.add(frozenset(component))
			if len(found_verts) == len(all_verts):
				return found_components
		return found_components

	def save_image(self, filename):
		entries = []
		edges = set()
		seen_verts = set()		
		for key in self.graph.keys():
			for edge in self.graph[key]:
				edges.add((key, edge[0], edge[1]))
				seen_verts.add(key)
		for edge in edges:
			entries.append('%s -> %s[label="%d",weight="%d"]' % (str(edge[0]), str(edge[1]), edge[2], edge[2]))

		with open(filename + ".dot", 'w') as outfile:
			outfile.write('digraph {')
			for entry in entries:
				outfile.write('\t%s;\n' % entry)

			for vert in self.graph.keys():
				if vert not in seen_verts:
					outfile.write('\t%s;\n' % vert)
			outfile.write('}')

	@staticmethod
	def random_simple_graph(vertex_start, vertex_end, num_edges, is_directed, is_connected, min_weight=1, max_weight=1):
		vertices = [x for x in range(vertex_start, vertex_end + 1)]
		possible_edges = [x for x in itertools.permutations(vertices, 2)] # This creates a list containing tuples with possible edges, excluding self loops
		generated_edges = []
		g = Graph()
		# Generate the requested number of edges
		for x in range(num_edges):
			new_edge = random.choice(possible_edges)
			possible_edges.remove(new_edge)
			generated_edges.append(new_edge)
			weight = min_weight if min_weight == max_weight else random.randint(min_weight, max_weight)
			g.add_edge(new_edge[0], new_edge[1], weight)
			
			if not is_directed and (new_edge[1], new_edge[0]) not in generated_edges:
				g.add_edge(new_edge[1], new_edge[0], weight)
				possible_edges.remove((new_edge[1], new_edge[0]))
				generated_edges.append((new_edge[1], new_edge[0]))

			generated_edges.append(new_edge)

		for vertex in vertices:
			if vertex not in g.graph.keys():
				g.add_vertex(vertex)

		if is_connected:
			components = g.components()
			if len(components) > 1:
				while len(components) != 0:
					curr = random.sample(components, 1)[0]
					components.remove(curr)
					if len(components) != 0:
						next_comp = random.sample(components, 1)[0]
						components.remove(next_comp)
						from_vert = random.sample(curr, 1)[0]
						to_vert = random.sample(next_comp, 1)[0]
						g.add_edge(from_vert, to_vert, min_weight)
						if not is_directed:
							g.add_edge(to_vert, from_vert, min_weight)
		return g


def from_file(filename):
	with open(filename) as infile:
		lines = infile.readlines()[1:] # skip the header; we're going to try to make this file a graph come hell or high water
		graph_type = lines[0].split()[1] # "directed" or "undirected"
		is_directed = False
		
		if graph_type.lower() == "directed":
			is_directed = True

		g = Graph()
		for vertex_label in lines[1].split()[1:]:
			g.add_vertex(vertex_label.strip())

		edge_definitions = lines[3:] # ignore the "edges" declaration that we know is there

		for edge_line in edge_definitions:
			edge_line = edge_line.split()
			from_vertex = edge_line[0].strip()
			to_vertex = edge_line[1].strip()
			weight = 1
			if len(edge_line) == 3:
				weight = int(edge_line[2].strip())

			g.add_edge(from_vertex, to_vertex, weight)

			if not is_directed:
				g.add_edge(to_vertex, from_vertex, weight)

		return g

class GraphAlgos:
	@staticmethod
	def floyd_warshall(g):
		num_verts = len(g.graph.keys())
		dist = np.full((num_verts, num_verts), 1 << 16, np.int32)
		npaths = np.full((num_verts, num_verts), -1, np.int32)

		for vert in g.graph:
			for edge in g.graph[vert]:
				dist[int(vert), int(edge[0])] = edge[1]
				npaths[int(vert), int(edge[0])] = int(edge[0])

		for k in range(num_verts):
			for i in range(num_verts):
				for j in range(num_verts):
					if dist[i][k] + dist[k][j] < dist[i][j]:
						dist[i][j] = dist[i][k] + dist[k][j]
						npaths[i][j] = npaths[i][k]
		return (dist, npaths)

	@staticmethod
	def floyd_warshall_path(g, u, v, next_matrix):
		print next_matrix
		path = []
		if next_matrix[u][v] == -1:
			print "next_matrix[%d][%d] = -1, returning" % (u, v)
			return path
		path = [u]
		while u != v:
			u = next_matrix[u][v]
			print "\tnext_matrix[%d][%d] = append %d" % (u, v, u)
			path.append(u)
		return path

	@staticmethod
	def kruskals(g):
		DS = DisjointSet()

		forest = Graph()
		edges = set()
		
		for vert in g.graph.keys():
			forest.add_vertex(vert)
			DS.make_set(vert)
			for edge in g.graph[vert]:
				edges.add((vert, edge[0], edge[1]))

		to_heap = [(edge[2], edge[0], edge[1]) for edge in edges]
		pq = []
		for item in to_heap:
			heappush(pq, item)

		while pq:
			edge = heappop(pq)
			if DS.find_label(edge[1]) != DS.find_label(edge[2]):
				DS.join(edge[1], edge[2])
				forest.add_edge(edge[1], edge[2], edge[0])				

		return forest

def write_kruskals(original, min_span, filename):
	entries = []
	edges = set()
	min_edges = set()
	for key in original.graph.keys():
		for edge in original.graph[key]:
			edges.add((key, edge[0], edge[1]))

	for key in min_span.graph.keys():
		for edge in min_span.graph[key]:
			min_edges.add((key, edge[0], edge[1]))

	for edge in edges:
		if edge in min_edges:
			entries.append('%s -- %s[color=red,penwidth=3.0,label="%d",weight="%d"]' % (str(edge[0]), str(edge[1]), edge[2], edge[2]))
		else:
			entries.append('%s -- %s[style="dashed",label="%d",weight="%d"]' % (str(edge[0]), str(edge[1]), edge[2], edge[2]))

	with open(filename + '.dot', 'w') as outfile:
		outfile.write('graph {')
		for entry in entries:
			outfile.write('\t%s;\n' % entry)
		outfile.write('}')

if __name__ == '__main__':
	g = Graph.random_simple_graph(0, 9, 6, True, True, 1, 15)
	g2 = Graph.random_simple_graph(0, 10, 8, True, True, 1, 6)

	res = GraphAlgos.floyd_warshall(g)[0]
	res2 = GraphAlgos.floyd_warshall(g2)[0]

	g.save_image('fw_1')
	g2.save_image('fw_2')

	print 'FW 1 distance matrix'
	print res
	print 'FW 2 distance matrix'
	print res2
	# Also try these:
	#write_kruskals(g, res, 'kruskals_result_3')
	#g.save_image('floydtest_span')
	#print_results(10, 200, 10)
	#print_results(200, 500, 100)
	#print_results(500,5000, 500)