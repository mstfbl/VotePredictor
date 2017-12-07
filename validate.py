import os
import sys
import json
import nltk
import time
import random
from heapq import heappush, heappop, heappushpop, nsmallest
from math import log

def main():
  startTime = time.time()
  with open('model.json') as d:
    model = json.load(d)
  with open('validation_set.json') as d:
    validation_set = json.load(d)
  # Usage 
  # python validate.py c n 
  # python validate.py c

  c = 0
  n = 1
  if len(sys.argv) >= 2:
    c = int(sys.argv[1])
  if len (sys.argv) == 3:
    n = int(sys.argv[2])
  for i in range(n):
    results = validate(validation_set, model, i + c)
    temp = list()
    for legislator in results[0]:
      temp.append(results[0][legislator].get("success", 0) / float(results[0][legislator].get("total", 1)))
      # print (results[0][legislator].get("success", 0) / float(results[0][legislator].get("total", 1)))
    print(sum(temp)/ len(temp))

    correct = 0
    for vote in results[1]:
      if results[1][vote]:
        correct += 1
    print ("Correct: " + str(float(correct) / len(results[1])))
    with open('results' + str(i + c) + '.txt', 'w') as f:
      for p in temp:
        f.write("%s\n" % str(p))
      f.write("%s\n" % ("Legislator Avg: " + str(sum(temp)/ len(temp))))
      f.write("%s\n" % ("Bills Correct: " + str(float(correct) / len(results[1]))))

def validate(validation_set, model, c):
  legislator_results = {}
  vote_results = {}
  count = 0
  print (len(validation_set))
  for vote in validation_set:
    vote_count = [0,0,0]
    count += 1
    print (count)
    with open("idf.json") as d:
      idf = json.load(d)
    if len(sys.argv) >= 2:
      billText = tfidf(nltk.word_tokenize(validation_set[vote]["bill"]["text"]), idf, c)
    else:
      billText = nltk.word_tokenize(validation_set[vote]["bill"]["text"])
      billText = [(1, word) for word in billText]
    if "Nay" in validation_set[vote]["votes"]:
      for legislator in validation_set[vote]["votes"]["Nay"]:
        if legislator["id"] not in model:
          continue
        label = generate_label(model[legislator["id"]], billText, vote_count)
        if legislator["id"] not in legislator_results:
          legislator_results[legislator["id"]] = {}

        if label == 0:
          legislator_results[legislator["id"]]["success"] = legislator_results[legislator["id"]].get("success", 0) + 1
        legislator_results[legislator["id"]]["total"] = legislator_results[legislator["id"]].get("total", 0) + 1
    else:
      for legislator in validation_set[vote]["votes"]["No"]:
        if legislator["id"] not in model:
          continue
        label = generate_label(model[legislator["id"]], billText, vote_count)
        if legislator["id"] not in legislator_results:
          legislator_results[legislator["id"]] = {}

        if label == 0:
          legislator_results[legislator["id"]]["success"] = legislator_results[legislator["id"]].get("success", 0) + 1
        legislator_results[legislator["id"]]["total"] = legislator_results[legislator["id"]].get("total", 0) + 1
    if "Yea" in validation_set[vote]["votes"]:
      for legislator in validation_set[vote]["votes"]["Yea"]:
        if legislator["id"] not in model:
          continue
        label = generate_label(model[legislator["id"]], billText, vote_count)
        if legislator["id"] not in legislator_results:
          legislator_results[legislator["id"]] = {}

        if label == 1:
          legislator_results[legislator["id"]]["success"] = legislator_results[legislator["id"]].get("success", 0) + 1
        legislator_results[legislator["id"]]["total"] = legislator_results[legislator["id"]].get("total", 0) + 1
    else:
      for legislator in validation_set[vote]["votes"]["Aye"]:
        if legislator["id"] not in model:
          continue
        label = generate_label(model[legislator["id"]], billText, vote_count)
        if legislator["id"] not in legislator_results:
          legislator_results[legislator["id"]] = {}

        if label == 1:
          legislator_results[legislator["id"]]["success"] = legislator_results[legislator["id"]].get("success", 0) + 1
        legislator_results[legislator["id"]]["total"] = legislator_results[legislator["id"]].get("total", 0) + 1
    

    for legislator in validation_set[vote]["votes"]["Not Voting"]:
      if legislator["id"] not in model:
        continue
      label = generate_label(model[legislator["id"]], billText, vote_count)
      if legislator["id"] not in legislator_results:
        legislator_results[legislator["id"]] = {}

      if label == 2:
        legislator_results[legislator["id"]]["success"] = legislator_results[legislator["id"]].get("success", 0) + 1
      legislator_results[legislator["id"]]["total"] = legislator_results[legislator["id"]].get("total", 0) + 1
    
    print (vote_count)
    model_result = (vote_count[1] / float(vote_count[0] + vote_count[1])) >= validation_set[vote]["requires"]
    if model_result == validation_set[vote]["result"]:
      vote_results[vote] = True
    else:
      vote_results[vote] = False

  return [legislator_results, vote_results]

def generate_label(legislator, billText, vote_count):
  p_nay = 0.
  p_yea = 0.
  p_not_voting = 0.
  k = 1
  for (word, count) in billText:
    word = word.lower()
    if "Nay" in legislator:
      p_nay += count * log(legislator["Nay"].get(word, 0) + k / float(legislator["Nay"].get("total_wc !@#", 0) + k))
    if "Yea" in legislator:
      p_yea += count * log(legislator["Yea"].get(word, 0) + k / float(legislator["Yea"].get("total_wc !@#", 0) + k))
    if "Not Voting" in legislator:
      p_not_voting += count * log(legislator["Not Voting"].get(word, 0) + k / float(legislator["Not Voting"].get("total_wc !@#", 0) + k))
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

def tfidf(billText, idf, c):
  # we got hyperparameters
  word_count = {}
  for word in billText:
    word = word.lower()
    word_count[word] = word_count.get(word, 0) + 1
  length = len(billText)
  heap = []
  for word in word_count:
    tfidf_val = (word_count[word] / float(length)) * (log(idf["total_wc !@#"]) / idf.get(word, 1))
    if len(heap) < c:
      heappush(heap, (tfidf_val, word))
    elif heap[0][0] < tfidf_val:
      heappushpop(heap, (tfidf_val, word))
  return [(word, word_count[word]) for (_, word) in heap]

if __name__ == "__main__":
  main()