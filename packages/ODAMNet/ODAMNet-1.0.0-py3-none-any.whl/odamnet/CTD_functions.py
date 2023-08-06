#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Morgane T.

CTD functions

Script to manage the input genes list reading.
Genes list could come from
- a chemical list and requested from CTD
- a CTD file (file created by request CTD)
- a list of interested genes

"""

# Libraries
import requests
import re
from datetime import datetime
from alive_progress import alive_bar


# Functions
def readFeaturesFile(featuresFile):
    """
    Read a list file (composed of gene names or chemical names).

    :param FILE featuresFile: Content of the features file
    :return:
        - **featureNamesList** (*list*) – List of feature names
    """
    # Parameters
    featureNamesList = []

    for line in featuresFile.readlines():
        featureNamesList.append(line.rstrip())

    # Return
    return featureNamesList


def readCTDFile(CTDFile, nbPub, outputPath):
    """
    Read CTD file, created from a request.

    :param FILE CTDFile: Content of the CTD file
    :param int nbPub: Minimum number of publications to keep an interaction
    :param PATH outputPath: Output path directory name
    :return:
        - **targetGenesDict** (*dict*) – Dictionary of genes for each chemical as query
    """
    # Parameters
    targetGenesList = []
    targetGenesDict = {}
    chemNameList = []
    outputLines = []
    header = ''

    for line in CTDFile:
        lineList = line.rstrip().split('\t')
        if lineList[0] == 'Input':
            header = '\t'.join(lineList)
        elif len(lineList[8].split('|')) >= nbPub:
            outputLines.append("\t".join(lineList))
            # Gene name extraction
            geneName = lineList[4]
            if geneName not in targetGenesList:
                targetGenesList.append(geneName)
            # Query name extraction
            chemName = lineList[0].upper()
            if chemName not in chemNameList:
                chemNameList.append(chemName)
    # Dictionary creation
    featureName = '_'.join(chemNameList)
    targetGenesDict[featureName] = targetGenesList

    # Write filtered result into file
    filteredResultFileName = outputPath + '/CTD_requestFiltered_' + featureName + '.tsv'
    with open(filteredResultFileName, 'w') as outputFileHandler:
        outputFileHandler.write(header)
        outputFileHandler.write('\n')
        for line in outputLines:
            outputFileHandler.write(line)
            outputFileHandler.write('\n')

    # Return
    return targetGenesDict


def CTDrequest(chemName, association, outputPath, nbPub):
    """
    Function to request CTD database.

    Search all genes which interact with the chemical given in input.
    Could be several chemicals names in the same line. Analysis will be done like if it's only one chemical.
    If hierarchicalAssociations is used, chemical related to the chemical given in input are used as query.
    Focus on genes present in Homo sapiens.

    :param str chemName: Chemical name of MeSH ids string
    :param str association: Association name (hierarchicalAssociations or directAssociations)
    :param str outputPath: Folder path to save the results
    :param int nbPub: Minimum number of publications to keep an interaction

    :return:
        - **homoGenesList** (*list*) – List of genes which interact with chemicals given in input (only Homo sapiens)
        - **chemMeSH** (*str*) – Composition of MeSH ID from chemicals given in input
    """
    # Parameters
    URL = 'http://ctdbase.org/tools/batchQuery.go'
    PARAMS = {'inputType': "chem", 'inputTerms': chemName, 'report': 'genes_curated', 'format': 'tsv',
              'inputTermSearchType': association}
    homoResultsList = []
    homoResultsListReferences = []
    homoGenesList = []
    meshNamesDict = {}
    chemMeSHList = []

    # Request CTD
    requestResult = requests.get(url=URL, params=PARAMS)
    requestResultString = requestResult.text.replace("'", "_")
    requestResultList = requestResultString.split("\n")
    # requestResultList = requestResult.text.split("\n")

    # Extract results only for Homo sapiens
    for element in requestResultList:
        elementList = element.split("\t")
        if re.match('#', elementList[0]):
            elementList[0] = re.sub('# ', '', elementList[0])
            homoResultsList.append(elementList)
        else:
            if re.match(PARAMS['inputTerms'].lower(), elementList[0]):
                if elementList[6] == 'Homo sapiens':
                    homoResultsList.append(elementList)
                    refList = elementList[8].split('|')
                    if len(refList) >= nbPub:
                        homoResultsListReferences.append(elementList)
                        if elementList[4] not in homoGenesList:
                            homoGenesList.append(elementList[4])
                    if elementList[1].lower() not in meshNamesDict:
                        meshNamesDict[elementList[1].lower()] = elementList[2]

    # Build name of output results file
    for chem in chemName.split('|'):
        if chem in meshNamesDict:
            chemMeSHList.append(meshNamesDict[chem.lower()])
        else:
            chemMeSHList.append(chem)
    chemMeSH = '_'.join(chemMeSHList)
    date = datetime.today().strftime('%Y_%m_%d')
    resultFileName = outputPath + '/CTD_request_' + chemMeSH + '_' + date + '.tsv'
    filteredResultFileName = outputPath + '/CTD_requestFiltered_' + chemMeSH + '_' + date + '.tsv'

    # Write result into file
    with open(resultFileName, 'w') as outputFileHandler:
        for resultLine in homoResultsList:
            outputFileHandler.write('\t'.join(resultLine))
            outputFileHandler.write('\n')

    # Write filtered result into file
    with open(filteredResultFileName, 'w') as outputFileHandler:
        outputFileHandler.write('\t'.join(homoResultsList[0]))
        outputFileHandler.write('\n')
        for resultLine in homoResultsListReferences:
            outputFileHandler.write('\t'.join(resultLine))
            outputFileHandler.write('\n')

    return chemMeSH, homoGenesList


def CTDrequestFromFeaturesList(chemList, association, outputPath, nbPub):
    """
    Make CTD request for each chemical present in the list given in input.
    Each element can be composed of one or more element.
    If several element, the analysis will be done like if there is only one chemical.

    :param list chemList: List of chemical to request to CTD (MeSH IDs or chemical names)
    :param str association: Association name (hierarchicalAssociations or directAssociations)
    :param str outputPath: Folder path to save the results
    :param int nbPub: Minimum number of publications to keep an interaction

    :return:
        - **chemTargetsDict** (*dict*) – Dict composed of interaction genes list for each chemical
    """
    # Parameters
    chemTargetsDict = {}

    # For each chemical, request CTD
    for chem in chemList:
        chemNamesList = chem.rstrip().split(';')
        chemNamesString = '|'.join(chemNamesList)
        chemNames, chemTargetsList = CTDrequest(chemName=chemNamesString, association=association,
                                                outputPath=outputPath, nbPub=nbPub)
        chemTargetsDict[chemNames] = chemTargetsList

    # Return
    return chemTargetsDict


def targetGenesExtraction(chemicalsFile, directAssociations, outputPath, nbPub):
    """
    Read environmental factor file
    Request CTD and extract target genes
    Save results into output file
    Return the gene targets list

    :param FILE chemicalsFile: Content of the chemicals file list
    :param bool directAssociations: Chemical only or descendants too
    :param PATH outputPath: Folder path name to save results
    :param int nbPub: Minimum number of publications to keep an interaction

    :return:
        - **chemTargetsDict** (*dict*) – Dict composed of interaction genes list for each chemical
    """
    # Parameters
    if directAssociations:
        association = 'directAssociations'
    else:
        association = 'hierarchicalAssociations'

    # Read CTD file and request CTD database
    with alive_bar(title='Request CTD', theme='musical') as bar:
        chemNameList = readFeaturesFile(featuresFile=chemicalsFile)
        chemTargetsDict = CTDrequestFromFeaturesList(chemList=chemNameList, association=association,
                                                     outputPath=outputPath, nbPub=nbPub)
        bar()

    # Return
    return chemTargetsDict
