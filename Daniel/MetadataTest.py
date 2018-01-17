#  UPDATE METADATA --- LYR
#  QPX
#  INPUT EXCEL FILE
#        SHEET1 -- METADATA
#        SHEET2 -- METADATA - AUTHORS
#  DEPENDENCIES = XLRD
#                 ARCPY_METADATA
#  ----------------------------------------------------------------
from xlrd import open_workbook, cellname  # @UnresolvedImport
import os.path
import arcpy
import arcpy_metadata as md


def insertTags(object, tags):
    listTags = tags.split(",")
    for t in listTags:
        t1 = t.strip()
        if len(t1) > 0:
            object.append(t1)


def buscaAutores(nombre, lista):
    autores = []
    for la in lista:
        if (nombre == la[0]):
            autores.append(la[1])
    return autores


elExcel = arcpy.GetParameterAsText(0).replace("\\", "/")
book = open_workbook(elExcel)  # abre el libro excel
sheet1 = book.sheet_by_index(1)
listaAutores = []
for rownum in range(1, sheet1.nrows, 1):
    listaAutores.append([sheet1.cell(rownum, 1).value, sheet1.cell(rownum, 2).value])
del sheet1
sheet = book.sheet_by_index(0)  # busca la primera hoja del libro (con el indice 0)
ruta_base = arcpy.GetParameterAsText(1)
# ruta_base = ruta_base.replace("\\","/")
arcpy.AddMessage(ruta_base)
arcpy.AddMessage(sheet.nrows)
for row_index in range(4, sheet.nrows, 1):
    print ruta_base + '\\' + sheet.cell(row_index, 0).value + '\\' + sheet.cell(row_index, 1).value
    archivo = ruta_base + '\\' + sheet.cell(row_index, 0).value + '\\' + sheet.cell(row_index, 1).value
    if (os.path.exists(archivo)):
        try:
            arcpy.AddMessage(archivo)
            metadata = md.MetadataEditor(archivo)
            # arcpy.AddMessage(archivo)
            metadata.title = sheet.cell(row_index, 2).value
            metadata.purpose = sheet.cell(row_index, 14).value
            if sheet.cell(row_index, 11).value == "":
                laesca = "Escala: " + str(sheet.cell(row_index, 10).value)
            else:
                laesca = "Escala: " + str(sheet.cell(row_index, 10).value) + \
                         " Resolucion: " + str(sheet.cell(row_index, 11).value)
            metadata.scale_resolution = laesca
            metadata.place_keywords = [sheet.cell(row_index, 6).value, sheet.cell(row_index, 7).value]
            los_meta = []
            if sheet.cell(row_index, 3).value != "" and sheet.cell(row_index, 3).value != "NO APLICA":
                insertTags(los_meta, sheet.cell(row_index, 3).value)
                # los_meta.append(sheet.cell(row_index,3).value)
            if sheet.cell(row_index, 4).value != "" and sheet.cell(row_index, 4).value != "NO APLICA":
                # los_meta.append(sheet.cell(row_index,4).value)
                insertTags(los_meta, sheet.cell(row_index, 4).value)
            if sheet.cell(row_index, 5).value != "" and sheet.cell(row_index, 5).value != "NO APLICA":
                # los_meta.append(sheet.cell(row_index,5).value)
                insertTags(los_meta, sheet.cell(row_index, 5).value)
            if sheet.cell(row_index, 6).value != "" and sheet.cell(row_index, 6).value != "NO APLICA":
                # los_meta.append(sheet.cell(row_index,6).value)
                insertTags(los_meta, sheet.cell(row_index, 6).value)
            if sheet.cell(row_index, 7).value != "" and sheet.cell(row_index, 7).value != "NO APLICA":
                # los_meta.append(sheet.cell(row_index,7).value)
                insertTags(los_meta, sheet.cell(row_index, 7).value)
            for autor in buscaAutores(sheet.cell(row_index, 1).value, listaAutores):
                los_meta.append(autor)
            metadata.tags = los_meta
            metadata.limitation = sheet.cell(row_index, 15).value
            metadata.point_of_contact.contact_name = sheet.cell(row_index, 17).value
            metadata.point_of_contact.email = sheet.cell(row_index, 18).value
            metadata.extent_description = "Proyeccion Origen: " + str(sheet.cell(row_index, 19).value) + \
                                          " Proyeccion Destino: " + str(sheet.cell(row_index, 20).value)
            metadata.entidad_formato_ver = "Entidad: " + str(sheet.cell(row_index, 8).value) + \
                                           " Formato: " + str(sheet.cell(row_index, 9).value)
            metadata.abstract = sheet.cell(row_index, 21).value
            # arcpy.AddMessage(archivo)
            metadata.finish()
            print("Se creo metadata para el archivo " + archivo)
        except:
            arcpy.AddMessage(arcpy.GetMessages())

del sheet
del book
# del metadata
