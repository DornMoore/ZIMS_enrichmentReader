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

df = pd.read_excel(dataPath+"\ExampleEnrichment.xls",
                   header=None, sheet_name="List")
# print(df.head(10))

# Gather data to add to each row #
individual = df.iat[0, 1]
localID = df.iat[1, 1]
preferredID = df.iat[2, 1]
species = df.iat[3, 1]
birth_loc = df.iat[4, 1]
birth_type = df.iat[5, 1]
birthAge = df.iat[6, 1]
current_collection = df.iat[7, 1]
current_enclosure = df.iat[8, 1]
# print("\n")
# print(len(df.index))

# Create DataFrame to store formatted data
outData = []
outColumns = ['individual', 'localId', 'preferredID', 'species', 'birth_loc', 'birth_type', 'birthAge', 'current_collection',
              'current_enclosure', 'enrichmentType', 'eCategory', 'eGoal', 'eDate', 'dateGiven', 'timeGiven', 'reaction', 'rating', 'providedBy', 'details']

# Structure
birdInfo = individual, localID, preferredID, species, birth_loc, birth_type, birthAge, current_collection, current_enclosure,

#Begin searching for Enrichment #
row = 9  # start where we left off
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

            time = df.iat[row, 2]

            # Handle nan values
            reaction = df.iat[row, 3]
            rating = df.iat[row, 4]
            providedBy = df.iat[row, 5]
            details = df.iat[row, 7]

            actInfo = date, time, reaction, rating, providedBy, details
            outData.append(birdInfo+eInfo+actInfo)

            # print(str(date) + ", " + str(time) +
            #       ", " + str(reaction) + ", " + str(details))

            row = row+1
        enrichment = ""

    row = row+1
    outDF = pd.DataFrame(outData, columns=outColumns)
    print(outDF.head())
    outDF.to_excel('output.xlsx')
