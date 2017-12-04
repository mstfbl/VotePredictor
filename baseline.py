import os
import json
import nltk
import time
import random
import matplotlib.pyplot

def main():
  with open('complete.json') as json_data:
    startTime = time.time()
    data = json.load(json_data)
    validation_set_size = len(data) / 10
    training_set = {}
    validation_set = {}
    for key in data:
      if validation_set_size > 0 and random.random() < .1:
        validation_set[key] = data[key]
        validation_set_size -= 1
      else:
        training_set[key] = data[key]
    
    model = train_weighted_flip(training_set)
    results = validate_weighted_flip(validation_set, model)
    temp = list()
    for legislator in results:
      temp.append(results[legislator].get("success", 0) / float(results[legislator]["total"]))
      print (results[legislator].get("success", 0) / float(results[legislator]["total"]))
    # print (time.time() - startTime)

    print(sum(temp)/ len(temp))
    matplotlib.pyplot.hist(temp, bins = 10)
    matplotlib.pyplot.show()



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

  for vote in validation_set:
    if "Nay" in validation_set[vote]["votes"]:
      for legislator in validation_set[vote]["votes"]["Nay"]:
        if legislator["id"] not in model:
          continue
        label = generate_label(model[legislator["id"]])    
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        if label == 0:
          results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    else:
      for legislator in validation_set[vote]["votes"]["No"]:
        if legislator["id"] not in model:
          continue
        label = generate_label(model[legislator["id"]])    
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        if label == 0:
          results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    if "Yea" in validation_set[vote]["votes"]:
      for legislator in validation_set[vote]["votes"]["Yea"]:
        if legislator["id"] not in model:
          continue
        label = generate_label(model[legislator["id"]])    
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        if label == 1:
          results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    else:
      for legislator in validation_set[vote]["votes"]["Aye"]:
        if legislator["id"] not in model:
          continue
        label = generate_label(model[legislator["id"]])    
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        if label == 1:
          results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    for legislator in validation_set[vote]["votes"]["Not Voting"]:
      if legislator["id"] not in model:
        continue
      label = generate_label(model[legislator["id"]])
      if legislator["id"] not in results:
        results[legislator["id"]] = {}

      if label == 2:
        results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
      results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
        
  return results


def generate_label(legislator):
  p_nay = legislator.get("Nay", 0) / float(legislator.get("Nay", 0) + legislator.get("Yea", 0)  + legislator.get("Not Voting", 0)) 
  p_yea = legislator.get("Yea", 0) / float(legislator.get("Nay", 0) + legislator.get("Yea", 0) + legislator.get("Not Voting", 0)) 
  r = random.random()

  p_nay = 0.
  p_yea = 1.
  if r < p_nay:
    return 0
  elif r < p_nay + p_yea:
    return 1
  else:
    return 2

if __name__ == "__main__":
  main()