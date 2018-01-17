# ===================   ========  =======================================================================================  ==========
# EGDB maintenance script
# Author: Daniel Scott
# one script to rule them all

# currently not catching errors for analyse and indexes see 50:00 in https://www.youtube.com/watch?v=pQpBXDOQU3s add the library for O365 and email
# ===================   ========  =======================================================================================  ==========

import arcpy, time, os, sys, csv, string


def write_log(text, file):
    f = open(file, 'a')  # a appends to an existing file if it exists
    f.write("{}\n".format(text))  # write the text to the logfile and move to the next line
    return

# ===================   ========  =======================================================================================  ==========
##RECONCILE##
try:
    # Set the workspace
    arcpy.env.workspace = r'C:\Scripts_2016\Dans_Scripts\Connection\SDE@SRV-SQLHA02@CL_DVC.sde'

    # Set a variable for the workspace
    workspace = arcpy.env.workspace

    SDEconnection = r'C:\Scripts_2016\Dans_Scripts\Connection\SDE@SRV-SQLHA02@CL_DVC.sde'

    # Set the date.
    Date = time.strftime("%m-%d-%Y", time.localtime())

    # Set the time.
    Time = time.strftime("%I:%M:%S %p", time.localtime())

    # Create a text file for logging
    log = r"C:\Scripts_2016\Dans_Scripts\Log\CompressLog.txt"
    write_log("***********************************************************",log)
    write_log("Starting maintenance for " + Date, log)
    try:
        arcpy.env.overwriteOutput = True
        # Block new connections to the database.
        arcpy.AcceptConnections(SDEconnection, False)

        # Disconnect all users from the database.
        arcpy.DisconnectUser(SDEconnection, "ALL")

        # Get a list of versions to pass into the ReconcileVersions tool.
        versionList = arcpy.ListVersions(SDEconnection)

        # Execute the ReconcileVersions tool.
        write_log("-----------------------------------------------------------", log)
        write_log("RECONCILE", log)
        write_log("-----------------------------------------------------------", log)
        reconcileLog = r"C:\Scripts_2016\Dans_Scripts\Log\ReconcileLog" + Date + ".txt"
        arcpy.ReconcileVersions_management(SDEconnection, "ALL_VERSIONS", "sde.QA", versionList, "LOCK_ACQUIRED","NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION",log)
    except:
        recMsg = 'Reconcile & post failed. Error message below.\n\r' + arcpy.GetMessages()
        write_log(recMsg,log)
# ===================   ========  =======================================================================================  ==========
##COMPRESS##
# ===================   ========  =======================================================================================  ==========

    try:
        #identify the log file
        log = 'C:\Scripts_2016\Dans_Scripts\Log\CompressLog.txt'
        write_log("-----------------------------------------------------------", log)
        write_log("COMPRESS", log)
        write_log("-----------------------------------------------------------", log)
        write_log("Starting to run compress...",log)
        # Run the compress tool on the sde connection.
        arcpy.Compress_management(SDEconnection)
        # if the compress is successful add a message.
        write_log("\t Compress success",log)
    except:
        # If the compress failed, add a message.
        write_log("\t Compress failed")
        write_log(arcpy.GetMessages(),log)

    try:
        time.sleep(600)
    except:
        write_log("Unable to sleep",log)

        # ===================   ========  =======================================================================================  ==========
        #                           #Analyse system tables##
        # ===================   ========  =======================================================================================  ==========
# Analyze system tables
    try:
        write_log("-----------------------------------------------------------", log)
        write_log("REBUILDING INDEXES (SYSTEM TABLES)", log)
        write_log("-----------------------------------------------------------", log)
        write_log("Rebuilding indexes on system tables ...",log)
        try:
            arcpy.RebuildIndexes_management(SDEconnection, "SYSTEM")
            write_log("\t Rebuilding of system table indexes successful." + arcpy.GetMessages(),log)
        except:
            rebuildSystemMsg = 'Rebuild indexes on system tables fail: error message below.\n\r' + arcpy.GetMessages()
            write_log("\t \t" + rebuildSystemMsg, log)
    except:
         # Allow the database to begin accepting connections again
        arcpy.AcceptConnections(SDEconnection, True)

    # Allow the database to begin accepting connections again
        arcpy.AcceptConnections(SDEconnection, True)

# ===================   ========  =======================================================================================  ==========
#                                   #INDEX##
# ===================   ========  =======================================================================================  ==========
    # Get a list of datasets owned by the dataowner
    try:
        # Rebuild indexes and analyze the states and states_lineages system tables
        # Get a list of all the datasets the user has access to.
        write_log("-----------------------------------------------------------", log)
        write_log("REBUILDING INDEXES (NO SYSTEM)", log)
        write_log("-----------------------------------------------------------", log)
        workspace = r'C:\Scripts_2016\Dans_Scripts\Connection\Dataowner@SRV-SQLHA02@DVC.sde'
        arcpy.env.workspace = workspace
        arcpy.env.overwriteOutput = True
        datasetlist = arcpy.ListDatasets()
        analysels = []
        for dataset in datasetlist:
            write_log("\t starting to rebuild indexes for dataset {0} time started {1}".format(dataset, Time), log)
            # Next, for feature datasets get all of the featureclasses
            fclist = arcpy.ListFeatureClasses("*", "ALL", dataset)
            for fc in fclist:
                # from the list and add them to the master list.
                analysels.append(fc)
                try:
                    arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataset, "ALL")
                    write_log("\t \t Indexes rebuilt for {0}".format(fc), log)
                    rebuildUserMsg = 'Rebuilding of user data indexes successful.\n\r'
                    write_log("\t \t" + rebuildUserMsg, log)
                except:
                    rebuildUserMsg = 'Rebuild user data indexes failed: error message below.\n\r' + arcpy.GetMessages()
                    write_log("Unable to analyse {0}".format(fc) + rebuildUserMsg, log)

        write_log("- rebuildmsg -" + rebuildUserMsg,log)
        write_log("-----------------------------------------------------------", log)
        write_log("Indexing complete at {0}".format(Time), log)
        write_log("-----------------------------------------------------------", log)
    except:
        write_log("Unable to index fcs",log)

    # Reset geoprocessing environment settings
    arcpy.ResetEnvironments()

    # Reset a specific environment setting
    arcpy.ClearEnvironment("workspace")


# ===================   ========  =======================================================================================  ==========
#                       #ANALYSE data tables##
# ===================   ========  =======================================================================================  ==========
    #dataowner admin tasks
    try:
        ownercon = r'C:\Scripts_2016\Dans_Scripts\Connection\Dataowner@SRV-SQLHA02@DVC.sde'
        write_log("-----------------------------------------------------------", log)
        write_log("ANALYSIS (No system)", log)
        write_log("-----------------------------------------------------------", log)
        write_log("\t Starting analysis of feature classes starting at {0}".format(Time),log )
        for fc in analysels:
            try:
                write_log("\t \t Analysing {0}".format(fc), log)
                arcpy.AnalyzeDatasets_management(ownercon, "NO_SYSTEM", fc, "ANALYZE_BASE", "ANALYZE_DELTA", "NO_ANALYZE_ARCHIVE")
                write_log("\t \t Analysis complete " + arcpy.GetMessages(), log)
                analyzeUserMsg = 'Analyzing of user datasets successful.\n\r'
            except:
                write_log("\t \t Unable to analyse {0}".format(fc),log)
                analyzeUserMsg = 'Analyze user datasets failed: error message below.\n\r' + arcpy.GetMessages()
                write_log(analyzeUserMsg,log)
                continue
        write_log("analys user msg " + analyzeUserMsg,log)
    except:
        write_log("Unable to analyse fcs as dataowner", log)

# Get a list of datasets owned by the SDE
    try:
        workspace = r'C:\Scripts_2016\Dans_Scripts\Connection\SDE@SRV-SQLHA02@CL_DVC.sde'
        arcpy.env.workspace = workspace
        arcpy.env.overwriteOutput = True
        log = r'C:\Scripts_2016\Dans_Scripts\Log\CompressLog.txt'  # name of log file
        write_log("-----------------------------------------------------------", log)
        write_log("ANALYSIS (system)", log)
        write_log("-----------------------------------------------------------", log)
        write_log("\t Starting analysis of system tables")
        write_log("\t Starting to analyse feature classes at {0}".format(Time), log)
        for fc in analysels:
                try:
                    write_log("\t Analysing {0}".format(fc), log)
                    arcpy.AnalyzeDatasets_management(workspace, "SYSTEM", fc, "ANALYZE_BASE", "ANALYZE_DELTA", "NO_ANALYZE_ARCHIVE")
                    write_log("\t Analysis complete " + arcpy.GetMessages(), log)
                    analyzeUserMsg = 'Analyzing of user datasets successful.\n\r'
                except:
                    write_log("Unable to analyse {0}".format(fc),log)
                    analyzeUserMsg = 'Analyze user datasets failed: error message below.\n\r' + arcpy.GetMessages()
                    write_log(analyzeUserMsg,log)
                    continue

    except:
        write_log("Unable to analyse fcs" + arcpy.GetMessages(), log)
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
    for line in failMsg:
        write_log("fail message " + line,log)

if scriptSuccess == True:
    write_log("MAINTENANCE COMPLETE FOR {0} at {1} ".format(Date, Time), log)
else:
    write_log("Geodatabase maintenance script failed", log)

# Reset geoprocessing environment settings
arcpy.ResetEnvironments()

# Reset a specific environment setting
arcpy.ClearEnvironment("workspace")

arcpy.AcceptConnections(SDEconnection, True)
