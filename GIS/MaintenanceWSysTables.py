#===================   ========  =======================================================================================  ==========
                    #EGDB maintenance script
#Author: Daniel Scott
#one script to rule them all

#currently not catching errors for analyse and indexes see 50:00 in https://www.youtube.com/watch?v=pQpBXDOQU3s add the library for O365 and email
#https://community.esri.com/docs/DOC-9598-gdbadminpython2017zip
#===================   ========  =======================================================================================  ==========

import arcpy, time, os, sys, csv, string

try:

    #===================   ========  =======================================================================================  ==========
                        ##RECONCILE##
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
    log = open("C:\Scripts_2016\Dans_Scripts\Log\CompressLog.txt", "a")
    log.write("***********************************************************\n")

    # Block new connections to the database.
    arcpy.AcceptConnections(SDEconnection, False)

    # Disconnect all users from the database.
    arcpy.DisconnectUser(SDEconnection, "ALL")

    # Get a list of versions to pass into the ReconcileVersions tool.
    versionList = arcpy.ListVersions(SDEconnection)

    # Execute the ReconcileVersions tool.
    reconcileLog = r"C:\Scripts_2016\Dans_Scripts\Log\ReconcileLog" + Date+ ".txt"
    arcpy.ReconcileVersions_management(SDEconnection, "ALL_VERSIONS", "sde.QA", versionList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION", reconcileLog)
    #open rec file
    with open (reconcileLog,'r') as RECFL:
        #iterate lines in rec file
        for line in RECFL:
            #write line to log file
            log.write (line)
    #close rec file
    RECFL.close()

    #===================   ========  =======================================================================================  ==========
                        ##COMPRESS##
    #===================   ========  =======================================================================================  ==========

    #identify the log file
    compresslog = 'C:\Scripts_2016\Dans_Scripts\Log\CompressLog.txt'
    # Run the compress tool on the sde connection.
    arcpy.Compress_management(SDEconnection)
    #add messages of compress to log file
    f = open(compresslog, 'a')
    log.write("\n" + "-----------------------------------------------------------\n" + arcpy.GetMessages() + "\n" + "Compressed database DVC \n")
    log.close()

    # Analyze system tables
    try:
        log.write("\n" + "Rebuilding indexes on system tables " + "\n")
        arcpy.RebuildIndexes(SDEconnection,"SYSTEM")
        log.write("\n" + arcpy.GetMessages() + "\n")
    except:
        log.write("\n" + "Unsuccessful in rebuilding system tables " + "\n")

    log.write("\n" + "Rebuilding indexes on system tables complete" + "\n")
    # Allow the database to begin accepting connections again
    arcpy.AcceptConnections(SDEconnection, True)


    #===================   ========  =======================================================================================  ==========
                        ##INDEX##
    #===================   ========  =======================================================================================  ==========
    # Get a list of datasets owned by the dataowner
    workspace = r'C:\Scripts_2016\Dans_Scripts\Connection\Dataowner@SRV-SQLHA02@DVC.sde'
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True

    def write_log(text,file):
        f = open(file,'a')  #a appends to an existing file if it exists
        f.write("{}\n".format(text)) #write the text to the logfile and move to the next line
        return
    indexlog = 'C:\Scripts_2016\Dans_Scripts\Log\CompressLog.txt' #name of log file

    # Rebuild indexes and analyze the states and states_lineages system tables
    datasetlist = arcpy.ListDatasets("", "Feature")
    analysels = []
    for dataset in datasetlist:
        write_log("-----------------------------------------------------------", indexlog)
        write_log("starting to rebuild indexes for {0} + time started {1}".format(dataset, Time), indexlog)
        fclist = arcpy.ListFeatureClasses("*", "", dataset)
        for fc in fclist:
            analysels.append(fc)
            arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataset, "ALL")
            write_log("Indexes rebuilt for {0}".format(fc), indexlog)
        write_log("-----------------------------------------------------------", indexlog)
    write_log("Indexing complete at {0}".format(Time),indexlog)
    write_log("-----------------------------------------------------------",indexlog)
    # Reset geoprocessing environment settings
    arcpy.ResetEnvironments()

    # Reset a specific environment setting
    arcpy.ClearEnvironment("workspace")

    #===================   ========  =======================================================================================  ==========
                        ##ANALYSE##
    #===================   ========  =======================================================================================  ==========
    def write_log(text,file):
        f = open(file,'a')  #a appends to an existing file if it exists
        f.write("{}\n".format(text)) #write the text to the logfile and move to the next line
        return
    # Get a list of datasets owned by the SDE

    workspace = r'C:\Scripts_2016\Dans_Scripts\Connection\SDE@SRV-SQLHA02@CL_DVC.sde'
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True

    Analyselog = r'C:\Scripts_2016\Dans_Scripts\Log\CompressLog.txt' #name of log file
    write_log("Starting to analyse feature classes at {0}".format(Time), Analyselog)
    for fc in analysels:
        write_log("Analysing {0}".format(fc), Analyselog)
        arcpy.AnalyzeDatasets_management(workspace, "SYSTEM",fc, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
    write_log("Completed analysing", Analyselog)
    write_log("MAINTENANCE COMPLETE FOR {0} at {1}".format(Date, Time), Analyselog)

except:
    import traceback
    scriptSuccess = False
    failMsg = '\n**SCRIPT FAILURE**\n'
    failMsg += 'Most recent GP messages below.\n'
    failMsg += arcpy.GetMessages() +'\n'
    failMsg += '\nTraceback messages below.\n'
    failMsg += traceback.format_exc().splitlines()[-1]


# Reset geoprocessing environment settings
arcpy.ResetEnvironments()

# Reset a specific environment setting
arcpy.ClearEnvironment("workspace")
