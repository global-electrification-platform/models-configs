#!/usr/bin/env python

import csv
import requests
import sys
import os


URL = os.environ.get('CKAN_URL')
AUTH = None
API_KEY = os.environ.get('CKAN_API_KEY')

GROUP_ID = '960aa075-ab33-43dd-a09b-f3c7a46cbff1'
owner_org = 'be8e5286-de7f-4759-9766-8b045e698798'

with open(sys.argv[1], 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

def dataset_name(line):
    return line['Final Link'].split('/')[-1]



def to_dataset(line):
    fields = {
        'Source': 'source',
        'country':'country',
        'title':'title',
        'notes':'notes',
        'topic':'topic',
        'country_code':'country_code',
        'region':'region',
        'license':'license_title',
        'Contact point name':'author',
        'Contact point email':'author_email',
        'release_date':'release_date',
        'start_date':'start_date',
        'end_date':'end_date',
        'group':'group',
        }

    # get groups/resolve group: GEP
    # org name/id: WBG

    dataset = {
        'private': False,
        'name': dataset_name(line),
        'license_id': 'CC-BY-4.0',
        'status': 'Complete',
        'owner_org': owner_org,
        }

    for source, target in fields.items():
        dataset[target] = line[source]

    def _fix(s):
        s = s.strip()
        s = s.capitalize()
        return s

    for field in ('country_code', 'topic'):
        if ';' in dataset[field]:
            dataset[field] = [_fix(s) for s in dataset[field].split(';')]
        else:
            dataset[field] = [ dataset[field] ]

    return dataset


def _fetch(action, params):

    resp = requests.get(URL + 'api/action/' + action,
                            headers={'X-CKAN-API-Key':API_KEY},
                            auth=AUTH,
                            params=params)
    return resp.json()['result']


def _modify(action, data):
    try:
        resp = requests.post(URL + 'api/action/' + action,
                             headers={'X-CKAN-API-Key':API_KEY},
                             auth=AUTH,
                             data=data)
        return resp.json()['result']
    except Exception as msg:
        pdb.post_mortem()
        raise


def fetch_dataset(line):
    return _fetch('package_show', {'id': dataset_name(line)})

def fetch_resource(rid):
    return _fetch('resource_show', {'id': rid})

def resource_patch(data):
    return _modify('resource_patch', data)

def resource_create(data):
    return _modify('resource_create', data)

def dataset_create(data):
    return _modify('package_create', data)

def dataset_patch(data):
    return _modify('package_patch', data)

def resource_reorder(data):
    return _modify('package_resource_reorder', data)


def ensure_dataset(line):
    try:
        dataset = fetch_dataset(line)
        return False
    except:
        dataset = dataset_create(to_dataset(line))
        add_v1_resources(line)
        return True

def update_resource_names(line):
    dataset = fetch_dataset(line)

    name_map = {
        'Energy Modeling Parameters': 'GEP V1 Energy Modeling Parameters',
        'GEP Scenario Results': 'GEP V1 Scenario Results',
        'Output Column Description': 'GEP V1 Output Column Description',
    }

    for resource in dataset['resources']:
        if resource['name'] not in name_map:
            continue

        resource_patch({'id': resource['id'], 'name':name_map[resource['name']]})
        print("patched %s: %s" % (dataset_name(line), name_map[resource['name']]))


def upload_resource(data, dataset):
    data['package_id'] = dataset['id']
    resource_create(data)


def add_new_resources(line, resources):
    dataset = fetch_dataset(line)

    for resource in resources:
        for existing in dataset['resources']:
            if resource['name'] == existing['name']:
                for k,v in resource.items():
                    if existing.get(k,None) != v:
                        break
                else:
                    break

                resource['id'] = existing['id']
                resource_patch(resource)
                break
        else:
            upload_resource(resource, dataset)




def add_v3_resources(line):
    iso2 = line['ISO2']

    resources = [
        {
            'name': 'GEP Climate Energy Modeling Parameters',
            'format': 'CSV',
            'description': 'Input parameters for the Climate model',
            'url': 'https://gep-source-archive.s3.amazonaws.com/GEP-Climate-2022/%s/inputs/%s-3-country-inputs.csv' % (iso2, iso2),
            'data-transform': '',
        },
        {
            'name': 'GEP Climate Secenario Specs',
            'format': 'XLSX',
            'description': 'Scenario Option Specifications',
            'url': 'https://gep-source-archive.s3.amazonaws.com/GEP-Climate-2022/%s/inputs/%s-3-specs.xlsx' % (iso2, iso2),
            'data-transform': '',
        },
        {
            'name': 'GEP Climate Scenario Results',
            'format': 'ZIP',
            'description': 'Zipfile of all 95 scenario results in CSV format',
            'url': 's3://gep-source-archive/GEP-Climate-2022/%s/outputs/%s-3-scenarios-results.zip' %(iso2, iso2),
        },
        {
            'name': 'GEP Climate Scenario Summaries',
            'format': 'ZIP',
            'description': 'Zipfile of all 95 scenario summaries in CSV format',
            'url': 'https://gep-source-archive.s3.amazonaws.com/GEP-Climate-2022/%s/outputs/%s-3-scenarios-summaries.zip' %(iso2, iso2),
        },
        {
            'name': 'GEP Climate Output Column Description',
            'format': 'DOC',
            'description': 'Description of the output columns in the Scenario Results',
            'url': 'https://gep-source-archive.s3.amazonaws.com/GEP-Climate-2022/GEP V.3 Column Description.xlsx',
        },
    ]

    return add_new_resources(line, resources)


def add_v2_resources(line):
    iso2 = line['ISO2']

    resources = [
        {
            'name': 'GEP V2 Energy Modeling Parameters',
            'format': 'PDF',
            'description': 'Input parameters for the V2 model',
            'url': 'https://gep-source-archive.s3.amazonaws.com/models-2021/%s-2/%s-2-scenario-description.pdf' %(iso2, iso2)
        },
        {
            'name': 'GEP V2 Scenario Results',
            'format': 'ZIP',
            'description': 'Zipfile of all 95 scenario results in CSV format',
            'url': 's3://gep-source-archive/models-2021/%s-2/outputs/%s-2-scenarios-results.zip' %(iso2, iso2)
        },
        {
            'name': 'GEP V2 Output Column Description',
            'format': 'DOC',
            'description': 'Description of the output columns in the Scenario Results',
            'url': 'https://gep-source-archive.s3.amazonaws.com/Description-of-output-columns_GEP_V2.docx'
        },
        {
            'name': 'GEP V2 Solar Resource',
            'format': 'CSV',
            'description': 'Hourly Solar GHI',
            'url': 's3://gep-source-archive/models-2021/%s-2/inputs/%s-2-pv.csv' %(iso2, iso2)
        },
        {
            'name': 'GEP V2 Wind Resource',
            'format': 'CSV',
            'description': 'Hourly Wind Velocity',
            'url': 's3://gep-source-archive/models-2021/%s-2/inputs/%s-2-wind.csv' %(iso2, iso2)
        }
    ]

    return add_new_resources(line, resources)

def add_v1_resources(line):
    iso2 = line['ISO2']

    resources = [
        {
            'name': 'GEP V1 Energy Modeling Parameters',
            'format': 'PDF',
            'description': 'Input parameters for the V1 model',
            'url': 'https://gep-source-archive.s3.amazonaws.com/models-august-2019/%s-1/%s-1-scenario-description.pdf' %(iso2, iso2)
        },
        {
            'name': 'Settlement Clusters',
            'format': 'SHP ZIP',
            'description': 'Settlement cluster shapefile',
            'url': 's3://gep-source-archive/Clusters with WB admin/%s-1.zip' %(iso2,)
        },
        {
            'name': 'GEP V1 Scenario Results',
            'format': 'ZIP',
            'description': 'Zipfile of all 216 scenario results in CSV format',
            'url': 's3://gep-source-archive/models-august-2019/%s-1/outputs/%s-1-scenarios-results.zip' %(iso2, iso2)
        },
        {
            'name': 'GEP V1 Output Column Description',
            'format': 'DOC',
            'description': 'Description of the output columns in the Scenario Results',
            'url': 'https://gep-source-archive.s3.amazonaws.com/Description-of-output-columns.docx'
        },
    ]

    return add_new_resources(line, resources)



def sort_resource_order(line):
    dataset = fetch_dataset(line)
    v1 = [r for r in dataset['resources'] if 'V1' in r['name']]
    v2 = [r for r in dataset['resources'] if 'V2' in r['name']]
    v3 = [r for r in dataset['resources'] if 'Climate' in r['name']]
    others = [r for r in dataset['resources'] if not ('V1' in r['name'] or 'V2' in  r['name'] or 'Climate' in r['name'])]

    resources = others
    resources.extend(v3)
    resources.extend(v2)
    resources.extend(v1)
    if not len(resources) == len(dataset['resources']):
        print ("Error: resource lists are different length: %s, %s" %(resources, dataset['resources']))
        raise Exception()
    resource_reorder({'id': dataset['id'], 'order': [r['id'] for r in resources]})

def update_dataset(dataset, line):
    print("Patching %s" % line['country'])

    if not dataset.get('groups'):
        _modify('member_create', {
            'id': GROUP_ID,
            'object': dataset['id'],
            'object_type': 'package',
            'capacity': 'public',
            })

    return dataset_patch({'id': dataset['id'],
                          'url': 'https://electrifynow.energydata.info/countries/%s/models' % line['ISO2'].upper(),
                          'topic': ['Energy access'],
                          'notes': '''[The Global Electrification Platform (GEP)](https://electrifynow.energydata.info) is a multi-phase project led by the World Bank to standardize and simplify the use of geospatial tools for least-cost electrification planning. The GEP provides a high-level overview of the technology mix (grid and off-grid) required to achieve universal access by 2030. It focuses on the countries with access rates below 90 percent and the 50 countries with the highest population deficit, with an intermediated investment prospectus for 2025. The results of the model indicate the least-cost investment requirements based on publicly available information on demand and existing infrastructure.'''
                          })


import pdb

for line in data:

    dataset = fetch_dataset(line)
    dataset = update_dataset(dataset, line)

    # print ("Adding resources %s" % line['country'])
    # add_v3_resources(line)

    #print ("Sorting resources %s" % line['country'])
    #sort_resource_order(line)
