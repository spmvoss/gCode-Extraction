import csv
import os
import numpy

layers = {}
out_dir = "output/"
csv_dir = "output/csv/"
currentLayer = 0
currentSub = 0
currentZ = 0
previousCoord = [0., 0., 0.]
discard_count = 0

with open("layer3.txt") as file:
    reader = csv.reader(file, delimiter=" ")    # Open the file and set delimiter to a space
    for rows in reader: # Iterate over every row/line
        if "layer" in rows and "Z" in rows: # Start of new layer and Z position information
            currentZ = rows[5]  # Set the Z value for current layer
            currentLayer = rows[2]  # Get the layer number
            currentLayer = currentLayer[:-1]    # Strip the "Z" from the layer number
            currentSub = 0  # Reset the sub curve counter to start at 0 again

        if len(rows) == 2 and "G92" in rows and currentLayer != 0:
            if currentSub == 0: # We have just changed layer
                currentSub = currentSub + 1
                key_name = currentLayer + "_" + str(currentSub)
                layers[key_name] = []  # Create a new key in the dict with an empty array for the layer's coordinates
            elif layers[key_name]:
                currentSub = currentSub + 1
                key_name = currentLayer + "_" + str(currentSub)
                layers[key_name] = []  # Create a new key in the dict with an empty array for the layer's coordinates
        # if "infill" in rows or "perimeter" in rows or "solid" in rows:     # Where the printhead starts a new section
        #     currentSub = currentSub + 1 # We need to change to a new sub curve
        #     key_name = currentLayer + "_" + str(currentSub)
        #     layers[key_name] = []   # Create a new key in the dict with an empty array for the layer's coordinates
        if currentLayer != 0:   # Skip all nonsense before first layer
            for items in rows:  # Iterate over the items in the row to check if it has X coordinates
                if "X" in items:
                    # We are dealing with position coordinates but not sure if extruding or not
                    for units in rows:
                        if "E" in units:
                            # There is both an E and an X in the row so we are extruding
                            X = rows[1] # Grab the X coord from the row
                            X = X[1:]   # Delete the first character (X)
                            Y = rows[2] # Grab the Y coord from the row
                            Y = Y[1:]   # Delete the first character (Y)
                            coordinate = [float(X), float(Y), float(currentZ)] # Construct the coordinate array
                            """
                            Since SolidWorks will freak out if points are too close together we will calculate the 
                            distance between two consecutive points and if it is smaller than 0.01 mm we will not include
                            it in the list
                            There were also problems with duplicate coordinates so we check the current list for 
                            already existing coordinates. 
                            """
                            dist = ((coordinate[0]-previousCoord[0])**2 + (coordinate[1]-previousCoord[1])**2)**0.5
                            if coordinate not in layers[key_name] and dist > 0.05:
                                layerList = layers[key_name]    # Grab the current list of coordinates
                                layerList.append(coordinate)    # Append with new coordinate
                                layers[key_name] = layerList    # Write back to dictionary
                            previousCoord = coordinate          # Save the current coord for distance calculation

for keys in layers:
    # iterate over all the keys in the layers dictionary
    if layers[keys]:
        # Because of the way that this script is set up the last dict entry of each layer is empty. Skip that in writing
        path = os.path.join(out_dir, keys + '.txt') # Create the output path
        with open(path, "w") as csv_file:   # Create the file
            writer = csv.writer(csv_file, delimiter="\t")   # Create writer with file structure
            for line in layers[keys]:   # Go over the lines in each dict
                writer.writerow(line)   # Write each line to the open file

for keys in layers:
    # iterate over all the keys in the layers dictionary
    if layers[keys]:
        # Because of the way that this script is set up the last dict entry of each layer is empty. Skip that in writing
        path = os.path.join(csv_dir, keys + '.txt') # Create the output path
        with open(path, "w") as csv_file:   # Create the file
            writer = csv.writer(csv_file, lineterminator='\n')   # Create writer with file structure
            for line in layers[keys]:   # Go over the lines in each dict
                writer.writerow(line)   # Write each line to the open file



