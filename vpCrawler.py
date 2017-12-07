import os
import json
from pprint import pprint

def getDateOfBill(fullDate):
    return fullDate[:10]

def main():
    parentPath = "./years/"
    startingYear = 2015
    mergedData = {}
    billIDCounter = {} #Counts the different versions of bills with the same bill code
    count = 0
    for year in range(startingYear,2017):
        currentParentPath = parentPath+str(year)+"/"
        for directory in os.listdir(currentParentPath):
            if not directory.startswith('.'): #Ignore hidden files/dirs
                currentParentPath = parentPath+str(year)+"/"+str(directory)
                data = json.load(open(currentParentPath+'/data.json'))
                if "bill" in data and "amendment" not in data:
                    count += 1
                    #billCode example: "2015-01-06_00_hr22"
                    #Layout:  Year-Month-Date_billVersion_billCode
                    #Indices:   4 -  2  - 2  _    2      _ ...
                    billID = getDateOfBill(data["date"]) + str(data["bill"]["type"])+str(data["bill"]["number"])
                    if billID in billIDCounter:
                        if int(billIDCounter[billID]) < 9:
                            billIDCounter[billID] = "0"+str(int(billIDCounter[billID])+1)
                        else:
                            billIDCounter[billID] = str(int(billIDCounter[billID])+1)
                    else: 
                        billIDCounter[billID] = "01"
                    billCode = getDateOfBill(data["date"]) + "_" + billIDCounter[billID] + "_" + str(data["bill"]["type"])+str(data["bill"]["number"])
                    mergedData[billCode] = {}
                    mergedData[billCode]["bill"] = data["bill"]
                    mergedData[billCode]["votes"] = data["votes"]
                    result = data["result_text"]
                    mergedData[billCode]["result"] = "Agreed" in result or "Passed" in result or "Overridden" in result 
                    fraction = data["requires"].split("/")
                    mergedData[billCode]["requires"] = float(fraction[0]) / float(fraction[1])
                    mergedData[billCode]["vote_id"] = data["vote_id"]
                # if count > 50:
                #     break
    with open('mergedData.json', 'w') as f:
     json.dump(mergedData, f, sort_keys=True, indent=4, separators=(',', ': '))
if __name__ == "__main__":
    main()