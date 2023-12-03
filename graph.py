from loguru import logger

"""
Graphs are a data structure with 2 key features, nodes and edges.

Graphs can implicit or explicit, can be finite or infinite, and can be cyclic or acyclic.

Lists and Trees are examples of types of Graphs.

We represent Graphs here with the class Graph. This class is intended be used to implement finite, explicit graphs,
which is what a Graph Database is.

As a template to explore, there are classes called Node and Edge which are referred to in Graph.
The classes don't have a whole lot going on in this implementation, but serve for the framework for how
design ideas for musical data and metadata can be filled out. For both Nodes and edges we can use classes
and inheritance to share as much code as possible between the different kinds of nodes we have, (doing them 
as classes lets us describe our expectations at the type level, which is a plus.

"""

###############################
## Node
###############################

class Node:
    def __init__(self, name):
        self.name = name

###############################
## Edge
###############################

## represents a directed edge going from Node start to node End
## 'meaning' is used to denote different kinds of edges
class Edge:
    def __init__(self, start, end, meaning : str="EXAMPLE", weight : float=1):
        self.start = start
        self.end = end
        self.meaning : str = meaning
        self.weight : float = weight




###############################
## Graph
###############################

class Graph:
    ## create a graph, with optional initial set of nodes and edges
    def __init__(self, nodes : list[Node] = [], edges : list[Edge] = []):

        ## We store nodes as a dictionary associating Node names to all the data for easy lookup
        self.nodes : dict[str : Node]= dict()

        ## We store edges as a dictionary of edges starting from a given node names to all edges with that start point
        ## for easy lookup
        self.edges : dict[str : list[Edge]] = dict()

        ## we store some other metadata about the graph
        self.num_nodes = 0
        self.num_edges = 0

        for n in nodes:
            self.add_node(n)
        for e in edges:
            self.add_edge(e)

    ## accessors to get all nodes
    def get_all_nodes(self) -> list[Node]:
        return self.nodes.values()
    
    ## accessors to get all edges
    def get_all_edges(self) -> list[Edge]:
        ans = []
        for v in self.edges.values():
            ans += v
        return ans
            
    ## Adding data to the Graph : Nodes
    def add_node(self, node : Node, allow_update=False):
        if (node.name in self.nodes.keys()) and (not allow_update):
            logger.warning(f"Ignoring node insert, update not enabled and Node already exists with name: {node.name}")
        else:
            self.nodes.update({node.name : node})
            self.num_nodes += 1
    
    ## Adding Edges to the Graoh : Edges
    def add_edge(self, edge : Edge):
        all_nodes = self.nodes.keys()
        if edge.start not in all_nodes:
            logger.warning(f"Unknown Start Node in {edge.meaning} Edge: {edge.start}, skipping")
        elif edge.end not in all_nodes:
            logger.warning(f"Unknown End Node in {edge.meaning} Edge: {edge.end}, skipping")
        else:
            curr : list = self.edges.get(edge.start, [])
            curr.append(edge)
            self.edges.update({edge.start : curr})
            self.num_edges += 1
        
    
    #################################
    ## What it's all been leading up to: GRAPH ALGORITHMS!!!

    ## There are many ways to write all of these algorithms. I tried to go with a straightforward
    ## but clean approach for them
    #################################

    # returns a list of node names showing a path from start to end, if one exists.
    # returns False if no path exists
    
    ## Note: Exiting gracefully when no path exists requires detecting when you're trapped in a cycle!
    ## Once you get it working with cycle detection, disable the detection and see what happens! 
    def path_exists(self, start, end):

        ## this is a list of all the searches that we are simultaneously trying out, 
        ## as long as we have new things to explore we pop off the front one, and then 
        ## any continued exploration from that option are appended to the back. 
        ## appending new options to the back is alled Breadth-First Search (BFS), and 
        ## appending them to the front is called Depth-First Search (DFS)
        ## in DFS we would call it a 'stack' instead of a 'queue'

        queue : list[list] = [[start]]
        while len(queue) > 0:
            ## pop off our current option
            curr = queue[0]
            queue = queue[1:]
            
            ## otherwise, we expand from the current spot in this path, and add all the options to the queue for
            ## search later
            edges = self.edges.get(curr[0], [])
            options = [e.end for e in edges]
            for n in options:
                ## if we are at end, we're good!
                if n == end:
                    ## reverse the list so it reads start -> end instead of end -> start, and return it
                    curr.reverse()
                    return curr
                
                ## Cycle Detection: only add the explorations of nodes that haven't been touched yet.
                if n not in curr:
                    path = curr.copy()
                    path = [n] + path
                    queue.append(path)
        ## if we get here, we have exhausted all paths without finding the end, and report failure to find a path
        return False
    
    ## returns a list of lists of nodes, breaking up all nodes in the graph
    ## into disjoint sections

    ## a somewhat low-effort version that just leverages path_exists, but it works
    def show_subgraphs(self) -> list[list]:
        ans : list[list] = []
        all_nodes = self.get_all_nodes()
        ## for each node n1, look for a group
        for n1 in all_nodes:
            found_group = False
            ## see if n1 points to or is pointed to by any node in any existing group
            for g in ans:
                for n2 in g:
                    if self.path_exists(n1.name, n2):
                        found_group = True
                        break
                    elif self.path_exists(n2, n1.name):
                        found_group = True
                        break
                if found_group:
                    g.append(n1.name)        
                    break
            # if no group had a node pointed to by or pointing to n1, create a new group with n1 as the only member
            if not found_group:
                ans.append([n1.name])
        return ans

"""
Our first sample graph, which looks like:

   0 ----> 1      4 ----> 5
   ^       |      ^
   |       |      |
   |       v      |
   3 <---- 2      6

It has a cycle, and has 2 disconnected components

"""

G1 = Graph(
    nodes=[Node(i) for i in range(7)],
    edges=[
        Edge(0, 1), Edge(1, 2), Edge(2, 3), Edge(3, 0),
        Edge(4, 5), Edge(6, 4)
    ]
)

assert G1.path_exists(0, 1)
assert G1.path_exists(0, 2)
assert G1.path_exists(0, 3)
assert G1.path_exists(1, 2)
assert G1.path_exists(1, 3)
assert G1.path_exists(1, 0)
assert G1.path_exists(2, 0)
assert G1.path_exists(3, 2)
assert G1.path_exists(6, 4)
assert G1.path_exists(4, 5)

assert not G1.path_exists(4, 6)
assert not G1.path_exists(5, 6)
assert not G1.path_exists(0, 6)
assert not G1.path_exists(0, 4)

## G1 with some names changed, some extra nodes added, and some edges removed
G2 = Graph(
    nodes=[Node(i) for i in range(10)],
    edges=[
        Edge(9, 1), Edge(1, 2), Edge(5, 9),
        Edge(4, 0), Edge(6, 4), 
        Edge(7, 3)
    ]
)

"""
Draw a picture of G2:

   9 ----> 1      4 ----> 0
   ^       |      ^
   |       |      |            7 ---> 3        8
   |       v      |
   5       2      6

"""

i_drew_it_and_im_not_lying = True
assert i_drew_it_and_im_not_lying
assert G2.path_exists(9, 1)
assert G2.path_exists(5, 1)
assert not G2.path_exists(2, 9)
assert not G2.path_exists(5, 4)
assert not G2.path_exists(9, 6)
assert G2.path_exists(4, 0)
assert G2.path_exists(7, 3)
assert not G2.path_exists(7, 8)


logger.success("Path Exists tests passed!")

################################
################################

def sort_subgroups(gs):
    for g in gs:
        g.sort()
    gs.sort(key=(lambda x : x[0]))

G1_groups = G1.show_subgraphs()
sort_subgroups(G1_groups)
assert G1_groups == [[0,1,2,3], [4,5,6]]

G2_groups = G2.show_subgraphs()
sort_subgroups(G2_groups)
assert G2_groups == [[0,4,6], [1,2,5,9], [3,7], [8]]

logger.success("Show Subgroups tests passed!")