import os
import json
import nltk
import time
import random
import matplotlib.pyplot

def main():

  with open('training_set.json') as d:
    training_set = json.load(d)

  with open('validation_set.json') as d:
    validation_set = json.load(d)
  model = train_weighted_flip(training_set)
  results = validate_weighted_flip(validation_set, model)
  legislator_success = list()
  for legislator in results[0]:
    legislator_success.append(results[0][legislator].get("success", 0) / float(results[0][legislator]["total"]))
    # print (results[legislator].get("success", 0) / float(results[legislator]["total"]))
  # print (time.time() - startTime)

  print(sum(legislator_success)/ len(legislator_success))
  correct = 0
  for vote in results[1]:
    if results[1][vote]:
      correct += 1
  print ("Correct: " + str(float(correct) / len(results[1])))
  with open('baseline_weightedflip.txt', 'w') as f:
    for p in legislator_success:
      f.write("%s\n" % str(p))
    f.write("%s\n" % ("Legislator Avg: " + str(sum(legislator_success)/ len(legislator_success))))
    f.write("%s\n" % ("Bills Correct: " + str(float(correct) / len(results[1]))))

  results = validate_yea(validation_set)
  legislator_success = list()
  for legislator in results[0]:
    legislator_success.append(results[0][legislator].get("success", 0) / float(results[0][legislator]["total"]))
    # print (results[legislator].get("success", 0) / float(results[legislator]["total"]))
  # print (time.time() - startTime)

  print(sum(legislator_success)/ len(legislator_success))
  correct = 0
  for vote in results[1]:
    if results[1][vote]:
      correct += 1
  print ("Correct: " + str(float(correct) / len(results[1])))
  with open('baseline_yea.txt', 'w') as f:
    for p in legislator_success:
      f.write("%s\n" % str(p))
    f.write("%s\n" % ("Legislator Avg: " + str(sum(legislator_success)/ len(legislator_success))))
    f.write("%s\n" % ("Bills Correct: " + str(float(correct) / len(results[1]))))

  results = validate_nay(validation_set)
  legislator_success = list()
  for legislator in results[0]:
    legislator_success.append(results[0][legislator].get("success", 0) / float(results[0][legislator]["total"]))
    # print (results[legislator].get("success", 0) / float(results[legislator]["total"]))
  # print (time.time() - startTime)

  print(sum(legislator_success)/ len(legislator_success))
  correct = 0
  for vote in results[1]:
    if results[1][vote]:
      correct += 1
  print ("Correct: " + str(float(correct) / len(results[1])))
  with open('baseline_nay.txt', 'w') as f:
    for p in legislator_success:
      f.write("%s\n" % str(p))
    f.write("%s\n" % ("Legislator Avg: " + str(sum(legislator_success)/ len(legislator_success))))
    f.write("%s\n" % ("Bills Correct: " + str(float(correct) / len(results[1]))))

    # matplotlib.pyplot.hist(temp, bins = 10)
    # matplotlib.pyplot.show()



def train_weighted_flip(training_set):
  model = {}
  for vote in training_set:
    if "Nay" in training_set[vote]["votes"]:
      for legislator in training_set[vote]["votes"]["Nay"]:
        if legislator["id"] not in model:
          model[legislator["id"]] = {}
        model[legislator["id"]]["Nay"] = model[legislator["id"]].get("Nay", 0) + 1
    else:
      for legislator in training_set[vote]["votes"]["No"]:
        if legislator["id"] not in model:
          model[legislator["id"]] = {}
        model[legislator["id"]]["Nay"] = model[legislator["id"]].get("Nay", 0) + 1

    if "Yea" in training_set[vote]["votes"]:
      for legislator in training_set[vote]["votes"]["Yea"]:
        if legislator["id"] not in model:
          model[legislator["id"]] = {}
        model[legislator["id"]]["Yea"] = model[legislator["id"]].get("Yea", 0) + 1
    else:
      for legislator in training_set[vote]["votes"]["Aye"]:
        if legislator["id"] not in model:
          model[legislator["id"]] = {}
        model[legislator["id"]]["Yea"] = model[legislator["id"]].get("Yea", 0) + 1

    for legislator in training_set[vote]["votes"]["Not Voting"]:
      if legislator["id"] not in model:
        model[legislator["id"]] = {}
      model[legislator["id"]]["Not Voting"] = model[legislator["id"]].get("Not Voting", 0) + 1
  
  return model

def validate_weighted_flip(validation_set, model):
  results = {}
  vote_results = {}

  for vote in validation_set:
    vote_count = [0,0,0]
    if "Nay" in validation_set[vote]["votes"]:
      for legislator in validation_set[vote]["votes"]["Nay"]:
        if legislator["id"] not in model:
          continue
        label = generate_label(model[legislator["id"]], vote_count)    
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        if label == 0:
          results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    else:
      for legislator in validation_set[vote]["votes"]["No"]:
        if legislator["id"] not in model:
          continue
        label = generate_label(model[legislator["id"]], vote_count)    
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        if label == 0:
          results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    if "Yea" in validation_set[vote]["votes"]:
      for legislator in validation_set[vote]["votes"]["Yea"]:
        if legislator["id"] not in model:
          continue
        label = generate_label(model[legislator["id"]], vote_count)    
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        if label == 1:
          results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    else:
      for legislator in validation_set[vote]["votes"]["Aye"]:
        if legislator["id"] not in model:
          continue
        label = generate_label(model[legislator["id"]], vote_count)    
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        if label == 1:
          results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    for legislator in validation_set[vote]["votes"]["Not Voting"]:
      if legislator["id"] not in model:
        continue
      label = generate_label(model[legislator["id"]], vote_count)
      if legislator["id"] not in results:
        results[legislator["id"]] = {}

      if label == 2:
        results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
      results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
  

    model_result = (vote_count[1] / float(vote_count[0] + vote_count[1])) >= validation_set[vote]["requires"]
    if model_result == validation_set[vote]["result"]:
      vote_results[vote] = True
    else:
      vote_results[vote] = False

  return [results, vote_results]

def validate_yea(validation_set):
  results = {}
  vote_results = {}

  for vote in validation_set:
    vote_count = [0,0,0]
    if "Nay" in validation_set[vote]["votes"]:
      for legislator in validation_set[vote]["votes"]["Nay"]:
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    else:
      for legislator in validation_set[vote]["votes"]["No"]:
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    if "Yea" in validation_set[vote]["votes"]:
      for legislator in validation_set[vote]["votes"]["Yea"]:
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    else:
      for legislator in validation_set[vote]["votes"]["Aye"]:
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    for legislator in validation_set[vote]["votes"]["Not Voting"]:
      if legislator["id"] not in results:
        results[legislator["id"]] = {}
      results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
  

    model_result = True
    if model_result == validation_set[vote]["result"]:
      vote_results[vote] = True
    else:
      vote_results[vote] = False

  return [results, vote_results]

def validate_nay(validation_set):
  results = {}
  vote_results = {}

  for vote in validation_set:
    vote_count = [0,0,0]
    if "Nay" in validation_set[vote]["votes"]:
      for legislator in validation_set[vote]["votes"]["Nay"]:
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    else:
      for legislator in validation_set[vote]["votes"]["No"]:
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    if "Yea" in validation_set[vote]["votes"]:
      for legislator in validation_set[vote]["votes"]["Yea"]:
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    else:
      for legislator in validation_set[vote]["votes"]["Aye"]:
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    for legislator in validation_set[vote]["votes"]["Not Voting"]:
      if legislator["id"] not in results:
        results[legislator["id"]] = {}
      results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
  
    model_result = False
    if model_result == validation_set[vote]["result"]:
      vote_results[vote] = True
    else:
      vote_results[vote] = False

  return [results, vote_results]

def generate_label(legislator, vote_count):
  p_nay = legislator.get("Nay", 0) / float(legislator.get("Nay", 0) + legislator.get("Yea", 0)  + legislator.get("Not Voting", 0)) 
  p_yea = legislator.get("Yea", 0) / float(legislator.get("Nay", 0) + legislator.get("Yea", 0) + legislator.get("Not Voting", 0)) 
  r = random.random()

  if r < p_nay:
    vote_count[0] += 1
    return 0
  elif r < p_nay + p_yea:
    vote_count[1] += 1
    return 1
  else:
    vote_count[2] += 1
    return 2

if __name__ == "__main__":
  main()