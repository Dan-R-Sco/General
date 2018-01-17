#------------------------------------------------------------------------------------------------
# Name: Enterprise GDB Maintenance
# Purpose: This script will compress a list of enterprise GDBs, update statistics, and  rebuild table indexes.
# Author:   Nicole Ceranek
# Date Created: 12/28/2015
# Last Modified:    01/05/2016
# ArcGIS Version    10.1
# Python Version:   2.7
#------------------------------------------------------------------------------------------------
## Import modules
import arceditor
import os, arcpy, datetime, sys,time, os.path, logging, fnmatch, traceback
from arcpy import env
from datetime import date, timedelta, datetime
from time import ctime
from os import listdir
from os.path import isfile, join

#Set global variables
datetime120 = time.strftime("%Y%m%d_%H%M%S")
time108 = time.strftime("%H:%M:%S")
arcpy.env.overwriteOutput = True
# Owner directory
OwnerFileDir = "C:/Users/daniel.scott/Desktop/DataOwner/"
AdminFileDir = "C:/Users/daniel.scott/Desktop/DataOwner/"
# Admin directory
LogFile = open(r"W:\daniel.scott\arcgis\egdb\Phase1\EGDBmaintenance_"+datetime120+".csv","w")
## Begin Script
ownerDB = os.listdir(OwnerFileDir)
for DB in ownerDB:
    try:
        arcpy.env.workspace = OwnerFileDir
        arcpy.AddMessage("Not Disconnecting users from "+DB+"\n")
        LogFile.write("Not Disconnecting users from,"+DB+"\n")
        #arcpy.AcceptConnections(DB, False)
        arcpy.DisconnectUser(DB, "ALL")
        arcpy.AddMessage("Compressing "+DB+"\n")
        LogFile.write("Compressing,"+DB+"\n")
        arcpy.Compress_management(DB)
        arcpy.AddMessage("Allowing connections to "+DB+"\n")
        LogFile.write("Allowing connections to,"+DB+"\n")
        arcpy.AcceptConnections(DB, True)
    except arcpy.ExecuteError:
        msgs = arcpy.GetMessages(2)
        arcpy.AddError(msgs)
        arcpy.AddMessage(msgs)
        LogFile.write(msgs)
        ErrorCount=ErrorCount+1
    except:
        if (arcpy.DisconnectUser == "true"):
            arcpy.AcceptConnections(DB, True)
    finally:
        pass
# Rebuild indexes and analyze the states and states_lineages system tables for each EGDB connection file found in the admin directory
adminDB = os.listdir(AdminFileDir)
for DB in adminDB:
    try:
        arcpy.env.workspace = AdminFileDir+DB
        userName = arcpy.Describe(arcpy.env.workspace).connectionProperties.user
        oDataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
        for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
            oDataList += arcpy.ListFeatureClasses(feature_dataset=dataset)
        LogFile.write("Tables owned by "+userName+":,"+str(oDataList)+",\n")
        arcpy.AddMessage("Rebuilding indexes for "+DB+"\n")
        LogFile.write("Rebuilding indexes for,"+DB+"\n")
        arcpy.RebuildIndexes_management(arcpy.env.workspace, "NO_SYSTEM", oDataList, "ALL")
        arcpy.AddMessage("Analyzing data for "+DB+"\n")
        LogFile.write("Analyzing data for,"+DB+"\n")
        arcpy.AnalyzeDatasets_management(arcpy.env.workspace, "NO_SYSTEM", oDataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
    except arcpy.ExecuteError:
        msgs = arcpy.GetMessages(2)
        arcpy.AddError(msgs)
        arcpy.AddMessage(msgs)
        LogFile.write(msgs)
        ErrorCount=ErrorCount+1
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
        msgs = arcpy.GetMessages(2) + "\n"
        arcpy.AddError(pymsg)
        arcpy.AddError(msgs)
        arcpy.AddMessage(pymsg)
        LogFile.write(pymsg)
        arcpy.AddMessage(msgs)
        LogFile.write(msgs)
        ErrorCount=ErrorCount+1
    finally:
        pass