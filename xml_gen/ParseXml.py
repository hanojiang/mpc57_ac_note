import xml.etree.ElementTree as ET
from base import *
import copy

def main():
    container_list = read_container_from_excel('input.xlsx')
    print(container_list)
    prefix = '{http://autosar.org/schema/r4.0}'
    ET.register_namespace('', "http://autosar.org/schema/r4.0")
    tree = ET.parse("./gen_template.xml")
    root = tree.getroot()
    #tree.write('test2.xml')

    for it in root.iter(prefix + 'ECUC-CONTAINER-VALUE'):
        name = it.find(prefix + 'SHORT-NAME')
        if(name.text == 'PortConfigSet'):
            break

    PortConfigSet = it

    subContainer = PortConfigSet.find(prefix + 'SUB-CONTAINERS')

    ## portcontainer[0] is NotUsedPortPin
    PortContainer = subContainer.findall(prefix + 'ECUC-CONTAINER-VALUE')
    #print(len(PortContainer))
    first_port_container = PortContainer[1]

    for idx in range(len(container_list)-1):
        new_ele = copy.deepcopy(first_port_container)
        subContainer.append(new_ele)

    PortContainer = subContainer.findall(prefix + 'ECUC-CONTAINER-VALUE')
    for idx in range(len(PortContainer)-1):
        container_tmp = PortContainer[idx+1]
        port_container_name = container_tmp.find(prefix + 'SHORT-NAME')
        port_container_name.text = container_list[idx].container_name
        port_container_number = container_tmp.find('.//' + prefix + 'VALUE')
        # print(port_container_number)
        port_container_number.text = container_list[idx].PortNumberOfPortPins

        pin_sub_container = container_tmp.find(prefix + 'SUB-CONTAINERS')
        first_pin = pin_sub_container.find(prefix + 'ECUC-CONTAINER-VALUE')
        for pin_idx in range(len(container_list[idx].pin_list)-1):
            new_pin = copy.deepcopy(first_pin)
            pin_sub_container.append(new_pin)

        all_pin = pin_sub_container.findall(prefix + 'ECUC-CONTAINER-VALUE')
        print(len(all_pin))
        for index, pin in enumerate(all_pin):
            pin_name = pin.find(prefix + 'SHORT-NAME')
            pin_name.text = container_list[idx].pin_list[index].PortPinName
            pin_attrib_value = pin.findall('.//' + prefix + 'VALUE')
            # print(container_list[idx].pin_list[index].__dict__)

            for value_idx in range(len(pin_attrib_value)):
                pin_attrib_dict = container_list[idx].pin_list[index].__dict__
                list_tmp = list(pin_attrib_dict.values())
                pin_attrib_value[value_idx].text = list_tmp[value_idx+2]


    tree.write('gen_result.arxml', encoding='UTF-8', xml_declaration=True)






def read_container_from_excel(filename):
    container_dict = get_pin_list(filename)
    container_list = []
    for key, value in container_dict.items():
        pc = PortContainer(key, value)
        container_list .append(pc)
    return container_list


if __name__ == '__main__':
    main()