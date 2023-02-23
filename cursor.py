print 'Running script....'

#Set up Env
folderPath = r'\\Mac\Home\Documents\GIS\data'
import arcpy
from arcpy import env
import os
arcpy.env.workspace = folderPath
arcpy.env.overwriteOutput = True

#Creates Table with new fields
arcpy.CreateTable_management(folderPath, 'Countries_Table.dbf')
newFields = [('CITY_NAME', 'TEXT'),
             ('ADMIN', 'TEXT'),
             ('CNTRY_NAME', 'TEXT'),
             ('POP', 'DOUBLE')
    ]
for n in newFields:
    arcpy.AddField_management('Countries_Table.dbf', n[0],n[1])

#Tells us current table with fields and fied types
tableList = arcpy.ListTables()
for table in tableList:
    print "***** The Current Table is:", table

    fields=arcpy.ListFields('Countries_Table.dbf')
    for field in fields:
        print field.name, field.type

#Search cursor and insert cursor: takes search cursor values and inserts them into the table
scur_fields=["CITY_NAME", "ADMIN_NAME", "CNTRY_NAME", "Population"]
icur_fields=["CITY_NAME", "ADMIN", "CNTRY_NAME", "POP"]

with arcpy.da.SearchCursor(os.path.join(folderPath, 'NA_Cities.shp'), scur_fields) as sCur:
    with arcpy.da.InsertCursor(os.path.join(folderPath, 'Countries_Table.dbf'), icur_fields) as iCur:
        for row in sCur:
            iCur.insertRow(row)

#Update cursor and for loop used to filter desired 
fc = (os.path.join(folderPath, 'Countries_Table.dbf'))
ucur_fields = ["CNTRY_NAME", "POP"]
with arcpy.da.UpdateCursor(fc, ucur_fields) as ucur:
    for row in ucur:
        if row[0] == 'Mexico' and row[1] <8000000:
                ucur.deleteRow()
        if row[0] == 'Canada' and row[1] <3000000:
                ucur.deleteRow()
        if row[0] == 'United States' and row[1] <8000000:
                ucur.deleteRow()

#Prints values in shell using a search cursor
fields = ["CITY_NAME", "ADMIN", "CNTRY_NAME", "POP"]
sCur2 = arcpy.SearchCursor(os.path.join(folderPath, 'Countries_Table.dbf'), fields)
for row in sCur2:
    print("City: {0}, Admin Name: {1}, Country: {2}, Population: {3}".format(
        row.getValue("CITY_NAME"),
        row.getValue("ADMIN"),
        row.getValue("CNTRY_NAME"),
        row.getValue("POP")))

print 'End of script.'
                             




