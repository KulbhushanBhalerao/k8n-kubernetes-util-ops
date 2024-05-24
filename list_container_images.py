from kubernetes import client, config
import sys
from collections import defaultdict

def list_container_images(namespace):

    # Check if namespace is null
    if not namespace:
        print("Usage: python3 list_container_images.py <namespace>")
        sys.exit(1)

    # Load kubeconfig
    config.load_kube_config()

    # Create API client
    v1 = client.CoreV1Api()

    # Get list of all Pods in the specified namespace
    pods = v1.list_namespaced_pod(namespace=namespace).items

    # Create a dictionary to group containers by image
    containers_by_image = defaultdict(set)

    # Iterate over all Pods
    for pod in pods:
        # Iterate over all containers in each Pod
        for container in pod.spec.containers:
            # Add the container to the set for this image
            containers_by_image[container.image].add(container.name)

    # Print the containers grouped by image
    for image, containers in containers_by_image.items():
        print(f"Image: {image}")
        for container in containers:
            print(f"  Container: {container}")

if __name__ == "__main__":
    # Check if a namespace was provided as a command line argument
    if len(sys.argv) != 2:
        print("Usage: python list_container_images.py <namespace>")
        sys.exit(1)

    # Call the function with the provided namespace
    list_container_images(sys.argv[1])