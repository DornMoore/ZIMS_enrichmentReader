#!/usr/bin/env python

"""
readEnrichment.py:
Script reads through enrichment xls files produced by ZIMS.
This is a work around to the fact that we can export formatted xls files
from ZIMS but not CSV files that ould be useful in analysis. ZIMS is working
a way to ge tthe data we need outside of ZIMS but in the meantime.

"""

import csv
from datetime import datetime
import os
import logging
import pandas as pd
# import glob
# import json
# import psycopg2
# import requests
# import shutil
# import subprocess
# import zipfile

__author__ = "Dorn Moore, International Crane Foundation"
__credits__ = ["Dorn Moore"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Dorn Moore"
__email__ = "dorn@savingcranes.org"
__status__ = "ALpha"

### Processs Variables ###
dataPath = "data"

outColumns = ['individual', 'localId', 'preferredID', 'species', 'birth_loc', 'birth_type', 'birthAge', 'current_collection',
              'current_enclosure', 'enrichmentType', 'eCategory', 'eGoal', 'eDate', 'dateGiven', 'timeGiven', 'reaction', 'rating', 'providedBy', 'items', 'details']


outData = []

for f in os.listdir(dataPath):

    if f.endswith(".xls") or f.endswith(".xlsx"):
        # print(f)

        df = pd.read_excel(os.path.join(dataPath, f),
                           header=None, sheet_name="List")
        # print(df.head(10))

        row = 0
        birdInfoDict = {}
        while pd.notnull(df.iat[row, 1]):
            key = df.iat[row, 0].lower()  # set the key to the field lowercase
            key = key.replace(" ", "")      # remove any spaces
            key = key.replace("/", "_")      # Change / to _

            birdInfoDict[key] = df.iat[row, 1]
            # print(birdInfoDict)
            row = row + 1

        # Structure - this needs to be re-configured to be more flexible
        birdInfo = birdInfoDict['individual'], birdInfoDict['localid'], birdInfoDict['preferredid'], birdInfoDict['species'], birdInfoDict[
            'birthlocation'], birdInfoDict['birthtype'], birdInfoDict['birth_age'], birdInfoDict['currentcollection'], birdInfoDict['currentenclosure']

        #Begin searching for Enrichment #
        enrichment = ""
        while row < len(df.index):
            if df.iat[row, 1] == "Enrichment Item Name":

                row = row+1
                enrichment = df.iat[row, 1]
                eCategory = df.iat[row, 2]
                eGoal = df.iat[row, 3]
                eDate = df.iat[row, 4]
                eInfo = enrichment, eCategory, eGoal, eDate
                # print(birdInfo + eInfo)

                # move to the records for this enrichment
                row = row+3
                while pd.notnull(df.iat[row, 1]):

                    # convert date
                    date = df.iat[row, 1]
                    # print(date)

                    time = df.iat[row, 2]

                    # Handle nan values
                    reaction = df.iat[row, 3]
                    rating = df.iat[row, 4]
                    providedBy = df.iat[row, 5]
                    details = df.iat[row, 6]

                    startKeyword = "Items:"
                    endKeyword = 'Description/ placement:'
                    index = 0
                    startIndex = 0
                    endIndex = 0
                    items = []
                    itemsFound = False

                    # while indexFound != False:
                    # for word in details.split():
                    #     if word == startKeyword:
                    #         startIndex = index
                    #     if word == endKeyword:
                    #         endIndex
                    #     while itemsFound:
                    #         items.append(word)
                    #         print(word)

                    if details.find(startKeyword) != -1:
                        items = details[details.find(
                            startKeyword)+len(startKeyword):details.find(endKeyword)]
                        print(items)

                    actInfo = date, time, reaction, rating, providedBy, items, details

                    # Add Row of Data to outData
                    outData.append(birdInfo+eInfo+actInfo)

                    row = row+1
                enrichment = ""

            row = row+1

export = pd.DataFrame(outData, columns=outColumns)
export.to_excel('output.xlsx')
