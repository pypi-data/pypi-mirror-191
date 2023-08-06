"""
Contains the methods to check compliance for ec2
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Checks compliance for EC2 Token Hop limit check
def ec2_token_hop_limit_check(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside ec2 :: ec2_token_hop_limit_check--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id45.2'
    compliance_type = 'EC2 Token hop limit check'
    description = "Checks if an Amazon Elastic Compute Cloud (EC2) instance metadata has a specified token hop limit " \
                  "that is equal to 1"
    resource_type = 'EC2'
    risk_level = 'Medium'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level,
            'ControlId': control_id
        }

    for region, reservations in kwargs['ec2_instances'].items():
        for reservation in reservations:
            for instance in reservation['Instances']:
                try:
                    hop_limit = instance['MetadataOptions']['HttpPutResponseHopLimit']
                    if not hop_limit == 1:
                        result = False
                        failReason = "Hop limit is not set to 1"
                        offenders.append(instance['InstanceId'])
                except KeyError:
                    result = False
                    failReason = "Hop limit is not set to 1"
                    offenders.append(instance['InstanceId'])

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level,
        'ControlId': control_id
    }


# Checks compliance for Ec2 security group attached to eni
def ec2_security_group_attached_to_eni(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside ec2 :: ec2_security_group_attached_to_eni()--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id18.2'
    compliance_type = 'EC2 Security Group Attached to ENI'
    description = "Checks if non-default security groups are attached to Elastic network interfaces (ENIs). The rule " \
                  "is NON_COMPLIANT if the security group is not associated with an elastic network interface (ENI)"
    resource_type = 'EC2'
    risk_level = 'Medium'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level,
            'ControlId': control_id
        }

    associated_security_groups = []
    security_groups = []

    for region, eni_lst in kwargs['eni_lst'].items():
        for eni in eni_lst:
            for group in eni['Groups']:
                associated_security_groups.append(group['GroupId'])

    for region, sg_lst in kwargs['sg_lst'].items():
        for sg in sg_lst:
            if sg['GroupName'] != 'default':
                if not sg['GroupId'] in associated_security_groups:
                    result = False
                    failReason = 'EC2 Security Group Not Attached to ENI'
                    offenders.append(sg['GroupId'])

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level,
        'ControlId': control_id
    }


# Checks compliance for EC2 Instance Role Assigned
def ec2_instance_role_assigned(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside ec2 :: ec2_instance_role_assigned--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id26.1'
    compliance_type = 'EC2 Instance Role Assigned'
    description = "Checks if an Amazon Elastic Compute Cloud (EC2) instance has role assigned"
    resource_type = 'EC2'
    risk_level = 'Medium'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level,
            'ControlId': control_id
        }

    for region, reservations in kwargs['ec2_instances'].items():
        for reservation in reservations:
            for instance in reservation['Instances']:
                try:
                    role = instance['IamInstanceProfile']['Id']
                except KeyError:
                    result = False
                    failReason = "IAM role is not assigned to the EC2 instance"
                    offenders.append(instance['InstanceId'])

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level,
        'ControlId': control_id
    }
