import arcpy, time, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Set the workspace
arcpy.env.workspace = 'Database Connections\Dataowner@SRV-SQLHA02.sde'

# Set a variable for the workspace
adminConn = arcpy.env.workspace

# Get a list of connected users.
userList = arcpy.ListUsers(adminConn)
print userList

