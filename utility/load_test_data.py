import os
import xml.etree.ElementTree as ET


#Extracting the correct URL from hive-site.xml
tree = ET.parse('/etc/hadoop/conf/hive-site.xml')
root = tree.getroot()

for prop in root.findall('property'):
    if prop.find('name').text == "hive.metastore.warehouse.dir":
        storage = prop.find('value').text.split("/")[0] + "//" + prop.find('value').text.split("/")[2]


print("The correct S3 URL is:{}".format(storage))

os.environ['STORAGE'] = storage


!hdfs dfs -put data/customer_support_tickets.json ${STORAGE}${DIRECTORY}