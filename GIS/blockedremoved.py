#===================   ========  =======================================================================================  ==========
                    #EGDB maintenance script
#Author: Daniel Scott
#one script to rule them all

#currently not catching errors for analyse and indexes see 50:00 in https://www.youtube.com/watch?v=pQpBXDOQU3s add the library for O365 and email
#===================   ========  =======================================================================================  ==========

import arcpy, time, os, sys, csv, string, O365

#===================   ========  =======================================================================================  ==========
                    ##Variables##
def write_log(text,file):
    f = open(file,'a')  #a appends to an existing file if it exists
    f.write("{}\n".format(text)) #write the text to the logfile and move to the next line
    return

log = r"C:\Users\daniel.scott\Desktop\MAINTENANCE.txt"

# Set the date.
Date = time.strftime("%m-%d-%Y", time.localtime())

# Set the time.
Time = time.strftime("%I:%M:%S %p", time.localtime())

try:
    log = r"C:\Users\daniel.scott\Desktop\MAINTENANCE.txt"
    # Set an gdb admin connection variable.
    adminConn = r'C:\Users\daniel.scott\AppData\Roaming\ESRI\Desktop10.4\ArcCatalog\SDE@SRV-SQLHA02@CL_DVC.sde'
    print("Connecting to the geodatabase as the gdb admin user (sde)")
    write_log("Connecting to the geodatabase as the gdb admin user (sde)",log)

    # Set a few environment variables
    arcpy.env.workspace = adminConn
    arcpy.env.overwriteOutput = True

    # block connections to the geodatabase during schema rec/post/compress.
    print("The database is no longer accepting connections")
    write_log("The database is no longer accepting connections", log)
    #arcpy.AcceptConnections(adminConn, False)

    #Disconnect all users
    print("Disconnecting all users")
    write_log("Disconnecting all users", log)
    #arcpy.DisconnectUser(adminConn, 'ALL')

    #Reconcile
    # Get a list of versions to pass into the ReconcileVersions tool.
    try:
        log = r"C:\Users\daniel.scott\Desktop\MAINTENANCE.txt"
        versionList = arcpy.ListVersions(adminConn)
        arcpy.ReconcileVersions_management(adminConn, "ALL_VERSIONS", "sde.QA", versionList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION", log)

        recMsg = 'Reconcile and post executed successfully.\n\r'
        recMsg += 'Reconcile Log is below.\n' #warning this can be very long.
        recMsg += open(log, 'r').read()
    except:
        log = r"C:\Users\daniel.scott\Desktop\MAINTENANCE.txt"
        recMsg = 'Reconcile & post failed. Error message below.\n\r' + arcpy.GetMessages()

    #Run compress
    try:
        log = r"C:\Users\daniel.scott\Desktop\MAINTENANCE.txt"
        print("Running compress")
        write_log("Running compress",log)
        arcpy.Compress_management(adminConn)
        # if the compress is successful add a message.
        compressMsg = '\nCompress was successful.\n\r'
        write_log(compressMsg, log)
    except:
        log = r"C:\Users\daniel.scott\Desktop\MAINTENANCE.txt"
        # If the compress failed, add a message.
        compressMsg = '\nCompress failed: error message below.\n\r' + arcpy.GetMessages()
        write_log(compressMsg,log)

    # Update statistics and indexes for the system tables
    try:
        log = r"C:\Users\daniel.scott\Desktop\MAINTENANCE.txt"
        print("Rebuilding indexes on the system tables")
        write_log("Rebuilding indexes on the system tables",log)
        arcpy.RebuildIndexes_management(adminConn, "SYSTEM")
        rebuildSystemMsg = 'Rebuilding of system table indexes successful.\n\r'
        write_log(rebuildSystemMsg,log)
    except:
        log = r"C:\Users\daniel.scott\Desktop\MAINTENANCE.txt"
        rebuildSystemMsg = 'Rebuild indexes on system tables fail: error message below.\n\r' + arcpy.GetMessages()
        write_log(rebuildSystemMsg, log)

    try:
        log = r"C:\Users\daniel.scott\Desktop\MAINTENANCE.txt"
        print("Updating statistics on the system tables")
        write_log("Updating statistics on the system tables",log)
        arcpy.AnalyzeDatasets_management(adminConn, "SYSTEM")
        analyzeSystemMsg = 'Analyzing of system tables successful.\n\r'
        write_log(analyzeSystemMsg,log)
    except:
        log = r"C:\Users\daniel.scott\Desktop\MAINTENANCE.txt"
        analyzeSystemMsg = 'Analyze system tables failed: error message below.\n\r' + arcpy.GetMessages()
        write_log(analyzeSystemMsg,log)

    try:
        log = r"C:\Users\daniel.scott\Desktop\MAINTENANCE.txt"
        # Allow connections again.
        print("Allow users to connect to the database again")
        write_log("Allow users to connect to the database again",log)
        arcpy.AcceptConnections(adminConn, True)
        print("Finshed gdb admin user (sde) tasks \n")
        write_log("Finished gdb admin user (sde) tasks", log)
    except:
        log = r"C:\Users\daniel.scott\Desktop\MAINTENANCE.txt"
        write_log("Unable to finish gdb admin user (sde) tasks", log)

    #####Starting dataowner admin########
    # Get a list of datasets owned by the gdb user
    print("Connecting to the geodatabase as the data owner (gdb)")
    log = r"C:\Users\daniel.scott\Desktop\MAINTENANCE.txt"
    write_log("Connecting to the geodatabase as the data owner (gdb)",log)
    # Get the user name for the workspace
    # this assumes you are using database authentication.
    # OS authentication connection files do not have a 'user' property.
    ownerConn = r'C:\Users\daniel.scott\AppData\Roaming\ESRI\Desktop10.4\ArcCatalog\Dataowner@SRV-SQLHA02@DVC.sde'
    print("Using Describe function to get the connected user name property from the connection file")
    write_log("Using Describe function to get the connected user name property from the connection file",log)
    desc = arcpy.Describe(ownerConn)
    connProps = desc.connectionProperties
    userName = connProps.user
    print("Connected as user {0}".format(userName))

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables and feature classes.
    print("Compiling a list of data owned by the {0} user".format(userName))
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*')
    dataList = arcpy.ListDatasets()
    # Next, for feature datasets get all of the featureclasses
    # from the list and add them to the master list.
    analysels = []
    for dataset in arcpy.ListDatasets():
        write_log(dataset,log)
        fclist = arcpy.ListFeatureClasses()
        for fc in fclist:
            try:
                analysels.append(fc)
                write_log("Rebuilding indexes on the data, as the data owner" + fc + " ", log)
                print("Rebuilding indexes on the data, as the data owner")
                arcpy.RebuildIndexes_management(ownerConn, "NO_SYSTEM", dataset, "ALL")
                write_log("Indexes rebuilt for {0}".format(fc), log)
                rebuildUserMsg = 'Rebuilding of user data indexes successful.\n\r'
                write_log(rebuildUserMsg, log)
            except:
                rebuildUserMsg = 'Rebuild user data indexes failed: error message below.\n\r' + arcpy.GetMessages()
                write_log(rebuildUserMsg, log)

    write_log("Indexing complete at {0}".format(Time), indexlog)

    try:

        print("Updating statistics on the data, as the data owner")
        write_log("Updating statistics on the data, as the data owner",log)
        arcpy.AnalyzeDatasets_management(adminConn, "NO_SYSTEM", dataList, "ANALYZE_BASE","ANALYZE_DELTA", "ANALYZE_ARCHIVE")
        analyzeUserMsg = 'Analyzing of user datasets successful.\n\r'
        write_log(analyzeUserMsg,log)
    except:
        analyzeUserMsg = 'Analyze user datasets failed: error message below.\n\r' + arcpy.GetMessages()
        write_log(analyzeUserMsg, log)

    print("Finished data owner (gdb) tasks \n")
    write_log("Finished data owner (gdb) tasks \n", log)

    #Set a flag to indicate that the script has finished executing its required tasks.
    scriptSuccess = True

except:
    import traceback

    scriptSuccess = False
    failMsg = '\n**SCRIPT FAILURE**\n'
    write_log(failMsg,log)
    failMsg += 'Most recent GP messages below.\n'
    write_log(failMsg, log)
    failMsg += arcpy.GetMessages() + '\n'
    write_log(failMsg, log)
    failMsg += '\nTraceback messages below.\n'
    write_log(failMsg, log)
    failMsg += traceback.format_exc().splitlines()[-1]
    write_log(failMsg, log)

#send email
from O365 import Message
authentication = ('daniel.scott@qpexploration.com','QPX123!!')

#Send a summary using the send email function and the messages that have been created.
if scriptSuccess == True:
    authentication = ('daniel.scott@qpexploration.com', 'QPX123!!')
    m = Message(auth=authenticiation)
    m.setRecipients('daniel.scott@qpexploration.com')
    m.setSubject = 'Geodatabase maintenance script summary.'
    m.setBody = recMsg + compressMsg + rebuildSystemMsg + analyzeSystemMsg +rebuildUserMsg + analyzeUserMsg
    write_log("Sending email report", log)
    m.sendMessage()
else:
    authentication = ('daniel.scott@qpexploration.com', 'QPX123!!')
    m= Message()
    m = Message(auth=authenticiation)
    m.setRecipients('daniel.scott@qpexploration.com')
    m.setSubject = 'Geodatabase maintenance script failed.'
    m.setBody = failMsg
    write_log("Sending email report",log)
    m.sendMessage()

print("Done.")
write_log("Maintenance completed for {0} at {1}".format(Date,Time),log)
