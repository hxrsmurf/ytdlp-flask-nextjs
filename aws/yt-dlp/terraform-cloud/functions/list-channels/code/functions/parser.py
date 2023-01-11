import logging

def parse_paginated_info(info):
    logging.info('Parsing info')

    list_of_channels = []

    for page in info:
        items = page['Items']

    for item in items:
        id = item['original_url']['S']
        list_of_channels.append(id)

    return list_of_channels