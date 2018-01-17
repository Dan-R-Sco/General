# Import system modules
import arcpy

connect = 'C:\Users\daniel.scott\AppData\Roaming\ESRI\Desktop10.4\ArcCatalog\Dataowner@SRV-SQLHA02@CL_Vector.sde'
connection = r"'" + connect + "'"
queryname = "'query10'"
projcode = 'CL_V01'
projectcode = "'" + projcode + "'"
print connection
print projectcode
fc = 'CL_Vector.OWD.QRY_ACQ_GEOCHRONOLOGY'
print queryname
print "{0} + {1}".format(fc,projectcode)
query = '"select * from {0} where PROJECTCODE = {1}"'.format(fc,projectcode)
print query