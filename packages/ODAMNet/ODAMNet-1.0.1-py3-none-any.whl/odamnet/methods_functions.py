#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Morgane T. and Ozan O.

Script of methods that we can apply to CTD and WP lists
Adapted from overlapAnalysis.py from Ozan O. (Paper vitamin A)
"""

# Libraries
import json
import ndex2
import requests
import os
import multixrank
import fnmatch
import pandas as pd
import networkx as nx
from scipy.stats import hypergeom
from statsmodels.stats.multitest import multipletests
from alive_progress import alive_bar


# Functions
def overlap(targetGeneSet, pathOfInterestGenesDict, pathOfInterestNamesDict, pathwaysOfInterestList,
            backgroundGenesDict, featureName, outputPath, analysisName):
    """
    Calculate overlap between target genes and pathways of interest

    Metrics :
        - M is the population size (Nb of genes inside WikiPathway for Homo sapiens pathways)
        - n is the number of successes in the population (Nb of genes inside the selected RD WP)
        - N is the sample size (Nb of genes shared between target list (from chemical) and background genes from WP)
        - x is the number of drawn “successes” (Nb of genes shared between target list and RD WP)

    :param set targetGeneSet: Set of HGNC targets
    :param dict pathOfInterestGenesDict: Dictionary of pathways of interest
    :param dict pathOfInterestNamesDict: Dictionary of WP composed of title of them
    :param set pathwaysOfInterestList: Pathways of interest list and their associated background name
    :param set backgroundGenesDict: Dict of background genes
    :param str featureName: Feature name (g.e. MeSH ID or chemical name etc.)
    :param str outputPath: Folder path to save the results
    :param str analysisName: Analysis name for the output name file
    """
    # Parameters
    pathwayIDsList = []
    pathwayNamesList = []
    pathwaySizesList = []
    pathwayBgList = []
    targetSizesList = []
    intersectionSizesList = []
    bgSizesList = []
    pValuesList = []
    intersectionsList = []

    # Displaying
    print('\tOverlap analysis for : ' + featureName)

    # Calculate pvalue overlap.rst for each RD WP found
    for pathway in pathwaysOfInterestList:
        pathwayName = pathway[0]
        source = pathway[1]

        genesSet = set(pathOfInterestGenesDict[pathwayName])
        backgroundGenesSet = set(backgroundGenesDict[source])

        # Metrics calculation
        M = len(backgroundGenesSet)
        n = len(genesSet)
        N = len(targetGeneSet.intersection(backgroundGenesSet))  # Taking only genes that are also in background
        intersection = list(genesSet.intersection(targetGeneSet))
        x = len(intersection)
        # print(pathwayName, M, n, N, x)

        # Hyper geometric test
        pval = hypergeom.sf(x - 1, M, n, N)

        # Fill variable to store information and metrics
        pathwayIDsList.append(pathwayName)
        pathwayNamesList.append(pathOfInterestNamesDict[pathwayName])
        pathwaySizesList.append(n)
        pathwayBgList.append(source)
        targetSizesList.append(N)
        intersectionSizesList.append(x)
        bgSizesList.append(M)
        pValuesList.append(pval)
        intersection.sort()
        intersectionsList.append(' '.join(intersection))

    # Multiple tests to correct pvalue
    reject, pValsAdjList, alphacSidak, alphacBonf = multipletests(pValuesList, alpha=0.05, method='fdr_bh')

    # Final
    df = pd.DataFrame({'PathwayIDs': pathwayIDsList,
                       'PathwayNames': pathwayNamesList,
                       'PathwayBackgroundNames': pathwayBgList,
                       'PathwaySizes': pathwaySizesList,
                       'TargetSizes': targetSizesList,
                       'IntersectionSize': intersectionSizesList,
                       'BackgroundSizes': bgSizesList,
                       'pValue': pValuesList,
                       'pAdjusted': pValsAdjList,
                       'Intersection': intersectionsList
                       })

    # Write into a file
    dfSorted = df.sort_values(by=['pAdjusted'])
    dfSorted.to_csv(outputPath + '/Overlap_' + featureName + '_with' + analysisName + '.csv', ';', index=False)

    # print('\tOverlap analysis done!')
    # return df


def overlapAnalysis(targetGenesDict, pathOfInterestGenesDict, pathOfInterestNamesDict, pathwaysOfInterestList,
                    backgroundGenesDict, outputPath, analysisName):
    """
    For each chemical given in input, calculate overlap.rst with RD WP.

    :param dict targetGenesDict: Dict composed of interaction genes list for each chemical
    :param dict pathOfInterestGenesDict: Dict of pathways of interest genes
    :param dict pathOfInterestNamesDict: Dict of pathways of interest names
    :param list pathwaysOfInterestList: Pathways of interest list and their associated background name
    :param list backgroundGenesDict: Dict of background genes
    :param str outputPath: Folder path to save the results
    :param str analysisName: Analysis name for the output name file
    """
    # For each chemical targets, calculate overlap.rst with RD WP
    for chem in targetGenesDict:
        overlap(targetGeneSet=set(targetGenesDict[chem]),
                pathOfInterestGenesDict=pathOfInterestGenesDict,
                pathOfInterestNamesDict=pathOfInterestNamesDict,
                pathwaysOfInterestList=pathwaysOfInterestList,
                backgroundGenesDict=backgroundGenesDict,
                featureName=chem,
                outputPath=outputPath,
                analysisName=analysisName)


def RWR(configPath, networksPath, outputPath, sifPathName, top):
    """
    Perform a Random Walk with Restart analysis on different multiplex and networks.
    You have to specify seeds and networks.

    :param str configPath: Configuration file name path
    :param str networksPath: Networks path name
    :param str outputPath: Output folder path name
    :param str sifPathName: Result file name path to write SIF result file
    :param int top: Number of results to report in SIF file
    """
    # Analysis
    with alive_bar(title='Random walks through the networks', theme='musical') as bar:
        multixrank_obj = multixrank.Multixrank(config=configPath, wdir=networksPath)
        ranking_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(ranking_df, path=outputPath)
        multixrank_obj.to_sif(ranking_df, path=sifPathName, top=top)
        bar()


def DOMINO(genesFileName, networkFileName, outputPath, featureName):
    """
    Run active modules identification analysis on the DOMINO server

    :param genesFileName: Active genes file name (g.e. list of genes of interest)
    :param networkFileName: Network file name
    :param outputPath: Output path name to save the results
    :param featureName: Feature name (g.e. chemical name)
    :return:
        - **activeModulesDict** (*dict*) – Dict of active modules identified
    """
    # Input file names
    data_dict = {
        'Network file name': os.path.basename(networkFileName),
        'Active gene file name': os.path.basename(genesFileName)
    }
    # Input file contents
    files_dict = {
        'Network file contents': open(networkFileName, 'rb'),
        'Active gene file contents': open(genesFileName, 'rb')
    }

    # Request and run DOMINO
    with alive_bar(title='Search active modules using DOMINO', theme='musical') as bar:
        response = requests.post(url='http://domino.cs.tau.ac.il/upload', data=data_dict, files=files_dict)
        bar()

        # Parse the result request
        response_dict = response.json()
        activeModules_list = response_dict['algOutput']['DefaultSet']['modules']

    # Read genes file
    genesList = []
    with open(genesFileName, 'r') as geneFile:
        for gene in geneFile:
            genesList.append(gene.strip())

    # Write results into file
    if len(activeModules_list.keys()) > 0:
        resultOutput = outputPath + '/DOMINO_' + featureName + '_activeModules.txt'
        with open(resultOutput, 'w') as outputFileHandler:
            outputFileHandler.write('GeneSymbol\tActiveModule\tActiveGene\n')
            for module in activeModules_list:
                for gene in activeModules_list[module]:
                    active = False
                    if gene in genesList:
                        active = True
                    line = gene + '\t' + module + '\t' + str(active) + '\n'
                    outputFileHandler.write(line)
        # Add feature name into AM name
        activeModules_list = {f'AM_{activeModules_list}_' + featureName: v for activeModules_list, v in
                              activeModules_list.items()}
    else:
        print('No Active Modules detected')

    # Return
    return activeModules_list


def DOMINOandOverlapAnalysis(featuresDict, networkFileName, pathOfInterestGenesDict, pathOfInterestNamesDict,
                             pathwaysOfInterestList, backgroundGenesDict, outputPath, analysisName):
    """
    For each genes list, run an active module identification.
    For each AM identified, run an overlap analysis against the pathways of interest.

    :param featuresDict: Dict of list of genes
    :param networkFileName: Content of network file
    :param pathOfInterestGenesDict: Genes dict of pathways of interest
    :param pathOfInterestNamesDict: Names dict of pathways of interest
    :param pathwaysOfInterestList: List of pathways of interest and their bg name associated
    :param backgroundGenesDict: Dict of background genes
    :param outputPath: Output path name to save results
    :param str analysisName: Analysis name for the output name file
    """
    # Parameters
    resultsDict = {}
    # For each feature, search active modules using DOMINO
    for featureName in featuresDict:
        print(featureName + ' analysis :')
        # Write genes list into result file
        resultFileName = outputPath + '/DOMINO_inputGeneList_' + featureName + '.txt'
        with open(resultFileName, 'w') as outputFileHandler:
            for gene in featuresDict[featureName]:
                outputFileHandler.write(gene)
                outputFileHandler.write('\n')
        # Run DOMINO
        resultsDict[featureName] = DOMINO(genesFileName=resultFileName,
                                          networkFileName=networkFileName,
                                          outputPath=outputPath,
                                          featureName=featureName)
        print('\tNumber of active genes  : ' + str(len(featuresDict[featureName])))
        print('\tNumber of AM identified : ' + str(len(resultsDict[featureName])))
        # Run Overlap
        overlapAnalysis(targetGenesDict=resultsDict[featureName],
                        pathOfInterestGenesDict=pathOfInterestGenesDict,
                        pathOfInterestNamesDict=pathOfInterestNamesDict,
                        pathwaysOfInterestList=pathwaysOfInterestList,
                        backgroundGenesDict=backgroundGenesDict,
                        outputPath=outputPath,
                        analysisName=analysisName)

        # Output
        AMIFileName = outputPath + '/DOMINO_' + featureName + '_activeModules.txt'
        DOMINOOutput(networkFileName, AMIFileName, featureName, outputPath)
        print(featureName + ' analysis done!\n')


def DOMINOOutput(networkFileName, AMIFileName, featureName, outputPath):
    # Output file name
    AMoutput = outputPath + '/DOMINO_' + featureName + '_activeModules.txt'
    metricsOutput = outputPath + '/DOMINO_' + featureName + '_activeModulesNetworkMetrics.txt'
    networkOutput = outputPath + '/DOMINO_' + featureName + '_activeModulesNetwork.txt'
    overlapOutput = outputPath + '/DOMINO_' + featureName + '_overlapAMresults4Cytoscape.txt'
    pathwaysOverlapOutput = outputPath + '/DOMINO_' + featureName + '_signOverlap.txt'
    # Parameters
    AM_dict = {}
    edges_df = pd.DataFrame(columns=['source', 'target', 'link', 'AMI_number'])
    AMNumbersList = []
    AMOverlapList = []
    edgeNumberList = []
    nodeNumberList = []
    overlapOutputLinesList = []
    AMIOutputLinesList = []
    AMPathwaysDict = {}

    # Create network graph
    network_df = pd.read_csv(networkFileName, delimiter='\t')
    network_graph = nx.from_pandas_edgelist(network_df, 'node_1', 'node_2', 'link')

    # Read Active Module composition
    with open(AMIFileName, 'r') as AMIFile:
        for line in AMIFile:
            line_list = line.strip().split('\t')
            AM = line_list[1]
            gene = line_list[0]
            if AM not in AM_dict:
                AM_dict[AM] = [gene]
            else:
                AM_dict[AM].append(gene)

    # Extract active module networks
    for AMnb in AM_dict:
        if AMnb != 'ActiveModule':
            AMlist = AM_dict[AMnb]
            # Extract active module network
            network_subgraph = network_graph.subgraph(AMlist)
            subgraph_df = nx.to_pandas_edgelist(network_subgraph)
            subgraph_df['AMI_number'] = AMnb
            # Metrics about active modules
            AMNumbersList.append(AMnb)
            edgeNumberList.append(network_subgraph.number_of_edges())
            nodeNumberList.append(network_subgraph.number_of_nodes())
            # Add the subnetwork edges into a dataframe
            edges_df = pd.concat([edges_df, subgraph_df], ignore_index=True)
    # Write active module networks into output file
    edges_df.to_csv(networkOutput, index=False, sep='\t')
    # Data frame of metrics
    metrics_df = pd.DataFrame({'AMINumber': AMNumbersList,
                               'EdgesNumber': edgeNumberList,
                               'NodesNumber': nodeNumberList})

    # Parse overlap results
    overlapFilesList = fnmatch.filter(os.listdir(outputPath), 'Overlap_AM_*')
    for file in overlapFilesList:
        AMnb = file.split('_')[2]
        with open(outputPath + '/' + file, 'r') as overlapResults:
            overlapResults.readline()
            for line in overlapResults:
                lineList = line.strip().split(';')
                padj = lineList[8]
                if float(padj) <= 0.05:
                    if AMnb not in AMOverlapList:
                        AMOverlapList.append(AMnb)
                    termID = lineList[0]
                    termTitle = lineList[1]
                    genesList = lineList[9].split(' ')
                    if termID in AMPathwaysDict:
                        if float(padj) < AMPathwaysDict[termID]:
                            AMPathwaysDict[termID] = float(padj)
                    else:
                        AMPathwaysDict[termID] = float(padj)
                    for gene in genesList:
                        overlapOutputLinesList.append([gene, AMnb, termID, termTitle, padj])
    # Write into output file
    with open(overlapOutput, 'w') as overlapOutputHandler:
        overlapOutputHandler.write('geneSymbol\tAM_number\ttermID\ttermTitle\toverlap_padj\n')
        for line in overlapOutputLinesList:
            overlapOutputHandler.write('\t'.join(line))
            overlapOutputHandler.write('\n')
    # Write list of sign overlap
    with open(pathwaysOverlapOutput, 'w') as pathwaySignOutput:
        AMPathwaysDict = dict(sorted(AMPathwaysDict.items(), key=lambda item: item[1]))
        for pathway in AMPathwaysDict:
            pathwaySignOutput.write('\t'.join([pathway, str(AMPathwaysDict[pathway])]))
            pathwaySignOutput.write('\n')

    # Add overlap significant in activeModuleFile
    activeGenesDict = dict.fromkeys(list(AM_dict.keys()), 0)
    with open(AMoutput, 'r') as AMIinputHandler:
        header = AMIinputHandler.readline().strip().split('\t')
        for line in AMIinputHandler:
            lineList = line.strip().split('\t')
            if lineList[2] == 'True':
                activeGenesDict[lineList[1]] = activeGenesDict[lineList[1]] + 1
            if lineList[1] in AMOverlapList:
                lineList.append('True')
            else:
                lineList.append('False')
            AMIOutputLinesList.append(lineList)
    # Write into activeModuleFile
    with open(AMoutput, 'w') as AMIoutputHandler:
        header.append('overlapSignificant\n')
        AMIoutputHandler.write('\t'.join(header))
        for line in AMIOutputLinesList:
            AMIoutputHandler.write('\t'.join(line))
            AMIoutputHandler.write('\n')

    # Write metrics into file
    activeGenes_df = pd.DataFrame({'AMINumber': list(activeGenesDict.keys()),
                                   'ActiveGenesNumber': list(activeGenesDict.values())})
    metrics_df = pd.merge(metrics_df, activeGenes_df, on='AMINumber')
    metrics_df.to_csv(metricsOutput, index=False, sep='\t')


def createNetworkandBipartiteFiles(bipartiteName, networkName, pathOfInterestGenesDict):
    """
    Create a bipartite between genes symbols and pathways of interest
    Create a disconnected network between pathways of interest

    :param filename bipartiteName: Bipartite file name
    :param FILENAME networkName: Network file name
    :param dict pathOfInterestGenesDict: Dict of pathways of interest
    """
    # Parameters
    pathwayIDs = []
    bipartiteOutputLines = []
    # For each pathway of interest
    # Take ID and genes into lists
    for ID in pathOfInterestGenesDict:
        if ID != 'pathwayIDs':
            if ID not in pathwayIDs:
                pathwayIDs.append(ID)
            for gene in pathOfInterestGenesDict[ID]:
                bipartiteOutputLines.append([ID, gene])
    # Write ID and genes into bipartite file
    with open(bipartiteName, 'w') as bipartiteOutputFile:
        for line in bipartiteOutputLines:
            bipartiteOutputFile.write('\t'.join(line))
            bipartiteOutputFile.write('\n')
    # Write ID and ID into network file
    with open(networkName, 'w') as networkOutputFile:
        for ID in pathwayIDs:
            networkOutputFile.write('\t'.join([ID, ID]))
            networkOutputFile.write('\n')


def downloadNDExNetwork(networkUUID, outputFileName):
    """
    Download network from NDEx website

    :param str networkUUID: Network ID
    :param FILENAME outputFileName: SIF file name to write network
    """
    # Create NDEx2 python client
    client = ndex2.client.Ndex2()

    # Download
    client_resp = client.get_network_as_cx_stream(networkUUID)

    # Convert downloaded network to NiceCXNetwork object
    net_cx = ndex2.create_nice_cx_from_raw_cx(json.loads(client_resp.content))
    print('Extract network with UUID : ' + networkUUID)
    net_cx.print_summary()

    # Convert to pandas dataframe
    df = net_cx.to_pandas_dataframe()
    df.columns = ['node_1', 'link', 'node_2']
    df.to_csv(outputFileName, index=False, sep='\t', na_rep='linked')
