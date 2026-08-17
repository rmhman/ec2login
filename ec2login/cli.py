#!/usr/bin/env python3
"""
EC2 Login Utility - Interactive AWS EC2 instance selector with SSM Session Manager
"""

import argparse
import os
import subprocess
import sys
from configparser import ConfigParser
from pathlib import Path

try:
    import boto3
except ImportError:
    print("Error: boto3 is not installed. Please run: pip install ec2login")
    sys.exit(1)

REGION_MAP = {
    "use1": "us-east-1",
    "use2": "us-east-2",
}


def get_aws_profile():
    """Get AWS profile from environment or prompt user to select one."""
    profile = os.environ.get("AWS_PROFILE")
    if profile:
        return profile

    # Read available profiles from ~/.aws/config
    config_path = Path.home() / ".aws" / "config"
    if not config_path.exists():
        print("Error: ~/.aws/config not found")
        sys.exit(1)

    config = ConfigParser()
    config.read(config_path)

    profiles = [s.replace("profile ", "") for s in config.sections() if s.startswith("profile ")]
    profiles = sorted(set(profiles))  # Remove duplicates and sort

    if not profiles:
        print("Error: No AWS profiles found in ~/.aws/config")
        sys.exit(1)

    try:
        result = subprocess.run(
            ["fzf", "--header", "Select an AWS profile"],
            input="\n".join(profiles),
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            # User cancelled
            sys.exit(0)

        return result.stdout.strip()

    except FileNotFoundError:
        print("Error: fzf is not installed. Please install it (e.g., brew install fzf)")
        sys.exit(1)


def get_running_instances(profile, region):
    """Fetch running EC2 instances from the specified region."""
    try:
        session = boto3.Session(profile_name=profile)
        ec2 = session.client("ec2", region_name=region)

        response = ec2.describe_instances(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
        )

        instances = []
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                # Get Name tag if it exists
                name = None
                for tag in instance.get("Tags", []):
                    if tag["Key"] == "Name":
                        name = tag["Value"]
                        break

                # Use Name if available, otherwise use Instance-ID
                display_name = name if name else instance_id
                instances.append(
                    {
                        "id": instance_id,
                        "name": name,
                        "display": display_name,
                        "type": instance.get("InstanceType", "N/A"),
                        "state": instance.get("State", {}).get("Name", "N/A"),
                    }
                )

        # Sort by display name
        instances.sort(key=lambda x: x["display"])
        return instances

    except Exception as e:
        print(f"Error fetching instances: {e}")
        sys.exit(1)


def select_instance_with_fzf(instances, region):
    """Use fzf to interactively select an instance."""
    if not instances:
        print(f"No running instances found in region {region}")
        sys.exit(1)

    # Format for fzf: "Display Name | Instance-ID"
    fzf_input = "\n".join([f"{inst['display']} | {inst['id']}" for inst in instances])

    try:
        result = subprocess.run(
            ["fzf", "--header", f"Select instance in region {region}"],
            input=fzf_input,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            # User cancelled
            sys.exit(0)

        # Extract instance ID from the selected line (format: "Display | ID")
        selected_line = result.stdout.strip()
        instance_id = selected_line.split(" | ")[-1]
        return instance_id

    except FileNotFoundError:
        print("Error: fzf is not installed. Please install it (e.g., brew install fzf)")
        sys.exit(1)


def connect_to_instance(instance_id, profile, region):
    """Connect to EC2 instance via SSM Session Manager."""
    try:
        # Set AWS_PROFILE for the session
        env = os.environ.copy()
        env["AWS_PROFILE"] = profile
        env["AWS_REGION"] = region

        # Build and execute SSM command
        cmd = [
            "aws",
            "ssm",
            "start-session",
            "--target",
            instance_id,
            "--profile",
            profile,
            "--region",
            region,
        ]

        subprocess.run(cmd, env=env)

    except FileNotFoundError:
        print("Error: AWS CLI is not installed")
        sys.exit(1)
    except Exception as e:
        print(f"Error connecting to instance: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Interactive AWS EC2 instance selector with SSM Session Manager"
    )
    parser.add_argument(
        "--region",
        default="use1",
        choices=["use1", "use2"],
        help="AWS region (default: use1)",
    )

    args = parser.parse_args()
    region = REGION_MAP[args.region]

    # Get profile
    profile = get_aws_profile()
    print(f"Using profile: {profile}")

    # Fetch instances
    print(f"Fetching instances from region {region}...")
    instances = get_running_instances(profile, region)

    # Select instance
    instance_id = select_instance_with_fzf(instances, region)

    # Find the selected instance details
    selected_instance = next((i for i in instances if i["id"] == instance_id), None)
    if selected_instance:
        print(f"Connecting to {selected_instance['display']} ({instance_id})...")

    # Connect
    connect_to_instance(instance_id, profile, region)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
