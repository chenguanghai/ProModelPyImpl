import json
import xml.etree.ElementTree as etree


class JSONConnector:
    def __init__(self, filePath):
        self.data = dict()
        with open(filePath, 'r') as f:
            self.data = json.load(f)

    @property
    def parsed_data(self):
        return self.data


class XMLConnector:
    def __init__(self, filePath):
        self.tree = etree.parse(filePath)

    @property
    def parsed_data(self):
        return self.tree


def connection_factory(filePath):
    if filePath.endswith('json'):
        connector = JSONConnector
    elif filePath.endswith('xml'):
        connector = XMLConnector
    else:
        raise ValueError("不支持的文件类型!{}".format(filePath))
    return connector(filePath)


def connect_to(filePath):
    factory = None
    try:
        factory = connection_factory(filePath)
    except ValueError as e:
        print(e)
    return factory


def main():
    sqlite_factory = connect_to('data/person.sql3')
    print()

    xml_factory = connect_to('data/person.xml')
    xml_data = xml_factory.parsed_data
    liars = xml_data.findall(".//{}[{}='{}']".format('person', 'lastName', 'Liar'))
    print('找到{}个人'.format(len(liars)))
    for liar in liars:
        print("姓:{}".format(liar.find('firstName').text))
        print("名:{}".format(liar.find('lastName').text))
        [print('电话号码:({})'.format(p.attrib['type']), p.text) for p in liar.find('phoneNumbers')]
    print()

    json_factory = connect_to('data/person.json')
    json_data = json_factory.parsed_data
    print('找到{}个食品'.format(len(json_data)))
    for donut in json_data:
        print('名称: {}'.format(donut['name']))
        print('价格: ${}'.format(donut['ppu']))
        [print('配料: {} {}'.format(t['id'], t['type'])) for t in donut['topping']]


if __name__ == '__main__':
    main()
