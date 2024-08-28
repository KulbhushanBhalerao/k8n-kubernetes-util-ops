import argparse
import os
from kubernetes import client, config

def list_labels(namespace):
    """
    Retrieves the labels of deployments and statefulsets in the specified namespace and generates patch commands.

    Args:
        namespace (str): The namespace to retrieve the labels from.

    Returns:
        Creaes a file called patch_commands.sh in the output directory with the patch commands.
        Outputs the labels of deployments and statefulsets to the console.

    Usage: 
        python generate-kubectl-patch-labels.py <namespace>
        or
        python3 generate-kubectl-patch-labels.py <namespace>
    """
    # Load the Kubernetes configuration
    config.load_kube_config()

    # Create an instance of the Kubernetes API client for CoreV1 and AppsV1
    core_v1_api = client.CoreV1Api()
    apps_v1_api = client.AppsV1Api()

    # Get all the deployments in the specified namespace
    deployments = apps_v1_api.list_namespaced_deployment(namespace)

    # Get all the statefulsets in the specified namespace
    statefulsets = apps_v1_api.list_namespaced_stateful_set(namespace)

    # Prepare the output directory
    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)

    # Open the output file
    with open(os.path.join(output_dir, "patch_commands.sh"), "w") as f:
        # Print the labels for each deployment and generate patch commands
        print("Deployments:")
        for deployment in deployments.items:
            print(f"Deployment: {deployment.metadata.name}")
            print(f"Labels: {deployment.metadata.labels}")
            patch_command = f"kubectl patch deployment {deployment.metadata.name} -n {namespace} --patch '{{\"metadata\": {{\"labels\": {deployment.metadata.labels}}}}}'"
            f.write(patch_command + "\n")

        # Print the labels for each statefulset and generate patch commands
        print("StatefulSets:")
        for statefulset in statefulsets.items:
            print(f"StatefulSet: {statefulset.metadata.name}")
            print(f"Labels: {statefulset.metadata.labels}")
            patch_command = f"kubectl patch statefulset {statefulset.metadata.name} -n {namespace} --patch '{{\"metadata\": {{\"labels\": {statefulset.metadata.labels}}}}}'"
            f.write(patch_command + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List labels of deployments and statefulsets in a namespace and generate kubectl patch commands.")
    parser.add_argument("namespace", type=str, help="The namespace to list labels from")
    args = parser.parse_args()

    list_labels(args.namespace)