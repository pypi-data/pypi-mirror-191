"""
Contains the methods to check compliance for ec2
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Checks the compliance for lambda-function-settings-check
def lambda_function_settings_check(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside lambda_fn :: lambda_function_settings_check()--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id93.1'
    compliance_type = 'Lambda function settings check'
    description = "Checks if the AWS Lambda function settings for runtime, role, timeout, and memory size match " \
                  "the expected values. The rule ignores functions with the 'Image' package type"
    resource_type = 'Lambda'
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

    for region, lambda_list in kwargs['lambda_lst'].items():
        for function in lambda_list:
            if not function['PackageType'] == 'Image':
                mem_size = function['MemorySize']
                timeout = function['Timeout']
                try:
                    role = function['Role']
                    if mem_size == 128 and timeout == 3:
                        pass
                    else:
                        result = False
                        failReason = 'Either memory size or timeout or role does not meet the expected values'
                        offenders.append(function['FunctionName'])

                except KeyError:
                    result = False
                    failReason = 'Either memory size or timeout or role does not meet the expected values'
                    offenders.append(function['FunctionName'])

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