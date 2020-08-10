import xlrd

class PortPin:
    def __init__(self, dict):
        """['PortContainer', 'PortPinName', 'PortPinDirection', 'PortPinDirectionChangeable', 'PortPinHysteresisControl',
         'PortPinId', 'PortPinInitialMode', 'PortPinLevelValue', 'PortPinMode', 'PortPinModeChangeable', 'PortPinOde',
         'PortPinPcr', 'PortPinSafeMode', 'PortPinSlewRate', 'PortPinWithReadBack', 'PortPinWpe', 'PortPinWps']"""
        self.__dict__.update(dict)
        self.PortPinId = str(round(self.PortPinId))
        self.PortPinPcr = str(round(self.PortPinPcr))

class PortContainer:
    def __init__(self, _container_name, _pin_list):

        self.PortNumberOfPortPins = str(len(_pin_list))
        self.container_name = _container_name
        self.pin_list = []
        for idx in _pin_list:
            pin = PortPin(idx)
            self.pin_list.append(pin)





def get_attrib_dict(file_name):
    wb = xlrd.open_workbook(file_name)
    sheet = wb.sheet_by_index(0)
    attrib_name = sheet.row_values(0)
    #print(attrib_name)
    attrib_list = []
    for i in range(1, sheet.nrows):
        attrib_list.append(sheet.row_values(i))

    return attrib_name, attrib_list

def get_one_pin_by_index(attrib_name, attrib_list, index):
    pin_dict ={}
    for col in range(len(attrib_name)):
        pin_dict[attrib_name[col]] = attrib_list[index][col]
    return pin_dict

def get_pin_list(filename):
    attrib_name, attrib_list = get_attrib_dict(filename)
    container_map = set()
    for index in attrib_list:
        container_map.add(index[0])
    #print(container_map)

    container_dict = {}

    for name in container_map:
        container_dict[name] = []

    for pin_idx in range(len(attrib_list)):
        pin = get_one_pin_by_index(attrib_name, attrib_list, pin_idx)
        container_dict[pin['PortContainer']].append(pin)

    return container_dict

def test():

    container_dict = get_pin_list('input.xlsx')

    for key, value in container_dict.items():
        pc = PortContainer(key, value)
        print(pc.pin_list[0].PortPinMode)




#test()