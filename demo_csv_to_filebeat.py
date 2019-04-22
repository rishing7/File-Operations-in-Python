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
    data=myfile.read()

# Loading json data
obj = json.loads(data)




# Adding logstash servers from inventory
inventory_file = open('demo_inventory', 'r')

ips_list = []

for item in obj:
    flag=0
    for line in inventory_file.readlines():
        l = line.strip().lower()
        if l == "[logstash_{}]".format(item['Env']):
           flag = 1
           continue          
        if l != "" and flag:
           ips_list.append("{}:5044".format(l))
         
print(ips_list)



# Default filebeat.yml
default_filebeat = open("important_default_files/filebeat.yml", "r")

# Modifying filebeat.yml
my_filebeat = open("my_filebeat.yml", "w+")

for line in default_filebeat.readlines():
 
     l = line.strip().lower()
     flag = 0 
     if l == "filebeat.prospectors:":
	my_filebeat.write(line)
	for item in obj:
            for i in range(len(item['LogPaths'].split(','))):
                tag = []
                tag.append(str(item['Env']+"_"+item['Proj']+"_"+item['Tags'].split(',')[i]))
                log_path = str(item['LogPaths'].split(',')[i])
                to_be_append = "\n- type: log\n  enabled: true\n  paths:\n    - {}\n  tags: {}\n".format(log_path, tag)	  
                my_filebeat.write(to_be_append) 

     # To remove default logpaths and tag      
     elif l == "- type: log" or l == "enabled: false" or l == "paths:" or l == "- /var/log/*.log":
          pass
     else:
          my_filebeat.write(line)
     
     if l == "#output.logstash:":
          my_filebeat.write("output.logstash:\n  hosts: {}".format(ips_list))
          continue
     if l == "output.elasticsearch:":
          my_filebeat.write("#{}".format(l))
          line = next(default_filebeat)
     elif l == "hosts: [\"localhost:9200\"]":
          my_filebeat.write("#{}".format(l))
          line = next(default_filebeat)
