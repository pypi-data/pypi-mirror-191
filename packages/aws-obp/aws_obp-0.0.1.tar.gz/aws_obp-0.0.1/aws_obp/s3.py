"""
Contains the methods to check compliance for s3
"""

import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Checks compliance for Alarm s3 bucket policy change
def alarm_s3_bucket_policy_change(self, **kwargs) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside s3 :: alarm_s3_bucket_policy_change()--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id25.17'
    compliance_type = 'Alarm S3 Bucket Policy Change'
    description = "Ensure there is an Amazon CloudWatch alarm created and configured in your AWS account " \
                  "to fire each time a S3 bucket configuration change is made."
    resource_type = 'S3'
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

    for region in kwargs['regions']:
        client = self.session.client('cloudwatch', region_name=region)
        response = client.describe_alarms_for_metric(
            MetricName='S3BucketEventCount',
            Namespace='CloudTrailMetrics'
        )
        if len(response['MetricAlarms']) == 0:
            result = False
            failReason = "Alarm does not exists for s3 bucket policy change"

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


# Checks compliance for s3 lifecycle policy check
def s3_lifecycle_policy_check(self) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside s3 :: s3_lifecycle_policy_check()--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id65.2'
    compliance_type = 'S3 lifecycle policy check'
    description = "Checks if a lifecycle rule is configured for an Amazon Simple Storage Service (Amazon S3) bucket. " \
                  "The rule is NON_COMPLIANT if there is no active lifecycle configuration rules or the " \
                  "configuration does not match with the parameter values."
    resource_type = 'S3'
    risk_level = 'Low'

    client = self.session.client('s3')
    buckets_response = client.list_buckets()

    for bucket in buckets_response['Buckets']:
        try:
            config_response = client.get_bucket_lifecycle_configuration(
                Bucket=bucket['Name']
            )
            flag = False
            for rule in config_response['Rules']:
                status = rule['Status']
                if status == 'Enabled':
                    flag = True
                    break

            if not flag:
                result = False
                offenders.append(bucket['Name'])
                failReason = "Either no lifecycle Configuration found, or set to disabled"

        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                result = False
                offenders.append(bucket['Name'])
                failReason = "Either no lifecycle Configuration found, or set to disabled"
            else:
                return {
                    'Result': False,
                    'failReason': e.response['Error']['Code'],
                    'resource_type': resource_type,
                    'Offenders': offenders,
                    'Compliance_type': compliance_type,
                    'Description': description,
                    'Risk Level': risk_level,
                    'ControlId': control_id
                }

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
