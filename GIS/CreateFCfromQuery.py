
import arcpy, sys, os
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r'Database Connections\Dataowner@SRV-SQLHA02@CL_Vector.sde\AcQuire'
viewtable = "C:\Program Files (x86)\ArcGIS\Desktop10.4"
prjcode = arcpy.GetParameterAsText(0)
outloc = arcpy.GetParameterAsText(1)

infc = 'CL_Vector.OWD.ALTERATION_CONSENSUS'

clause = "PROJECTCODE = " + "'{0}'".format(prjcode)
#make query table
qrytable = arcpy.MakeFeatureLayer_management(infc, viewtable, where_clause=clause)
outFC = prjcode + "_AlterationConsensus"
#copy features tool
arcpy.CopyFeatures_management(qrytable, outloc + "\\" + outFC)

#add global ids
fc = outloc + "\\" + outFC

fields = arcpy.ListFields(fc,"","GlobalID")
if "GlobalID" in fields:
    pass
else:
    arcpy.AddGlobalIDs_management(outloc + "\\" + outFC)

fields = ["Fresh_Final_Score",
         "Potassic_Final_Score",
         "Chloritic_Final_Score",
         "Chl-Ep_Final_Score",
         "Qz-Ser_Final_Score",
         "Argillic_Final_Score",
         "AAA_Alu_Final_Score",
         "AAA_Dick_Final_Score",
         "AAA_Pyr_Final_Score",
         "Phyllic_Final_Score",
         "Propylitic_Final_Score",
         "Final_Alteration",
         "Completeness",
         "Coherence_Fresh",
         "Coherence_Potassic",
         "Coherence_Chloritic",
         "Coherence_Qt-Ser",
         "Coherence_Chl-Ep",
         "Coherence_Argillic",
         "Coherence_AAA_Alu",
         "Coherence_AAA_Dick",
         "Coherence_AAA_Pyr",
         "Coherence_Phyllic",
         "Coherence_Propylitic",
         "Final Flag Status"]

for field in fields:
    if field not in arcpy.ListFields(fc):
        arcpy.AddField_management(fc,field,field_type = "TEXT",field_precision = 5, field_scale = 4, field_length = 70)