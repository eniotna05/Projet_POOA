from utils.form_class import WBCircle, WBEllipse, WBRectangle, WBSquare, \
    WBLine, WBLabel, WBPoint, WBPicture

from utils.command_class import Create, Delete, Move, Quit, Hello, \
    DeleteRequest, NegativeAnswer


def string_to_circle(string):
    parameters = string.split(",")
    return WBCircle(WBPoint(int(parameters[0]), int(parameters[1])),
                    int(parameters[2]),
                    identifier=parameters[3])


def string_to_ellipse(string):
    parameters = string.split(",")
    return WBEllipse(WBPoint(int(parameters[0]), int(parameters[1])),
                     int(parameters[2]),
                     int(parameters[3]),
                     identifier=parameters[4])


def string_to_square(string):
    parameters = string.split(",")
    return WBSquare(WBPoint(int(parameters[0]), int(parameters[1])),
                    WBPoint(int(parameters[2]), int(parameters[3])),
                    identifier=parameters[4])


def string_to_lign(string):
    parameters = string.split(",")
    return WBLine(WBPoint(int(parameters[0]), int(parameters[1])),
                  WBPoint(int(parameters[2]), int(parameters[3])),
                  identifier=parameters[4])


def string_to_rectangle(string):
    parameters = string.split(",")
    return WBRectangle(WBPoint(int(parameters[0]), int(parameters[1])),
                       WBPoint(int(parameters[2]), int(parameters[3])),
                       identifier=parameters[4])


def string_to_label(string):
    parameters = string.split(",")
    return WBLabel(WBPoint(int(parameters[0]), int(parameters[1])),
                   WBPoint(int(parameters[2]), int(parameters[3])),
                   parameters[4],
                   identifier=parameters[5])


def string_to_image(string):
    parameters = string.split(",")
    return WBPicture(WBPoint(int(parameters[0]), int(parameters[1])),
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
        return Create(string_to_image(string[1:]))
    elif FL == "T":
        return Create(string_to_label(string[1:]))

    elif FL == "Q":
        return Quit()
    elif FL == "H":
        return Hello()
    elif FL == "D":
        parameter = string[1:]
        return Delete(parameter)
    elif FL == "Z":
        parameters = string[1:].split(",")
        return DeleteRequest(parameters[0], parameters[1])
    elif FL == "N":
        parameters = string[1:].split(",")
        return NegativeAnswer(parameters[0], parameters[1])
    elif FL == "M":
        parameters = string[1:].split(",")
        return Move(parameters[0], int(parameters[1]), int(parameters[2]))

    else:
        raise ValueError("The first letter is incorrect")
