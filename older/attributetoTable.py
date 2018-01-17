# Name: alltablestoExcel.py

# autor: Tomás iglesias
# mail: tomas.iglesias@qpexploration.com

import arcpy

# Set environment settings
arcpy.env.workspace = "X:/daniel.scott/data_2_merge/Attribute Tables.gdb"

featclassList = arcpy.ListFeatureClasses()

for fc in featclassList:
    # Set local variables
    in_table = fc
    out_xls = "X:/daniel.scott/data_2_merge/" + fc + ".xls"
    # Execute TableToExcel
    arcpy.TableToExcel_conversion(in_table, out_xls)
