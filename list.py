
from loguru import logger

"""
A List has either no values and is Empty (represented by None)
or has at least one value and is a Node

A Node has two subcomponents:
 - a value
 - a 'next' element, which is a List

We visualize lists as values and pointers. The data structure

  Node(2, Node(-1, Node(1, Node(3, None))))    
  
  looks like
  
  2 -> -1 -> 1 -> 3 -> None
  
Finally, we define the class List as either a Node or None,
but primarily implement things for Node.

We could implement full versions full the list class as well, but who cares about 
that for right here. Node methods covers everythng interesting, don't want to get hung up on lists.
Using a class for nodes is the cleanest way to do it simply but still using classes. 

It's a classic problem
of how to handle the empty case when defining lists and trees, for Lists we're lazy
and for Trees we'll do it right.

"""

class Node():
    def __init__(self, val, next=None):
        self.value = val
        self.next : List = next

    ## print out the list showing the sequence
    def __str__(self):
        return f"{self.value} -> {self.next}"

    ## Return the number of elements in the list
    def length(self) -> int: 
        if self.next:
            return 1 + self.next.length()
        else:
            return 1
    
    ## tell whether v is an element somewhere in the list
    def member(self, v) -> bool:
        if self.value == v:
            return True
        elif self.next:
            return self.next.member(v)
        else:
            return False   
        
    ## given an index, provide the value at that index. 
    ## If out of bounds, return None
    def val_at(self, index : int):
        if index == 0:
            return self.value
        elif self.next:
            return self.next.val_at(index-1)
        else:
            return None

    ## insert the value into the list at the provided index
    def insert(self, val, index : int):
        if index == 0:
            tmp = Node(self.value, self.next)
            self.value = val
            self.next = tmp
        elif self.next:
            self.next.insert(val, index-1)
        else:
            self.next = Node(val)

class List: Node | None


## the empty list (aka [] in python)
ls0 = None

ls1 = Node("hello")

# two lists, both with the same 3 elements, but with a different order
ls2 = Node(1, Node(2, Node(3)))
ls3 = Node(2, Node(1, Node(3)))

logger.info(f"ls0 = {ls0}")
logger.info(f"ls1 = {ls1}")
logger.info(f"ls2 = {ls2}")
logger.info(f"ls3 = {ls3}")

###################
## Tests
###################

assert ls1.length() == 1
assert ls2.length() == 3
assert ls2.length() == ls3.length()
logger.success("Length tests passed")

assert ls2.member(3) == True
assert ls2.member(2) == True
assert ls2.member(1) == True
logger.success("member tests passed")

assert ls2.val_at(2) == 3
assert ls2.val_at(500) == None
assert ls2.val_at(0) == 1
logger.success("val_at tests passed")

assert ls3.member(-1) == False
ls3.insert(-1, 1)
assert ls3.member(-1) == True
assert ls3.val_at(1) == -1
assert ls3.val_at(0) == 2
assert ls3.val_at(2) == 1
logger.success("insert tests passed")
