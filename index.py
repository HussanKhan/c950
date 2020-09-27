from GPS import GPS
from Assets import Truck
from HashTable import HashTable
from HelperFunctions import loadMap, processPackageData
from sortingFunctions import extractNumbers
import random
import time
from datetime import datetime

class main():

    def __init__(self, distanceMap, packageFile, truckNames=[1, 2, 3], numberOfDrivers=2):
        wguMap = loadMap(distanceMap)
        self.gps = GPS(wguMap)

        self.packages, columnNames = processPackageData(packageFile)
        self.sortedPackages = []
        self.hub = []
        self.hashTable = HashTable(50)
        self.truckNames = truckNames
        self.nDrivers = numberOfDrivers

        self.knownDeadlines = []

        for p in self.packages:
            self.hashTable.insert(p.get('package id'), p)
            if p.get('delivery deadline') != 'EOD' and p.get('delivery deadline') not in self.knownDeadlines:
                self.knownDeadlines.append(p.get('delivery deadline'))
        
        self.knownDeadlines = self.sortDeadlines(self.knownDeadlines)

        # Finds order of packages that is delivered on time
        for i in range(0, 10000):
            self.sortedPackages = []
            self.hub = []
            self.resetPackageStatus()
            res = self.findBestSort()
            if res != "Fail":
                print(self.packages)
                break
            else:
                print("Run {} Failed to delilver before deadline".format(i))
    
    def resetPackageStatus(self):
        for p in self.packages:
            p.update("status", "")

    def findBestSort(self):

        truckMap = []
        for name in self.truckNames:
            truck = Truck(str(name), 16, 18, "4001 South 700 East", self.gps, self.hashTable, self.knownDeadlines)
            truckMap.append(truck)

        # store packages that have a truck requirment
        for i, IDs in enumerate(self.truckNumberRequirment()):
            for j in IDs:
                truckMap[i].addPackage(j)

        bundle = list(self.bundlePackages())

                # hours that packages arrive 
        delayed, hour = self.delayedPackages()
        # packages with deadlines
        activedDeadline = self.activeDeadlinePackages()

        random.shuffle(bundle)
        random.shuffle(delayed)
        random.shuffle(activedDeadline)

        # manual truck fill truck 1, bundles
        for p in bundle:
            truckMap[0].addPackage(p)

        # maunal fill delayed truck
        truckMap[1].changeStartTime(hour)
        for p in delayed:
            truckMap[1].addPackage(p)
        
        # keep fill truck to max
        while len(activedDeadline) > 0:
            for truck in truckMap[0:self.nDrivers]:
                try:
                    truck.addPackage(activedDeadline.pop(0))
                except Exception as e:
                    break

        # store all remaining packages
        for p in self.packages:
            IDs = [p.get("package id")]

            if 'On Truck' not in p.get('status'):

                for truck in truckMap:

                    while True and len(IDs) > 0:
                        try:
                            pID = IDs.pop(0)
                            truck.addPackage(pID)
                            self.sortedPackages.append(pID)
                        except Exception as e:
                            IDs = [p.get("package id")]
                            break

                if len(IDs) > 0:
                    self.sortedPackages.append(IDs[0])
                    self.hub.append(IDs[0])
                    p.update('status', 'At Hub')

        # they can drive near same time
        returnTimes = []
        for i in range(0,self.nDrivers):
            returnTime = truckMap[i].startDelivery()
            returnTimes.append(datetime.strptime(":".join(str(returnTime).split(":")[0:2]), "%H:%M").strftime("%I:%M %p"))
        print(returnTimes)
        # no next truck can drive
        lowestTime = datetime.strptime("11:59 pm", "%H:%M %p").strftime("%I:%M")
        for t in returnTimes:
            if t < lowestTime:
                lowestTime = t

        lowestTime = datetime.strptime(lowestTime, "%H:%M %p").strftime("%I:%M")

        for p in self.packages:
            deadline = p.get("delivery deadline")

            if deadline != "EOD":
                delivered = datetime.strptime(":".join(p.get('status').split(",")[-3].split(":")[0:2]), "%H:%M").strftime("%I:%M %p")                
                deliveredTime = datetime.strptime(delivered, "%H:%M %p")
                deadlineTime = datetime.strptime(deadline, "%H:%M %p")
                
                if deliveredTime > deadlineTime:
                    return "Fail"

        for p in self.packages:
            print(p.get('status'), p.get('delivery deadline'))
        
        print("PATH FOUND")
        print(lowestTime)

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

    
    def bundlePackages(self):
        bundle = []

        for p in self.packages:
            if "must be delivered with" in p.get('notes'):
                bundle.append(p.get('package id'))
                bundle = bundle + extractNumbers(p.get('notes'))

        bundle = set(bundle)

        for n in bundle:
            if n not in self.sortedPackages:
                self.sortedPackages.append(n)

        return bundle

    def delayedPackages(self):

        delayed = []
        times = []
        for p in self.packages:
            if "delayed" in p.get('notes') and p.get('package id') not in self.sortedPackages:
                delayed.append(p.get('package id'))

                timeStated = ":".join(extractNumbers(p.get('notes'))) + " " + p.get('notes').split(" ")[-1].upper()
                
                if timeStated not in times:
                    times.append(timeStated)
                
                self.sortedPackages.append(p.get('package id'))

        timeList = self.sortDeadlines(times)[0].split(" ")[0].split(":")
        (hour, minute) = int(timeList[0]), int(timeList[1])

        return delayed, (hour, minute)

    def truckNumberRequirment(self):

        truckIndex = [[]] * len(self.truckNames)

        for p in self.packages:

            if "can only be on truck" in p.get('notes') and p.get('package id') not in self.sortedPackages:
                number = int(extractNumbers(p.get('notes'))[0]) - 1
                truckIndex[number] = truckIndex[number] + [p.get('package id')]
                self.sortedPackages.append(p.get('package id'))

        return truckIndex

    def activeDeadlinePackages(self):
        IDs = []

        for p in self.packages:

            if p.get('delivery deadline') != "EOD" and p.get('package id') not in self.sortedPackages:
                IDs.append(p.get('package id'))
                self.sortedPackages.append(p.get('package id'))

        return IDs



main("WGU Distance Table.csv", 'WGUPS Package File.csv')