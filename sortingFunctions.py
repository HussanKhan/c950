import re
# this function extract all numbers from a string
def extractNumbers(string):
    return re.findall(r'\d+', string)

# this functions returns a list of packages IDs that
# must be delivered together
# pushs time senstive packages to the front
def bundlePackages(packageList):
    
    # 1 - get all special notes
    notes = []

    for p in packageList:
        if "must be delivered with" in p.get('notes'):
            notes.append(p.get('package id'))
            notes.append(extractNumbers(p.get('notes')))

    print(notes)

    relevantNotes = []

    # keyphrase - "must be delivered with" is 
    # used to find these packages
    for note in notes:

        if "must be delivered with" in note:
            relevantNotes.append(note)

    specialPackageIDs = []
    for note in relevantNotes:
        IDs = packageHashTable.getColumnValueToPackageId('notes', note)
        specialPackageIDs  = specialPackageIDs + IDs + extractNumbers(note)

    specialPackageIDs = list(set(specialPackageIDs))
    priority = []

    for id in specialDeliveryTimes(packageHashTable):
        
        if id in specialPackageIDs:
            priority.append(specialPackageIDs.pop(specialPackageIDs.index(id)))

    print(priority + specialPackageIDs)
    return priority + specialPackageIDs

# this functions returns a list of packages

def specialDeliveryTimes(packageHashTable):

    import time

    times = packageHashTable.getColumnValues('delivery deadline')

    specialTimes = []

    for timeData in times:
        if timeData != 'EOD' and timeData not in specialTimes:
            specialTimes.append(timeData)
    print(specialTimes)
    # sort times in order
    tempArr = []
    for t in specialTimes:
        tempArr.append(time.strptime(t, '%I:%M %p'))

    specialTimes = []
    for i in sorted(tempArr):

        reFormattedTime = list(time.strftime('%I:%M %p', i))
        
        # remove leading zero
        if reFormattedTime[0] == '0':
            reFormattedTime.pop(0)

        reFormattedTime = ''.join(reFormattedTime)
            
        specialTimes.append(reFormattedTime)

    print(specialTimes)
    specialPackageIDs = [] 
    for time in specialTimes:
        IDs = packageHashTable.getColumnValueToPackageId('delivery deadline', time)
        specialPackageIDs = specialPackageIDs + IDs

    return specialPackageIDs