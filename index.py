from GPS import GPS
from Assets import Truck
from HashTable import HashTable
from HelperFunctions import loadMap, processPackageData, gridifyList
from sortingFunctions import extractNumbers
import time
import json
from datetime import datetime

class main():

    def __init__(self, distanceMap, packageFile, truckNames=[1, 2, 3], numberOfDrivers=2):
        wguMap = loadMap(distanceMap)

        gps = GPS(wguMap)
        self.packages, columnNames = processPackageData(packageFile)
        self.sortedPackages = []
        self.hashTable = HashTable(50)
        self.truckNames = truckNames
        self.knownDeadlines = []

        for p in self.packages:
            self.hashTable.insert(p.get('package id'), p)
            if p.get('delivery deadline') != 'EOD' and p.get('delivery deadline') not in self.knownDeadlines:
                self.knownDeadlines.append(p.get('delivery deadline'))
        
        self.knownDeadlines = self.sortDeadlines(self.knownDeadlines)

        truckMap = []
        for name in self.truckNames:
            truck = Truck(str(name), 16, 18, "4001 South 700 East", gps, self.hashTable, self.knownDeadlines)
            truckMap.append(truck)

        data = self.getSortedPackages('sortedPackages.json')

        for key, values in data.items():
            key = int(key) - 1
            for id in values:
                truckMap[key].addPackage(id)

        returnTimes = [truckMap[0].startDelivery(), truckMap[1].startDelivery()]
        
        if returnTimes[0] < returnTimes[1]:
            truckMap[2].changeStartTime(self.createTimeTuple(returnTimes[0]))
        else:
            truckMap[2].changeStartTime(self.createTimeTuple(returnTimes[1]))

        truckMap[2].startDelivery()

        totalMilage = 0

        for t in truckMap:
            totalMilage = totalMilage + t.totalMilage

        while True:

            print("Total Milage for this Route: ", round(totalMilage))

            allPackageSnapshot = []

            timeRange = input('Please Input Time Range, ex: 8:25 am-9:25 am: ').split("-")
            for p in self.packages:
                allPackageSnapshot.append( p.returnStatus( (timeRange[0], timeRange[1]) ) )

            allPackageSnapshot = gridifyList(allPackageSnapshot)

            for p in allPackageSnapshot:
                print(p)

    def getPackageDataByTimeRange(self, lowerTime, upperTime):
        pass



    def getSortedPackages(self, fileName):
        with open(fileName) as js_file:
            data = json.load(js_file)
            return data

    def createTimeTuple(self, dateTimeObject):
        timeList = str(dateTimeObject).split(":")[:2]
        return ( int(timeList[0]), int(timeList[1]) )

    def sortDeadlines(self, times):
        
        tempArr = []
        for t in times:
            tempArr.append(time.strptime(t, '%I:%M %p'))

        times = []
        for i in sorted(tempArr):
            reFormattedTime = list(time.strftime('%I:%M %p', i))
        
            # remove leading zero
            if reFormattedTime[0] == '0':
                reFormattedTime.pop(0)

            reFormattedTime = ''.join(reFormattedTime)
            
            times.append(reFormattedTime)

        return times


main("WGU Distance Table.csv", 'WGUPS Package File.csv')