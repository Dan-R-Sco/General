#renaming dataset and then FCs
import arcpy

arcpy.env.workspace = r'Database Connections\Dataowner@SRV-SQLHA02@DVC.sde'
currentname = 'PCDConditions_E200_1' #may need to add quotes to string
newname = 'PCDLowRes_E200' #may need to add quotes to string
arcpy.Rename_management(currentname,newname)
fclist = arcpy.ListFeatureClasses("","",'newname') #may need to add quotes to string
for fc in fclist:
    if fc.endswith("_1"):
        newname = fc.replace('_1', "")
        arcpy.Rename_management(fc, newname)
else:
    pass

arcpy.env.workspace = r'Database Connections\admin_ndp@srv-sql03@egdtesting.sde'
lstDatasets = arcpy.ListDatasets("*")
oldnme = "PCDConditions_E200_1"
newname = "PCDConditionsLR"
for dataset in lstDatasets:
    if dataset == oldnme:
        arcpy.Rename_management(dataset,newname,data_type=DEFeatureDataset)
        lstFCs = arcpy.ListFeatureClasses("_1", "", dataset)
        for fc in lstFCs:
            if fc.endswith("_1"):
                newname = fc.replace('_1', "")
                arcpy.Rename_management(fc, newname)

import arcpy
from arcpy import env

env.workspace = r'Database Connections\admin_ndp@srv-sql03@egdtesting.sde'

lstDatasets = arcpy.ListDatasets("*")
for dataset in lstDatasets:
    lstFCs = arcpy.ListFeatureClasses("road_*", "", dataset)
    for fc in lstFCs:
        oldName = str(fc)
        newName = oldName.replace("road", "RD")
        newName = newName.replace("ns", "_NS12_13")
        arcpy.Rename_management(fc, newName)