if __name__ == "__main__":
    from Form_class import *
    


class Create:
    def __init__(self, created_form):
       
        self.created_form = created_form 
          
        
    def __repr__(self):
        
        return """Creation of the form: {}""".format(self.created_form)

    def get_string(self):

        # method to transform command into string
        # return string of created form 

        return self.created_form.get_string()



class Delete:
    def __init__(self, form_id):
       
        if not isinstance(form_id, str):
            raise TypeError("The parameter has to be a string")
        self.form_id = form_id
        self.symbol = "D"
          
        
    def __repr__(self):
        
        return """Deletion of the form id: """.format(self.form)

    def get_string(self):

        # method to transform command into string
        # Ex: delection of Form 45 => return D45

        return self.symbol + self.form_id


class Quit:
    def __init__(self):
        self.symbol = "Q"
        self.message = "You are disconnected from the server"

    def get_string(self):

        return self.symbol 


class Hello:
    def __init__(self):
        self.symbol = "H"
        self.message = "The client is connected to the server"

    def get_string(self):

        return self.symbol



class Move:
    """ horizontal movement and y = vertical movement
    x an y are integers and can be negative """

    

    
    def __init__(self, form_id, x, y):

        if not isinstance(form_id, str):
            raise TypeError("The parameter has to be a string")
        if not isinstance(x, int):
            raise TypeError("The parameter has to be a string")
        if not isinstance(y, int):
            raise TypeError("The parameter has to be a string")
       
        self.form_id = form_id
        self.x = x
        self. y = y
        self.symbol = "M"
          
        
    def __repr__(self):
        
        return """Moving of the form: {}, horizontal movement = {},
        vertical movement = {}""".format(self.form_id, self.x, self. y)

    def get_string(self):

        # method to transform command into string
        # return string of created form 

        return self.symbol + self.form_id + ","
        + str(self.x) + "," + str(self.y)

       
          
if __name__ == "__main__":
    Creation_1 = Create(WB_Rectangle(Point(1,3),Point(10,100)))
    Creation_2 = Create(WB_Line(Point(134,27),Point(1439,238)))
    Creation_3 = Create(WB_Circle(Point(43,372),37))

   
    print(Creation_1)
    print(Creation_2)
    print(Creation_3)


   
