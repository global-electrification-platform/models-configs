import csv
import io
import subprocess

with open('gep-data.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        iso2 = row['ISO2']
        if 'http' in row['Final Link']:
            url = row['Final Link']
        else:
            url = "https://%s" % (row['Final Link'])
        model = "%s-2" % (iso2)
        print (model, url)
        # warning, funky spacing required
        proc = subprocess.run("cat >> data/%s.yml" % model, shell=True,
                              encoding='utf8',
                              input="""sourceData:
  scenarios: '%s'
  clusters: null
""" % url)
