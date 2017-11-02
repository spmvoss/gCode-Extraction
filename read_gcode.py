import csv
import os
import numpy

layers = {}
out_dir = "output/"
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
        if "infill" in rows or "perimeter" in rows or "solid" in rows:     # Where the printhead starts a new section
            currentSub = currentSub + 1 # We need to change to a new sub curve
            key_name = currentLayer + "_" + str(currentSub)
            print(rows)
            print(key_name)
            layers[key_name] = []   # Create a new key in the dict with an empty array for the layer's coordinates
        if currentLayer != 0:   # Skip all nonsense before first layer
            for items in rows:  # Iterate over the items in the row to check if it has X coordinates
                if "X" in items:
                    # We are dealing with position coordinates but not sure if extruding or not
                    for units in rows:
                        if "E" in units:
                            # There is both an E and an X in the row
                            X = rows[1]
                            X = X[1:]
                            Y = rows[2]
                            Y = Y[1:]
                            coordinate = [float(X), float(Y), float(currentZ)]
                            dist = ((coordinate[0]-previousCoord[0])**2 + (coordinate[1]-previousCoord[1])**2)**0.5
                            if coordinate not in layers[key_name] and dist > 0.1:
                                layerList = layers[key_name]
                                layerList.append(coordinate)
                                layers[key_name] = layerList
                            previousCoord = coordinate

# We could write each layer to a separate file and use an excel macro to import it into SW as curves.
for keys in layers:
    path = os.path.join(out_dir, keys+'.txt')
    with open(path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter="\t")
        for line in layers[keys]:
            writer.writerow(line)

