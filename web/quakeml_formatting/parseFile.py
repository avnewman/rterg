from obspy import read_events

def parseFile(n):
    catalog = read_events()
    catalog.write(n, format="QUAKEML")
    """
    file = open(n, "r")
    header = file.readline()
    nextLine = file.readline()
    name = ""
    for char in nextLine:
        if (char == " " and name != ""):
            break
        elif (char != " "):
            name += char
        else:
            continue
    fileName = name + ".xml"
    catalog.write(fileName, format="QUAKEML")
    """
    return
parseFile("21012303.txt")

"""
error: UserWarning: 'smi://eu.emsc/unid' is not a valid QuakeML URI. It will be in the final file but note that the file will not be a valid QuakeML file. warnings.warn(msg % obj.id)
"""
