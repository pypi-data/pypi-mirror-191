"""
Contains the methods to check compliance for auto scaling
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Checks the compliance for auto-scaling multiple az
def auto_scaling_multiple_az(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside auto_scaling :: auto_scaling_multiple_az()--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id85.4'
    compliance_type = 'Auto Scaling Multiple AZ'
    description = "Checks if the Auto Scaling group spans multiple Availability Zones. The rule is NON_COMPLIANT " \
                  "if the Auto Scaling group does not span multiple Availability Zones"
    resource_type = 'Auto Scaling'
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

    for region, asg_lst in kwargs['asg_lst'].items():
        for asg in asg_lst:
            if len(asg['AvailabilityZones']) <= 1:
                result = False
                failReason = 'AWS Auto Scaling Group can launch EC2 instances only within a single Availability Zone'
                offenders.append(asg['AutoScalingGroupName'])

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


# checks compliance for Auto Scaling launch config requires imdsv2
def auto_scaling_launch_config_requires_imdsv2(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside auto_scaling :: auto_scaling_launch_config_requires_imdsv2()--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id85.3'
    compliance_type = 'Auto Scaling Launch Configuration Requires IMDSV2'
    description = "Checks whether only IMDSv2 is enabled. This rule is NON_COMPLIANT if the " \
                  "Metadata version is not included in the launch configuration or if both Metadata " \
                  "V1 and V2 are enabled"
    resource_type = 'Auto Scaling'
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

    for region, lc_list in kwargs['launch_config_list'].items():
        for lc in lc_list:
            try:
                httpTokens = lc['MetadataOptions']['HttpTokens']
            except KeyError:
                result = False
                failReason = 'Either metadata version 1 is used or configuration not found'
                offenders.append(lc['LaunchConfigurationName'])
            else:
                if httpTokens == 'optional':
                    result = False
                    failReason = 'Either metadata version 1 is used or configuration not found'
                    offenders.append(lc['LaunchConfigurationName'])

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


# checks compliance for Auto Scaling launch config hop limit
def auto_scaling_launch_config_hop_limit(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside auto_scaling :: auto_scaling_launch_config_hop_limit--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id85.2'
    compliance_type = 'Auto Scaling Launch Configuration Hop Limit'
    description = "Checks the number of network hops that the metadata token can travel. This rule is NON_COMPLIANT " \
                  "if the Metadata response hop limit is greater than 1"
    resource_type = 'Auto Scaling'
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

    for region, lc_list in kwargs['launch_config_list'].items():
        for lc in lc_list:
            try:
                hoplimit = lc['MetadataOptions']['HttpPutResponseHopLimit']
            except KeyError:
                result = False
                failReason = 'Either Hop limit is greater than 1 or configuration not found'
                offenders.append(lc['LaunchConfigurationName'])
            else:
                if hoplimit >1:
                    result = False
                    failReason = 'Either Hop limit is greater than 1 or configuration not found'
                    offenders.append(lc['LaunchConfigurationName'])

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