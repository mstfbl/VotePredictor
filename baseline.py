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

  # Weighted flip baseline
  model = train_weighted_flip(training_set)
  results = validate_weighted_flip(validation_set, model)
  legislator_success = list()
  for legislator in results[0]:
    legislator_success.append(results[0][legislator].get("success", 0) / float(results[0][legislator]["total"]))

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

  # All Yea Baseline
  results = validate_yea(validation_set)
  legislator_success = list()
  for legislator in results[0]:
    legislator_success.append(results[0][legislator].get("success", 0) / float(results[0][legislator]["total"]))

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

  # All Nay Baseline
  results = validate_nay(validation_set)
  legislator_success = list()
  for legislator in results[0]:
    legislator_success.append(results[0][legislator].get("success", 0) / float(results[0][legislator]["total"]))

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


def train_weighted_flip(training_set):
  model = {}
  for vote in training_set:
    
    def trainer(givenVote):
        if givenVote in training_set[vote]["votes"]:
          for legislator in training_set[vote]["votes"][givenVote]:
            # group Aye with Yea and No with Nay
            loggedCategory = givenVote
            if givenVote == "Aye":
              loggedCategory = "Yea"
            elif givenVote == "No":
              loggedCategory = "Nay"

            # initialize new congressman
            if legislator["id"] not in model:
              model[legislator["id"]] = {}

            # increment word count for a given label
            model[legislator["id"]][loggedCategory] = model[legislator["id"]].get(loggedCategory, 0) + 1
      
    trainer("Nay")
    trainer("No")
    trainer("Yea")
    trainer("Aye")
    trainer("Not Voting")
  return model

def validate_weighted_flip(validation_set, model):
  vote_results = {}
  legislator_results = {}
  for vote in validation_set:
    vote_count = [0,0,0]

    def validateXVotes(givenVote,givenLabel):
      if givenVote in validation_set[vote]["votes"]:
        for legislator in validation_set[vote]["votes"][givenVote]:
          if legislator["id"] not in model:
            dprint("Congressman not seen in training set preset in model test - " + givenVote)
            continue
          label = generate_label(model[legislator["id"]], vote_count)
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

def validate_yea(validation_set):
  vote_results = {}
  legislator_results = {}
  for vote in validation_set:
    def validateXVotes(givenVote,givenLabel):
      if givenVote in validation_set[vote]["votes"]:
        for legislator in validation_set[vote]["votes"][givenVote]:
          if legislator["id"] not in legislator_results:
            legislator_results[legislator["id"]] = {}
          #If predicted correctly
          if givenVote == "Yea" or givenVote == "Aye":
            legislator_results[legislator["id"]]["success"] = legislator_results[legislator["id"]].get("success", 0) + 1
          legislator_results[legislator["id"]]["total"] = legislator_results[legislator["id"]].get("total", 0) + 1
 
    #Validating votes predicted
    validateXVotes("Nay",0)
    validateXVotes("No",0)
    validateXVotes("Yea",1)
    validateXVotes("Aye",1)
    validateXVotes("Not Voting",2)

    model_result = True
    if model_result == validation_set[vote]["result"]:
      vote_results[vote] = True
    else:
      vote_results[vote] = False

  return [legislator_results, vote_results]

def validate_nay(validation_set):
  vote_results = {}
  legislator_results = {}
  for vote in validation_set:
    def validateXVotes(givenVote,givenLabel):
      if givenVote in validation_set[vote]["votes"]:
        for legislator in validation_set[vote]["votes"][givenVote]:
          if legislator["id"] not in legislator_results:
            legislator_results[legislator["id"]] = {}
          #If predicted correctly
          if givenVote == "Nay" or givenVote == "No":
            legislator_results[legislator["id"]]["success"] = legislator_results[legislator["id"]].get("success", 0) + 1
          legislator_results[legislator["id"]]["total"] = legislator_results[legislator["id"]].get("total", 0) + 1
 
    #Validating votes predicted
    validateXVotes("Nay",0)
    validateXVotes("No",0)
    validateXVotes("Yea",1)
    validateXVotes("Aye",1)
    validateXVotes("Not Voting",2)

    model_result = True
    if model_result == validation_set[vote]["result"]:
      vote_results[vote] = True
    else:
      vote_results[vote] = False

  return [legislator_results, vote_results]

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