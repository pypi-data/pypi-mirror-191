"""
Contains the methods to check compliance for rds
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks compliance for RdsClusterIamAuthenticationEnabled
def rds_cluster_iam_authentication_enabled(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside rds :: rds_cluster_iam_authentication_enabled()--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id95.1'
    compliance_type = 'Rds Cluster Iam Authentication Enabled'
    description = "Checks if an Amazon RDS Cluster has AWS Identity and Access Management (IAM) authentication enabled"
    resource_type = 'RDS'
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

    for region, clusters in kwargs['cluster_list'].items():
        for cluster in clusters:
            if not cluster['IAMDatabaseAuthenticationEnabled']:
                result = False
                failReason = 'IAM Database Authentication is not enabled'
                offenders.append(cluster['DBClusterIdentifier'])

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