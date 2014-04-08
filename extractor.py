import xml.etree.ElementTree as ET

inputfile = 'c:\\patenty\\ipg131224\\concated\\USD0695987-20131224.XML'

tree = ET.parse(inputfile)
root = tree.getroot()
print "Document ID:", root.findall('.//publication-reference//document-id//doc-number')[0].text