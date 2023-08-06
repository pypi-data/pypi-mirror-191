class Pathway():
    """
    Class for describing one pathway. It contains the following attributes:
    - Pathway-specific attributes
        name: 'name of pathway corresponding to system'
    - Instances of ::State:: (defined in "energyleveler.py")
    """
    def __init__(self):
        self.name = None
        self.colour = "k"
        self.states = []
        
    def print_pathway(self):
        for state in self.states:
            print(state.label, state.energy)
        
    def add_state(self, new_state):
        self.states.append(new_state)
        
    def add_colour(self, colour):
        self.colour = colour

class State:
    """
    Class for describing one state
    """
    def __init__(self):
        self.name        = ""
        self.color       = "k"
        self.labelColor  = "k"
        self.linksTo     = ""
        self.label       = ""
        self.legend      = None
        self.energy      = 0.0
        self.normalisedPosition = 0.0
        self.column      = 1
        self.leftPointx  = 0
        self.leftPointy  = 0
        self.rightPointx = 0
        self.rightPointy = 0
        self.labelOffset = (0,0)
        self.textOffset  = (0,0)
        self.imageOffset = (0,0)
        self.imageScale = 1.0
        self.image = None
        self.show_energy = True
        
