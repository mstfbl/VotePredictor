import os
import json
from pprint import pprint

def getDateOfBill(fullDate):
    return fullDate[:10]


def main():
    parentPath = "./years/"
    startingYear = 2015
    mergedData = {}
    count = 0
    for year in range(startingYear,2017):
        currentParentPath = parentPath+str(year)+"/"
        for directory in os.listdir(currentParentPath):
            if not directory.startswith('.'): #Ignore hidden files/dirs
                currentParentPath = parentPath+str(year)+"/"+str(directory)
                data = json.load(open(currentParentPath+'/data.json'))
                if "bill" in data and "amendment" not in data:
                    count += 1
                    billCode = getDateOfBill(data["date"]) + str(data["bill"]["type"])+str(data["bill"]["number"])
                    mergedData[billCode] = {}
                    mergedData[billCode]["bill"] = data["bill"]
                    mergedData[billCode]["votes"] = data["votes"]
            
    with open('mergedData.json', 'w') as f:
     json.dump(mergedData, f, sort_keys=True, indent=4, separators=(',', ': '))
if __name__ == "__main__":
    main()