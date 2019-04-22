import csv
import json

# .csv file
with open('demo.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

f.close()

# creating json file
with open('test.json', 'w') as f:
    json.dump(rows, f)

f.close()

with open('test.json', 'r') as myfile:
    data = myfile.read()

# Loading json data
obj = json.loads(data)
myfile.close()

# Creating Own filebeat.yml

my_filebeat = open("my_filebeat.yml", "w+")
my_filebeat.write('filebeat.prospectors:')

for item in obj:
    for i in range(len(item['LogPaths'].split(','))):
        tag = [str(item['Env'] + "_" + item['Proj'] + "_" + item['Tags'].split(',')[i])]
        log_path = str(item['LogPaths'].split(',')[i])
        to_be_append = "\n- type: log\n  enabled: true\n  paths:\n    - {}\n  tags: {}\n".format(log_path, tag)
        my_filebeat.write(to_be_append)

inventory_file = open('demo_inventory', 'r')

# Making Dictionary of the Inventory File
d = {}
ip = []
flag = 1
for line in inventory_file:
    l = line.strip().lower()
    if l.startswith('['):
        k = l
    elif line =='\n':
        ip.append(l)
        d[k] = ip
        ip = []
    else:
        ip.append(l)

# Add ips to the filebeat
with open('test.json', 'r') as myfile:
    data = myfile.read()

# Loading json data
obj = json.loads(data)
myfile.close()

env = set()
for item in obj:
    env.add(item['Env'])

hosts = []
for i in env:
    for j in d['[logstash_{}]'.format(i)]:
        if j is '':
            continue
        else:
            hosts.append("{}:5044".format(j))

my_filebeat = open("my_filebeat.yml", "a")

to_be_append = "\noutput.logstash:\n  hosts: {}".format(hosts)
my_filebeat.write(to_be_append)

my_filebeat.close()