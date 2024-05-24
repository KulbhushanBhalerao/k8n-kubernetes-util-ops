from datetime import datetime, timedelta
from kubernetes import client, config
import argparse

def list_pod_events(namespace, time):
    # Load the Kubernetes configuration
    config.load_kube_config()

    # Create a Kubernetes API client
    api_client = client.CoreV1Api()

    # Get the current time and calculate the time ago based on the input
    now = datetime.now()
    if time.endswith("m"):
        minutes = int(time[:-1])
        time_ago = now - timedelta(minutes=minutes)
    elif time.endswith("hr"):
        hours = int(time[:-2])
        time_ago = now - timedelta(hours=hours)
    elif time.endswith("d"):
        days = int(time[:-1])
        time_ago = now - timedelta(days=days)
    else:
        print("Invalid time format. Please use 'm' for minutes, 'hr' for hours, or 'd' for days.")
        return

    # Get the events in the specified namespace
    events = api_client.list_namespaced_event(namespace=namespace).items

    # Iterate over the events
    for event in events:
        if event.last_timestamp is not None:
            event_time = event.last_timestamp.replace(tzinfo=None)
            if event_time >= time_ago:
                print(f"Time: [{event_time}] Pod [{event.involved_object.name}], [Reason: {event.reason}] ==>> [Event: {event.type}] {event.message} ")

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="List pod events ")

    # Add arguments for namespace and time
    parser.add_argument("namespace", help="The namespace to search for pod events")
    parser.add_argument("time", help="The time range to search for pod events (e.g. 10m, 1hr, 1d)")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function to list pod events 
    list_pod_events(args.namespace, args.time)

if __name__ == "__main__":
    main()
