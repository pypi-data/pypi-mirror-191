import json
import pandas as pd
import sys

class fairy_data:
    """fairy data  from CSV file and output them as single JSON_LD format file"""

    def json_generate(self, workon):

        """generate valid JSON-LD format output file

        Args:
            workon(list):current processing dataframe

        Returns:
            str:JSON-lD format string
        """
        full_header_str = ""
        full_list = ""
        for i in range(len(self.header)):
            full_header_str = full_header_str + str(self.header[i]) + ","
        for j in range(len(self.working_on)):
            full_list += self.working_on_key[j] + ":" + str(workon[j]) + ","
        top_json = '{' + '"@context"' + ':' + str(self.context) + "," + full_header_str + full_list[:-1] + "}"
        top_json = top_json.replace("'", '"')
        return top_json

    def fair_dataframe(self, csv_df):

        """Fairy data file from dataframe and process input data into single JSON-LD file

        Args:
            csv_df(path): dataframe file path want to be process
        """

        count = 0
        for i in csv_df.index:
            work_list = self.working_on
            for j in list(csv_df.columns):
                setlist = []
                for k in range(0, len(self.working_on)):
                    if j in self.context.keys():
                        setlist = self.replace(work_list, '$' + str(j), str(csv_df.loc[i, j]))
                        work_list = setlist

                    if j not in self.context.keys():
                        newdic = {j: {"@type": "propertyValue", "description": "Description of new key",
                                      "value": str(csv_df.loc[i, j]), "unit": "null"}}
                        work_list[-1].append(newdic)
                resultjson = self.json_generate(work_list)
                with open(str(count), 'w') as f:
                    f.write("%s\n" % resultjson)
                    print("Successfully generated JSON")
            count += 1

    def fair_csv(self, csvname):

        """Fairy data file from csv file and process input data into single JSON-LD file

        Args:
            csvname(path):CSV file path want to be process
        """

        csv_df = pd.read_csv(csvname)
        count = 0
        for i in csv_df.index:
            work_list = self.working_on
            for j in list(csv_df.columns):
                setlist = []
                for k in range(0, len(self.working_on)):
                    if j in self.context.keys():
                        setlist = self.replace(work_list, '$' + str(j), str(csv_df.loc[i, j]))
                        work_list = setlist

                    if j not in self.context.keys():
                        newdic = {j: {"@type": "propertyValue", "description": "Description of new key",
                                      "value": str(csv_df.loc[i, j]), "unit": "null"}}
                        work_list[-1].append(newdic)
                resultjson = self.json_generate(work_list)
                with open(str(count), 'w') as f:
                    f.write("%s\n" % resultjson)
                    print("Successfully generated JSON")
            count += 1

    def replace(self, data, val_from, val_to):

        """replace placeholder with the value inside csv file

        Args:
            data(list or dic):current processing dataframe

            val_from(int or string):value need to be modify

            val_to(int or string):value after modify

        Returns:
            str:dataframe with modified value
        """

        if isinstance(data, list):
            return [self.replace(x, val_from, val_to) for x in data]
        if isinstance(data, dict):
            return {k: self.replace(v, val_from, val_to) for k, v in data.items()}
        return val_to if data == val_from else data

    def __init__(self,domain):
        """initilize class faircsv"""
        if domain == "XRD":
            name="../jsonld/XRD_json-ld_template.json"
        if domain == "CE":
            name="../jsonld/CE_json-ld_template.json"
        if domain == "polymerAM":
            name = "../jsonld/polymer_AM_json-ld_template.json"
        if domain == "pv-module":
            name = "../jsonld/pv-module.json"
        if domain == "RWB_YI":
            name = "../jsonld/RWB_YI.json"
        if domain == "OpticalSpc":
            name = "../jsonld/OpticalSpc.json"


        with open(name) as data:
            self.json_data = json.load(data)
        self.context = self.json_data["@context"]
        self.working_on = []
        self.working_on_key = []
        self.header = []
        self.key_list = []
        for key, value in self.json_data.items():
            if type(value) == str:
                self.header.append(
                    '"' + str(key) + '"' + ":" + '"' + str(value) + '"' if str(value) is not None else '""')
            if type(value) == list:
                self.working_on_key.append('"' + str(key) + '"')
                self.working_on.append(value)
        if domain == "XRD":
            self.fair_csv('../csv/XRD_demo.csv')
        if domain == "CE":
            self.fair_csv('../csv/CE_demo.csv')
        if domain == "polymerAM":
            self.fair_csv('../csv/polymer_AM_demo.csv')
        if domain == "pv-module":
            self.fair_csv('../csv/pv-module.csv')
        if domain == "RWB_YI":
            self.fair_csv('../csv/RWB_YI.csv')
        if domain == "OpticalSpc":
            self.fair_csv('../csv/OpticalSpc.csv')




