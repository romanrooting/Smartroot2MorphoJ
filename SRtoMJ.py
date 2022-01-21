import numpy
import pandas as pd
import math

def calculate_distance(x1,x2,y1,y2,x0,y0):
    return ((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1)) / math.sqrt((x2 - x1)**2+(y2 -y1)**2)

#get specific locations of files
globalRootData = input("Enter the path to your GlobalRootData.csv:")
rootNodes = input("Enter the path to your RootNodes.csv:")
treatmentPosition = input("Which position contains your factor for classification?")

#load the global root data files        
root_data_reader = pd.read_csv(globalRootData, delimiter=',')

#Load the root nodes data
rootreader = pd.read_csv(rootNodes, delimiter=',')

#Get all of the roots that have parent "-1", which means that they are for sure 1st order root/primary roots. Also filter out roots with 0 or 1 lateral roots. Put those in a list.
parentList = root_data_reader[root_data_reader.parent == "-1" & root_data_reader.n_child > 1].get("root")

#Load two files for storing data
with open("MorphoFile.txt", 'w') as out:
    with open("ClassifierTable.txt", 'w') as table:
        #iterate over each parent in the list with parents
        for parent in parentList:
            #check if the root has secondary roots. If not, then landmarks will not be able to be placed.
            parentName = root_data_reader[root_data_reader['root'] == parent].get("root_name").values[0]
            parentTreatment = parentName.split("_")[2]
            out.write(parentName)
            table.write(parentName + "," + parentTreatment + "\n")
            #get base position
            baseCoords = rootreader[(rootreader['distance_from_base'] == 0) & (rootreader['root'] == parent)].get(["x","y"])
            x1 = baseCoords.values[0][0]
            out.write("," + str(x1))
            y1 = baseCoords.values[0][1]
            out.write("," + str(y1))
            #get apex position
            apexCoords = rootreader[(rootreader['distance_from_apex'] == 0) & (rootreader['root'] == parent)].get(["x","y"])
            x2 = apexCoords.values[0][0]
            out.write("," + str(x2))
            y2 = apexCoords.values[0][1]
            out.write("," + str(y2))
            #find youngest lateral root position
            lastRootIndex = root_data_reader[root_data_reader['parent'] == parent].get("insertion_position").idxmax()
            lastRootName = root_data_reader["root"][lastRootIndex]
            lastRootCoords = rootreader[(rootreader['distance_from_base'] == 0) & (rootreader['root'] == lastRootName)].get(["x","y"])
            x3 = lastRootCoords.values[0][0]
            out.write("," + str(x3))
            y3 = lastRootCoords.values[0][1]
            out.write("," + str(y3))
            #find widest parts
            firstChildNameList = root_data_reader[root_data_reader['parent'] == parent].get("root")
            firstChildList = rootreader[rootreader["root"].isin(firstChildNameList)]
            firstChildList["distance"] = calculate_distance(x1,x2,y1,y2,firstChildList.x,firstChildList.y)
            x4 = firstChildList["x"][firstChildList["distance"].idxmax()]
            out.write("," + str(x4))
            y4 = firstChildList["y"][firstChildList["distance"].idxmax()]
            out.write("," + str(y4))
            x5 = firstChildList["x"][firstChildList["distance"].idxmin()]
            out.write("," + str(x5))
            y5 = firstChildList["y"][firstChildList["distance"].idxmin()]
            out.write("," + str(y5))
            out.write("\n")