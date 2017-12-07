import os
import json
import nltk
import time
import random
import argparse

def dprint(explanation,msg):
  if args.debug == 1:
    print(explanation + ": " + str(msg))

def main():
  #Pre data collection and setup
  with open('complete.json') as json_data:
    data = json.load(json_data)
    validation_set_size = round(len(data) / 10)
    training_set_size = len(data) - validation_set_size
    training_set = {}
    validation_set = {}
    for key in data:
      if (training_set_size == 0) or (validation_set_size > 0 and random.random() < .1):
        validation_set[key] = data[key]
        validation_set_size -= 1
      else:
        training_set_size -= 1
        training_set[key] = data[key]
    with open('training_set.json', 'w') as f:
      json.dump(training_set, f)

    with open('validation_set.json', 'w') as f:
      json.dump(validation_set, f)

    #Train model and time the training
    startTime = time.time()
    model = train(training_set)
    dprint("Time for model to train",time.time() - startTime)
    with open('model.json', 'w') as f:
      json.dump(model, f)

#Training our prediction model
def train(training_set):
  model = {}
  idf = {}
  counter = 0
  for vote in training_set:
    #Splits text into words
    full_text = nltk.word_tokenize(training_set[vote]["bill"]["text"])
    words = set(full_text)
    for word in words:
      idf[word] = idf.get(word, 0) + 1

    #Iterate over words in text
    for word in full_text:
      word = word.lower()
      counter += 1
      if (counter % 10000 == 0):
        dprint("Iterator",counter)
      
      #Train prediction model for each given vote aka Nay,No,Yea,Aye,Not Voring
      def trainer(givenVote):
        if givenVote in training_set[vote]["votes"]:
          for legislator in training_set[vote]["votes"][givenVote]:
            if legislator["id"] not in model:
              model[legislator["id"]] = {}
            if givenVote not in model[legislator["id"]]:
              model[legislator["id"]][givenVote] = {}
            model[legislator["id"]][givenVote][word] = model[legislator["id"]][givenVote].get(word, 0) + 1
            model[legislator["id"]][givenVote]["total_wc !@#"] = model[legislator["id"]][givenVote].get(1, 0) + 1
      trainer("Nay")
      trainer("No")
      trainer("Yea")
      trainer("Aye")
      trainer("Not Voting")

  idf["total_wc !@#"] = len(training_set)
  with open('idf.json', 'w') as f:
    json.dump(idf, f)
  return model

parser = argparse.ArgumentParser()
parser.add_argument("debug")
parser.parse_args()

if __name__ == "__main__":
  main()