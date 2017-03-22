#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from geometry.Polygon import Polygon
from geometry.MultiPolygon import MultiPolygon

class GeometryFactory:
    def get(self, geometry_name):
        return {
        'Polygon': Polygon(),
        'MultiPolygon': MultiPolygon(),
    }[geometry_name]