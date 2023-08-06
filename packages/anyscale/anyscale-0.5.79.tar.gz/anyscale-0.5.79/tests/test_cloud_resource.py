import json
import random
import re
import string
import sys
from typing import Any, Callable, Dict, List, Optional
from unittest.mock import Mock, patch

import boto3
from moto import mock_cloudformation, mock_ec2, mock_efs, mock_iam, mock_s3
import pytest

from anyscale.cloud_resource import (
    aws_subnet_has_enough_capacity,
    verify_aws_cloudformation_stack,
    verify_aws_efs,
    verify_aws_iam_roles,
    verify_aws_s3,
    verify_aws_security_groups,
    verify_aws_subnets,
    verify_aws_vpc,
)
from anyscale.conf import ANYSCALE_IAM_ROLE_NAME
from anyscale.shared_anyscale_utils.aws import AwsRoleArn
from anyscale.shared_anyscale_utils.conf import ANYSCALE_HOST
from frontend.cli.anyscale.aws_iam_policies import (
    AMAZON_ECR_READONLY_ACCESS_POLICY_ARN,
    AMAZON_S3_FULL_ACCESS_POLICY_ARN,
    ANYSCALE_IAM_PERMISSIONS_EC2_INITIAL_RUN,
    ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE,
    get_anyscale_aws_iam_assume_role_policy,
)
from frontend.cli.anyscale.cli_logger import BlockLogger
from frontend.cli.anyscale.client.openapi_client.models.create_cloud_resource import (
    CreateCloudResource,
)


DEFAULT_RAY_IAM_ROLE = "ray-autoscaler-v1"


def _create_roles(anyscale_account: str):
    iam = boto3.client("iam")
    suffix = "".join(random.choices(string.ascii_lowercase, k=10))
    control_plane_role = iam.create_role(
        RoleName=ANYSCALE_IAM_ROLE_NAME + suffix,
        AssumeRolePolicyDocument=json.dumps(
            get_anyscale_aws_iam_assume_role_policy(
                anyscale_aws_account=anyscale_account
            )
        ),
    )["Role"]["Arn"]

    # Create & Configure the Dataplane Role
    dataplane_role_name = DEFAULT_RAY_IAM_ROLE + suffix
    dataplane_role = iam.create_role(
        RoleName=dataplane_role_name, AssumeRolePolicyDocument="{}"
    )["Role"]["Arn"]

    iam.attach_role_policy(
        RoleName=dataplane_role_name, PolicyArn=AMAZON_ECR_READONLY_ACCESS_POLICY_ARN
    )
    iam.attach_role_policy(
        RoleName=dataplane_role_name, PolicyArn=AMAZON_S3_FULL_ACCESS_POLICY_ARN
    )
    return [control_plane_role, dataplane_role]


def generate_cloud_resource_mock_aws() -> CreateCloudResource:
    return CreateCloudResource(
        aws_vpc_id="fake_aws_vpc_id",
        aws_subnet_ids=["fake_aws_subnet_id_0", "fake_aws_subnet_id_1"],
        aws_iam_role_arns=[
            "arn:aws:iam::123:role/mock_anyscale_role",
            "arn:aws:iam::123:role/mock_dataplane_role",
        ],
        aws_security_groups=["fake_aws_security_group_0"],
        aws_s3_id="fake_aws_s3_id",
        aws_efs_id="fake_aws_efs_id",
        aws_cloudformation_stack_id="fake_aws_cloudformation_stack_id",
    )


def _attach_iam_roles_to_role(role_arn: str) -> None:
    iam = boto3.client("iam")
    role_name = AwsRoleArn.from_string(role_arn).to_role_name()

    steady_state = iam.create_policy(
        PolicyName="".join(random.choices(string.ascii_lowercase, k=10)),
        PolicyDocument=json.dumps(ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE),
    )["Policy"]["Arn"]
    iam.attach_role_policy(RoleName=role_name, PolicyArn=steady_state)

    initial_run = iam.create_policy(
        PolicyName="".join(random.choices(string.ascii_lowercase, k=10)),
        PolicyDocument=json.dumps(ANYSCALE_IAM_PERMISSIONS_EC2_INITIAL_RUN),
    )["Policy"]["Arn"]
    iam.attach_role_policy(RoleName=role_name, PolicyArn=initial_run)


def _attach_inline_iam_policy_to_role(role_arn: str) -> None:
    iam = boto3.client("iam")
    role_name = AwsRoleArn.from_string(role_arn).to_role_name()

    iam.put_role_policy(
        RoleName=role_name,
        PolicyName="".join(random.choices(string.ascii_lowercase, k=10)),
        PolicyDocument=json.dumps(ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE),
    )
    iam.put_role_policy(
        RoleName=role_name,
        PolicyName="".join(random.choices(string.ascii_lowercase, k=10)),
        PolicyDocument=json.dumps(ANYSCALE_IAM_PERMISSIONS_EC2_INITIAL_RUN),
    )


def _create_instance_profile_for_role(
    role_arn: str, instance_profile_name: Optional[str]
) -> None:
    role_name = AwsRoleArn.from_string(role_arn).to_role_name()
    if instance_profile_name is None:
        instance_profile_name = role_name

    iam = boto3.client("iam")
    iam.create_instance_profile(InstanceProfileName=instance_profile_name)
    iam.add_role_to_instance_profile(
        RoleName=role_name, InstanceProfileName=instance_profile_name,
    )


def _create_vpc(cidr_block: str = "10.0.0.0/16", region: str = "us-west-2") -> str:
    ec2 = boto3.client("ec2", region_name=region)
    vpc = ec2.create_vpc(CidrBlock=cidr_block)
    return vpc["Vpc"]["VpcId"]


def _create_subnets(
    vpc_id: str, region: str, num_subnets: int = 2, assign_public_ip: bool = False
) -> List[str]:
    ec2 = boto3.client("ec2", region_name=region)
    subnet_ids = []
    for i in range(num_subnets):
        subnet = ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=f"10.0.{i}.0/24",
            AvailabilityZone=f"{region}{string.ascii_lowercase[i]}",
        )
        subnet_id = subnet["Subnet"]["SubnetId"]
        subnet_ids.append(subnet_id)
        # MapPublicIpOnLaunch is by default False.
        if assign_public_ip:
            ec2.modify_subnet_attribute(
                SubnetId=subnet_id, MapPublicIpOnLaunch={"Value": True},
            )

    return subnet_ids


def _create_security_group(region: str) -> str:
    ec2 = boto3.client("ec2", region_name=region)
    vpc_id = _create_vpc(region=region)

    security_group = ec2.create_security_group(
        VpcId=vpc_id, GroupName="mock_security_group", Description="mock_security_group"
    )
    security_group_id = security_group["GroupId"]
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                "IpProtocol": "-1",
                "FromPort": -1,
                "ToPort": -1,
                "UserIdGroupPairs": [{"GroupId": security_group_id,}],
            }
        ],
    )

    return security_group_id


def _create_security_group_inbound_permission_expected(region: str) -> str:
    ec2 = boto3.client("ec2", region_name=region)
    vpc_id = _create_vpc(region=region)

    security_group = ec2.create_security_group(
        VpcId=vpc_id, GroupName="mock_security_group", Description="mock_security_group"
    )
    security_group_id = security_group["GroupId"]
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                "IpProtocol": "tcp",  # use tcp instead of -1 because of moto impl issue
                "FromPort": 443,
                "ToPort": 443,
                "UserIdGroupPairs": [{"GroupId": security_group_id}],
            },
            {
                "IpProtocol": "tcp",  # use tcp instead of -1 because of moto impl issue
                "FromPort": 22,
                "ToPort": 22,
                "UserIdGroupPairs": [{"GroupId": security_group_id}],
            },
            {
                "IpProtocol": "-1",  # -1 is needed for check here: https://github.com/anyscale/product/blob/master/frontend/cli/anyscale/cloud_resource.py#L378
                "FromPort": -1,
                "ToPort": -1,
                "UserIdGroupPairs": [{"GroupId": security_group_id}],
            },
        ],
    )
    return security_group_id


def _create_security_group_inbound_permission_excessive_permission(region: str) -> str:
    ec2 = boto3.client("ec2", region_name=region)
    vpc_id = _create_vpc(region=region)

    security_group = ec2.create_security_group(
        VpcId=vpc_id, GroupName="mock_security_group", Description="mock_security_group"
    )
    security_group_id = security_group["GroupId"]
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                "IpProtocol": "tcp",  # use tcp instead of -1 because of moto impl issue
                "FromPort": 443,
                "ToPort": 443,
                "UserIdGroupPairs": [{"GroupId": security_group_id}],
            },
            {
                "IpProtocol": "tcp",  # use tcp instead of -1 because of moto impl issue
                "FromPort": 22,
                "ToPort": 22,
                "UserIdGroupPairs": [{"GroupId": security_group_id}],
            },
            {
                "IpProtocol": "tcp",  # use tcp instead of -1 because of moto impl issue
                "FromPort": 123,
                "ToPort": 123,
                "UserIdGroupPairs": [{"GroupId": security_group_id}],
            },
            {
                "IpProtocol": "-1",  # -1 is needed for check here: https://github.com/anyscale/product/blob/master/frontend/cli/anyscale/cloud_resource.py#L378
                "FromPort": -1,
                "ToPort": -1,
                "UserIdGroupPairs": [{"GroupId": security_group_id}],
            },
        ],
    )
    return security_group_id


def _create_bucket(bucket_name: str = "mock_bucket", cors_rules: Any = None) -> Any:
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket=bucket_name)
    if cors_rules:
        s3.put_bucket_cors(
            Bucket=bucket_name, CORSConfiguration={"CORSRules": cors_rules}
        )
    return boto3.resource("s3").Bucket(bucket_name)


def _create_efs(region: str, subnet_ids: List[str], security_group_id: str):
    efs = boto3.client("efs", region_name=region)
    create_resp = efs.create_file_system(CreationToken="mock_efs")
    efs_id = create_resp["FileSystemId"]

    for subnet_id in subnet_ids:
        efs.create_mount_target(
            FileSystemId=efs_id, SubnetId=subnet_id, SecurityGroups=[security_group_id],
        )
    return efs_id


def _create_cloudformation_stack(region: str) -> str:
    cloudformation = boto3.client("cloudformation", region_name=region)
    cfn = cloudformation.create_stack(
        StackName="mock_cloudformation_stack",
        TemplateBody=json.dumps(
            {
                "Resources": {
                    "mock_resource": {
                        "Type": "AWS::EC2::Instance",
                        "Properties": {
                            "InstanceType": "t2.micro",
                            "ImageId": "ami-0b69ea66ff7391e80",
                        },
                    }
                }
            }
        ),
    )

    return cfn["StackId"]


@pytest.mark.parametrize(
    ("vpc_exists", "vpc_cidr_block", "expected_result", "expected_log_message"),
    [
        pytest.param(False, "0.0.0.0/0", False, r"does not exist."),
        # Happy sizes
        pytest.param(True, "0.0.0.0/16", True, r"verification succeeded."),
        pytest.param(True, "0.0.0.0/20", True, r"verification succeeded."),
        # Warn sizes
        pytest.param(
            True, "0.0.3.0/21", True, r"but this vpc only supports up to \d+ addresses",
        ),
        pytest.param(
            True, "0.0.4.0/24", True, r"but this vpc only supports up to \d+ addresses",
        ),
        # Error sizes
        pytest.param(
            True,
            "0.0.4.0/25",
            False,
            r"Please reach out to support if this is an issue!",
        ),
    ],
)
@mock_ec2
def test_verify_aws_vpc(
    capsys,
    vpc_exists: bool,
    vpc_cidr_block: str,
    expected_result: bool,
    expected_log_message: str,
):
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    region = "us-west-2"
    if vpc_exists:
        vpc_id = _create_vpc(cidr_block=vpc_cidr_block, region=region)
        cloud_resource_mock.aws_vpc_id = vpc_id

    result = verify_aws_vpc(
        cloud_resource=cloud_resource_mock,
        boto3_session=boto3.Session(region_name=region),
        logger=BlockLogger(),
    )
    assert result == expected_result

    stdout, stderr = capsys.readouterr()
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)

    if expected_log_message:
        assert re.search(expected_log_message, stderr)


@pytest.mark.parametrize(
    ("is_private_network"), [False, True],
)
@mock_ec2
def test_verify_aws_subnets(capsys, is_private_network: bool):
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    region = "us-west-2"
    vpc_id = _create_vpc(region=region)
    subnet_ids = _create_subnets(
        vpc_id=vpc_id, region=region, assign_public_ip=not is_private_network
    )

    cloud_resource_mock.aws_vpc_id = vpc_id
    cloud_resource_mock.aws_subnet_ids = subnet_ids

    result, _ = verify_aws_subnets(
        cloud_resource=cloud_resource_mock,
        region=region,
        is_private_network=is_private_network,
        logger=BlockLogger(),
    )

    _, stderr = capsys.readouterr()

    assert result
    assert not re.search(
        r"does not have the 'Auto-assign Public IP' option enabled", stderr
    )
    assert re.search(r"verification succeeded.", stderr)


@mock_ec2
def test_verify_aws_subnets_warn_about_not_assigning_public_ip_in_public_subnets(
    capsys,
):
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    region = "us-west-2"
    vpc_id = _create_vpc(region=region)
    subnet_ids = _create_subnets(vpc_id=vpc_id, region=region, assign_public_ip=False)

    cloud_resource_mock.aws_vpc_id = vpc_id
    cloud_resource_mock.aws_subnet_ids = subnet_ids

    result, _ = verify_aws_subnets(
        cloud_resource=cloud_resource_mock,
        region=region,
        is_private_network=False,
        logger=BlockLogger(),
    )

    _, stderr = capsys.readouterr()

    assert result
    assert re.search(
        r"does not have the 'Auto-assign Public IP' option enabled", stderr
    )
    assert re.search(r"verification succeeded.", stderr)


@mock_ec2
def test_verify_aws_subnets_vpc_subnet_mismatch(capsys):
    cloud_resource_mock = generate_cloud_resource_mock_aws()

    region = "us-west-2"
    vpc_id = _create_vpc(region=region)
    subnet_ids = _create_subnets(vpc_id=vpc_id, region=region, num_subnets=2)

    irrevalent_vpc_id = _create_vpc(region=region)

    cloud_resource_mock.aws_vpc_id = irrevalent_vpc_id
    cloud_resource_mock.aws_subnet_ids = subnet_ids

    result, _ = verify_aws_subnets(
        cloud_resource=cloud_resource_mock,
        region=region,
        is_private_network=False,
        logger=BlockLogger(),
    )

    _, stderr = capsys.readouterr()

    assert not result
    assert re.search(r"is not in a vpc of this cloud.", stderr)


@mock_ec2
def test_verify_aws_subnets_insufficient_subnets(capsys):
    cloud_resource_mock = generate_cloud_resource_mock_aws()

    region = "us-west-2"
    vpc_id = _create_vpc(region=region)
    subnet_ids = _create_subnets(vpc_id=vpc_id, region=region, num_subnets=1)

    cloud_resource_mock.aws_vpc_id = vpc_id
    cloud_resource_mock.aws_subnet_ids = subnet_ids
    cloud_resource_mock.aws_subnet_ids_with_availability_zones = None

    result, returned_cloud_resource = verify_aws_subnets(
        cloud_resource=cloud_resource_mock,
        region=region,
        is_private_network=False,
        logger=BlockLogger(),
    )
    assert result is False
    assert returned_cloud_resource is None
    _, stderr = capsys.readouterr()
    assert re.search(r"Need at least 2 subnets for a cloud.", stderr)


@mock_ec2
def test_verify_aws_subnets_no_subnets():
    cloud_resource_mock = generate_cloud_resource_mock_aws()

    cloud_resource_mock.aws_subnet_ids = None
    cloud_resource_mock.aws_subnet_ids_with_availability_zones = None

    result, returned_cloud_resource = verify_aws_subnets(
        cloud_resource=cloud_resource_mock,
        region="us-west-2",
        is_private_network=False,
        logger=BlockLogger(),
    )
    assert result is False
    assert returned_cloud_resource is None


@pytest.mark.parametrize(
    ("subnet_cidr", "has_capacity", "expected_log_message"),
    [
        # Happy sizes
        ("10.0.0.0/16", True, None),
        ("0.0.0.0/0", True, None),
        ("0.0.1.0/24", True, None),
        # Warn sizes
        ("0.0.2.0/25", True, r"but this subnet only supports up to \d+ addresses"),
        ("0.0.3.0/28", True, r"but this subnet only supports up to \d+ addresses"),
        # Error sizes
        ("0.0.3.0/29", False, r"Please reach out to support if this is an issue!"),
    ],
)
def test_aws_subnet_has_enough_capacity(
    subnet_cidr, has_capacity, expected_log_message, capsys
):
    subnet = Mock()
    subnet.id = "vpc-fake_id"
    subnet.cidr_block = subnet_cidr

    assert aws_subnet_has_enough_capacity(subnet, BlockLogger()) == has_capacity

    stdout, stderr = capsys.readouterr()
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)

    if expected_log_message:
        assert re.search(expected_log_message, stderr)


@mock_iam
@pytest.mark.parametrize(
    ("iam_roles_mock_fn", "expect_warning"),
    [
        pytest.param(lambda _: None, True, id="No Policies"),
        pytest.param(_attach_iam_roles_to_role, False, id="Separate Policies"),
        pytest.param(_attach_inline_iam_policy_to_role, False, id="Inline Policies"),
    ],
)
def test_verify_aws_iam_roles(
    iam_roles_mock_fn: Callable[[str], None], expect_warning: bool
):
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    cp_role_arn, dp_role_arn = _create_roles("fake_anyscale_aws_account")
    _create_instance_profile_for_role(dp_role_arn, None)
    cloud_resource_mock.aws_iam_role_arns = [cp_role_arn, dp_role_arn]
    iam_roles_mock_fn(cp_role_arn)
    mock_logger = Mock()
    assert verify_aws_iam_roles(
        cloud_resource=cloud_resource_mock,
        boto3_session=boto3.Session(),
        anyscale_aws_account="fake_anyscale_aws_account",
        logger=mock_logger,
    )

    if expect_warning:
        assert len(mock_logger.warning.mock_calls) == 1
    else:
        mock_logger.warning.assert_not_called()

    assert len(mock_logger.info.mock_calls) == 2


@mock_iam
def test_verify_aws_iam_roles_instance_profiles():
    """Tests that the dataplane role only passes validation if it has
    an InstanceProfile with the same name as the Role."""
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    cp_role_arn, dp_role_arn = _create_roles("fake_anyscale_aws_account")
    cloud_resource_mock.aws_iam_role_arns = [cp_role_arn, dp_role_arn]
    mock_logger = Mock()

    # No instance profile for role
    assert not verify_aws_iam_roles(
        cloud_resource=cloud_resource_mock,
        boto3_session=boto3.Session(),
        anyscale_aws_account="fake_anyscale_aws_account",
        logger=mock_logger,
    )

    # Create an instance profile for the role, but with the wrong name
    _create_instance_profile_for_role(dp_role_arn, "wrong_name")
    assert not verify_aws_iam_roles(
        cloud_resource=cloud_resource_mock,
        boto3_session=boto3.Session(),
        anyscale_aws_account="fake_anyscale_aws_account",
        logger=mock_logger,
    )

    # Create a correct insance profile with the role!
    _create_instance_profile_for_role(dp_role_arn, None)
    assert verify_aws_iam_roles(
        cloud_resource=cloud_resource_mock,
        boto3_session=boto3.Session(),
        anyscale_aws_account="fake_anyscale_aws_account",
        logger=mock_logger,
    )


@pytest.mark.parametrize(
    ("sg_exists", "sg_valid", "expected_result", "expected_log_message"),
    [
        pytest.param(
            False, False, False, r"Missing security group IDs", id="SG-Does-Not-Exist"
        ),
        pytest.param(True, False, False, r"does not exist", id="SG-Exists-Not-Valid"),
        pytest.param(True, True, True, None, id="SG-Exists-And-Valid"),
    ],
)
@mock_ec2
def test_verify_aws_security_groups_exist_and_valid(
    capsys,
    sg_exists: bool,
    sg_valid: bool,
    expected_result: bool,
    expected_log_message: str,
):
    cloud_resource_mock = generate_cloud_resource_mock_aws()

    region = "us-west-2"
    if sg_exists:
        if sg_valid:
            sg_id = _create_security_group(region)
        else:
            sg_id = "Invalid_SG"
        cloud_resource_mock.aws_security_groups = [sg_id]
    else:
        cloud_resource_mock.aws_security_groups = []

    result = verify_aws_security_groups(
        cloud_resource=cloud_resource_mock,
        boto3_session=boto3.Session(region_name=region),
        logger=BlockLogger(),
    )

    stdout, stderr = capsys.readouterr()
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)

    assert result == expected_result
    if expected_log_message:
        assert re.search(expected_log_message, stderr)


@pytest.mark.parametrize(
    ("not_enough_permission", "excessive_permission", "expected_log_message"),
    [
        pytest.param(False, False, None, id="Expected_Permission"),
        pytest.param(
            True,
            False,
            r"does not contain inbound permission for ports",
            id="Not_Enough_Permission",
        ),
        pytest.param(
            False, True, r"allows access to more than", id="Excessive_Permission"
        ),
    ],
)
@mock_ec2
def test_verify_aws_security_groups_inbound_permissions(
    capsys,
    not_enough_permission: bool,
    excessive_permission: bool,
    expected_log_message: str,
):
    cloud_resource_mock = generate_cloud_resource_mock_aws()

    region = "us-west-2"

    if not_enough_permission:
        sg_id = _create_security_group(region)
    elif excessive_permission:
        sg_id = _create_security_group_inbound_permission_excessive_permission(region)
    else:  # expected permission
        sg_id = _create_security_group_inbound_permission_expected(region)

    cloud_resource_mock.aws_security_groups = [sg_id]

    result = verify_aws_security_groups(
        cloud_resource=cloud_resource_mock,
        boto3_session=boto3.Session(region_name=region),
        logger=BlockLogger(),
    )
    stdout, stderr = capsys.readouterr()
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)

    assert result
    if expected_log_message:
        assert re.search(expected_log_message, stderr)


@pytest.mark.parametrize(
    ("s3_exists", "expected_result"),
    [
        pytest.param(False, False, id="S3-Does-Not-Exist"),
        pytest.param(True, True, id="S3-Exists"),
    ],
)
@pytest.mark.parametrize(
    "cors_rules,expected_warning_call_count",
    [
        pytest.param(
            [
                {
                    "AllowedHeaders": ["*"],
                    "AllowedMethods": ["GET"],
                    "AllowedOrigins": [ANYSCALE_HOST],
                    "ExposeHeaders": [],
                }
            ],
            0,
            id="CorrectCORS",
        ),
        pytest.param(
            [
                {
                    "AllowedHeaders": ["*"],
                    "AllowedMethods": ["GET"],
                    "AllowedOrigins": ["openai.com"],
                    "ExposeHeaders": [],
                }
            ],
            1,
            id="ImproperCORS",
        ),
        pytest.param([], 2, id="NoCORS"),
    ],
)
@mock_s3
@mock_iam
def test_verify_aws_s3(
    s3_exists: bool,
    expected_result: bool,
    cors_rules: List[Dict[str, List[str]]],
    expected_warning_call_count: int,
):
    cloud_resource_mock = generate_cloud_resource_mock_aws()

    region = "us-west-2"
    if s3_exists:
        bucket = _create_bucket(cors_rules=cors_rules)
        cloud_resource_mock.aws_s3_id = bucket.name

    cp_role_arn, dp_role_arn = _create_roles("fake_anyscale_aws_account")
    cloud_resource_mock.aws_iam_role_arns = [cp_role_arn, dp_role_arn]

    mock_logger = Mock()

    with patch.multiple(
        "anyscale.cloud_resource", verify_s3_access=Mock(return_value=True),
    ):
        result = verify_aws_s3(
            cloud_resource=cloud_resource_mock,
            boto3_session=boto3.Session(region_name=region),
            logger=mock_logger,
        )

    if s3_exists:
        assert mock_logger.warning.call_count == expected_warning_call_count
    else:
        assert mock_logger.error.call_count == 1
        assert mock_logger.warning.call_count == 0

    assert result == expected_result


@pytest.mark.parametrize(
    ("efs_exists", "expected_result"),
    [pytest.param(False, False), pytest.param(True, True)],
)
@mock_efs
@mock_ec2
def test_verify_aws_efs(efs_exists: bool, expected_result: bool):
    cloud_resource_mock = generate_cloud_resource_mock_aws()

    region = "us-west-2"
    if efs_exists:
        vpc_id = _create_vpc(region=region)
        subnet_ids = _create_subnets(vpc_id, region)
        security_group_ids = _create_security_group(region)
        efs_id = _create_efs(region, subnet_ids, security_group_ids)
        cloud_resource_mock.aws_efs_id = efs_id

    result = verify_aws_efs(
        cloud_resource=cloud_resource_mock,
        boto3_session=boto3.Session(region_name=region),
        logger=Mock(),
    )
    assert result == expected_result


@pytest.mark.parametrize(
    ("cloudformation_stack_exists", "expected_result"),
    [pytest.param(False, False), pytest.param(True, True)],
)
@mock_cloudformation
def test_verify_aws_cloudformation_stack(
    cloudformation_stack_exists: bool, expected_result: bool
):
    cloud_resource_mock = generate_cloud_resource_mock_aws()

    region = "us-west-2"
    if cloudformation_stack_exists:
        cloud_resource_mock.aws_cloudformation_stack_id = _create_cloudformation_stack(
            region
        )

    result = verify_aws_cloudformation_stack(
        cloud_resource=cloud_resource_mock,
        boto3_session=boto3.Session(region_name=region),
        logger=BlockLogger(),
    )
    assert result == expected_result
