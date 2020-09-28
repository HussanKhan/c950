# assets of WGU
from HashTable import HashTable
import time
import sys
import datetime

class Truck():

    def __init__(self, name, maxCap, speedMPH, location, gps, packageHash, deadlines, startTime=(8,0)):

        self.cargo = []
        self.delivered = []
        self.maxCap = maxCap
        self.totalMilage = 0
        self.name = name
        self.currentLocation = location
        self.origin = location
        self.destination = None
        self.speed = speedMPH # mph
        self.packageHash = packageHash
        self.gps = gps
        self.time = datetime.datetime(100,1,1,startTime[0],startTime[1],0)
        self.status = "None"
        self.knownDeadlines = deadlines

    def changeStartTime(self, newTime):
        self.time = datetime.datetime(100,1,1,newTime[0],newTime[1],0)

    def addPackage(self, packageID):
        if len(self.cargo) < self.maxCap + 1:
            self.updatePackageStatus(packageID, self.time.time(), 'On Truck {}'.format(self.name))
            self.cargo.append(packageID)
        else:
            raise ValueError("Not enough room in truck")

    def sortPackagesByDeadline(self, packageList):
        orderedPackages = []
        noDeadline = []
        
        for time in self.knownDeadlines:
            
            for id in packageList:
                if self.packageHash.get(id).get('delivery deadline') == time:
                    orderedPackages.append(id)
                elif self.packageHash.get(id).get('delivery deadline') == 'EOD' and id not in noDeadline:
                    noDeadline.append(id)

        return orderedPackages + noDeadline

    # returns times in minutes
    def calculateDeliveryTime(self, totalDistance):
        return (totalDistance*60)/self.speed

    def updatePackageStatus(self, packageID, timestamp, status):
            packageObject = self.packageHash.get(packageID)
            lastStatus = packageObject.get('status')
            packageObject.update('status', lastStatus + str(timestamp) + ',' + status + ',')


    def startDelivery(self):

        # deliver packages with deadline first
        self.cargo = self.sortPackagesByDeadline(self.cargo)
        
        for i, id in enumerate(self.cargo.copy()):
            
            packageId = self.cargo.pop(0)

            self.delivered.append(packageId)
            
            address = self.packageHash.get(packageId).get('address')
            
            self.updatePackageStatus(packageId, self.time.time(), 'On Route')

            path = self.gps.findPath(self.currentLocation, address)

            timeNeeded = self.calculateDeliveryTime(path[-1])

            # Update 
            self.totalMilage += path[-1]
            self.currentLocation = address
            self.time = self.time + datetime.timedelta(minutes=timeNeeded)

            self.updatePackageStatus(packageId, self.time.time(), 'Delivered')

            #print(self.time.time())
            
            self.status = "{} | Cargo Left: {} | Delivering Package: {} | Destination: {} | Time Remaining: {}\n". format(self.name, len(self.cargo) ,id, address, round(timeNeeded))


            if len(self.cargo) == 0:
                # go home
                path = self.gps.findPath(self.currentLocation, self.origin)
            
                timeNeeded = self.calculateDeliveryTime(path[-1])

                # Update 
                self.totalMilage += path[-1]
                self.currentLocation = address
                self.time = self.time + datetime.timedelta(minutes=timeNeeded)
                
                self.status = "{} Finished Delivery".format(self.name)

        return self.time.time()


class Package():
    import time

    def __init__(self, columnNames, values):

        self.hashMap = HashTable(10)
        self.columnName = columnNames

        for i, v in enumerate(values):
            self.hashMap.insert(columnNames[i], v)

    def get(self, columnName):
        try:
            return self.hashMap.get(columnName)
        except Exception as e:
            raise e
    
    def update(self, columnName, value):
        try:
            return self.hashMap.update(columnName, value)
        except Exception as e:
            raise e

    def returnStatus(self, timeRange):

        lowerRequest = datetime.datetime.strptime(timeRange[0], '%I:%M %p')
        upperRequest = datetime.datetime.strptime(timeRange[1], '%I:%M %p')

        print(lowerRequest)
        print(upperRequest)
        
        status = self.get('status')

        times = []
        message = []
        for data in status.split(","):
            if ':' in data:
                data = ":".join(data.split(":")[:2])
                times.append(data)
            elif data != "":
                message.append(data)


        for i, t in enumerate(times):
            try:
                times[i] = times[i] + "-" + times[i+1]
            except Exception as e:
                times[i] = times[i] + "-" + "23:59"

        finalStatus = ""
        for i, time in enumerate(times):
            time = time.split("-")
            lowerRange = datetime.datetime.strptime(time[0], '%H:%M')
            upperRange = datetime.datetime.strptime(time[1], '%H:%M')
            
            if lowerRange <= upperRequest <= upperRange:
                finalStatus = message[i]

        row = None
        if finalStatus == 'Delivered':
            row = [self.get('package id'), self.get('city'), self.get('delivery deadline'), "Status:", finalStatus, str(lowerRange).split(" ")[1]]
        else:
            row = [self.get('package id'), self.get('city'), self.get('delivery deadline'), "Status:", finalStatus]
        return ",".join(row)

    

    