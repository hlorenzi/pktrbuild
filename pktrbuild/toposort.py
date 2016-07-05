import sys
import pktrbuild


def topological_sort(dict, roots):
	sorted_list = []
	visited_nodes = set()
	
	for node in roots:
		
		if node not in dict:
			pktrbuild.error("unknown action '" + node + "'")
			
		if not visit_topological_sort(dict, node, visited_nodes, sorted_list):
			return None
			
	return sorted_list
	

def visit_topological_sort(dict, node, visited_nodes, sorted_list):
	if node not in visited_nodes:
		visited_nodes.add(node)
			
		for dep in dict[node].deps:
		
			if dep not in dict:
				pktrbuild.error("unknown dependency '" + dep + "' from action '" + node + "'")
				
			if not visit_topological_sort(dict, dep, visited_nodes, sorted_list):
				return False
			
		sorted_list.append(node)
		return True
		
	else:
		return node in sorted_list
	