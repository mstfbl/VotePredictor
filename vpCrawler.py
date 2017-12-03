import os
import json
from pprint import pprint

def crawl():
    pass


def main():
    parentPath = "./years/"
    startingYear = 2015
    mergedData = {}
    count = 0
    for year in range(startingYear,2017):
        currentParentPath = parentPath+str(year)+"/"
        for directory in os.listdir(currentParentPath):
            if not directory.startswith('.'): #Ignore hidden files/dirs
                count += 1
                currentParentPath = parentPath+str(year)+"/"+str(directory)
                data = json.load(open(currentParentPath+'/data.json'))
                if "bill" in data and "amendment" not in data:
                    billCode = str(startingYear) + str(data["bill"]["type"])+str(data["bill"]["number"])
                    mergedData[billCode] = {}
                    mergedData[billCode]["bill"] = data["bill"]
                    mergedData[billCode]["votes"] = data["votes"]
            
    with open('mergedData.json', 'w') as f:
     json.dump(mergedData, f)
        
if __name__ == "__main__":
    main()