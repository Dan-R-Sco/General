# -*- coding: utf-8 -*-
import arcpy

arcpy.AddToolbox("C:/Program Files (x86)/DataEast/XTools Pro/Toolbox/XTools Pro.tbx")

arcpy.XToolsGP_CreateRandomSamplingPoints("#","443411.478917272 7444278.59767323 511098.432642961 7465590.76076364","#","#","CONSTANT","TOTAL","10","#","CONSTANT","1 Meters","#","Unknown")
