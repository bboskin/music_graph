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
## Nodes
###############################

class Node:
    def __init__(self, name):
        self.name = name

###############################
## Edge
###############################

## represents a directed edge going from Node start to Node end
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

        ## We store nodes as a dictionary associating Node names to all the data, for easy lookup
        self.nodes : dict[str : Node]= dict()

        ## We store edges as a dictionary of edges starting from a given node names to all edges with that start point
        ## also for easy lookup. 
        # (This is called a 'bucket' dictionary, 
        #  when the values are lists (buckets) to allow multiple values associated to a given key)
        self.edges : dict[str : list[Edge]] = dict()

        ## we can store some metadata about the graph
        self.num_nodes = 0
        self.num_edges = 0

        for n in nodes:
            self.add_node(n)
        for e in edges:
            self.add_edge(e)

    ## accessor to get all nodes
    def get_all_nodes(self) -> list[Node]:
        return self.nodes.values()
    
    ## accessor to get all edges
    def get_all_edges(self) -> list[Edge]:
        ans = []
        for v in self.edges.values():
            ans += v
        return ans
            
    ## Adding Nodes to the Graph
    def add_node(self, node : Node, allow_update=False):
        if (node.name in self.nodes.keys()) and (not allow_update):
            logger.warning(f"Ignoring node insert, update not enabled and Node already exists with name: {node.name}")
        else:
            self.nodes.update({node.name : node})
            self.num_nodes += 1
    
    ## Adding Edges to the Graph
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

    ## TODO 1
    # returns a list of node names showing a path from start to end, if one exists.
    # returns False if no path exists
    
    ## Note: Exiting gracefully when no path exists requires detecting when you're trapped in a cycle!
    ## Once you get it working with the cycle detection, disable the detection and see what happens! 
    def path_exists(self, start, end):
        pass
    
    ## TODO 2
    ## returns a list of lists of nodes, breaking up all nodes in the graph
    ## into disjoint sections
    def show_subgraphs(self) -> list[list]:
        pass

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

# TODO 3
"""
Draw a picture of G2:






"""

i_drew_it_and_im_not_lying = False
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
## disconnected subsections tests
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