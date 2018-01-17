import arcpy

arcpy.env.workspace = r'Database Connections\Dataowner@SRV-SQLHA02@DVC.sde'
arcpy.Rename_management('W1902','W1709')
fclist = arcpy.ListFeatureClasses("","",'W1709')
for fc in fclist:
    print fc
    fcstripped = fc.lstrip('CL_DVC.OWD.')
    print fcstripped
    name = "CL_DVC.OWD.W1709_" + fcstripped
    print name
    arcpy.Rename_management(fc, name)