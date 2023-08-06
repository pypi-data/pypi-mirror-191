import logging

import botocore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_regions(self):
    logger.info(" ---Inside utils :: get_regions()--- ")
    """Summary

    Returns:
        TYPE: Description
    """

    client = self.session.client('ec2', region_name='us-east-1')
    region_response = {}
    try:
        region_response = client.describe_regions()
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'AuthFailure':
            logger.error(f" AccessKey credentails not found here: {error}")
            exit(1)
    except botocore.exceptions.NoCredentialsError as e:
        logger.error(f" Unable to locate credentials: {e} ")
        exit(1)

    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions


# return the list of rds clusters
def list_rds_clusters(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_rds_clusters()--- ")

    cluster_lst = {}

    for region in regions:
        client = self.session.client('rds', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_db_clusters()
            else:
                response = client.describe_db_clusters(
                    Marker=marker
                )
            cluster_lst.setdefault(region, []).extend(response['DBClusters'])

            try:
                marker = response['Marker']
                if marker == '':
                    break
            except KeyError:
                break

    return cluster_lst


# returns the list of ec2 instances
def list_ec2_instances(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_ec2_instances()--- ")

    instances = {}

    for region in regions:
        client = self.session.client('ec2', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_instances()
            else:
                response = client.describe_instances(
                    NextToken=marker
                )
            instances.setdefault(region, []).extend(response['Reservations'])

            try:
                marker = response['NextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return instances


# returns the list of security Groups
def list_security_groups(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_security_groups()--- ")

    sg_lst = {}

    for region in regions:
        client = self.session.client('ec2', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_security_groups()
            else:
                response = client.describe_security_groups(
                    NextToken=marker
                )
            sg_lst.setdefault(region, []).extend(response['SecurityGroups'])

            try:
                marker = response['NextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return sg_lst


# return the list of ENI
def list_eni(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_eni()--- ")

    eni_lst = {}

    for region in regions:
        client = self.session.client('ec2', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_network_interfaces()
            else:
                response = client.describe_network_interfaces(
                    NextToken=marker
                )
            eni_lst.setdefault(region, []).extend(response['NetworkInterfaces'])

            try:
                marker = response['NextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return eni_lst


# returns the list of lambda functions
def list_lambda_functions(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_lambda_functions()--- ")

    lambda_list = {}

    for region in regions:
        client = self.session.client('lambda', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.list_functions()
            else:
                response = client.list_functions(
                    Marker=marker
                )
            lambda_list.setdefault(region, []).extend(response['Functions'])

            try:
                if marker == '':
                    break
            except KeyError:
                break

    return lambda_list


# returns the list Elastic load balancers
def list_elbv2(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_elbv2()--- ")

    elb_lst = {}

    for region in regions:
        client = self.session.client('elbv2', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_load_balancers()
            else:
                response = client.describe_load_balancers(
                    Marker=marker
                )
            elb_lst.setdefault(region, []).extend(response['LoadBalancers'])

            try:
                marker = response['NextMarker']
                if marker == '':
                    break
            except KeyError:
                break

    return elb_lst


# returns the list of auto scaling groups
def list_auto_scaling_groups(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_auto_scaling_groups()--- ")

    asg_lst = {}

    for region in regions:
        client = self.session.client('autoscaling', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_auto_scaling_groups()
            else:
                response = client.describe_auto_scaling_groups(
                    NextToken=marker
                )

            asg_lst.setdefault(region, []).extend(response['AutoScalingGroups'])

            try:
                marker = response['NextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return asg_lst


# returns the list of auto scaling launch configs
def list_as_launch_configs(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_as_launch_configs()--- ")

    launch_configs = {}

    for region in regions:
        client = self.session.client('autoscaling', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_launch_configurations()
            else:
                response = client.describe_launch_configurations(
                    NextToken=marker
                )
            launch_configs.setdefault(region, []).extend(response['LaunchConfigurations'])\

            try:
                marker = response['NextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return launch_configs


# returns the list Elastic load balancers
def list_elb(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_elb()--- ")

    elb_lst = {}

    for region in regions:
        client = self.session.client('elb', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_load_balancers()
            else:
                response = client.describe_load_balancers(
                    Marker=marker
                )
            elb_lst.setdefault(region, []).extend(response['LoadBalancerDescriptions'])

            try:
                marker = response['NextMarker']
                if marker == '':
                    break
            except KeyError:
                break

    return elb_lst
