=SUM(IF(ISNUMBER(VALUE(SUBSTITUTE(LEFT(A2:INDEX(A:A, MATCH(9.99999999999999E+307, A:A))), "m", ""))), VALUE(SUBSTITUTE(LEFT(A2:INDEX(A:A, MATCH(9.99999999999999E+307, A:A))), "m", "")), 0))


import sys
import csv
from openshift import config, client

def get_resource_limits(api_instance, namespace, dep_config):
    limits = {}
    dc_name = dep_config.metadata.name
    pods = api_instance.list_namespaced_pod(namespace, label_selector=f'app={dc_name}')
    if pods.items:
        pod = pods.items[0]
        containers = pod.spec.containers
        for container in containers:
            limits[container.name] = {
                'request_cpu': container.resources.requests['cpu'],
                'limit_cpu': container.resources.limits['cpu'],
                'request_memory': container.resources.requests['memory'],
                'limit_memory': container.resources.limits['memory']
            }
    return limits

def export_to_csv(data, namespace):
    with open(f'{namespace}_deployment_configs.csv', 'w', newline='') as csvfile:
        fieldnames = ['DeploymentConfig', 'Container', 'Request CPU', 'Limit CPU', 'Request Memory', 'Limit Memory']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for dep_config, containers in data.items():
            for container, limits in containers.items():
                writer.writerow({'DeploymentConfig': dep_config, 'Container': container,
                                 'Request CPU': limits['request_cpu'], 'Limit CPU': limits['limit_cpu'],
                                 'Request Memory': limits['request_memory'], 'Limit Memory': limits['limit_memory']})

def main(api_server, token):
    # Load the OpenShift configuration
    configuration = client.Configuration()
    
    # Set the API server URL
    configuration.host = api_server
    
    # Set the token
    configuration.api_key = {
        "Authorization": f"Bearer {token}"
    }

    # Disable SSL verification
    configuration.verify_ssl = False

    # Create an OpenShift API client
    api_client = client.ApiClient(configuration)

    # Example: Get deployment configs and resource limits for each namespace
    v1_client = client.AppsV1Api(api_client)
    namespaces = v1_client.list_namespace().items
    for namespace in namespaces:
        namespace_name = namespace.metadata.name
        print(f"Processing namespace: {namespace_name}")

        dep_configs = v1_client.list_namespaced_deployment_config(namespace_name).items
        data = {}
        for dep_config in dep_configs:
            data[dep_config.metadata.name] = get_resource_limits(v1_client, namespace_name, dep_config)

        export_to_csv(data, namespace_name)
        print(f"Exported data for namespace: {namespace_name}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <api_server> <api_token>")
        sys.exit(1)
    api_server = sys.argv[1]
    token = sys.argv[2]
    main(api_server, token)




import sys
import csv
import requests

def get_resource_limits(api_server, token, namespace, dep_config):
    limits = {}
    dc_name = dep_config['metadata']['name']
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    params = {
        "labelSelector": f"app={dc_name}"
    }
    response = requests.get(f"{api_server}/api/v1/namespaces/{namespace}/pods", headers=headers, params=params, verify=False)
    pods = response.json()['items']
    if pods:
        pod = pods[0]
        containers = pod['spec']['containers']
        for container in containers:
            limits[container['name']] = {
                'request_cpu': container['resources']['requests']['cpu'],
                'limit_cpu': container['resources']['limits']['cpu'],
                'request_memory': container['resources']['requests']['memory'],
                'limit_memory': container['resources']['limits']['memory']
            }
    return limits

def export_to_csv(data, namespace):
    with open(f'{namespace}_deployment_configs.csv', 'w', newline='') as csvfile:
        fieldnames = ['DeploymentConfig', 'Container', 'Request CPU', 'Limit CPU', 'Request Memory', 'Limit Memory']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for dep_config, containers in data.items():
            for container, limits in containers.items():
                writer.writerow({'DeploymentConfig': dep_config, 'Container': container,
                                 'Request CPU': limits['request_cpu'], 'Limit CPU': limits['limit_cpu'],
                                 'Request Memory': limits['request_memory'], 'Limit Memory': limits['limit_memory']})

def main(api_server, token):
    # Example: Get deployment configs and resource limits for each namespace
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    response = requests.get(f"{api_server}/apis/apps/v1/deploymentconfigs", headers=headers, verify=False)
    namespaces = [item['metadata']['name'] for item in response.json()['items']]
    
    for namespace in namespaces:
        print(f"Processing namespace: {namespace}")

        response = requests.get(f"{api_server}/apis/apps/v1/namespaces/{namespace}/deploymentconfigs", headers=headers, verify=False)
        dep_configs = response.json()['items']
        data = {}
        for dep_config in dep_configs:
            data[dep_config['metadata']['name']] = get_resource_limits(api_server, token, namespace, dep_config)

        export_to_csv(data, namespace)
        print(f"Exported data for namespace: {namespace}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <api_server> <api_token>")
        sys.exit(1)
    api_server = sys.argv[1]
    token = sys.argv[2]
    main(api_server, token)


import sys
import pandas as pd
import requests

def get_resource_limits(api_server, token, namespace, dep_config):
    limits = {}
    dc_name = dep_config['metadata']['name']
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    params = {
        "labelSelector": f"app={dc_name}"
    }
    response = requests.get(f"{api_server}/api/v1/namespaces/{namespace}/pods", headers=headers, params=params, verify=False)
    if response.status_code == 200:
        pods = response.json().get('items', [])
        if pods:
            pod = pods[0]
            containers = pod['spec']['containers']
            for container in containers:
                limits[container['name']] = {
                    'request_cpu': container['resources']['requests']['cpu'],
                    'limit_cpu': container['resources']['limits']['cpu'],
                    'request_memory': container['resources']['requests']['memory'],
                    'limit_memory': container['resources']['limits']['memory']
                }
    return limits

def main(api_server, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    # Example: Get deployment configs and resource limits for each namespace
    response = requests.get(f"{api_server}/apis/apps/v1/deploymentconfigs", headers=headers, verify=False)
    if response.status_code == 200:
        namespaces = [item['metadata']['name'] for item in response.json().get('items', [])]
        
        writer = pd.ExcelWriter('deployment_configs.xlsx', engine='xlsxwriter')
        
        for namespace in namespaces:
            print(f"Processing namespace: {namespace}")

            response = requests.get(f"{api_server}/apis/apps/v1/namespaces/{namespace}/deploymentconfigs", headers=headers, verify=False)
            if response.status_code == 200:
                dep_configs = response.json().get('items', [])
                data = {}
                for dep_config in dep_configs:
                    data[dep_config['metadata']['name']] = get_resource_limits(api_server, token, namespace, dep_config)

                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=namespace)
                
                print(f"Exported data for namespace: {namespace}")
            else:
                print(f"Failed to fetch deployment configs for namespace: {namespace}")

        writer.save()
        print("All data exported to deployment_configs.xlsx")
    else:
        print("Failed to fetch deployment configs.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <api_server> <api_token>")
        sys.exit(1)
    api_server = sys.argv[1]
    token = sys.argv[2]
    main(api_server, token)


def get_resource_limits(api_server, token, namespace, dep_config):
    limits = {}
    dc_name = dep_config['metadata']['name']
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    params = {
        "labelSelector": f"app={dc_name}"
    }
    response = requests.get(f"{api_server}/api/v1/namespaces/{namespace}/pods", headers=headers, params=params, verify=False)
    if response.status_code == 200:
        pods = response.json().get('items', [])
        if pods:
            pod = pods[0]
            containers = pod['spec']['containers']
            for container in containers:
                resources = container.get('resources', {})
                limits[container['name']] = {
                    'request_cpu': resources.get('requests', {}).get('cpu', '0'),
                    'limit_cpu': resources.get('limits', {}).get('cpu', '0'),
                    'request_memory': resources.get('requests', {}).get('memory', '0'),
                    'limit_memory': resources.get('limits', {}).get('memory', '0')
                }
    return limits

import sys
import csv
import requests
import pandas as pd

def get_resource_limits(api_server, token, namespace, dep_config):
    limits = {}
    dc_name = dep_config['metadata']['name']
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    params = {
        "labelSelector": f"app={dc_name}"
    }
    response = requests.get(f"{api_server}/api/v1/namespaces/{namespace}/pods", headers=headers, params=params, verify=False)
    if response.status_code == 200:
        pods = response.json().get('items', [])
        if pods:
            pod = pods[0]
            containers = pod['spec']['containers']
            for container in containers:
                resources = container.get('resources', {})
                limits[container['name']] = {
                    'request_cpu': resources.get('requests', {}).get('cpu', '0'),
                    'limit_cpu': resources.get('limits', {}).get('cpu', '0'),
                    'request_memory': resources.get('requests', {}).get('memory', '0'),
                    'limit_memory': resources.get('limits', {}).get('memory', '0')
                }
        else:
            print(f"No pods found for deployment configuration: {dc_name}")
    return limits

def export_to_csv(data, namespace):
    with open(f'{namespace}_deployment_configs.csv', 'w', newline='') as csvfile:
        fieldnames = ['DeploymentConfig', 'Container', 'Request CPU', 'Limit CPU', 'Request Memory', 'Limit Memory']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for dep_config, containers in data.items():
            if not containers:
                writer.writerow({'DeploymentConfig': dep_config, 'Container': 'N/A',
                                 'Request CPU': 'N/A', 'Limit CPU': 'N/A',
                                 'Request Memory': 'N/A', 'Limit Memory': 'N/A'})
            else:
                for container, limits in containers.items():
                    writer.writerow({'DeploymentConfig': dep_config, 'Container': container,
                                     'Request CPU': limits['request_cpu'], 'Limit CPU': limits['limit_cpu'],
                                     'Request Memory': limits['request_memory'], 'Limit Memory': limits['limit_memory']})

def main(api_server, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    # Example: Get deployment configs and resource limits for each namespace
    response = requests.get(f"{api_server}/apis/apps/v1/deploymentconfigs", headers=headers, verify=False)
    if response.status_code == 200:
        namespaces = [item['metadata']['name'] for item in response.json().get('items', [])]
        
        for namespace in namespaces:
            print(f"Processing namespace: {namespace}")

            response = requests.get(f"{api_server}/apis/apps/v1/namespaces/{namespace}/deploymentconfigs", headers=headers, verify=False)
            if response.status_code == 200:
                dep_configs = response.json().get('items', [])
                data = {}
                for dep_config in dep_configs:
                    data[dep_config['metadata']['name']] = get_resource_limits(api_server, token, namespace, dep_config)

                export_to_csv(data, namespace)
                print(f"Exported data for namespace: {namespace}")
            else:
                print(f"Failed to fetch deployment configs for namespace: {namespace}")

        print("All data exported.")
    else:
        print("Failed to fetch deployment configs.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <api_server> <api_token>")
        sys.exit(1)
    api_server = sys.argv[1]
    token = sys.argv[2]
    main(api_server, token)





import sys
import requests
import csv

def get_resource_limits(api_server, token, namespace, dep_config):
    limits = {}
    dc_name = dep_config['metadata']['name']
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    params = {
        "labelSelector": f"app={dc_name}"
    }
    response = requests.get(f"{api_server}/api/v1/namespaces/{namespace}/pods", headers=headers, params=params, verify=False)
    if response.status_code == 200:
        pods = response.json().get('items', [])
        if pods:
            pod = pods[0]
            containers = pod['spec']['containers']
            for container in containers:
                resources = container.get('resources', {})
                limits[container['name']] = {
                    'request_cpu': resources.get('requests', {}).get('cpu', '0'),
                    'limit_cpu': resources.get('limits', {}).get('cpu', '0'),
                    'request_memory': resources.get('requests', {}).get('memory', '0'),
                    'limit_memory': resources.get('limits', {}).get('memory', '0')
                }
        else:
            print(f"No pods found for deployment configuration: {dc_name}")
    return limits

def export_to_csv(data):
    with open('deployment_configs.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Namespace', 'DeploymentConfig', 'Container', 'Request CPU', 'Limit CPU', 'Request Memory', 'Limit Memory'])
        for namespace, namespace_data in data.items():
            for dep_config, containers in namespace_data.items():
                if not containers:
                    writer.writerow([namespace, dep_config, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
                else:
                    for container, limits in containers.items():
                        writer.writerow([namespace, dep_config, container, limits['request_cpu'], limits['limit_cpu'], limits['request_memory'], limits['limit_memory']])

def main(api_server, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    # Example: Get deployment configs and resource limits for each namespace
    response = requests.get(f"{api_server}/apis/apps/v1/deploymentconfigs", headers=headers, verify=False)
    if response.status_code == 200:
        namespaces = [item['metadata']['name'] for item in response.json().get('items', [])]
        
        data = {}
        for namespace in namespaces:
            print(f"Processing namespace: {namespace}")

            response = requests.get(f"{api_server}/apis/apps/v1/namespaces/{namespace}/deploymentconfigs", headers=headers, verify=False)
            if response.status_code == 200:
                dep_configs = response.json().get('items', [])
                namespace_data = {}
                for dep_config in dep_configs:
                    namespace_data[dep_config['metadata']['name']] = get_resource_limits(api_server, token, namespace, dep_config)
                data[namespace] = namespace_data
                print(f"Exported data for namespace: {namespace}")
            else:
                print(f"Failed to fetch deployment configs for namespace: {namespace}")

        export_to_csv(data)
        print("All data exported to deployment_configs.csv")
    else:
        print("Failed to fetch deployment configs.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <api_server> <api_token>")
        sys.exit(1)
    api_server = sys.argv[1]
    token = sys.argv[2]
    main(api_server, token)


