
import json
import pandas as pd
import sys
from pyld import jsonld

class fairify_data:
    """fairify data  from CSV file and output them as single JSON_LD format file"""

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
    def fairify_dataframe(self, csv_df):

        """Fairify data file from dataframe and process input data into single JSON-LD file

        Args:
            csv_df(path): dataframe file path want to be process
        """

        count = 0
        for i in csv_df.index:
            work_list = self.working_on
            #print("this is :",work_list)
            for j in list(csv_df.columns):
                if j in self.context.keys():
                    for k in range(0, len(self.working_on)):
                        setlist = self.replace(work_list, '$' + str(j), str(csv_df.loc[i, j]))
                        work_list = setlist
                        resultjson = self.json_generate(work_list)

                else:

                    findflag = False
                    for key, value in self.dic.items():

                        if j in value:
                            print(key+" has key:"+j)
                            self.domain_selection(key)
                            self.read_data(self.name)
                            newwork_list=self.working_on
                            newsetlist = self.replace(newwork_list, '$' + str(j), str(csv_df.loc[i, j]))
                            newwork_list = newsetlist
                            newresultjson = self.json_generate(newwork_list)
                            self.generate_file(count,newresultjson,key)
                            self.domain_selection(self.domain)
                            findflag=True
                    if findflag==False:
                        print(
                            " Please review the existing keys and reformat if you find a match. If you can't find a match, please email us at fairmaterials@gmail.com, and we will add it to our template. For now, your key will reside in the AdditionalProperty section of the json-ld document.")
                        newdic = {j: {"@type": "propertyValue", "description": "Description of new key",
                                      "value": str(csv_df.loc[i, j]), "unit": "null"}}
                        work_list[-1].update(newdic)
                        resultjson = self.json_generate(work_list)
                        #resultjson=jsonld.to_rdf(resultjson)
            count = self.generate_file(count, resultjson, self.domain)
    def generate_file(self,count,resultjson,key):

        """generate json file with the valid formate

        Args:
            count(int or string):current processing dataframe index

            resultjson(string):json ld content after fairified

            key(string):domain for json ld content after fairified

        Returns:
            int:move to next index content
        """
        with open(str(key)+str(count)+".json", 'w') as f:
            f.write("%s\n" % resultjson)
            print("Successfully generated JSON")
            count += 1
        return count

    def fairify_csv(self, csvname):

        """Fairify data file from csv file and process input data into single JSON-LD file

        Args:
            csvname(path):CSV file path want to be process
        """

        csv_df = pd.read_csv(csvname)
        count = 0
        for i in csv_df.index:
            work_list = self.working_on
            for j in list(csv_df.columns):
                if j in self.context.keys():
                    for k in range(0, len(self.working_on)):
                        setlist = self.replace(work_list, '$' + str(j), str(csv_df.loc[i, j]))
                        work_list = setlist
                        resultjson = self.json_generate(work_list)

                else:

                    findflag = False
                    for key, value in self.dic.items():

                        if j in value:
                            print(key+" has key:"+j)
                            self.domain_selection(key)
                            self.read_data(self.name)
                            newwork_list=self.working_on
                            newsetlist = self.replace(newwork_list, '$' + str(j), str(csv_df.loc[i, j]))
                            newwork_list = newsetlist
                            newresultjson = self.json_generate(newwork_list)
                            self.generate_json(count,newresultjson,key)
                            self.domain_selection(self.domain)
                            findflag=True
                    if findflag==False:

                        print(" Please review the existing keys and reformat if you find a match. If you can't find a match, please email us at fairmaterials@gmail.com, and we will add it to our template. For now, your key will reside in the AdditionalProperty section of the json-ld document.")
                        newdic = {j: {"@type": "propertyValue", "description": "Description of new key",
                                      "value": str(csv_df.loc[i, j]), "unit": "null"}}
                        work_list[-1].update(newdic)
                        resultjson = self.json_generate(work_list)
            count=self.generate_file(count,resultjson,self.domain)






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

    def read_data(self, name):
        """read json-LD file and spilt them accoording to their header content"

        Args:
            name(string):domain name corresponding to json ld file

        """


        with open(name) as data:
            self.json_data = json.load(data)
            self.context = self.json_data["@context"]
            self.working_on = []
            self.working_on_key = []
            self.header = []
            self.key_list = []
            self.json_data.pop("@context")
        for key, value in self.json_data.items():
            if type(value) == str:
                self.header.append(
                    '"' + str(key) + '"' + ":" + '"' + str(value) + '"' if str(value) is not None else '""')
            else:
                self.working_on_key.append('"' + str(key) + '"')

                self.working_on.append(value)




    def domain_selection(self, domain):
        """domain selection base on user input"

        Args:
            domain(string):domain name for fairmaterials

        """

        if domain == "diffractionXRay":
            self.name = "./json-ld/diffractionXRay-json-ld-template.json"
        if domain == "capillaryElectrophoresis":
            self.name = "./json-ld/capillary-electrophoresis-json-ld-template.json"
        if domain == "polymerAdditiveManufacturing":
            self.name = "./json-ld/polymerAdditiveManufacturing-json-ld-template.json.json"
        if domain == "photovoltaicModule":
            self.name = "./json-ld/photovoltaicModule-json-ld-template.json"
        if domain == "photovoltaicBacksheet":
            self.name = "./json-ld/photovoltaicBacksheet-json-ld-template.json"
        if domain == "opticalSpectroscopy,":
            self.name = "./json-ld/opticalSpectroscopy-json-ld-template.json"
        if domain == "buildings":
            self.name = "./json-ld/buildings-json-ld-template.json"
        if domain == "metalAdditiveManufacturing":
            self.name = "./json-ld/metalAdditiveManufacturing-json-ld-template.json"
        if domain == "opticalProfilometry":
            self.name = "./json-ld/opticalProfilometry-json-ld-template.json"
        if domain == "photovoltaicSystem":
            self.name = "./json-ld/photovoltaicSystem-json-ld-template.json.json"
        if domain == " computedTomographyXRay":
            self.name = "./json-ld/computedTomographyXRay-json-ld-template.json"
        if domain == "polymerFormulations":
            self.name = "./json-ld/polymerFormulation-json-ld-template.json"
        if domain == " materialsProcessing":
            self.name = "./json-ld/materials-processing-json-ld-template.json"
        if domain == "photovoltaicCell":
            self.name = "./json-ld/photovoltaicCell-json-ld-template.json"
        if domain == "photovoltaicInverter":
            self.name = "./json-ld/photovoltaicInverter-json-ld-template.json"
        if domain == "asterGdem":
            self.name = "./json-ld/asterGdem-json-template.json"
        if domain == "environmentalExposure":
            self.name = "./json-ld/environmentalExposure-json-ld-template.json"
        if domain == "geospatialWell":
            self.name = "./json-ld/geospatialWell-json-ld-template.json"
        if domain == "soil":
            self.name = "./json-ld/soil-json-ld-template.json"
        if domain == "streamWater":
            self.name = "./json-ld/streamWater-json-ld-template.json"


    def __init__(self,file,input):
        self.domain=input
        """initilize class fairify csv"""
        self.dic = {"buildings": ["SampleID", "Building", "PremisesName", "OperatorType", "Longitude", "Latitude", "Address",
                             "City", "County", "State", "PostalCode", "ClimateZoneType", "ASHRAE", "KöppenClimate",
                             "FloorArea", "FloorAreaType", "FloorAreaPercentage", "FloorAreaValue",
                             "OverallWindowToWallRatio", "ConditionedFloorsAboveGrade"],
               "capillaryElectrophoresis": ["electrophoresisType",
                      "sievingElectrophoresis",
                      "isotachophoresis",
                      "afinityElectrophoresis",
                      "freeFlowElectrophoreis",
                      "gasPhaseElectrophoreticMobilityMolecularAnalysis",
                      "pulsedFieldElectrophoresis",
                      "capillaryElectrophoresis",
                      "description",
                      "value",
                      "unit",
                      "sampleID",
                      "analyteSize",
                      "analyteMass",
                      "analyteCharge",
                      "pka",
                      "analyteConcentration",
                      "mobility",
                      "bufferComposition",
                      "bufferPh",
                      "zetaPotential",
                      "appliedVoltage",
                      "columnTemperature",
                      "detectorType",
                      "capillaryLength",
                      "capillaryMaterial",
                      "capillaryCoating",
                      "capillaryDiameter",
                      "analyteConcentration",
                      "ion1",
                      "ionName",
                      "ionType",
                      "time",
                      "absorbanceValue",
                      "ionType",
                      "ion2",
                      "ion3",
                      "ion4"],

               "CasferWater": ['SampleID', 'site', 'date', 'startDate', 'endDate', 'metaData', 'state', 'siteNumber',
                         'longitude', 'latitude', 'parameterCode', 'information', 'physical', 'radiochemical',
                         'sediment', 'biological', 'inorganicMinorNonMetals', 'inorganicMinorMetals',
                         'inorganicMajorMetals', 'organicPesticide', 'populationComunity', 'toxicity', 'organicOther',
                         'nutrient', 'stableIsotopes', 'organicPCBs'],
               "polymerFormulations": ['SampleID', 'experiment', 'afm', 'scanParameters', 'scanSize', 'scanRate', 'scanAngle',
                      'scanLines', 'afmVoltage', 'springConstant', 'gainParameters', 'integralGain', 'proportionalGain',
                      'setPoint', 'driveAmplitude', 'dimensionsImage', 'resonanceFrequency', 'hotStageTemperature',
                      'piezoelectricSensorLocation', 'afmInstrument', 'afmChannel', 'height', 'amplitude', 'phase',
                      'zSensor', 'fluoroelastomer', 'fluoroelastomerProperties', 'material', 'batch',
                      'polydispersityIndex', 'gyrationRadius', 'hydrodynamicRadius', 'peakMolecularWeight',
                      'numberAverageMolecularWeight', 'weightAverageMolecularWeight', 'intrinsicVelocity',
                      'fluoroelastomerFilmPreparation', 'substrate', 'cleaningProcess', 'substrateType',
                      'substrateDimensions', 'solventProperties', 'solventType', 'solventConcentration',
                      'adhesionPromoter', 'filmDimensions', 'spincoatingParameters', 'spincoatingTime',
                      'spincoatingSpeed', 'dryingTemperature', 'dryingTime', 'spincoaterInstrument', 'preFiltration',
                      'description', 'value', 'units'],
               "GeospatialWell": ['SampleID', 'longitude', 'latitude', 'location', 'country', 'state', 'county', 'field', 'header',
                       'name', 'well', 'decription', 'curve', 'quantity', 'unit', 'well logs', 'curves'],
               "materialsProcessing": ['SampleID', '@vocab', 'sinteringTemperature', 'sinteringPressure',
                                        'sinteringAtmosphere', 'thermalCuringTemperature', 'thermalCuringPressure',
                                        'thermalCuringDuration', 'etchingTemperature', 'etchingDwellTime',
                                        'etchingRampRates', 'forgingTemperature', 'forgingPressure',
                                        'annealingTemperature', 'annealingTime', 'annealingAtmosphere',
                                        'quenchingTemperature', 'quenchingTime', 'quenchingCoolingRate',
                                        'weldingTravelSpeed', 'weldingCurrent', 'weldingArc', 'electroplatingCurrent',
                                        'electroplatingIonConcentration', 'extrusionTemperature', 'extrusionRate',
                                        'value', 'description', 'unitText'],
               "metalAdditiveManufacturing": ['@vocab', 'PrinterMetaData', 'MeasurementTechnique', 'value', 'unitText', 'description',
                            'sampleID', 'PrintMethod', 'manufacturer', 'brand', 'material', 'chemicalComposition',
                            'lotNumber', 'buildGeometry', 'buildParameter', 'flowRate', 'layerThickness', 'laserSpeed',
                            'infillPercentage', 'laserTurnPower', 'laserTurnSpeed', 'contourWidth', 'defect',
                            'spotSize', 'widthTop', 'widthBot', 'buildOrientation', 'temperature',
                            'environmentalTemperature', 'extrusionTemperature', 'platformTemperature', 'inSitu',
                            'exSitu', 'profilometer', 'IRCamera', 'HighSpeedCamera', 'image', 'VideoObject', 'duration',
                            'SurfaceRoughness', 'FrameRate', 'CompositeRatio', 'BasePolymer', 'FillerMaterial',
                            'MechanicalProperties', 'TensileStrength', 'TensileModulus', 'Density', 'MolecularWeight',
                            'Viscosity'],
               "opticalProfilometry": ['@vocab', 'value', 'description', 'unit', 'SampleID', 'Material', 'sample',
                                        'rrms', 'pen', 'date', 'exposureCondition', 'hoursExposed', 'scanArea',
                                        'xPosition', 'yPosition', 'zPosition', 'lightLevel', 'frequency', 'xScanStep',
                                        'yScanStep', 'xDistance', 'yDistance', 'formRemoved', 'scanSpeed',
                                        'magnification', 'zHeight', 'surface', 'ySize', 'xSize', 'minMod', 'cameraMode',
                                        'scanLength', 'fdaRes', 'stitch', 'percentOverlap', 'stitchNCols',
                                        'stitchNRows', 'formRemoved__1'],
               "opticalSpectroscopy": ['@vocab', 'SampleID', 'OpticalSpectroscopy', 'RamanSpectroscopy', 'FTIRSpectroscopy',
                               'UVvisSpectroscopy', 'FluorescenceSpectroscopy', 'SampleThickness', 'SampleType',
                               'SampleMaterial', 'wavelength', 'intensity', 'z', 'z.end', 'excitation', 'emission',
                               'absorbance', 'BioChemEntity', 'propertyValue'],
               "polymerAdditiveManufacturing": ['@vocab', 'PrinterMetaData', 'MeasurementTechnique', 'value', 'unitText', 'description',
                              'sampleID', 'PrintMethod', 'manufacturer', 'brand', 'material', 'ChemicalComposition',
                              'LotNumber', 'BuildGeometry', 'SlicingParameter', 'flowRate', 'LayerThickness',
                              'DepositionSpeed', 'InfillPercentage', 'RasterAngle', 'RasterPattern', 'ContourWidth',
                              'AirGap', 'NozzleDiameter', 'WidthTop', 'WidthBot', 'BuildOrientation', 'temperature',
                              'EnvironmentTemperature', 'ExtrusionTemperature', 'PlatformTemperature', 'InSitu',
                              'ExSitu', 'profilometer', 'IRCamera', 'HighSpeedCamera', 'image', 'VideoObject',
                              'duration', 'SurfaceRoughness', 'FrameRate', 'CompositeRatio', 'BasePolymer',
                              'FillerMaterial', 'MechanicalProperties', 'TensileStrength', 'TensileModulus', 'Density',
                              'MolecularWeight', 'Viscosity'],
               "photovoltaicModule": ['SampleID', '@vocab', 'ProdModule', 'ProdMfr', 'ProdCode', 'ModuleEfficiency', 'PowerSTC',
                             'TemperatureNOCT', 'CellCount', 'FrameColor', 'FluorescencePattern', 'ProdCell',
                             'CellTechnologyType', 'CellMaterial', 'CellColor', 'ProdBacksheet', 'BacksheetMaterial',
                             'BacksheetColor', 'ProdEncapsulant', 'EncapsulantMaterial', 'Dimension', 'Height',
                             'Length', 'Weight', 'Mass', 'Width', 'value', 'description', 'unitText'],
               "photovoltaicSystem": ['SampleID', '@vocab', 'ProdModule', 'PVSystem', 'BillOfMaterials', 'Devices', 'DeviceID',
                             'Location', 'Altitude', 'Elevation', 'Latitude', 'LocationID', 'LocationType', 'Longitude',
                             'Orientation', 'Azimuth', 'Tilt', 'Product', 'ProdDatasheet', 'ProdMfr', 'ProdName',
                             'ProdType', 'SerialNum', 'SystemID', 'SystemType', 'CapacityAC', 'CapacityDC',
                             'Production', 'IrradGlobalHorizMeas', 'Decimals', 'EndTime', 'StartTime',
                             'IrradPlaneOfArrayMeas', 'PowerACMeas', 'PowerACArray', 'TempAmbMeas', 'VoltageDCMeas',
                             'WeatherDataRecord', 'HumidityRelative', 'IrradDirectNormal', 'IrradPlaneOfArray',
                             'PrecipitalWater', 'ReferenceCellMeasurement', 'CurrentShortCircuit', 'TempRefCell',
                             'VoltageOpenCircuit', 'Snowfall', 'TempAmb', 'WindSpeed', 'unitText', 'value',
                             'description'],
               "real_world": ['SampleID', '@vocab', 'value', 'description', 'unitText', 'SiteInfo', 'FTIR', 'Raman',
                              'Weather', 'YellownessIndex', 'Gloss', 'MeasurementInfo', 'Rows', 'InstrumentInfoRaman',
                              'InstrumentInfoFTIR', 'InstrumentInfoYI', 'InstrumentInfoGloss', 'FTIRData', 'RamanData',
                              'WeatherData', 'Tube', 'Subrow', 'Module', 'Cell', 'SiteName', 'RowName', 'SubrowName',
                              'ModuleName', 'MeasumentPositionX', 'MeasumentPositionY', 'MeasurementTimeYI', 'Standard',
                              'LStar', 'AStar', 'BStar', 'YI', 'MeasurementTimeGloss', 'Gloss20', 'Gloss60', 'Gloss85',
                              'JunctionBoxPosition', 'RowEnvironment', 'Latitude', 'Longitude', 'Elevation',
                              'InstalledDate', 'SurveyDate', 'ExposureTime', 'RowCount', 'Pitch', 'GroundCover',
                              'Albedo', 'TubeType', 'TubeDiameter', 'SubrowCount', 'ModuleCount', 'Azimuth', 'Tilt',
                              'Clearance', 'HubHeight', 'MountType', 'ModuleSizeX', 'ModuleSizeY', 'ModuleSizeXGap',
                              'ModuleSizeYGap', 'ModuleSizeZGap', 'BacksheetMaterial', 'CellSizeX', 'CellSizeY',
                              'CellCountX', 'CellCountY', 'CellSizeXGap', 'CellSizeYGap', 'FilenameRaman',
                              'FilenameFTIR'],
               "computedTomographyXRay": ['SampleID', 'Material', 'Experiment', 'Data', 'SourceProperties', 'Alloy', 'Composition',
                       'Series', 'Temper', 'Hardness', 'Namlt', 'SampleProperties', 'Shape', 'Diameter', 'Length',
                       'Supplier', 'Date', 'Preprocessing', 'SolutionConcentation', 'SensitizationTemperature',
                       'SensitizationDuration', 'PreStrainRate', 'StrainMax', 'Site', 'SiteName', 'Address', 'Device',
                       'DeviceName', 'Energy', 'FovWidth', 'FovHeight', 'VoxelResolution', 'Methodology', 'Technique',
                       'Method', 'RelativeHumidity', 'StrainRate', 'DisplacementRate', 'Scan', 'SequenceNumber',
                       'StartTime', 'EndTime', 'StartLoad', 'EndLoad', 'StartDisplacement', 'EndDisplacement', 'Image',
                       'StackNumber', 'FilePath', 'FileName', 'FileSize', 'Resolution', 'Timeseries', 'Timestamp',
                       'Load', 'Strain', 'description', 'value', 'unitText'],
               "diffractionXRay": ['SampleID', 'Material', '@vocab', 'value', 'description', 'unitText', 'pattern',
                       'experimentSetting', 'imageAttr', 'imageMeta', 'logs', 'beamlineAttr', 'detectorAttr',
                       'sampleAttr', 'otherAttr', 'said', 'indx', 'img_stck', 'tif_path', 'bttm_pzo_', 'btm_rota',
                       'cesr', 'crys_rtrn', 'crys_sply', 'data_xrd', 'diod', 'fst_shtr', 'hepp', 'hep_stat', 'ic0_',
                       'ic1_', 'ic2_', 'ic3_', 'load_cll', 'load_scrw', 'mo_stab_', 'summary_', 'sync_cnt', 'time',
                       'top_pzo_', 'top_rota', 'leng', 'wdth', 'thckness', 'print_sh', 'beamnrgy', 'wavelngt',
                       'ti_mater', 'log_files'],
               "photovoltaicCell":["ProdCell","SampleID","value","description","unitText","Dimensions","CellCutType","CellTechnologyType"],
"photovoltaicInverter":["ProdInverter","SampleID","value",
    "description",
    "unitText",
    "FileFolderURL",
    "ProdType",
    "ProdName",
    "ProdMfr",
    "ProdDatasheet",
    "CircuitBoardType",
    "InverterSwitchoverTime",
    "InverterStyle",
    "DCInput",
    "ACOutputs",
    "InverterEfficiency"],
        "streamWater":  [
                        "SampleID",
                        "@vocab",
                        "site",
                        "siteNumber",
                        "date",
                        "startDate",
                        "endDate",
                        "metaData",
                        "stationName",
                        "latitude",
                        "longitude",
                        "state",
                        "parameterCode",
                        "value",
                        "description",
                        "unitText"],
                  "soil":  ['SampleID', '@vocab', 'site', 'value', 'description', 'soilMappingUnitIdentifier', 'ID',
                     'muGlobal', 'muSource1', 'muSource2', 'coverage', 'isSoil', 'sequence', 'share', 'soilUnitNaming',
                     'texture', 'refDepth', 'AWC', 'SUSymbol', 'SUSym74', 'SUSym85', 'SUSym90', 'SUCode74', 'SUCode85',
                     'SUCode90', 'soilPhases', 'phase1', 'phase2', 'roots', 'impermeableLayer', 'soilWaterRegimeSWR',
                     'soilProperties', 'addProp', 'topSoil', 'tGravel', 'tSand', 'tSlit', 'tClay', 'tUsdaTexClass',
                     'tRefBulkDensity', 'tTeb', 'tOc', 'tPhH2O', 'tCecClay', 'tCecSoil', 'tBs', 'tCaCO3', 'tCaSO4',
                     'tEsp', 'tEce', 'sGravel', 'sSand', 'sSlit', 'sClay', 'sUsdaTexClass', 'sRefBulkDensity', 'sTeb',
                     'sOc', 'sPhH2O', 'sCecClay', 'sCecSoil', 'sBs', 'sCaCO3', 'sCaSO4', 'sEsp', 'sEce', 'subSoil'],
                    "asterGdem":['asterGdem', 'latitude', 'longitude', 'elevationLand', 'elevationRiver', 'elevationLake', 'elevationOcean', 'typeBody', 'land', 'water', 'ocean', 'river', 'lake', 'value', 'unit', 'description', 'unitText'],
                    "environmentExposure":['@vocab', 'EnvironmentalExposure', 'degradation', 'ThermalDegradation', 'heat', 'temperature', 'HydrolyticDegradation', 'moisture', 'WaterAbsorption', 'RelativeHumidity', 'photodegradation', 'radiation', 'SynergyEffect', 'value', 'unit', 'description', 'unitText'],
                    "geospatialWell":['longitude', 'latitude', 'location', 'country', 'state', 'county', 'field', 'header', 'name', 'well', 'description', 'curve', 'curves', 'quantity', 'unit', 'date', 'startIndex', 'endIndex', 'step', 'rockType', 'totalorganicCarbon', 'totalPorosity', 'porosity', 'waterSaturation', 'densityofthemineralMatrix', 'volumeofSand', 'volumeofLime', 'volumeofdolomite', 'VolumeofClay', 'photoelectric', 'density', 'neutronPorosity', 'laterologdeep', 'gammaray', 'Measureddepth', 'valueType', 'value', 'unitText', 'definedRegion', 'place', 'propertyValue', 'wellLogs', 'dimensions', 'geocoordinates']
,
                    "photovoltaicBacksheet":['SampleID', '@vocab', 'value', 'description', 'unitText', 'SiteInfo', 'FTIR', 'Raman', 'Weather',
                     'YellownessIndex', 'Gloss', 'MeasurementInfo', 'Rows', 'InstrumentInfoRaman', 'InstrumentInfoFTIR',
                     'InstrumentInfoYI', 'InstrumentInfoGloss', 'FTIRData', 'RamanData', 'WeatherData', 'Tube',
                     'Subrow', 'Module', 'Cell', 'SiteName', 'RowName', 'SubrowName', 'ModuleName',
                     'MeasumentPositionX', 'MeasumentPositionY', 'MeasurementTimeYI', 'Standard', 'LStar', 'AStar',
                     'BStar', 'YI', 'MeasurementTimeGloss', 'Gloss20', 'Gloss60', 'Gloss85', 'JunctionBoxPosition',
                     'RowEnvironment', 'Latitude', 'Longitude', 'Elevation', 'InstalledDate', 'SurveyDate',
                     'ExposureTime', 'RowCount', 'Pitch', 'GroundCover', 'Albedo', 'TubeType', 'TubeDiameter',
                     'SubrowCount', 'ModuleCount', 'Azimuth', 'Tilt', 'Clearance', 'HubHeight', 'MountType',
                     'ModuleSizeX', 'ModuleSizeY', 'ModuleSizeXGap', 'ModuleSizeYGap', 'ModuleSizeZGap',
                     'BacksheetMaterial', 'CellSizeX', 'CellSizeY', 'CellCountX', 'CellCountY', 'CellSizeXGap',
                     'CellSizeYGap', 'FilenameRaman', 'FilenameFTIR']
               }


        self.domain_selection(input)
        self.read_data(self.name)
        if str(file)[-4:] == ".csv":
            self.fairify_csv(file)
        else:
            self.fairify_dataframe(file)


