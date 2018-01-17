import arcpy, time, smtplib

# Set the workspace 
arcpy.env.workspace = 'C:\Users\daniel.scott\Desktop\SDE\SDE@SRV-SQLHA02@CL_DVC.sde'

# Set a variable for the workspace
workspace = arcpy.env.workspace

# Get a list of connected users.
#userList = arcpy.ListUsers("'C:\Users\daniel.scott\Desktop\SDE\SDE@SRV-SQLHA02@CL_DVC.sde'")

# Get a list of user names of users currently connected and make email addresses
emailList = 'Daniel.scott@qpexploration.com'#[user.Name + "@yourcompany.com" for user in arcpy.ListUsers("Database Connections/admin.sde")]

# Take the email list and use it to send an email to connected users.
SERVER = "srv-smtp01"
FROM = "Daniel <daniel.scott@qpexploration.com>"
TO = emailList
SUBJECT = "Maintenance is about to be performed"
MSG = "Auto generated Message.\n\rServer maintenance will be performed in 15 minutes. Please log off."

# Prepare actual message
MESSAGE = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, MSG)

# Send the mail
server = smtplib.SMTP(SERVER)
server.sendmail(FROM, TO, MESSAGE)
server.quit()

# Block new connections to the database.
#arcpy.AcceptConnections('C:\Users\daniel.scott\Desktop\SDE\SDE@SRV-SQLHA02@CL_DVC.sde', True)

# Wait 15 minutes
#time.sleep(900)

# Disconnect all users from the database.
#arcpy.DisconnectUser('Database Connections/admin.sde', "ALL")

# Get a list of versions to pass into the ReconcileVersions tool.
versionList = arcpy.ListVersions('C:\Users\daniel.scott\Desktop\SDE\SDE@SRV-SQLHA02@CL_DVC.sde')
print versionList
# Execute the ReconcileVersions tool.
print "Reconciling"
arcpy.ReconcileVersions_management('C:\Users\daniel.scott\Desktop\SDE\SDE@SRV-SQLHA02@CL_DVC.sde', "ALL_VERSIONS", "sde.DEFAULT", versionList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION", "c:/temp/reconcilelog.txt")
# Run the compress tool. 
print "compressing"
arcpy.Compress_management('C:\Users\daniel.scott\Desktop\SDE\SDE@SRV-SQLHA02@CL_DVC.sde')
# Allow the database to begin accepting connections again
arcpy.AcceptConnections('C:\Users\daniel.scott\Desktop\SDE\SDE@SRV-SQLHA02@CL_DVC.sde', True)

# Get a list of datasets owned by the admin user
print "rebuilding indexes"
# Rebuild indexes and analyze the states and states_lineages system tables
arcpy.RebuildIndexes_management(workspace, "SYSTEM", "ALL")
print "analysing datasets"
arcpy.AnalyzeDatasets_management(workspace, "SYSTEM", "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")