#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""First step for RITE: extract valid information in xml"""

import xml.sax


class DataHandler(xml.sax.ContentHandler):
    """
    override xml handler for sax to convert xml in simple txt
    """

    def __init__(self):
        super().__init__()

        self.__currentLabel = ''
        self.__currentData = ''
        self.result = []
        self.__num = 0

    def startElement(self, name, attr):
        if name == 'pair':
            self.__currentLabel = attr['label']

    def endElement(self, name):
        if name == 't1' or name == 't2':
            self.result.append(str(self.__num) + ' ' + self.__currentData + '\n')
            self.__num += 1

        if name == 't2':
            self.result.append(self.__currentLabel + '\n')

    def characters(self, content):
        self.__currentData = content


def convert_to(xmlName, resultName):
    """
    function to use for converting
    :param xmlName: original xml file path
    :param resultName: result txt file path
    :return: none
    """

    data_handler = DataHandler()

    xml_file = open(xmlName, encoding='utf-8')
    xml_file_read = xml_file.read().replace('&', '%')  # & has another means in xml file
    xml.sax.parseString(xml_file_read, data_handler)
    xml_file.close()

    result_file = open(resultName, 'w', encoding='utf-8')
    result_file.writelines(data_handler.result)
    result_file.close()


if __name__ == '__main__':
    convert_to('../Data/train.xml', '../Data/train.txt')
