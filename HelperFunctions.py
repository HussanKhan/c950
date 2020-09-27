import csv
from Assets import Package


"""
Data is processed from package csv
and returned in list format
O(N) where n is number of rows in package csv
"""
def processPackageData(filename):

    # holds lists of packages
    packages = []
    columnNames = []

    # begin sorting as soon as file is opened
    with open(filename) as f:

        rows = csv.reader(f)
        
        columnsInit = False
        addressIndex = 0
        for row in rows:

            currentRow = row
            # Wrong addresses require imnediate user correction
            notes = row[-1].lower()
            row[-1] = notes

            if 'wrong' in notes and 'address' in notes:
                correctAddress = input("Please Enter Correct Address for Package {}: ".format(row[0])).strip() or '410 S State St'
                currentRow[addressIndex] = correctAddress
            
            # skip columns row
            if columnsInit:
                
                # adding entry for status column
                row.append("")

                package = Package(columnNames, currentRow)
                packages.append(package)
            else:

                # fill column names
                for i, name in enumerate(currentRow):
                    
                    formattedName = " ".join(name.split()).lower()
                    columnNames.append(formattedName)
                
                    if 'address' in formattedName:
                        addressIndex = i


                # renaming last column to just notes
                columnNames[-1] = "notes"
                
                # adding status column
                columnNames.append("status")

                columnsInit = True

                print("\n")
                print("Columns in Data")
                print(columnNames)
                print("\n")
    
    return packages, columnNames

def findIndexofDigit(string):
    for n, chara in enumerate(string):
        if chara.isdigit():
            return n

def formatAddress(address):
    frontHalf = address.split(",")[0]
    extractedAddress = frontHalf[findIndexofDigit(frontHalf):]
    return extractedAddress

# Load distance information from csv file
# Create a weighted graph of all hubs in WGU distance table
def loadMap(filename):

    import csv

    with open(filename) as f:

        rows = csv.reader(f)
        columns = []
        hubMap = {}

        secondRowName = ""

        columnsInit = False
        for row in csv.reader(f):

            if not columnsInit:         # first row in CSV is just column names                      
                for addresses in row:   # creating columns array
                    columns.append(formatAddress(' '.join(addresses.split())))

                columns.pop(0) # dumping first cell data, not useful, just title
                columnsInit = True

            else:

                if secondRowName == "": # save name of first address row
                    secondRowName = formatAddress(' '.join(row[0].split()))

                innerHash = {}

                # loop through row elements and create dictionary to add to graph
                for i in range(0, len(row[1:])):
                    if row[1:][i] != '' and row[1:][i] != '0':

                        innerHash[columns[i]] = float(row[1:][i])

                # add dictionary to graph
                hubMap[formatAddress(' '.join(row[0].split()))] = innerHash

                # add distance to first row item in csv
                if ' '.join(row[0].split()) is not secondRowName and innerHash != {}:
                    hubMap[secondRowName][formatAddress(' '.join(row[0].split()))] = innerHash[secondRowName]

        return hubMap

def gridifyList(menuItems, delimiter=","):

    for i, item in enumerate(menuItems):
        menuItems[i] = item.split(delimiter)

    maxLen = 0
    
    for data in menuItems:    
        for string in data:
            
            dataLen = len(string)
            
            if dataLen > maxLen:
                maxLen = dataLen

    for o, data in enumerate(menuItems):
        for i, string in enumerate(data):
            menuItems[o][i] = string.ljust(maxLen)

    for i, data in enumerate(menuItems):
        menuItems[i] = "".join(data) 

    return menuItems


