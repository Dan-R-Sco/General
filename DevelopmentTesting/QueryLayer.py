# Name: MakeQueryLayer.py
# Description: Creates an output query layer based on a where clause.
#   This example shows how to create a spatial reference object using the
#   name of a coordinate system. It also demonstrates how to use two fields
#   to generate a dynamic unique row identifier for the query layer.


# Import system modules
import arcpy

connect = arcpy.GetParameterAsText(0)
connection = r"'" + connect + "'"
queryname = arcpy.GetParameterAsText(1)
queryname1 = "'" + queryname + "'"
projcode = arcpy.GetParameterAsText(2)
projectcode = "'" + projcode + "'"
print projectcode
fc = 'CL_Vector.OWD.QRY_ACQ_GEOCHRONOLOGY'
print queryname
print "{0} + {1}".format(fc,projectcode)
query = '"select * from {0} where PROJECTCODE = {1}"'.format(fc,projectcode)
print query

# Run the tool
try:
    arcpy.MakeQueryLayer_management(connection, queryname1, query, oid_fields="OBJECTID", shape_type="POINT", srid="32719", spatial_reference="PROJCS['WGS_1984_UTM_Zone_19S',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',10000000.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]];-5120900 1900 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision")

except:
    print connection
    print queryname1
    print query