import os
import csv
import requests
import pandas as pd

# Set the OpenShift API URL and your token
api_url = "https://your-openshift-api-url"
token = "your-openshift-token"

# Define headers with the token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

# Initialize CSV data for namespaces and nodes
namespace_data = []
node_data = []

# Get all namespaces
namespace_url = f"{api_url}/api/v1/namespaces"
namespace_response = requests.get(namespace_url, headers=headers, verify=False)

if namespace_response.status_code == 200:
    namespaces = namespace_response.json()["items"]

    # Iterate through namespaces
    for namespace in namespaces:
        namespace_name = namespace["metadata"]["name"]

        # Get pods in the namespace
        pods_url = f"{api_url}/api/v1/namespaces/{namespace_name}/pods"
        pods_response = requests.get(pods_url, headers=headers, verify=False)

        if pods_response.status_code == 200:
            pods = pods_response.json()["items"]

            # Append pod count to namespace_data
            namespace_data.append([namespace_name, len(pods)])

            # Iterate through pods and collect data for nodes
            for pod in pods:
                node_name = pod["spec"]["nodeName"]

                # Append data to node_data
                node_data.append([node_name])

# Create a Pandas DataFrame for namespaces and nodes
namespace_df = pd.DataFrame(namespace_data, columns=["Namespace", "Total Pods"])
node_df = pd.DataFrame(node_data, columns=["Node Name"])

# Define CSV file paths
namespace_csv_file = "total_pods_in_namespace.csv"
node_csv_file = "total_pods_on_nodes.csv"

# Write DataFrames to separate CSV files
namespace_df.to_csv(namespace_csv_file, index=False)
node_df.to_csv(node_csv_file, index=False)
