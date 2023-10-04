import os
import csv
import requests

# Set the OpenShift API URL and your token
api_url = "https://your-openshift-api-url"
token = "your-openshift-token"

# Define headers with the token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

# Initialize CSV data
csv_data = []

# Get all namespaces
namespace_url = f"{api_url}/api/v1/namespaces"
namespace_response = requests.get(namespace_url, headers=headers)

if namespace_response.status_code == 200:
    namespaces = namespace_response.json()["items"]

    # Iterate through namespaces
    for namespace in namespaces:
        namespace_name = namespace["metadata"]["name"]

        # Get pods in the namespace
        pods_url = f"{api_url}/api/v1/namespaces/{namespace_name}/pods"
        pods_response = requests.get(pods_url, headers=headers)

        if pods_response.status_code == 200:
            pods = pods_response.json()["items"]

            # Iterate through pods and collect data
            for pod in pods:
                pod_name = pod["metadata"]["name"]
                node_name = pod["spec"]["nodeName"]

                # Append data to CSV
                csv_data.append([namespace_name, pod_name, node_name])

# Define CSV file path
csv_file = "pod_data.csv"

# Write data to CSV
with open(csv_file, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Namespace", "Pod Name", "Node Name"])
    csv_writer.writerows(csv_data)
