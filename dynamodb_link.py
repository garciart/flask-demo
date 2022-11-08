import boto3
from validator import (validate_integer, validate_regex_match, validate_type, )

resource = boto3.resource('dynamodb', region_name='us-east-1')

med_table = resource.Table('medications')

# Lookahead to prevent injections that use dashes or pluses (e.g., 'rm -rf', etc.)
lookahead_regex = r'(?!.+?(?: -|\- | \+|\+ |\+\-|\-\+|\-\-).+?)'
# Short descriptions must start and end with a letter
# Details must start with a letter and end with a letter or period
# Regex for name, action, and condition
short_desc_regex = r'^' + lookahead_regex + r'([A-Z])([A-Z\d\-\+ ]{1,32})([A-Z])$'
# Regex for interactions, side effects, and warnings
details_regex = r'^' + lookahead_regex + r'([A-Z])([A-Z\d\-\+\,\. ]{1,255})([A-Z\.])$'
link_regex = r'^http([s]?)\:\/\/[A-Za-z\d\.\_\-\/]{1,255}$'


def get_items() -> object:
    """Gets all the data from the DynamoDB database.

    :return: The data from the DynamoDB database
    :rtype: dict
    """
    all_items = med_table.scan()
    return all_items['Items']


def create_item(generic_name,
                brand_name,
                action,
                conditions,
                side_effects,
                interactions,
                warnings,
                link,
                *,
                schedule,
                blood_thinner):
    # type: (str, str, str, list, str, str, str, str, object, int, bool) -> dict
    """
    """
    # Validate inputs
    validate_regex_match(generic_name, short_desc_regex, err_msg='Invalid generic name.')
    validate_regex_match(brand_name, short_desc_regex, err_msg='Invalid brand name.')
    validate_regex_match(action, short_desc_regex, err_msg='Invalid action.')
    [validate_regex_match(
        c, short_desc_regex, err_msg='Invalid condition.') for c in conditions]
    validate_regex_match(side_effects, details_regex,
                         err_msg='Side effects contains invalid characters.')
    validate_regex_match(interactions, details_regex,
                         err_msg='Interactions contains invalid characters.')
    validate_regex_match(warnings, details_regex, err_msg='Warnings contains invalid characters.')
    validate_regex_match(link, link_regex, err_msg='Invalid reference link.')
    validate_integer(schedule, min_val=0, max_val=4)
    validate_type(blood_thinner, bool)

    # Convert key to upper before put
    generic_name = generic_name.upper()
    # Add to database or raise and exception if the key already exists
    response = med_table.put_item(
        Item={
            'generic_name': generic_name,
            'brand_name': brand_name.upper(),
            'action': action.upper(),
            'conditions': set([c.upper() for c in conditions]),
            'side_effects': side_effects,
            'interactions': interactions,
            'warnings': warnings,
            'link': link,
            'schedule': int(schedule),
            'blood_thinner': bool(blood_thinner),
        },
        ConditionExpression='generic_name <> :uid',
        ExpressionAttributeValues={':uid': generic_name}
    )
    return response


def read_item(generic_name):
    # type: (str) -> dict
    """
    """
    # Validate inputs
    validate_regex_match(generic_name, short_desc_regex, err_msg='Invalid generic name.')

    response = med_table.get_item(
        Key={
            'generic_name': generic_name
        },
        AttributesToGet=[
            'generic_name',
            'brand_name',
            'action',
            'conditions',
            'side_effects',
            'interactions',
            'warnings',
            'link',
            'schedule',
            'blood_thinner',
        ]
    )
    return response


def update_item(generic_name,
                brand_name,
                action,
                conditions,
                side_effects,
                interactions,
                warnings,
                link,
                *,
                schedule=0,
                blood_thinner=False):
    # type: (str, str, str, list, str, str, str, str, object, int, bool) -> dict
    """
    """
    # Validate inputs
    validate_regex_match(generic_name, short_desc_regex, err_msg='Invalid generic name.')
    validate_regex_match(brand_name, short_desc_regex, err_msg='Invalid brand name.')
    validate_regex_match(action, short_desc_regex, err_msg='Invalid action.')
    [validate_regex_match(
        c, short_desc_regex, err_msg='Invalid condition.') for c in conditions]
    validate_regex_match(side_effects, details_regex,
                         err_msg='Side effects contains invalid characters.')
    validate_regex_match(interactions, details_regex,
                         err_msg='Interactions contains invalid characters.')
    validate_regex_match(warnings, details_regex,
                         err_msg='Warnings contains invalid characters.')
    validate_regex_match(link, link_regex, err_msg='Invalid reference link.')
    validate_integer(schedule, min_val=0, max_val=4)
    validate_type(blood_thinner, bool)

    response = med_table.update_item(
        Key={
            'generic_name': generic_name.upper()
        },
        AttributeUpdates={
            'brand_name': {
                'Value': brand_name.upper(),
                'Action': 'PUT'
            },
            'action': {
                'Value': action.upper(),
                'Action': 'PUT'
            },
            'conditions': {
                'Value': set([c.upper() for c in conditions]),
                'Action': 'PUT'
            },
            'side_effects': {
                'Value': side_effects,
                'Action': 'PUT'
            },
            'interactions': {
                'Value': interactions,
                'Action': 'PUT'
            },
            'warnings': {
                'Value': warnings,
                'Action': 'PUT'
            },
            'link': {
                'Value': link,
                'Action': 'PUT'
            },
            'schedule': {
                'Value': int(schedule),
                'Action': 'PUT'
            },
            'blood_thinner': {
                'Value': bool(blood_thinner),
                'Action': 'PUT'
            },
        },
    )
    return response


def delete_item(generic_name):
    # type: (str) -> dict
    """
    """
    # Validate inputs
    validate_regex_match(generic_name, short_desc_regex, err_msg='Invalid generic name.')

    response = med_table.delete_item(
        Key={
            'generic_name': generic_name.upper()
        }
    )
    return response
