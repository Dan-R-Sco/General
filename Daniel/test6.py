import arcpy, time, os, sys, csv, string

# Set the workspace
arcpy.env.workspace = r'C:\Scripts_2016\Dans_Scripts\Connection\SDE@SRV-SQLHA02@CL_DVC.sde'

# Set a variable for the workspace
workspace = arcpy.env.workspace

connection = r'C:\Scripts_2016\Dans_Scripts\Connection\SDE@SRV-SQLHA02@CL_DVC.sde'

# Set the date.
Date = time.strftime("%m-%d-%Y", time.localtime())

# Set the time.
Time = time.strftime("%I:%M:%S %p", time.localtime())

# Create a text file for logging
log = open("C:\Scripts_2016\Dans_Scripts\Log\CompressLog.txt", "a")
log.write("***********************************************************\n")

# Block new connections to the database.
#arcpy.AcceptConnections(connection, False) #removed due to not working the accept

# Disconnect all users from the database.
#arcpy.DisconnectUser(connection, "ALL")

# Get a list of versions to pass into the ReconcileVersions tool.
versionList = arcpy.ListVersions(connection)

# Execute the ReconcileVersions tool.
reconcileLog = r"C:\Scripts_2016\Dans_Scripts\Log\ReconcileLog" + Date+ ".txt"
arcpy.ReconcileVersions_management(connection, "ALL_VERSIONS", "sde.QA", versionList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION", reconcileLog)
#open rec file
with open (reconcileLog,'r') as RECFL:
    #iterate lines in rec file
    for line in RECFL:
        #write line to log file
        log.write (line)
#close rec file
RECFL.close()

#Compress
compresslog = 'C:\Scripts_2016\Dans_Scripts\Log\CompressLog.txt'
# Run the compress tool.
arcpy.Compress_management(connection)
#add messages of compress to log file
f = open(compresslog, 'a')
log.write("\n" + "-----------------------------------------------------------" + "\n" + arcpy.GetMessages() + "\n" + "Compressed database DVC ")
log.close()

# Allow the database to begin accepting connections again
arcpy.AcceptConnections(connection, True)

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
for dataset in datasetlist:
    write_log("-----------------------------------------------------------", indexlog)
    write_log("starting to rebuild indexes for " + dataset, indexlog)
    fclist = arcpy.ListFeatureClasses("*", "", dataset)
    for fc in fclist:
        arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataset, "ALL")
        write_log("Indexes rebuilt for {0}".format(fc), indexlog)


#arcpy.AnalyzeDatasets_management(workspace, "SYSTEM","", "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
