import arcpy

input = arcpy.GetParameterAsText(0)
arcpy.env.workspace = path = arcpy.GetParameterAsText(1)
outputLayerName = arcpy.GetParameterAsText(2)
spatial_reference = arcpy.GetParameterAsText(3)


if arcpy.Exists("Temp"):
    arcpy.Delete_management("Temp")
table = arcpy.conversion.ExcelToTable(input, "Temp")

arcpy.management.AddField(table, "Y", "DOUBLE")
arcpy.management.AddField(table, "X", "DOUBLE")
arcpy.management.AddField(table, "Line_Field", "TEXT")

with arcpy.da.UpdateCursor(table, ["Code", "Y","Line_Field", "KP", "X"]) as cursor:
    RDCounter = 0
    ECounter = 0
    FCounter = 0
    for row in cursor:
        row[4] = row[3] * 1000
        if row[0] == "RDS":
            row[1] = 10
            row[2] = "RD" + str(RDCounter)
            cursor.updateRow(row)
        elif row[0] == "RDE":
            row[1] = 10
            row[2] = "RD" + str(RDCounter)
            RDCounter+=1
            cursor.updateRow(row)
        elif row[0] == "ES":
            row[1] = 25
            row[2] = "E" + str(ECounter)
            cursor.updateRow(row)
        elif row[0] == "EE":
            row[1] = 25
            row[2] = "E" + str(ECounter)
            ECounter+=1
            cursor.updateRow(row)
        elif row[0] == "FS":
            row[1] = 40
            row[2] = "F" + str(FCounter)
            cursor.updateRow(row)
        elif row[0] == "FE":
            row[1] = 40
            row[2] = "F" + str(FCounter)
            FCounter+=1
            cursor.updateRow(row)

temp_layer = "Temp"
arcpy.management.MakeXYEventLayer(table, 'X', 'Y', temp_layer, spatial_reference=spatial_reference)
if arcpy.Exists("TempPoints"):
    arcpy.Delete_management("TempPoints")
points = arcpy.CopyFeatures_management(temp_layer, "TempPoints")

output = arcpy.management.PointsToLine(points, outputLayerName, Line_Field="Line_Field")
arcpy.management.AddField(output, "Code", "TEXT")

with arcpy.da.UpdateCursor(output, ["Line_Field", "Code"]) as cursor:
    for row in cursor:
        if row[0][0] == "R":
            row[1] = "RDS"
            cursor.updateRow(row)
        elif row[0][0] == "E":
            row[1] = "ES"
            cursor.updateRow(row)
        elif row[0][0] == "F":
            row[1] = "FS"
            cursor.updateRow(row)

arcpy.management.DeleteField(output, "Line_Field")
arcpy.Delete_management("TempPoints")

if arcpy.Exists("Temp"):
    arcpy.Delete_management("Temp")