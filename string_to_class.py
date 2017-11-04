from Form_class import WB_Circle, WB_Ellipse, WB_Rectangle, WB_Square, WB_Line, Point, Pic
from Command_class import Create, Delete, Move, Quit, Hello, Delete_demend, Negative_answer





def convertStrIntoForm(string):
    # Converts an input into the right Form object
    letter = string[0]
    if letter == "R":
        return string_to_rectangle(string[1:])
    elif letter == "C":
        return string_to_circle(string[1:])
    elif letter == "L":
        return string_to_lign(string[1:])
    elif letter == "S":
        return string_to_square(string[1:])
    elif letter == "P":
        return string_to_image(string[1:])


def string_to_circle(string):
    parameters = string.split(",")
    return WB_Circle(Point(int(parameters[0]), int(parameters[1])),
                     int(parameters[2]), identifier=parameters[3])


def string_to_ellipse(string):
    parameters = string.split(",")
    return WB_Ellipse(Point(int(parameters[0]), int(parameters[1])),
                      int(parameters[2]), int(parameters[3]),
                      identifier=parameters[4])


def string_to_square(string):
    parameters = string.split(",")
    return WB_Square(Point(int(parameters[0]), int(parameters[1])),
                     Point(int(parameters[2]), int(parameters[3])),
                     identifier=parameters[4])


def string_to_lign(string):
    parameters = string.split(",")
    return WB_Line(Point(int(parameters[0]), int(parameters[1])),
                   Point(int(parameters[2]), int(parameters[3])),
                   identifier=parameters[4])


def string_to_rectangle(string):
    parameters = string.split(",")
    return WB_Rectangle(Point(int(parameters[0]), int(parameters[1])),
                        Point(int(parameters[2]), int(parameters[3])),
                        identifier=parameters[4])


def string_to_image(string):
    parameters = string.split(",")
    return Pic(Point(int(parameters[0]), int(parameters[1])),
               identifier=parameters[2])


def string_to_command(string):

    """Function to transform a string into appropriate command"""

    if not isinstance(string, str):
        raise TypeError("The parameter of string_to_command is a string")

    FL = string[0]

    if FL == "C":
        return Create(string_to_circle(string[1:]))
    elif FL == "E":
        return Create(string_to_ellipse(string[1:]))
    elif FL == "S":
        return Create(string_to_square(string[1:]))
    elif FL == "R":
        return Create(string_to_rectangle(string[1:]))
    elif FL == "L":
        return Create(string_to_lign(string[1:]))
    elif FL == "P":
        return  Create(string_to_image(string[1:]))

    elif FL == "Q":
        return Quit()
    elif FL == "H":
        return Hello()
    elif FL == "D":
        parameter = string[1:]
        return Delete(parameter)
    elif FL == "Z":
        parameters = string[1:].split(",")
        return Delete_demend(parameters[0], parameters[1])
    elif FL == "N":
        parameters = string[1:].split(",")
        return Negative_answer(parameters[0], parameters[1])
    elif FL == "M":
        parameters = string[1:].split(",")
        return Move(parameters[0], int(parameters[1]), int(parameters[2]))

    else:
        raise ValueError("The first letter is incorrect")


# Zone de test
if __name__ == "__main__":


    Deletion1 = Delete("Antoine5")
    Negative_answer1 = Negative_answer(("Anais3"),"Antoine")
    print(Deletion1,"\n")
    print(Negative_answer1,"\n")

    string1 = Deletion1.get_string()
    string2 = Negative_answer1.get_string()

    print(string1)
    print(string2)

    Deletion1R = string_to_command(string1)

    Negative_answer11R = string_to_command(string2)

    print(Deletion1R,"\n")
    print(Negative_answer1,"\n")




#
#     Creation_1 = Create(WB_Rectangle(Point(1,3),Point(10,100)))
#     Creation_2 = Create(WB_Line(Point(134,27),Point(322,238)))
#     Creation_3 = Create(WB_Circle(Point(43,372),37))
#     Creation_4 = Create(WB_Square(Point(74,23),Point(80,29)))
#     Creation_5 = Create(WB_Ellipse(Point(74,23),5,8))
#
#     print(Creation_1,"\n")
#     print(Creation_2,"\n")
#     print(Creation_3,"\n")
#     print(Creation_4,"\n")
#     print(Creation_5,"\n")
#
#     string_1 = Creation_1.get_string()
#     string_2 = Creation_2.get_string()
#     string_3 = Creation_3.get_string()
#     string_4 = Creation_4.get_string()
#     string_5 = Creation_5.get_string()
#
#     print(string_1)
#     print(string_2)
#     print(string_3)
#     print(string_4)
#     print(string_5)
#
#     Creation_1_R = string_to_command(string_1)
#     Creation_2_R = string_to_command(string_2)
#     Creation_3_R = string_to_command(string_3)
#     Creation_4_R = string_to_command(string_4)
#     Creation_5_R = string_to_command(string_5)
#
#     print("\n",Creation_1_R,"\n")
#     print(Creation_2_R,"\n")
#     print(Creation_3_R,"\n")
#     print(Creation_4_R,"\n")
#     print(Creation_5_R,"\n")
#
#     Creation_1_R.created_form.change_position(1000,1000)
#     Creation_2_R.created_form.change_position(1000,1000)
#     Creation_3_R.created_form.change_position(1000,1000)
#     Creation_4_R.created_form.change_position(1000,1000)
#     Creation_5_R.created_form.change_position(-20,-20)
#
#     print("\n",Creation_1_R,"\n")
#     print(Creation_2_R,"\n")
#     print(Creation_3_R,"\n")
#     print(Creation_4_R,"\n")
#     print(Creation_5_R,"\n")
