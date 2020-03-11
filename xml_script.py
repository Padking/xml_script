from lxml import etree



# Определяем входные данные
XML_PATH = "D:\\Projects_py\\xml_script\\CD_collection.xml"
XSD_PATH = "D:\\Projects_py\\xml_script\\CD_collection.xsd"
XSL_PATH = "D:\\Projects_py\\xml_script\\CD_collection.xsl"
XML_PATH_NEW = "D:\\Projects_py\\xml_script\\CD_collection_.xml"
LOGFILE_NAME = "process.log"


def validate(xml_path: str, xsd_path: str, log_name=LOGFILE_NAME):
    """ Выполняет валидацию xml-файла по xsd-схеме
    
    :param xml_path: путь к xml-файлу
    :param xsd_path: путь к xsd-файлу
    """

    with open(log_name, 'a', encoding="utf-8") as logfile:
        # Анализируем xsd-файл
        schema_doc = etree.parse(xsd_path)
        logfile.write(f"Начало валидации файла {xml_path}\n")
        schema = etree.XMLSchema(schema_doc)
        try:
            xml_doc = etree.parse(xml_path)
        except etree.XMLSyntaxError as e:
            for error in e.error_log:
                logfile.write(f"В файле {error.filename} | в строке {str(error.line)} | ошибка: {error.message}\n")
        else: # если xml-файл не содержит ошибок
            result_of_validation = schema.validate(xml_doc)
            logfile.write(f"Файл {xml_path} валидный!\n" if result_of_validation else f"Файл {xml_path} невалидный\n")
        finally:
            logfile.write(f"Завершение проверки на валидность файла {xml_path}\n\n")


def convert(xml_path, xsl_path, transformed_xml_path=XML_PATH_NEW, log_name=LOGFILE_NAME):
    """ Выполняет xslt-трансформацию валидного xml-файла
    
    :param xml_path: путь к xml-файлу
    :param xsl_path: путь к xsl-файлу
    :param transformed_xml_path: путь с именем xml-файла после xslt-трансформации
    """

    with open(log_name, 'a', encoding="utf-8") as logfile:
        try:
            logfile.write(f"Начало трансформации файла {xml_path}\n")
            xslroot = etree.parse(xsl_path)
        except etree.XMLSyntaxError as e:
            for error in e.error_log:
                logfile.write(f"В файле {error.filename} | в строке {str(error.line)} | ошибка: {error.message}\n")
        else: # если xsl-файл не содержит ошибок
            transform = etree.XSLT(xslroot)
            xmlroot = etree.parse(xml_path)
            transroot = transform(xmlroot)
            logfile.write(f"Трансформация файла {xml_path} завершена успешно!\n")

            with open(transformed_xml_path, 'w') as f:
                f.write(etree.tostring(transroot).decode())
            # Форматируем xml-файл, прошедший xslt-трансформацию
            parser = etree.XMLParser(resolve_entities=False, strip_cdata=False)
            document = etree.parse(transformed_xml_path, parser)
            document.write(transformed_xml_path, pretty_print=True, encoding='utf-8')
        finally:
            logfile.write(f"Завершение трансформации файла {xml_path}\n\n")


if __name__ == '__main__':
    validate(XML_PATH, XSD_PATH)
    convert(XML_PATH, XSL_PATH)
    validate(XML_PATH_NEW, 'CD_collection_after.xsd')