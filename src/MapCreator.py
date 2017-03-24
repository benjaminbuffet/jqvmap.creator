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
    flip_horizontally = False
    size = None
    map_name = ""

    def __init__(self, max_width = 500, max_height = 500, id_col_name = "ID", name_col_name = "NAME", flip_horizontally = False, map_name = "") :
        self.id_col_name = id_col_name
        self.name_col_name = name_col_name        
        self.max_width = max_width
        self.max_height = max_height
        self.flip_horizontally = flip_horizontally
        self.map_name = map_name

    def init_base_map(self, input_map_file):
        f = open(input_map_file, 'r')
        file_content = f.read()
        f.close()
        geo_json = json.loads(file_content)
        self.size = self._calc_size(geo_json)

    def convert_map(self, input_map_file, output_map_file):
        f = open(input_map_file, 'r')
        file_content = f.read()
        f.close()
        geo_json = json.loads(file_content)       
        canvas = self.convert_to_canvas(geo_json)
        self.writeJsonFile(canvas, output_map_file, prefix="jQuery.fn.vectorMap('addMap', '"+ self.map_name +"', ", suffix=");")

    def convert_marker(self, input_marker_file, output_marker_file):
        f = open(input_marker_file, 'r')
        file_content = f.read()
        f.close()
        geo_json = json.loads(file_content)           
        basic_json = self.convert_to_basic_json(geo_json)
        self.writeJsonFile(basic_json, output_marker_file)
    
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
    
    def convert_to_canvas(self, geo_json):
        canvas = {"width": self.size["image_width_px"], "height": self.size["image_height_px"], "paths":{}}
        for elt in geo_json["features"]:
            id = elt["properties"][self.id_col_name]
            name = elt["properties"][self.name_col_name]
            canvas["paths"][id] = {
                "path":self.convert_to_canvas_path(elt["geometry"]),
                "name":name}
        return canvas

    def convert_to_canvas_path(self, geometry):
        geometry_service = self.geometry_factory.get(geometry["type"])
        return geometry_service.to_canvas(geometry["coordinates"], self.size, self.flip_horizontally)

    def convert_to_basic_json(self, geo_json):
        basic_json = {self.map_name : []}
        for elt in geo_json["features"]:
            geometry = elt["geometry"]
            if geometry["type"] == "Point":                
                geometry_service = self.geometry_factory.get(geometry["type"])
                xy = geometry_service.convert_single_coordinates(geometry["coordinates"], self.size, self.flip_horizontally)
                basic_json[self.map_name].append(elt["properties"])
                basic_json[self.map_name][-1]["x"] = xy[0]
                basic_json[self.map_name][-1]["y"] = xy[1]
        return basic_json

    def writeJsonFile(self, canvas, output_file, prefix = "", suffix = ""):
        json_content = prefix + json.dumps(canvas) + suffix
        f = open(output_file, 'w')
        f.write(json_content)
        f.close()


if __name__ == '__main__':           
    input_map_file = "/home/bb/NetBeansProjects/AssistanceMeteoCustomerFront/data/france.geojson"
    input_marker_file = "/home/bb/NetBeansProjects/AssistanceMeteoCustomerFront/data/france.marker.city.geojson"
    output_map_file = "/var/www/assistance-meteo/html/public/js/jquery.vmap.qgis.js"
    output_marker_file = "/var/www/assistance-meteo/html/data/poi/poi-0.json"

    creator = MapCreator(id_col_name="code_insee", name_col_name="nom", flip_horizontally=True, map_name="france_fr")
    
    creator.init_base_map(input_map_file)
    creator.convert_map(input_map_file, output_map_file)
    creator.convert_marker(input_marker_file, output_marker_file)
