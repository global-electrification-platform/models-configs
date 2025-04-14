import yaml
import csv

with open('minigrid.yml', 'r') as f:
    base = yaml.safe_load(f)

with open('minigrid-iso.csv', 'r') as f:
    reader = csv.DictReader(f, ['name', 'url', 'iso3', 'iso2'])
    countries = [r for r in reader]

for country in countries:
    data = dict(base)
    data['id'] = data['id'] % country['iso2'].lower()
    data['name'] = data['name'] % country['name']
    data['country'] = country['iso2'].lower()
    data['externalUrl'] = country['url']
    data['description'] = data['description'] % country['name']

    with open('data/%s-dre.yml' % country['iso2'].lower(), 'w') as f:
        yaml.dump(data, f)
