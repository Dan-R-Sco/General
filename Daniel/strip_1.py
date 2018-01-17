import arcpy

arcpy.env.workspace = r'Database Connections\Dataowner@SRV-SQLHA02@DVC.sde'
fclist = arcpy.ListFeatureClasses("_1","",'W1709')
for fc in fclist:
    print fc
    fcstripped = fc.rstrip('_1')
    name = "CL_DVC.OWD." + fcstripped
    print name
    arcpy.Rename_management(fc,name)