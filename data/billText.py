import os
import json
import datetime
from pprint import pprint

def crawl():
    pass


def main():
    parentPath = "./114/bills/"
    mergedData = {}
    count = 0
    for chamber in os.listdir(parentPath):
        if not chamber.startswith('.'):
            currentChamberPath = parentPath + str(chamber)+"/"
            for bill in os.listdir(currentChamberPath):
                count += 1
                if (str(bill).startswith("hr10") and len(str(bill)) < 6):
                    print str(bill)
                if count % 100 == 0:
                    print count
                if not bill.startswith('.'): #Ignore hidden files/dirs
                    currentBillPath = currentChamberPath + str(bill) + "/text-versions/"
                    maxDate = None
                    bill_id = None
                    for version in os.listdir(currentBillPath):
                        currentVersionPath = currentBillPath + version + "/"
                        if not version.startswith('.'): #Ignore hidden files/dirs
                            data = json.load(open(currentBillPath + version +'/data.json'))
                            if maxDate == None or maxDate < datetime.datetime.strptime(data["issued_on"], '%Y-%m-%d'): 
                                maxDate = datetime.datetime.strptime(data["issued_on"], '%Y-%m-%d')
                                with open(currentVersionPath + 'document.txt', 'r') as myfile:
                                    text = myfile.read()
                                bill_id = data["bill_version_id"].split("-")
                                bill_id =  str(maxDate.year) + bill_id[0]
                                bill_dict = {"issued_on" : data["issued_on"], "text" : text}
                
                    mergedData[bill_id] = bill_dict
                    if (str(bill).startswith("hr10") and len(str(bill)) < 6):
                        print bill_id



    with open('billText.json', 'w') as f:
        json.dump(mergedData, f)
        
if __name__ == "__main__":
    main()