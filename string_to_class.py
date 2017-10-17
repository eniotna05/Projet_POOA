if __name__ == "__main__":
    from Form_class import *
    from Command_class import *



def string_to_circle(string):
    parameters = string.split(",")
    return Circle(Point(int(parameters[0]),int(parameters[1])),
    int(parameters[2]),identifier = parameters[3])


def string_to_square(string):
    parameters = string.split(",")
    return Square(Point(int(parameters[0]),int(parameters[1])),
    int(parameters[2]),identifier = parameters[3])


def string_to_lign(string):
    parameters = string.split(",")
    return Lign(Point(int(parameters[0]),int(parameters[1])),
    Point(int(parameters[2]),int(parameters[3])), identifier = parameters[4])

def string_to_rectangle(string):
    parameters = string.split(",")
    return Rectangle(Point(int(parameters[0]),int(parameters[1])),
    Point(int(parameters[2]),int(parameters[3])), identifier = parameters[4])




def string_to_command(string):

# Function to transform a string into appropriate command

    if not isinstance(string, str):
        raise TypeError("The parameter of string_to_command is a string")
                        
    FL = string[0]

    if FL == "C":
        return Create(string_to_circle(string[1:]))
    elif FL == "S":
        return Create(string_to_square(string[1:]))
    elif FL == "R":
        return Create(string_to_rectangle(string[1:]))
    elif FL == "L":
        return Create(string_to_lign(string[1:]))
    
    elif FL == "Q":
        return Quit()
    elif FL == "H":
        return Hello()
    elif FL == "D":
        return Delete(int(string[1:]))

    else:
        raise ValueError("The first letter is incorrect")
        


# Zone de test                
if __name__ == "__main__":
   

    
    Creation_1 = Create(Rectangle(Point(1,3),Point(10,100)))
    Creation_2 = Create(Lign(Point(134,27),Point(1439,238)))
    Creation_3 = Create(Circle(Point(43,372),37))
    Creation_4 = Create(Square(Point(74,23),7))

   
    print(Creation_1,"\n")
    print(Creation_2,"\n")
    print(Creation_3,"\n")
    print(Creation_4,"\n")

    string_1 = Creation_1.get_string()
    string_2 = Creation_2.get_string()
    string_3 = Creation_3.get_string()
    string_4 = Creation_4.get_string()

    print(string_1)
    print(string_2)
    print(string_3)
    print(string_4)

    Creation_1_R = string_to_command(string_1)
    Creation_2_R = string_to_command(string_2)
    Creation_3_R = string_to_command(string_3)
    Creation_4_R = string_to_command(string_4)

    print("\n",Creation_1_R,"\n")
    print(Creation_2_R,"\n")
    print(Creation_3_R,"\n")
    print(Creation_4_R,"\n")
    

 

