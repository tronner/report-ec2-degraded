#!/usr/bin/env python3
import boto3

def instance_name(instance):
    for tag in instance["Tags"]:
        if tag["Key"] == "Name":
            return tag["Value"]
    return ""

ec2 = boto3.client("ec2")

degraded_statuses = [
        instance
        for instance in ec2.describe_instance_status()["InstanceStatuses"]
        if "Events" in instance
        ]

def report():
    result = []
    for status in degraded_statuses:
        result.append(60*"=")
        instance_id = status["InstanceId"]
        instance = ec2.describe_instances(
                InstanceIds=[instance_id]
            )["Reservations"][0]["Instances"][0]

        result.append("Instance ID: {}".format(instance_id))
        result.append("Name: {}".format(instance_name(instance)))
        result.append("Events:")
        for event in status["Events"]:
            result.append(" + Code:        {}".format(event["Code"]))
            result.append(" | Description: {}".format(event["Description"]))
            result.append(" | Not before:  {}".format(event["NotBefore"]))
    if len(degraded_statuses) > 0:
        result.append(60*"=")
    return "\n".join(result)

if __name__ == "__main__":
    print(report())
