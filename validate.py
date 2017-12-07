import os
import sys
import json
import nltk
import time
import random
import argparse
from heapq import heappush, heappop, heappushpop, nsmallest
from math import log
DEBUG = 1

def main():
  # Usage 
  # python validate.py start numIter step
  # python validate.py start numIter 
  # python validate.py start
  # python validate.py

  with open('model.json') as d:
    model = json.load(d)
  with open('validation_set.json') as d:
    validation_set = json.load(d)

  c = 12
  numIter = 1
  step = 1
  if len(sys.argv) >= 2:
    c = int(sys.argv[1])
  if len(sys.argv) >= 3:
    numIter = int(sys.argv[2])
  if len(sys.argv) == 4:
    step = int(sys.argv[3])
  for i in range(numIter):
    startTime = time.time()
    results = validate(validation_set, model, i * step + c)
    endTime = time.time()
    temp = list()
    for legislator in results[0]:
      temp.append(results[0][legislator].get("success", 0) / float(results[0][legislator].get("total", 1)))
    dprint("Words Considered: ",  str(step * i + c))
    dprint("Success rate on average for predicting votes of Congressmen",sum(temp)/ len(temp))
    dprint("Time to validate",str((endTime-startTime)//60) + " minutes " + str((endTime-startTime)%60) + " seconds")
    correct = 0
    for vote in results[1]:
      if results[1][vote]:
        correct += 1
    dprint("Correct votes: ",str(float(correct) / len(results[1])))
    with open('results' + str(i * step + c) + '.txt', 'w') as f:
      for p in temp:
        f.write("%s\n" % str(p))
      f.write("%s\n" % ("Legislator Avg: " + str(sum(temp)/ len(temp))))
      f.write("%s\n" % ("Bills Correct: " + str(float(correct) / len(results[1]))))

#Validate predicted votes with actual votes
def validate(validation_set, model, c):
  legislator_results = {}
  vote_results = {}
  count = 0
  dprint("Length of validation set",len(validation_set))
  for vote in validation_set:
    with open("idf.json") as d:
      idf = json.load(d)
    count += 1
    vote_count = [0,0,0]

    #Restricted TF-IDF version of bill texts, cmd line arg for TF-IDF hyperparameter
    if len(sys.argv) >= 2:
      billText = tfidf(nltk.word_tokenize(validation_set[vote]["bill"]["text"]), idf, c)
    else:
      billText = nltk.word_tokenize(validation_set[vote]["bill"]["text"])
      billText = [(1, word) for word in billText]

    #Background info: In Congress, due to small legislature differences, some
    #bills are votes as Nay or No and Aye or Yea. For these purposes, we count
    #Nay & No and Aye & Yeah the same

    #Label = 0 means Nay/No
    #Label = 1 means Yea/Aye

    def validateXVotes(givenVote,givenLabel):
      if givenVote in validation_set[vote]["votes"]:
        for legislator in validation_set[vote]["votes"][givenVote]:
          if legislator["id"] not in model:
            dprint("Congressman not seen in training set preset in model test - " + givenVote)
            continue
          label = generate_label(model[legislator["id"]], billText, vote_count)
          if legislator["id"] not in legislator_results:
            legislator_results[legislator["id"]] = {}
          #If predicted correctly
          if label == givenLabel:
            legislator_results[legislator["id"]]["success"] = legislator_results[legislator["id"]].get("success", 0) + 1
          legislator_results[legislator["id"]]["total"] = legislator_results[legislator["id"]].get("total", 0) + 1
 
    #Validating votes predicted
    validateXVotes("Nay",0)
    validateXVotes("No",0)
    validateXVotes("Yea",1)
    validateXVotes("Aye",1)
    validateXVotes("Not Voting",2)
    
    model_result = (vote_count[1] / float(vote_count[0] + vote_count[1])) >= validation_set[vote]["requires"]
    if model_result == validation_set[vote]["result"]:
      vote_results[vote] = True
    else:
      vote_results[vote] = False
      
  return [legislator_results, vote_results]

#Generate predictions for bills given the legislator(Congressman)
def generate_label(legislator, billText, vote_count):
  #Probability of votes being Nay vs Yea, as well as not voting
  p_nay = 0.
  p_yea = 0.
  p_not_voting = 0.
  k = 1
  for (word, count) in billText:
  #Modifying Nay vs Yeah probabilities given each word
    word = word.lower()
    if "Nay" in legislator:
      p_nay += count * log(legislator["Nay"].get(word, 0) + k / float(legislator["Nay"].get("total_wc !@#", 0) + k))
    if "Yea" in legislator:
      p_yea += count * log(legislator["Yea"].get(word, 0) + k / float(legislator["Yea"].get("total_wc !@#", 0) + k))
    if "Not Voting" in legislator:
      p_not_voting += count * log(legislator["Not Voting"].get(word, 0) + k / float(legislator["Not Voting"].get("total_wc !@#", 0) + k))
  #Choose the highest probable label
  p_max = max(p_nay,p_yea,p_not_voting)
  if p_max == p_nay:
    vote_count[0] += 1
    return 0
  elif p_max == p_yea:
    vote_count[1] += 1
    return 1
  else:
    vote_count[2] += 1
    return 2

#The TF-IDF algorithm with hyperparameters
def tfidf(billText, idf, c):
  word_count = {}
  for word in billText:
    word = word.lower()
    word_count[word] = word_count.get(word, 0) + 1
  length = len(billText)
  heap = []
  #Obtain the most important words using TF-IDF with heapsort
  for word in word_count:
    tfidf_val = (word_count[word] / float(length)) * (log(idf["total_wc !@#"]) / idf.get(word, 1))
    if len(heap) < c:
      heappush(heap, (tfidf_val, word))
    elif heap[0][0] < tfidf_val:
      heappushpop(heap, (tfidf_val, word))
  return [(word, word_count[word]) for (_, word) in heap]

def dprint(explanation,msg):
  if DEBUG == 1:
    print(explanation + ": " + str(msg))

if __name__ == "__main__":
  main()