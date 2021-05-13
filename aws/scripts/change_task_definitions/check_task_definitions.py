# coding: utf-8

import boto3

SECRET_KEY_NAME = 'MIIDAS_SES_PASSWORD'

ecs = boto3.client('ecs')

def list_task_definition_families():
    response = ecs.list_task_definition_families(
        status='ACTIVE',

    )
    task_family_name_array = [ task_family_name for task_family_name in response["families"] ]

    while response.get('nextToken'):
        response = ecs.list_task_definition_families(
            status='ACTIVE',
            nextToken=response['nextToken'],
        )
        task_family_name_array.extend([ task_family_name for task_family_name in response["families"] ])

    return(task_family_name_array)

def check_task_definitions(task_family_name_array):
    for task_family_name in task_family_name_array:
        td = ecs.describe_task_definition(
            taskDefinition=task_family_name,
        )
        for cd in td['taskDefinition']['containerDefinitions']:
            if cd.get('secrets'):
                for secret in cd['secrets']:
                    if secret['name'] == SECRET_KEY_NAME:
                        print(task_family_name)


def main():
    check_task_definitions(list_task_definition_families())

main()