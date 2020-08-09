from lxml import etree
import re
import csv

# parser = etree.XMLParser(ns_clean=True)
xml = etree.parse('Port.xml')
ns = {'a':'http://www.tresos.de/_projects/DataModel2/08/attribute.xsd'}
# for node in root.iter():
#     print(node.tag)
root = xml.getroot()
res = root.xpath('.//a:tst[contains(@expr, "PortPinPcr, 0")]', namespaces=ns)
patten = r'= (\d*)'
pin_list = []

for pin in res:
    pin_attr = pin.attrib
    pcr_str = pin_attr['expr']
    if pcr_str.find('=3') != -1:
        print(pcr_str)
        continue
    pin_mode = pin_attr['true']
    pin_pcr_number = re.search(patten, pcr_str).group(1)
    pin = [pin_pcr_number, pin_mode]
    pin_list.append(pin)

print(len(pin_list))
file = open('test.csv', 'w', newline='')


ff = csv.writer(file)

ff.writerows(pin_list)




