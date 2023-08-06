"""
Contains the methods to check compliance for Load Balancers
"""

import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Checks the compliance for alb-http-drop-invalid-header-enabled
def alb_http_drop_invalid_header_enabled(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside lb :: alb_http_drop_invalid_header_enabled()--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.4'
    compliance_type = 'ALB HTTP drop invalid header enabled'
    description = "Checks if rule evaluates AWS Application Load Balancers (ALB) to ensure they are configured to " \
                  "drop http headers. The rule is NON_COMPLIANT if the value of " \
                  "routing.http.drop_invalid_header_fields.enabled is set to false"
    resource_type = 'ELB'
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

    for region, lb_list in kwargs['lb_list'].items():
        client = self.session.client('elbv2', region_name=region)
        for lb in lb_list:
            if lb['Type'] == 'application':
                response = client.describe_load_balancer_attributes(
                    LoadBalancerArn=lb['LoadBalancerArn']
                )
                for attr in response['Attributes']:
                    if attr['Key'] == 'routing.http.drop_invalid_header_fields.enabled' and attr['Value'] == 'false':
                        result = False
                        failReason = 'ALB http drop invalid header fields is not enabled'
                        offenders.append(lb['LoadBalancerName'])

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


# checks the compliance for alb-waf-enabled
def alb_waf_enabled(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside lb :: alb_waf_enabled()--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.6'
    compliance_type = 'ALB WAF Enabled'
    description = "Checks if Web Application Firewall (WAF) is enabled on Application Load Balancers (ALBs). " \
                  "This rule is NON_COMPLIANT if key: waf.enabled is set to false"
    resource_type = 'ELB'
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

    for region, lb_list in kwargs['lb_list'].items():
        client = self.session.client('elbv2', region_name=region)
        for lb in lb_list:
            if lb['Type'] == 'application':
                response = client.describe_load_balancer_attributes(
                    LoadBalancerArn=lb['LoadBalancerArn']
                )
                found = False
                for attr in response['Attributes']:
                    if attr['Key'] == 'waf.enabled':
                        found = True
                        if attr['Value'] == 'false':
                            result = False
                            failReason = 'ALB WAF is not enabled'
                            offenders.append(lb['LoadBalancerName'])
                        break

                if not found:
                    result = False
                    failReason = 'ALB WAF is not enabled'
                    offenders.append(lb['LoadBalancerName'])

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


# checks the compliance for elbv2-multiple-az
def elbv2_multiple_az(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside lb :: elbv2_multiple_az()--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id30.4'
    compliance_type = 'ELBV2 Multiple AZ'
    description = "Checks if an Elastic Load Balancer V2 (Application, Network, or Gateway Load Balancer) has " \
                  "registered instances from multiple Availability Zones (AZ's). The rule is NON_COMPLIANT if an " \
                  "Elastic Load Balancer V2 has instances registered in less than 2 AZ's"
    resource_type = 'ELB'
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

    for region, lb_list in kwargs['lb_list'].items():
        for lb in lb_list:
            if len(lb['AvailabilityZones']) <= 1:
                result = False
                failReason = "Elastic Load Balancer V2 has instances registered in less than 2 AZ's"
                offenders.append(lb['LoadBalancerName'])

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


# checks compliance for elbv2 acm certificate required
def elbv2_acm_certificate_required(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside lb :: elbv2_acm_certificate_required()---  ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.51'
    compliance_type = 'ELBV2 ACM Certificate Required'
    description = "Checks if Application Load Balancers and Network Load Balancers have listeners that are " \
                  "configured to use certificates from AWS Certificate Manager (ACM). This rule is NON_COMPLIANT " \
                  "if at least 1 load balancer has at least 1 listener that is configured without a certificate " \
                  "from ACM or is configured with a certificate different from an ACM certificate"
    resource_type = 'ELB'
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

    for region, lb_list in kwargs['lb_list'].items():
        client = self.session.client('elbv2', region_name=region)
        for lb in lb_list:
            if lb['Type'] in ['application', 'network']:
                marker = ''
                while True:
                    if marker == '':
                        response = client.describe_listeners(
                            LoadBalancerArn=lb['LoadBalancerArn']
                        )
                    else:
                        response = client.describe_listeners(
                            LoadBalancerArn=lb['LoadBalancerArn'],
                            Marker=marker
                        )
                    for listener in response['Listeners']:
                        try:
                            for certificate in listener['Certificates']:
                                if not certificate['CertificateArn'].startswith("arn:aws:acm:"):
                                    result = False
                                    failReason = "Load Balancer listener is configured without certificate from ACM or " \
                                                 "is configured with a certificate different from an ACM certificate"
                                    offenders.append(lb['LoadBalancerArn'])
                        except KeyError:
                            result = False
                            failReason = "Load Balancer listener is configured without certificate from ACM or " \
                                         "is configured with a certificate different from an ACM certificate"
                            offenders.append(lb['LoadBalancerArn'])

                    try:
                        marker = response['NextMarker']
                        if marker == '':
                            break
                    except KeyError:
                        break

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


# checks the compliance for elb-multiple-az
def clb_multiple_az(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside lb :: clb_multiple_az()--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id56.3'
    compliance_type = 'CLB Multiple AZ'
    description = "Checks if a Classic Load Balancer spans multiple Availability Zones (AZs). The rule is " \
                  "NON_COMPLIANT if a Classic Load Balancer spans less than 2 AZs"
    resource_type = 'ELB'
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

    for region, lb_list in kwargs['lb_list'].items():
        for lb in lb_list:
            if len(lb['AvailabilityZones']) <= 1:
                result = False
                failReason = "Classic Load Balancer has instances registered in less than 2 AZ's"
                offenders.append(lb['LoadBalancerName'])

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

#
# # Checks compliance for ELB predefined security policy ssl check
# def elb_predefined_security_policy_ssl_check(self, **kwargs) -> dict:
#     """
#     :param self:
#     :param kwargs:
#     :return:
#     """
#     logger.info(" ---Inside lb :: elb_predefined_security_policy_ssl_check()--- ")
#
#     result = True
#     failReason = ''
#     offenders = []
#     control_id = 'Id6.4'
#     compliance_type = 'ELB Predefined Security Policy SSL check'
#     description = "Checks whether your Classic Load Balancer SSL listeners are using a predefined policy. The rule " \
#                   "is only applicable if there are SSL listeners for the Classic Load Balancer"
#     resource_type = 'ELB'
#     risk_level = 'Medium'
#
#     if 'exception' in kwargs.keys() and kwargs['exception']:
#         return {
#             'Result': False,
#             'failReason': kwargs['exception_text'],
#             'resource_type': resource_type,
#             'Offenders': offenders,
#             'Compliance_type': compliance_type,
#             'Description': description,
#             'Risk Level': risk_level,
#             'ControlId': control_id
#         }
#
#     for region, lb_list in kwargs['lb_list'].items():
#         client = self.session.client('elb', region_name=region)
#         for lb in lb_list:
#             try:
#                 response = client.describe_load_balancer_policies(
#                     LoadBalancerName=lb['LoadBalancerName']
#                 )
#                 for desc in response['PolicyDescriptions']:
#                     for attr in desc['PolicyAttributeDescriptions']:
#                         if attr['AttributeName'] == 'Reference-Security-Policy' and attr['AttributeValue'] not in ['ELBSecurityPolicy-2016-08', 'ELBSecurityPolicy-TLS-1-2-2017-01', 'ELBSecurityPolicy-TLS-1-1-2017-01']:
#                             result = False
#                             offenders.append(lb['LoabBalancerName'])
