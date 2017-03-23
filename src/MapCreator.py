#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from geometry.GeometryFactory import GeometryFactory

class MapCreator:
    id_col_name = "ID"
    name_col_name = "NAME"
    max_width = 500
    max_height = 500
    geometry_factory = GeometryFactory()
    output_file = ""
    flip_horizontally = False

    def __init__(self, output_file, max_width = 500, max_height = 500, id_col_name = "ID", name_col_name = "NAME", flip_horizontally = False) :
        self.id_col_name = id_col_name
        self.name_col_name = name_col_name        
        self.max_width = max_width
        self.max_height = max_height
        self.output_file = output_file
        self.flip_horizontally = flip_horizontally

    def execute(self, file_path):
        f = open(file_path, 'r')
        file_content = f.read()
        f.close()
        geo_json = json.loads(file_content)
        size = self._calc_size(geo_json)        
        canvas = self.convert_to_canvas(geo_json, size)
        self.writeJsonFile(canvas)
    
    def _calc_size(self,geo_json):
        size = {
            'orig_top' : 0,
            'orig_left' : 0,
            'image_width_px' : 0,
            'image_height_px' : 0,
            'image_width_orig' : 0,
            'image_height_orig' : 0,
            'x_transform_factor' : 0,
            'y_transform_factor' : 0
            }

        min_x = None
        min_y = None
        max_x = None
        max_y = None
        
        for elt in geo_json["features"]:
            geometry_service = self.geometry_factory.get(elt["geometry"]["type"])
            min_max = geometry_service.get_min_max(elt["geometry"]["coordinates"])            
            if min_x is None or min_x > min_max["min_x"]:
                min_x = min_max["min_x"]
            if min_y is None or min_y > min_max["min_y"]:
                min_y = min_max["min_y"]
            if max_x is None or max_x < min_max["max_x"]:
                max_x = min_max["max_x"]
            if max_y is None or max_y < min_max["max_y"]:
                max_y = min_max["max_y"]
                
        size["image_width_orig"] = max_x - min_x
        size["image_height_orig"] = max_y - min_y
        size["orig_left"] = min_x
        size["orig_top"] = min_y

        ratio_width_height = size["image_width_orig"] / size["image_height_orig"]
        if  size["image_height_orig"] > size["image_width_orig"]:
            size["image_width_px"] = round(self.max_height * ratio_width_height)
            size["image_height_px"] = self.max_height
        else:
            size["image_width_px"] = self.max_width
            size["image_height_px"] = round(self.max_width / ratio_width_height)
        
        size["x_transform_factor"] = size["image_width_px"] / size["image_width_orig"]
        size["y_transform_factor"] = size["image_height_px"] / size["image_height_orig"]

        return size
    
    def convert_to_canvas(self, geo_json, size):
        canvas = {"width": size["image_width_px"], "height": size["image_height_px"], "paths":{}}
        for elt in geo_json["features"]:
            id = elt["properties"][self.id_col_name]
            name = elt["properties"][self.name_col_name]
            canvas["paths"][id] = {
                "path":self.convert_to_canvas_path(elt["geometry"],size),
                "name":name}
        return canvas

    def convert_to_canvas_path(self, geometry, size):
        geometry_service = self.geometry_factory.get(geometry["type"])
        return geometry_service.to_canvas(geometry["coordinates"], size, self.flip_horizontally)

    def writeJsonFile(self, canvas):
        jsonContent = "jQuery.fn.vectorMap('addMap', 'test_fr', "
        jsonContent = jsonContent + json.dumps(canvas) + ");"

        f = open(self.output_file, 'w')
        file_content = f.write(jsonContent)
        f.close()


if __name__ == '__main__':           
    file_path = "/home/titi/NetBeansProjects/AssistanceMeteoCustomerFront/data/europe.geojson"
    output_file = "/var/www/assistance-meteo/html/public/js/jquery.vmap.qgis.js"
    creator = MapCreator(output_file = output_file, id_col_name="FIPS_CNTRY", name_col_name="CNTRY_NAME", flip_horizontally=True)
    #output_file = "/home/bb/NetBeansProjects/AssistanceMeteoCustomerFront/public/js/jquery.vmap.qgis.js"
    creator.execute(file_path)
