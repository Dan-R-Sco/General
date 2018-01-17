import arcpy, sys, os

arcpy.env.workspace = arcpy.GetParameterAsText(0)
workspace = arcpy.env.workspace
dsname = arcpy.GetParameterAsText(1)
fcs = arcpy.ListFeatureClasses("*","",dsname)
prjcode = arcpy.GetParameterAsText(2)
oldcode = arcpy.GetParameterAsText(3)
arcpy.AddMessage("Listing FCs in dataset: ")
for fc in fcs:
    if oldcode in fc:
        continue
    else:
        arcpy.AddMessage(fc)
        newname = fc.replace(prjcode,oldcode)
        arcpy.AddMessage("Renaming fc {0} to {1})".format(fc,newname))
        arcpy.Rename_management(fc,newname)

for fc in fcs:
    if fc.endswith("_1"):
        removeone = fc.replace('_1', "")
        arcpy.AddMessage("Removing _1 from {0})".format(fc))
        arcpy.Rename_management(fc, removeone)
    else:
        continue

arcpy.RegisterAsVersioned_management(dsname, "NO_EDITS_TO_BASE")