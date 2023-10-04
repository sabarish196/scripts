import os
import csv
from openshift import client, config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set OpenShift configuration
config.load_kube_config()

# Connect to OpenShift cluster
oapi = client.OapiApi()

# Get all namespaces
namespaces = oapi.list_namespace()

# Initialize CSV data
csv_data = []

# Iterate through namespaces
for namespace in namespaces.items:
    namespace_name = namespace.metadata.name

    # Get all pods in the namespace
    pods = oapi.list_namespaced_pod(namespace=namespace_name)

    # Iterate through pods and collect data
    for pod in pods.items:
        pod_name = pod.metadata.name
        node_name = pod.spec.node_name

        # Append data to CSV
        csv_data.append([namespace_name, pod_name, node_name])

# Define CSV file path
csv_file = "pod_data.csv"

# Write data to CSV
with open(csv_file, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Namespace", "Pod Name", "Node Name"])
    csv_writer.writerows(csv_data)

# Email configuration
email_from = "your_email@gmail.com"
email_to = "recipient_email@gmail.com"
email_subject = "OpenShift Pod Data"
email_body = "Please find the attached CSV file with OpenShift pod data."

# Create and send the email
msg = MIMEMultipart()
msg["From"] = email_from
msg["To"] = email_to
msg["Subject"] = email_subject

# Attach the CSV file
with open(csv_file, "rb") as attachment:
    part = MIMEText(email_body)
    msg.attach(part)

    part = MIMEText(attachment.read())
    part.add_header("Content-Disposition", f"attachment; filename= {csv_file}")
    msg.attach(part)

# SMTP configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_user = "your_email@gmail.com"
smtp_password = "your_email_password"

# Create an SMTP server object
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()

# Login to the SMTP server
server.login(smtp_user, smtp_password)

# Send the email
server.sendmail(email_from, email_to, msg.as_string())

# Close the SMTP server
server.quit()

import os
import csv
import pandas as pd
from openshift import client, config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set OpenShift configuration
config.load_kube_config()

# Connect to OpenShift cluster
oapi = client.OapiApi()

# Get all namespaces
namespaces = oapi.list_namespace()

# Initialize CSV data for namespaces and nodes
namespace_data = []
node_data = []

# Iterate through namespaces
for namespace in namespaces.items:
    namespace_name = namespace.metadata.name

    # Get all pods in the namespace
    pods = oapi.list_namespaced_pod(namespace=namespace_name)

    # Iterate through pods and collect data
    for pod in pods.items:
        pod_name = pod.metadata.name
        node_name = pod.spec.node_name

        # Append data to the appropriate list
        namespace_data.append([namespace_name, pod_name])
        node_data.append([node_name, pod_name])

# Define CSV file path
csv_file = "pod_data.csv"

# Create a Pandas DataFrame for namespaces and nodes
namespace_df = pd.DataFrame(namespace_data, columns=["Namespace", "Pod Name"])
node_df = pd.DataFrame(node_data, columns=["Node Name", "Pod Name"])

# Write DataFrames to the same CSV file with different sheets
with pd.ExcelWriter(csv_file, engine='xlsxwriter') as writer:
    namespace_df.to_excel(writer, sheet_name='Namespaces', index=False)
    node_df.to_excel(writer, sheet_name='Nodes', index=False)

# Email configuration (same as in the previous example)

# Create and send the email (same as in the previous example)

# SMTP configuration (same as in the previous example)

# Create an SMTP server object (same as in the previous example)

# Login to the SMTP server (same as in the previous example)

# Send the email (same as in the previous example)

# Close the SMTP server (same as in the previous example)
