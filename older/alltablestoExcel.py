# Name: alltablestoExcel.py

# autor: Tomás iglesias
# mail: tomas.iglesias@qpexploration.com

import arcpy

# Set environment settings
arcpy.env.workspace = "W:/tomas.iglesias/Documents/Visualization Tool/Materials for PopUp/E200attributeTable/Attribute Tables Access.mdb"

featclassList = arcpy.ListFeatureClasses()

for fc in featclassList:
    # Set local variables
    in_table = fc
    out_xls = "W:/tomas.iglesias/Documents/Visualization Tool/Materials for PopUp/E200attributeTable/xls/" + fc + ".xls"
    # Execute TableToExcel
    arcpy.TableToExcel_conversion(in_table, out_xls)
