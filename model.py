from .graph import *

############
## Types of Nodes
############

## Artist Data
class Artist(Node):
    def __init__(self, name, value, whatever):
        super().__init__(name)
        self.value = value
        self.whatever = whatever

## Musical Release Data
class Release(Node):
    def __init__(self, name, value, year):
        super().__init__(name)
        self.value = value
        self.year = year

## Recording Studio Data
class Studio(Node):
    def __init__(self, name, value, city):
        super().__init__(name)
        self.value = value
        self.city = city

############
## Types of Edges
############

## Edge that means artist "Start" is a member of artist "End"
class MemberOf(Edge):
    def __init__(self, start, end, weight=1):
        super().__init__(start, end, "MEMBER_OF", weight)

## Edge that means artist "Start" played on release "End"
class PlayedOn(Edge):
    def __init__(self, start, end, weight=1):
        super().__init__(start, end, "PLAYED_ON", weight)

## Edge that means release "Start was recorded at studio" "End"
class RecordedAt(Edge):
    def __init__(self, start, end, weight=1):
        super().__init__(start, end, "RECORDED_AT", weight)

## Edge that means relase "Start" appeared on release "End"
class AppearedOn(Edge):
    def __init__(self, start, end, weight=1):
        super().__init__(start, end, "APPEARED_ON", weight)




## Using the graph class, implement Music Network which does some fun stuff. 
## Use the classes above if you want, or make others. I think the Node classes are useful 
## since there will (probably) be different types of data
# in different Nodes types, 
## the Edge classes are a bit over the top since we have the "meaning" parameter. Up to you how you want to set it up!
class MusicNetwork(Graph):
    pass