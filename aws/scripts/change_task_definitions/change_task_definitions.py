# coding: utf-8

import argparse
import boto3

NEW_SECRETS = {} 

ecs = boto3.client('ecs')

def get_task_definitions(task_family_name):
    td = ecs.describe_task_definition(
        taskDefinition=task_family_name,
    )
    return(td)

def change_task_definitions(td):
    for cd in td['taskDefinition']['containerDefinitions']:
        if 0 != len(cd['secrets']):
            cd['secrets'].append(NEW_SECRETS)
    print(td)
    return(td)

def register_task_definition(td):
    taskRoleArn = td['taskDefinition']['taskRoleArn'] if td['taskDefinition'].get('taskRoleArn') else ""
    executionRoleArn = td['taskDefinition']['executionRoleArn'] if td['taskDefinition'].get('executionRoleArn') else ""
    requiresCompatibilities = td['taskDefinition']['requiresCompatibilities'] if td['taskDefinition'].get('requiresCompatibilities') else []
    cpu = td['taskDefinition']['cpu'] if td['taskDefinition'].get('cpu') else ""
    memory = td['taskDefinition']['memory'] if td['taskDefinition'].get('memory') else ""

    response = ecs.register_task_definition(
        family=td['taskDefinition']['family'],
        taskRoleArn=taskRoleArn,
        executionRoleArn=executionRoleArn,
        networkMode=td['taskDefinition']['networkMode'],
        containerDefinitions=td['taskDefinition']['containerDefinitions'],
        volumes=td['taskDefinition']['volumes'],
        placementConstraints=td['taskDefinition']['placementConstraints'],
        requiresCompatibilities=requiresCompatibilities,
        # Fargateの場合のみcpu,memを指定する
        #cpu=cpu,
        #memory=memory,
    )
    print(response)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('family')
    args = parser.parse_args()
    print('Target family name' + args.family)

    td = get_task_definitions(args.family)
    new_td = change_task_definitions(td)
    register_task_definition(new_td)

main()