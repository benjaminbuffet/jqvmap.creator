#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Polygon:
    def get_min_max(self,coordinates):
        min_x = None
        min_y = None
        max_x = None
        max_y = None

        for i in range(len(coordinates)):
            for j in range(len(coordinates[i])):
                actual_x = coordinates[i][j][0]
                actual_y = coordinates[i][j][1]
                if min_x is None or min_x > actual_x:
                    min_x = actual_x
                if min_y is None or min_y > actual_y:
                    min_y = actual_y
                if max_x is None or max_x < actual_x:
                    max_x = actual_x
                if max_y is None or max_y < actual_y:
                    max_y = actual_y
        return {
            'min_x':min_x,
            'min_y':min_y,
            'max_x':max_x,
            'max_y':max_y,
        }

    def to_canvas(self, coordinates, size, flip_horrizontaly):
        path = "M"
        previous_x_in_px = None
        previous_y_in_px = None
        first_point = ""
        
        for i in range(len(coordinates)):  
            if i > 0 and path[-4:] != " Z M":
                path = path + " Z M"
            for j in range(len(coordinates[i])):
                actual_x = coordinates[i][j][0]
                actual_y = coordinates[i][j][1]
                x_in_px = round((actual_x - size["orig_left"])*size["x_transform_factor"])
                y_in_px = round((actual_y - size["orig_top"])*size["y_transform_factor"])
                
                if flip_horrizontaly:
                    y_in_px = size["image_height_px"] - y_in_px

                if x_in_px != previous_x_in_px and y_in_px != previous_y_in_px :
                    if path[-1:] != "M":
                        path = path + " L"
                    path = path + " " + str(x_in_px) + "," + str(y_in_px)
                    previous_x_in_px = x_in_px
                    previous_y_in_px = y_in_px

                if j == 0:
                    first_point = str(x_in_px) + "," + str(y_in_px)

        path = path + " L " + first_point + " z"
        return path
