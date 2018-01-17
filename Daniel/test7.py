import arcpy, time, os, sys, csv, string

# Get a list of datasets owned by the admin user
workspace = r'C:\Users\daniel.scott\Desktop\DataOwner\Dataowner@SRV-SQLHA02@DVC.sde'
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

def write_log(text,file):
    f = open(file,'a')  #a appends to an existing file if it exists
    f.write("{}\n".format(text)) #write the text to the logfile and move to the next line
    return
indexlog = 'C:\Users\daniel.scott\Desktop\CompressLog.txt' #name of log file

# Rebuild indexes and analyze the states and states_lineages system tables
datasetlist = arcpy.ListDatasets("", "Feature")
analysels = []
for dataset in datasetlist:
    write_log("-----------------------------------------------------------", indexlog)
    write_log("starting to rebuild indexes for " + dataset, indexlog)
    fclist = arcpy.ListFeatureClasses("*", "", dataset)
    for fc in fclist:
        analysels.append(fc)
        #arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataset, "ALL")
        write_log("Indexes rebuilt for {0}".format(fc), indexlog)
    write_log("-----------------------------------------------------------", indexlog)
write_log("Indexing complete",indexlog)
write_log("-----------------------------------------------------------",indexlog)
# Reset geoprocessing environment settings
arcpy.ResetEnvironments()

# Reset a specific environment setting
arcpy.ClearEnvironment("workspace")

def write_log(text,file):
    f = open(file,'a')  #a appends to an existing file if it exists
    f.write("{}\n".format(text)) #write the text to the logfile and move to the next line
    return
# Get a list of datasets owned by the admin user
workspace = r'C:\Users\daniel.scott\Desktop\SDE\SDE@SRV-SQLHA02@CL_DVC.sde'
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

Analyselog = 'C:\Users\daniel.scott\Desktop\CompressLog.txt' #name of log file
write_log("Starting to analyse feature classes", Analyselog)
for fc in analysels:
    write_log("Analysing {0}".format(fc), Analyselog)
    arcpy.AnalyzeDatasets_management(workspace, "SYSTEM",fc, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
write_log("Completed analysing", Analyselog)

# Reset geoprocessing environment settings
arcpy.ResetEnvironments()

# Reset a specific environment setting
arcpy.ClearEnvironment("workspace")