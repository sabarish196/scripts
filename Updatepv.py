import yaml

def modify_pv_yaml(input_file, output_file):
    # Load the YAML file
    with open(input_file, 'r') as file:
        data = yaml.safe_load(file)
    
    # Retain specific fields
    retained_data = {
        'kind': data.get('kind'),
        'apiVersion': data.get('apiVersion'),
        'metadata': {
            'name': data['metadata'].get('name'),
            'namespace': data['metadata'].get('namespace')
        },
        'spec': data.get('spec', {})
    }
    
    # Remove spec.volumeName if it exists
    if 'volumeName' in retained_data['spec']:
        del retained_data['spec']['volumeName']
    
    # Remove status if it exists
    if 'status' in retained_data:
        del retained_data['status']
    
    # Save the modified YAML back to a file
    with open(output_file, 'w') as file:
        yaml.safe_dump(retained_data, file)
        
    print(f"Modified YAML saved to {output_file}")

# Example usage
modify_pv_yaml('input.yaml', 'output.yaml')
