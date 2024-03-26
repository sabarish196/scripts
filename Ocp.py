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

def main(token):
    # Load the OpenShift configuration
    configuration = config.new_client_from_config()
    
    # Set the token
    configuration.api_key = {
        "Authorization": f"Bearer {token}"
    }

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
    if len(sys.argv) != 2:
        print("Usage: python script.py <api_token>")
        sys.exit(1)
    token = sys.argv[1]
    main(token)
