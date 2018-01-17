# Name: Maintenance.py
# Description: This script will reconcile, post and compress an
#              enterprise geodatabase. It will then rebuild indexes
#              and gather statistics on the data in the geodatabase.

# Author: Esri

# Import the required modules
import arcpy, smtplib, sys

try:
    # Set an admin connection variable.
    adminConn = 'Database Connections/admin2.sde'

    # Set a few environment variables
    arcpy.env.workspace = adminConn
    arcpy.env.overwriteOutput = True

    # For demo purposes we will block connections to the geodatabase during schema rec/post/compress.
    arcpy.AcceptConnections(adminConn, False)

    # Disconnect any connected users.
    arcpy.DisconnectUser(adminConn, 'ALL')

    # Get a list of versions to pass into the ReconcileVersions tool.
    # Only reconcile versions that are children of Default
    verList = arcpy.da.ListVersions(adminConn)
    versionList = [ver.name for ver in verList if ver.parentVersionName == 'sde.DEFAULT']

    # Execute the ReconcileVersions tool.
    try:
        arcpy.ReconcileVersions_management(adminConn, "ALL_VERSIONS", "sde.DEFAULT",
                                           versionList,"LOCK_ACQUIRED", "NO_ABORT",
                                           "BY_OBJECT", "FAVOR_TARGET_VERSION","POST",
                                           "KEEP_VERSION", sys.path[0] + "/reclog.txt")
        recMsg = 'Reconcile and post executed successfully.\n\r'
        recMsg += 'Reconcile Log is below.\n' #warning this can be very long.
        recMsg += open(sys.path[0] + "/reclog.txt", 'r').read()
    except:
        recMsg = 'Reconcile & post failed. Error message below.\n\r' + arcpy.GetMessages()

    # Run the compress tool.
    try:
        arcpy.Compress_management(adminConn)
        #if the compress is successful add a message.
        compressMsg = '\nCompress was successful.\n\r'
    except:
        #If the compress failed, add a message.
        compressMsg = '\nCompress failed: error message below.\n\r' + arcpy.GetMessages()

    # Allow connections again.
    arcpy.AcceptConnections(adminConn, True)

    #Get a list of datasets owned by the admin user

    # Get the user name for the workspace
    # this assumes you are using database authentication.
    # OS authentication connection files do not have a 'user' property.
    ownerConn = 'C:/presentations/DevSummit2013/Owner.sde'
    desc = arcpy.Describe(ownerConn)
    connProps = desc.connectionProperties
    userName = connProps.user

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters.
    dataList = arcpy.ListTables('*.' + userName + '.*') \
             + arcpy.ListFeatureClasses('*.' + userName + '.*') \
             + arcpy.ListRasters('*.' + userName + '.*')

    # Next, for feature datasets get all of the featureclasses
    # from the list and add them to the master list.
    for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
        dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)

    # Pass in the list of datasets owned by the admin to the rebuild indexes and
    # analyze datasets tools.
    # Note: to use the "SYSTEM" option the user must be an administrator.
    try:
        arcpy.RebuildIndexes_management(ownerConn, "NO_SYSTEM", dataList, "ALL")
        rebuildMsg = 'Rebuilding of indexes successful.\n\r'
    except:
        rebuildMsg = 'Rebuild Indexes failed: error message below.\n\r' + arcpy.GetMessages()

    try:
        arcpy.AnalyzeDatasets_management(ownerConn, "NO_SYSTEM", dataList,"ANALYZE_BASE",
                                         "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
        analyzeMsg = 'Analyzing of datasets successful.\n\r'
    except:
        analyzeMsg = 'Analyze Datasets failed: error message below.\n\r' + arcpy.GetMessages()

    #Set a flag to indicate that the script has finished executing its required tasks.
    scriptSuccess = True

except:
    import traceback
    scriptSuccess = False
    failMsg = '\n**SCRIPT FAILURE**\n'
    failMsg += 'Most recent GP messages below.\n'
    failMsg += arcpy.GetMessages() +'\n'
    failMsg += '\nTraceback messages below.\n'
    failMsg += traceback.format_exc().splitlines()[-1]

# Email function for sending emails.
def sendEmail(subject, emailmessage):
        # take the email list and use it to send an email to connected users.
        SERVER = "esrimail.esri.com"
        FROM = "Python Admin <rbrennan@esri.com>"
        TO = 'rbrennan@esri.com'
        SUBJECT = subject
        MSG = emailmessage

        # Prepare actual message
        MESSAGE = """\
From: %s
To: %s
Subject: %s

%s
        """ % (FROM, TO, SUBJECT, MSG)
        #Connect to the server
        server = smtplib.SMTP(SERVER)
        # Send the mail
        server.sendmail(FROM, TO, MESSAGE)
        #Disconnect from the server.
        server.quit()
        #multiple examples for sending emails.
        #http://docs.python.org/library/email-examples.html#email-examples

#Send a summary using the send email function and the messages that have been created.
if scriptSuccess == True:
    subject = 'Geodatabase maintenance script summary.'
    msg = recMsg + compressMsg + rebuildMsg + analyzeMsg
else:
    subject = 'Geodatabase maintenance script failed.'
    msg = failMsg

sendEmail(subject, msg)
