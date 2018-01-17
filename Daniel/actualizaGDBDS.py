# -*- coding: cp1252 -*-
# -------------------------------------------------------------------------------
# Name:        actualizaGDB.py
# Purpose:
#
# Author:      caranda
#
# Created:     02/10/2017
# Copyright:   (c) caranda 2017
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# Modified     ESRI --- Try, AddMessage, Connection, re, string  FHP

import arcpy
import os
import sys
from xlrd import open_workbook, cellname  # @UnresolvedImport
import string
import re


def find_field(fc, name):
    atrs = arcpy.ListFields(fc)
    for atr in atrs:
        nf = atr.name
        if nf.upper() == name.upper():
            return True
    return False


nOk = 0
nNoOk = 0
patron = re.compile('[a-zA-Z]')

try:
    arcpy.env.workspace = 'in_memory'
    arcpy.env.overwriteOutput = True
    arcpy.env.maintainAttachments = True
    arcpy.env.maintainSpatialIndex = True
    arcpy.env.preserveGlobalIds = True
    excelfile = r'\\srv-arc01\Public\Tools\AcQuireToFC\AcquireToFCSciptTemplateWORKING.xlsx'
    book = open_workbook(excelfile)  # abre el libro excel
    sheet1 = book.sheet_by_index(0)
    arcpy.AddMessage("Execution begins...\n")
    ult_connection = "no*a*valid*connection"
    for rownum in range(1, sheet1.nrows, 1):
        # for rownum in range(3, 5, 1):
        connIn = sheet1.cell(rownum, 0).value
        tablein = sheet1.cell(rownum, 1).value
        connOut = sheet1.cell(rownum, 5).value
        tableOut = sheet1.cell(rownum, 6).value
        fieldX = sheet1.cell(rownum, 2).value
        fieldY = sheet1.cell(rownum, 3).value
        action = sheet1.cell(rownum, 7).value
        ready = "Proccess OK"
        if action == "":
            action = "TA"
        nOk = nOk + 1
        if ult_connection <> connIn:
            ult_connection = connIn
            arcpy.AddMessage("\n" + connIn)
        arcpy.AddMessage("\n" + action + " Input = " + tablein + " ==> " + tableOut)

        if arcpy.Exists(os.path.join(connIn, tablein)):
            if arcpy.Exists(os.path.join(connOut, tableOut)):
                if find_field(os.path.join(connIn, tablein), fieldX):
                    if find_field(os.path.join(connIn, tablein), fieldY):
                        if fieldX <> "" and fieldY <> "":
                            sr = arcpy.SpatialReference(int(sheet1.cell(rownum, 4).value))
                            try:
                                arcpy.MakeXYEventLayer_management(os.path.join(connIn, tablein), fieldX, fieldY,
                                                                  "salida_tmp", sr, "")
                                if action == "T":
                                    arcpy.TruncateTable_management(os.path.join(connOut, tableOut))
                                elif action == "A":
                                    arcpy.Append_management("salida_tmp", os.path.join(connOut, tableOut), "TEST", "",
                                                            "")
                                elif action == "TA":
                                    arcpy.TruncateTable_management(os.path.join(connOut, tableOut))
                                    arcpy.Append_management("salida_tmp", os.path.join(connOut, tableOut), "TEST", "",
                                                            "")
                            except:
                                problem = arcpy.GetMessages()
                                arcpy.AddMessage("\n==============================================")
                                arcpy.AddMessage(problem)
                                m = False
                                if "MakeXYEventLayer" in problem:
                                    campos = arcpy.ListFields(os.path.join(connIn, tablein))
                                    for campo in campos:
                                        gr = patron.match(campo.name[0])
                                        if gr == None:
                                            arcpy.AddMessage("===============================")
                                            arcpy.AddMessage("Invalid field Name " + campo.name)

                                            m = True
                                        else:
                                            if "-" in campo.name:
                                                arcpy.AddMessage("===============================")
                                                arcpy.AddMessage("Invalid field Name " + campo.name)
                                                m = True
                                    if not m:
                                        n = 1
                                        for campo in campos:
                                            arcpy.AddMessage(str(n) + " " + campo.name)
                                            n = n + 1

                                ready = "Proccess failed"
                                nNoOk = nNoOk + 1
                        else:
                            arcpy.AddMessage("In SQL " + os.path.join(connIn,
                                                                         tablein) + " -- The coordinate fields are blank")
                            ready = "ERROR no field coordinates"
                            nNoOk = nNoOk + 1
                    else:
                        arcpy.AddMessage("In SQL " + os.path.join(connIn,
                                                                     tablein) + " -- The Y coordinate field coordinate doesnt exist (" + fieldY + ")")
                        ready = "ERROR  Y doesnt exist"
                        nNoOk = nNoOk + 1
                else:
                    arcpy.AddMessage("In SQL " + os.path.join(connIn,
                                                                 tablein) + " -- The field X coordinate doesnt exist (" + fieldX + ")")
                    ready = "ERROR  X doesnt exist"
                    nNoOk = nNoOk + 1
            else:
                arcpy.AddMessage("The output FC  " + os.path.join(connOut, tableOut) + " -- Cannot be reached")
                ready = "ERROr Target FC"
                nNoOk = nNoOk + 1
        else:
            arcpy.AddMessage("The input SQL  " + os.path.join(connIn, tablein) + " -- Cannot be reached")
            ready = "ERROR Source FC"
            nNoOk = nNoOk + 1
        arcpy.AddMessage(ready)
    arcpy.AddMessage("\nExecution finished")
    arcpy.AddMessage("QTY Tables proccessed = " + str(nOk))
    arcpy.AddMessage("QTY failures          = " + str(nNoOk))
    arcpy.AddMessage("QTY success           = " + str(nOk - nNoOk))
except ValueError as ve:
    print("ERROR!! ", ve)
finally:
    del sheet1

# Connection to compress
SDEconnection = r'C:\Scripts_2016\Dans_Scripts\Connection\SDE@SRV-SQLHA02@CL_Vector.sde'
# Run the compress tool on the sde connection.
arcpy.Compress_management(SDEconnection)