import string,os,math,json,unicodedata

# Calculates the frequency of words in a given 
# bill text and keeps a list of seen words
def calcWordFrequencyInSingleText(plainText,allSeenWords):
    count = {}
    plainText.translate(string.punctuation) #Removes punctuations from text of bill
    plainText = plainText.lower() #Make all strings lowercase to avoid capitilization differences
    text = plainText.split(" ")
    for word in text:
        if word in count:
            count[word] += 1
        else:
            count[word] = 1
        if word not in allSeenWords:
            allSeenWords.add(word)
    freq = {}
    countSum = sum(count.values())
    for word in count:
        freq[word] = (count[word] * 1.0) / countSum
    return freq,allSeenWords

# Calculates the Term Frequency (tf) of the bills
# as required in the tf-idf calculations, and returns
# all seen words
def calcTermFrequency(bills):
    freqs = {}
    allSeenWords = set()
    for billCode in bills:
        freqs[billCode] = {}
        billText = bills[billCode]["bill"]["text"]
        freqs[billCode],allSeenWords = calcWordFrequencyInSingleText(billText,allSeenWords) #bill["text"] is text of bill
    return freqs,allSeenWords

# Calculates the inverse document frequency of seen words
# as required in the tf-idf calculations
def calcInverseDocumentFrequency(allSeenWords,tfDict):
    idfDict = {}
    numDocuments = len(tfDict)*1.0
    for word in allSeenWords:
        numDocumentsWithWord = 0
        for billDict in tfDict:
            if word in tfDict[billDict]:
                numDocumentsWithWord += 1
        idfDict[word] = math.log(numDocuments/numDocumentsWithWord)
    return idfDict

def calcTF_IDF(tfDict,idfDict):
    tfidfDict = {}
    for billCode in tfDict:
        for word in idfDict:
            tfidfDict[word] = tfDict[billCode][word] * idfDict[word]
    return tfidfDict

def calcTF_IDFDictionary():
    jsonDocument = "./sampleBillTextAndVoterData.json"
    #jsonDocument = "./mergedBillTextAndVoterData.json" #Name of JSON document
    bills = json.load(open(jsonDocument))
    tfDict,allSeenWords = calcTermFrequency(bills)
    print(allSeenWords)
    idfDict = calcInverseDocumentFrequency(allSeenWords,tfDict)
    tfidfDict = calcTF_IDF(tfDict,idfDict)
    print(idfDict)
    print(tfDict)
    print(tfidfDict)
    exit(0)

if __name__ == "__main__":
    calcTF_IDFDictionary()