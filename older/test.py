import time, arcpy, arceditor

#block new connections to the database.
arcpy.AcceptConnections('Database Connections/Daniel@10.70.2.155.NDP_EGDB_20170105A.sde', False)

# wait 3 seconds
time.sleep(0.1)

# Disconnect all users from the database.
arcpy.DisconnectUser('Database Connections/Daniel@10.70.2.155.NDP_EGDB_20170105A.sde', "ALL")

# Get a list of versions to pass into the ReconcileVersions tool.
versionList = arcpy.ListVersions('Database Connections/Daniel@10.70.2.155.NDP_EGDB_20170105A.sde')

# Execute the ReconcileVersions tool.
arcpy.ReconcileVersions_management('Database Connections/Daniel@10.70.2.155.NDP_EGDB_20170105A.sde', "ALL_VERSIONS", "sde.DEFAULT", versionList, "LOCK_ACQUIRED", "ABORT_CONFLICTS", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION", r"C:/Users/daniel.scott/Desktop/log.txt")

# Run the compress tool. 
arcpy.Compress_management('Database Connections/Daniel@10.70.2.155.NDP_EGDB_20170105A.sde')

#Allow the database to begin accepting connections again
arcpy.AcceptConnections('Database Connections/Daniel@10.70.2.155.NDP_EGDB_20170105A.sde', True)

# Get Messages
ScriptMessages = arcpy.GetMessages()

#Get a list of datasets owned by the admin user
workspace = arcpy.env.workspace('Daniel@10.70.2.155.NDP_EGDB_20170105A.sde')
dataList = arcpy.ListTables() + arcpy.ListFeatureClasses() + arcpy.ListRasters()
for dataset in arcpy.ListDatasets("", "Feature"):
    arcpy.env.workspace = os.path.join(workspace,dataset)
    dataList += arcpy.ListFeatureClasses() + arcpy.ListDatasets()

# reset the workspace
arcpy.env.workspace = workspace

# Get the user name for the workspace
userName = arcpy.Describe(workspace).connectionProperties.user.lower()

# remove any datasets that are not owned by the connected user.
userDataList = [ds for ds in dataList if ds.lower().find(".%s." % userName) > -1]

# Execute rebuild indexes
# Note: to use the "SYSTEM" option the workspace user must be an administrator.
arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", userDataList, "ALL")
print('Rebuild Complete')

arcpy.AnalyzeDatasets_management(workspace, "SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
print ('Analyze dataset')