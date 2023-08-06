# --------------------
## holds various values for the "model" in MVC pattern
class Model:
    # --------------------
    ## constructor
    def __init__(self):
        ## the state for button1/label1
        self.state1 = None
        ## the state for button2/label2
        self.state2 = None

        self.clear()

    # --------------------
    ## initialization of objects
    #
    # @return None
    def init(self):
        pass

    # --------------------
    ## reset the current states
    #
    # @return None
    def clear(self):
        self.state1 = 0
        self.state2 = 0

    # --------------------
    ## toggle state1
    #
    # @return None
    def toggle_state1(self):
        self.state1 = 1 - self.state1

    # --------------------
    ## toggle state2
    #
    # @return None
    def toggle_state2(self):
        self.state2 = 1 - self.state2
