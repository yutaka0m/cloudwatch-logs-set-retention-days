import argparse

import boto3

regions = [
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "us-east-1",
]


def get_cloudwatch_log_groups():
    cloudwatch_log_groups = []
    kwargs = {"limit": 50}

    while True:
        response = cloudwatch.describe_log_groups(**kwargs)
        cloudwatch_log_groups += [log_group for log_group in response["logGroups"]]
        if "nextToken" in response:
            print(f"NextToken: {response['nextToken']}")
            kwargs["nextToken"] = response["nextToken"]
        else:
            break

    return cloudwatch_log_groups


def cloudwatch_set_retention(retention, cloudwatch):
    cloudwatch_log_groups = get_cloudwatch_log_groups()

    for group in cloudwatch_log_groups:
        if "retentionInDays" not in group:
            print(f"!! {group['logGroupName']}: put the specified retention of {retention} days.")
            cloudwatch.put_retention_policy(logGroupName=group["logGroupName"], retentionInDays=retention)
        else:
            print(
                f"{group['logGroupName']}: already has the specified retention of {group['retentionInDays']} days."
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("retention", type=int)
    parser.add_argument("profile", type=str)
    args = parser.parse_args()

    for region in regions:
        print(f"Region: {region}")
        cloudwatch = boto3.session \
            .Session(profile_name=args.profile) \
            .client("logs", region_name=region)
        cloudwatch_set_retention(args.retention, cloudwatch)
