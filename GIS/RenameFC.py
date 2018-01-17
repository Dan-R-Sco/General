#script to rename fcs in a template dataset to remove the _1's

import arcpy

arcpy.env.workspace = r'Database Connections\Dataowner@SRV-SQLHA02@DVC.sde'
datasetlist = arcpy.ListDatasets()
datasetname = "PCDConditions_E200_1"
newdatasetname = "PCDConditionsLR"
if dataset in datasetlist == datasetname :
    arcpy.Rename_management(datasetname, newdatasetname)
    fclist = arcpy.ListFeatureClasses("","")
    for fc in fclist:
        if fc.endswith("_1"):
            newname = fc.replace('_1',"")
            arcpy.Rename_management(fc, newname)
        else:
            pass