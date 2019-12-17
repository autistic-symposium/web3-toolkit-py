# -*- coding: utf-8 -*-
# Wrapper for K8s API

import os

from kubernetes import client, config
from wrappers.settings import ORG, K8S_ENV_LIST


def get_pod_data(namespace):
    ''' Retrieve and return data from K8s from a given namepasce.'''

    config.load_kube_config()
    api_instance = client.CoreV1Api()

    try:
        ret = api_instance.list_pod_for_all_namespaces(watch=False)

        ip_list, name_list, stat_list = [], [], []
        for item in ret.items:
            if (item.metadata.namespace != namespace):
                continue
            
            ip_list.append(item.status.pod_ip)
            name_list.append(item.metadata.name)
            stat_list.append(item.status.phase)

        dtag_list, dimage_list = [], []
        for pod in name_list:
            dtag_str, dimage_str = get_pod_info(namespace, api_instance, pod)
            dtag_list.append(dtag_str)
            dimage_list.append(dimage_str)


        return { 
                'Status': stat_list,
                'Name': name_list,
                'Pod IP': ip_list, 
                'Docker Image': dimage_list,
                'Docker Tag': dtag_list
                }

    except Exception as e:
        print("Error retrieving K8s data: \n{}".format(e))
        return None

def generate_env_dict():
    ''' Retrieve K8s namespaces from env, and return a dict of it. '''
    env_list = K8S_ENV_LIST.split(',')
    return [{'label': i.strip(), 'value': i.strip()} for i in env_list]


def get_pod_info(namespace, api_instance, pod_name):
    ''' Retrieve the Docker info from a given pod. '''
    api_response = api_instance.read_namespaced_pod(pod_name, namespace)

    dtag_str, dimage_str = '', ''
    if len(api_response.spec.containers) < 2:
        dimage_str, dtag_str = api_response.spec.containers[0].image.split(':')
    else:
        for container in api_response.spec.containers:
            im, tg = container.image.split(':')
            dimage_str += '{}; '.format(im)
            dtag_str += '{}; '.format(tg)
    
    
    return dtag_str, dimage_str 


if __name__ == '__main__':

    test_namespace = 'staging'
    print('Printing k8s data for giving namespace')
    print(get_pod_data(test_namespace))

