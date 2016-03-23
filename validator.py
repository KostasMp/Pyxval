#!/usr/bin/python

import sys
from lxml import etree
import argparse

parser = argparse.ArgumentParser(description='Check for a given xml file, if it is well formed, or validate it according to a specified schema...')
parser.add_argument('xml', nargs='+', help='The xml file to be  validated')
parser.add_argument('-s','--schema', help='The schema, against which, the xml file will be validated')

args = parser.parse_args()
xml_src = args.xml

if args.schema:
    schema_src = args.schema
    try:
        xmlschema_doc = etree.parse(schema_src)
        xmlschema = etree.XMLSchema(xmlschema_doc)

    except etree.XMLSchemaParseError as parse_err:
        print parse_err
        print "Ignoring..."
    except IOError as xsd_io_err:
        print xsd_io_err

for xml in xml_src:
    try:
        xml_doc = etree.parse(xml)
    except etree.XMLSyntaxError as syntax_err:
        print "The xml file " + xml + " is not well-formed..."
        print syntax_err
        continue
    except IOError as io_err:
        print io_err
        continue

    validation = xmlschema.validate(xml_doc)

    if validation == False:
        err_log = xmlschema.error_log
        print err_log
    else:
        print "File " + xml + " is built according to the schema"
