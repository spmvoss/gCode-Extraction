import csv
import os
import math


class Processor():
    def __init__(self, filename: str, csv_out_directory: str = "output/csv",
                 sub_distance: float = 0.1, min_dist: float = 0.1, max_dist: float = 0.5,
                 use_intermediates: bool = False):
        """
        :param filename: The name of the file that contains the gCODE
        :param csv_out_directory: The directory where the txt files should be saved
        :param sub_distance: The distance that will be used to create intermediate points (if True)
        :param min_dist: Minimum distance that points need to be apart before they get rejected
        :param max_dist: Maximum distance before which intermediate points get added (might be useful for splines)
        :param use_intermediates: Boolean True = intermediate points will be generated when distance > max_dist
        """
        self.csv_dir = csv_out_directory
        self.filename = "input/" + filename
        self.min_dist = min_dist
        self.use_inter = use_intermediates

        if use_intermediates:
            self.d = sub_distance
            self.max_dist = max_dist
        else:
            self.d = 0.
            self.max_dist = float('inf')
        self.check_folder_structure()

    layers = {}

    @staticmethod
    def check_folder_structure():
        """
        Checks if folder structure is present and otherwise will generate it
        """
        if not os.path.exists("output"):
            os.makedirs("output")
            os.makedirs("output/csv")
            os.makedirs("output/SW")
            os.makedirs("output/SW/extrudes")
        if not os.path.exists("logs"):
            os.makedirs("logs")
        return None

    def intermediates(self, p1, p2, z):
        """"Return a list of equally spaced points
        between p1 and p2 of about distance d"""
        d2 = self.d ** 2
        c = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) / d2
        D = 2 ** 2 - (4 * (1 - c))  # discriminant

        if D < 0:
            print('No Solution')
        elif D == 0:
            n = -2 / (2 * 1)
            n = int(n)
        else:  # if D > 0
            n = (-2 + math.sqrt(D)) / (2 * 1)
            n = int(n)
            # x2 = (-2 - math.sqrt(D)) / (2 * 1)

        x_spacing = (p2[0] - p1[0]) / (n + 1)
        y_spacing = (p2[1] - p1[1]) / (n + 1)

        return [[p1[0] + i * x_spacing, p1[1] + i * y_spacing, float(z)]
                for i in range(1, n + 1)]

    def read(self):
        """Reads the gcodes file and stores data in layers dict"""
        current_layer = 0
        current_sub = 0
        current_z = 0
        previous_coordinate = [0., 0., 0.]
        discard_count = 0
        with open(self.filename) as file:
            reader = csv.reader(file, delimiter=" ")  # Open the file and set delimiter to a space
            for rows in reader:  # Iterate over every row/line
                if "layer" in rows and "Z" in rows:  # Start of new layer and Z position information
                    current_z = rows[5]  # Set the Z value for current layer
                    current_layer = rows[2]  # Get the layer number
                    current_layer = current_layer[:-1]  # Strip the "Z" from the layer number
                    current_sub = 0  # Reset the sub curve counter to start at 0 again

                if len(rows) == 2 and "G92" in rows and current_layer != 0:
                    if current_sub == 0:  # We have just changed layer
                        current_sub = current_sub + 1
                        key_name = str(current_layer) + "_" + str(current_sub)
                        # Create a new key in the dict with an empty array for the layer's coordinates
                        self.layers[key_name] = []
                    elif self.layers[key_name]:
                        current_sub = current_sub + 1
                        key_name = str(current_layer) + "_" + str(current_sub)
                        # Create a new key in the dict with an empty array for the layer's coordinates
                        self.layers[key_name] = []
                if current_layer != 0:  # Skip all nonsense before first layer
                    for items in rows:  # Iterate over the items in the row to check if it has X coordinates
                        if "X" in items:
                            # We are dealing with position coordinates but not sure if extruding or not
                            for units in rows:
                                if "E" in units:
                                    # There is both an E and an X in the row so we are extruding
                                    X = rows[1]  # Grab the X coord from the row
                                    X = X[1:]  # Delete the first character (X)
                                    Y = rows[2]  # Grab the Y coord from the row
                                    Y = Y[1:]  # Delete the first character (Y)
                                    coordinate = [float(X), float(Y),
                                                  float(current_z)]  # Construct the coordinate array

                                    # Since SolidWorks will freak out if points are too close together we will calculate
                                    # the distance between two consecutive points and if it is smaller than 0.01 mm we
                                    # will not include it in the list
                                    # There were also problems with duplicate coordinates so we check the current list
                                    # for already existing coordinates.

                                    dist = ((coordinate[0] - previous_coordinate[0]) ** 2 + (
                                        coordinate[1] - previous_coordinate[1]) ** 2) ** 0.5
                                    if coordinate not in self.layers[key_name] and self.min_dist < dist < self.max_dist:
                                        layer_list = self.layers[key_name]  # Grab the current list of coordinates
                                        layer_list.append(coordinate)  # Append with new coordinate
                                        self.layers[key_name] = layer_list  # Write back to dictionary
                                    elif coordinate not in self.layers[key_name] and dist >= self.max_dist:
                                        intermediate_coordinates = self.intermediates(coordinate, previous_coordinate,
                                                                                      z=current_z)
                                        layer_list = self.layers[key_name]  # Grab the current list of coordinates
                                        for coords in intermediate_coordinates:
                                            layer_list.append(coords)  # Append with new coordinate
                                        layer_list.append(coordinate)  # Append with new coordinate
                                        self.layers[key_name] = layer_list  # Write back to dictionary

                                    previous_coordinate = coordinate  # Save the current coord for distance calculation

    def write_csv(self):
        if self.layers:  # Check if the dictionary already exists, else run read and rerun self
            for keys in self.layers:  # iterate over all the keys in the layers dictionary
                # Check if there is an entry in the current key
                if self.layers[keys]:
                    # The below if statement makes sure that 1.txt becomes 001.txt and 10.txt becomes 010.txt etc.
                    layer_n, line_n = keys.split("_", 1)
                    key_name = self.seq_names(layer_n, line_n)
                    path = os.path.join(self.csv_dir, key_name + '.txt')  # Create the output path
                    with open(path, "w") as csv_file:  # Create the file
                        writer = csv.writer(csv_file, lineterminator='\n')  # Create writer with file structure
                        for line in self.layers[keys]:  # Go over the lines in each dict
                            writer.writerow(line)  # Write each line to the open file
        else:
            self.read()
            self.write_csv()

    @staticmethod
    def seq_names(layer_n: str, line_n: str) -> str:
        """
        This method takes the layer number and line number and outputs a sequence name in the format of xxx_xxx
        :param layer_n: The layer number
        :param line_n: The line number
        :return: the name for the layer and line
        """
        if len(line_n) < 3:
            if len(line_n) < 2:
                key_end = "_00" + line_n
            else:
                key_end = "_0" + line_n
        else:
            key_end = line_n

        if len(layer_n) < 3:
            if len(layer_n) < 2:
                key_name = "00" + layer_n + key_end
            else:
                key_name = "0" + layer_n + key_end
        else:
            key_name = layer_n + key_end
        return key_name


# Here the script is run and where the correct settings are put in
Processor(filename="model.gcode").write_csv()
