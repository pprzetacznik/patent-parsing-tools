import os
import re
import lxml.etree as ET
import json
from pkg_resources import resource_stream

# from patent_parsing_tools import Patent, log
from patent_parsing_tools.utils.log import log


class NotSupportedDTDConfiguration(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


@log
class Extractor:
    def __init__(self, dir="."):
        self.dir = dir
        if not os.path.isdir(dir):
            os.makedirs(dir)
        json_data = resource_stream(
            "patent_parsing_tools.config", "extractor_configuration.json"
        )
        self.structure = json.load(json_data)
        json_data.close()

    def parse(self, inputfile):
        tree = ET.parse(inputfile)
        root = tree.getroot()

        try:
            dtdStructure = self.getDTDXpathConfiguration(inputfile, tree)
        except NotSupportedDTDConfiguration as e:
            self.logger.warning(e.message)
            raise e

        patent = Patent()
        patent.documentID = root.findall(dtdStructure["documentID"])[0].text
        patent.title = root.findall(dtdStructure["inventionTitle"])[0].text
        patent.date = root.findall(dtdStructure["date"])[0].text
        patent.abstract = self.node_to_text(
            inputfile, root, dtdStructure, "abstract"
        )
        patent.description = self.node_to_text(
            inputfile, root, dtdStructure, "description"
        )
        patent.claims = self.node_to_text(
            inputfile, root, dtdStructure, "claims"
        )

        section = root.findall(dtdStructure["section"])
        clazz = root.findall(dtdStructure["class"])
        subclass = root.findall(dtdStructure["subclass"])
        main_group = root.findall(dtdStructure["main-group"])
        subgroup = root.findall(dtdStructure["subgroup"])

        list_of_patent_classes = []
        for n in range(1, len(section)):
            list_of_patent_classes.append(
                [
                    section[n].text,
                    clazz[n].text,
                    subclass[n].text,
                    main_group[n].text,
                    subgroup[n].text,
                ]
            )
        patent.classification = list_of_patent_classes
        return patent

    def node_to_text(self, inputfile, root, structure, filepart):
        try:
            node = root.findall(structure[filepart])[0]
            text = ET.tostring(node, pretty_print=True).decode()
            return re.sub("<[^<]+?>", "", text)
        except IndexError as e:
            self.logger.warning(f"Message: {e}")
            self.logger.warning(
                f"Node: {filepart} doesn't exists in file: {inputfile}"
            )
        return None

    def getDTDXpathConfiguration(self, inputfile, tree):
        try:
            dtdFile = tree.docinfo.internalDTD.system_url
        except Exception:
            raise NotSupportedDTDConfiguration(
                f"File: {inputfile} has not supported xml structure"
            )

        try:
            return self.structure[dtdFile]
        except Exception:
            raise NotSupportedDTDConfiguration(
                f"File: {inputfile} has not implemented structure ("
                + f"{dtdFile})"
            )
