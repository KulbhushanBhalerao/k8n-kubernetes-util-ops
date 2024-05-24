from kubernetes import client, config
import sys
from collections import defaultdict

def list_ingress_paths(namespace):

    # Check if namespace is null
    if not namespace:
        print("Usage: python3 list_ingress_paths.py <namespace>")
        sys.exit(1)

    # Load kubeconfig
    config.load_kube_config()

    # Create API client
    v1 = client.NetworkingV1Api()

    # Get list of all Ingresses in the specified namespace
    ingresses = v1.list_namespaced_ingress(namespace=namespace).items

    # Create a dictionary to group paths by service
    paths_by_service = defaultdict(list)

    # Iterate over all Ingresses
    for ingress in ingresses:
        # Iterate over all rules in each Ingress
        for rule in ingress.spec.rules:
            # Iterate over all paths in each rule
            for path in rule.http.paths:
                # Add the path to the list for this service
                paths_by_service[path.backend.service.name].append(path.path)

    # Print the paths grouped by service
    for service, paths in paths_by_service.items():
        print(f"Service: {service}")
        for path in paths:
            print(f"  Path: {path}")

if __name__ == "__main__":
    # Check if a namespace was provided as a command line argument
    if len(sys.argv) != 2:
        print("Usage: python list_ingress_paths.py <namespace>")
        sys.exit(1)

    # Call the function with the provided namespace
    list_ingress_paths(sys.argv[1])