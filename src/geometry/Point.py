#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Point:
    def get_min_max(self,coordinates):
        return None

    def to_canvas(self, coordinates, size, flip_horrizontaly):        
        return None

    def convert_single_coordinates(self, coordinate, size, flip_horizontaly):
        actual_x = coordinate[0]
        actual_y = coordinate[1]
        x_in_px = round((actual_x - size["orig_left"])*size["x_transform_factor"])
        y_in_px = round((actual_y - size["orig_top"])*size["y_transform_factor"])
        if flip_horizontaly:
            y_in_px = size["image_height_px"] - y_in_px

        return [x_in_px, y_in_px]
        