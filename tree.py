from loguru import logger

"""
A Tree is a data structure similar to a List, but where each node an point to multiple children instead of just 1,
and where there are no cycles,
A Tree, more precisely, is a Directed Acyclic Graph (DAG), and is a great stepping stone to working 
with full Graphs. A graph can have cycles, non-directed edges, and as many children for a given node as desired.
One step at a time...

In this file we implement Binary Trees, which are trees where every non-terminal node has 2 children.
"""

"""
A Tree is either a Leaf or a Branch.

A Leaf may or may not have a value. A Leaf with no value is a Bud.

A Branch has three subcomponents:
 - a value
 - a 'left' element, which is a Tree
 - a 'right' element, which is a Tree

We also visualize trees as values and pointers. The data structure

  Branch(2, 
       Branch(0, Leaf(-1), Leaf(1)),
       Branch(3, Leaf(2),  Branch(5, Leaf(4), Leaf.Bud())))    
  
  looks like
                        2
                    /      \
                   0        3
                  / \      /  \ 
                -1   1    2    5
                              /
                             4

  and I choose ot print it dumbly on one line like:

    [-1 <- 0 -> 1] <- 2 -> [ 2 <- 3 -> [4 <- 5 -> .]] 

Examples of some terms:
- the root value is 2
- the number of elements is 9
- the height is 4.

It also has the property that is a Binary Search Tree (BST),
because for every branch b in the tree:
      all values in b.left <= b.value, and 
      all values in b.right >= b.value

The BST property is classic. We care about keeping data structures organized when possible to make things efficient!
When we ask a 1,000,000 entry data structure if 1 thing exists, it's a lot better if we know exactly/roughly where it 
would be if it did exist. BST helps us narrow down our search.

We will give Trees the full treatment, and define a wrapper class
to assign collective behavior for all entities with this structure. We write methods for
Nodes and Leaves as helpers, and for user features we implement wrappers in the Tree class.
(and if this was a real package we would then only expose the Tree class)

"""


## Leaf class: terminal data points in the tree
class Leaf:
    def __init__(self, val=None, has_val=True):
        self.value = val
        self.has_value = has_val

    def __str__(self):
        if self.has_value:
            return f"{self.value}"
        else:
            return "."
        
    ## return the number of elements in the Leaf (either 0 or 1)
    def size(self) -> int:
        if self.has_value:
            return 1
        else:
            return 0

    ## same as size, implemented here for convenience in 
    ## Branch method (see height in Branch class)
    def height(self) -> int:
        return self.size()    
        
    # tells is the Leaf satisfies BST given its context
    def is_bst(self, min, max) -> bool:
        if not self.has_value:
            return True
        elif ((not min) or (self.value >= min)) and ((not max) or (self.value <= max)):
            return True
        else:
            return False
        
    # converts a Leaf to a Python List
    def to_list(self):
        if self.has_value:
            return [self.value]
        else:
            return []

    ## inserts the value into the leaf, creating a Branch if necessary
    ## and returns the result
    def insert(self, value):
        if not self.has_value:
            res = Leaf(value)
        elif self.value < value:
            res = Branch(value, Leaf(self.value), Leaf.Bud())
        else:
            res = Branch(value, Leaf.Bud(), Leaf(self.value))
        return res

    ## A function to be re used when we want to create a value-less Leaf
    ## it is called with Leaf.Bud()
    ## (it's a classmethod so you don't need an instance of Leaf to call it.)
    @classmethod
    def Bud(cls):
        return Leaf(has_val=False)


## Branch class : non-terminal data points
class Branch:
    def __init__(self, val, left=Leaf.Bud(), right=Leaf.Bud()):
        self.value = val
        self.left : Branch | Leaf = left
        self.right : Branch | Leaf = right

    def __str__(self):
        return f"[{self.left}] <- {self.value} -> [{self.right}]"
    
    # returns the number of elements in the Branch
    def size(self) -> int:
        return 1 + self.left.size() + self.right.size()
    
    # returns the number of elements in the longest path from the root to a Leaf
    def height(self) -> int:
        h_left = self.left.height()
        h_right = self.right.height()
        return 1 + max(h_left, h_right)
    
    # tells if the Branch satisfies the BST property given its context
    def is_bst(self, min, max) -> bool:
        if min and self.value <= min:
            return False
        if max and self.value >= max:
            return False
        else:
            ans_l = self.left.is_bst(min, self.value)
            ans_r = self.right.is_bst(self.value, max)
            return ans_l and ans_r
        
    ## insert a value into the Tree as a new leaf while
    ## maintaing the BST property, if it is true before the insert starts.
    def insert(self, value):
        if value < self.value:
            self.left = self.left.insert(value)
        else:
            self.right = self.right.insert(value)
        return self
    
    # converts a Branch to a Python List
    def to_list(self):
        list_l = self.left.to_list()
        list_r = self.right.to_list()
        return list_l + [self.value] + list_r

# The tree class just has a top pointer, which is either a Leaf or a Branch.
# We can also use the top-level class to hold other metadata about the object.

# We will store the number of elements so have constant-time access,
class Tree:
    def __init__(self, head : Leaf | Branch):
        self.root = head
        self.num_elements = head.size()

    ## longest path from root to leaf
    def height(self):
        return self.root.height()
        
    ## tells if the bst property is maintained by the tree
    def is_bst(self) -> bool:
        return self.root.is_bst(None, None)
    
    ## insert a value into the Tree as a new leaf while
    ## maintaing the BST property, if it is true before the insert starts.
    def insert(self, value):
        self.root = self.root.insert(value)
        self.num_elements += 1

    ## converts the tree to a Python List
    def to_list(self) -> list:
        return self.root.to_list()
    
    def to_bst(self):
        return BinarySearchTree(self.root)

    def __str__(self):
        return str(self.root)
    
#################
## Testing Tree Class

t0 = Tree(Leaf.Bud())
t1 = Tree(Leaf(1))
t2 = Tree(Branch(4, t0.root, t1.root))
t3 = Tree(Branch(2, 
       Branch(0, Leaf(-1), Leaf(1)),   
       Branch(3, Leaf(2),  Branch(5, Leaf(4), Leaf(6)))))

assert t0.num_elements == 0
assert t1.num_elements == 1
assert t2.num_elements == 2
assert t3.num_elements == 9
logger.success("size tests passed")

assert t0.height() == 0
assert t1.height() == 1
assert t2.height() == 2
assert t3.height() == 4
logger.success("height tests passed")

assert t0.to_list() == []
assert t1.to_list() == [1]
assert t2.to_list() == [4,1]
assert t3.to_list() == [-1,0,1,2,2,3,4,5,6] ## notice that for a BST this list is sorted
logger.success("to_list tests passed")

assert t0.is_bst() == True
assert t1.is_bst() == True
assert t2.is_bst() == False
assert t3.is_bst() == True
logger.success("bst test checks passed")

###############################
## Second Class: the Binary Search Tree

## create a class that inherits everything from Tree, but
## for instances of this type we always guarantee the BST property.
## and we define an insert and lookup method that maintains the property

class BinarySearchTree(Tree):
    def __init__(self, head : Leaf | Branch):
        super().__init__(head)
        self.build_bst()
        assert self.is_bst()
        
    def build_bst(self):
        ## We re-build the tree if it fails the test
        if not self.is_bst():
            self.num_elements = 0
            values = self.to_list()
            self.root = Leaf.Bud()
            for v in values:
                self.root = self.root.insert(v)
                self.num_elements += 1

    ## tells if a given value is present in the tree, taking advantage of BST property
    def exists(self, value) -> bool:
        curr = self.root
        while True:
            if curr.value == value:
                return True
            elif isinstance(curr, Branch):
                if curr.value < value:
                    curr = curr.right
                else:
                    curr = curr.left
            else:
                return False
            
t0_bst = t0.to_bst()
t1_bst = t1.to_bst()
t2_bst = t2.to_bst()

## t3, but the values are out of order
t4 = BinarySearchTree(Branch(3, 
       Branch(4, Leaf(-1), Leaf(5)),   
       Branch(2, Leaf(2),  Branch(1, Leaf(0), Leaf(6)))))

assert t0_bst.num_elements == 0
assert len(t0_bst.to_list()) == 0
assert t1_bst.num_elements == 1
assert len(t1_bst.to_list()) == 1
assert t2_bst.num_elements == 2

assert len(t2_bst.to_list()) == 2
assert len(t4.to_list()) == 9
assert t4.num_elements  == 9
assert t4.to_list() == t3.to_list()
logger.success("build_bst tests passing")

t0_bst.insert(2.5)
t1_bst.insert(2.5)
t2_bst.insert(2.5)
t4.insert(2.5)



assert t0_bst.is_bst()
assert t1_bst.is_bst()
assert t2_bst.is_bst()
assert t4.is_bst()
assert t2_bst.to_list() == [1,2.5,4]


logger.success("BST insert tests passing")


assert t2_bst.exists(1)
assert t2_bst.exists(2.5)
assert t2_bst.exists(4)
assert not t2_bst.exists(0)

logger.success("BST exists tests passing")