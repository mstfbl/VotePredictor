import os
import json
import nltk
import time
import random
from math import log

def main():
  startTime = time.time()
  with open('complete.json') as json_data:
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
  
    # model = train(training_set)
    # print (time.time() - startTime)
    # with open('model.json', 'w') as f:
    #   json.dump(model, f)

  with open('test.json') as d:
    model = json.load(d)
  results = validate(validation_set, model)
  temp = list()
  for legislator in results:
    temp.append(results[legislator].get("success", 0) / float(results[legislator]["total"]))
    print (results[legislator].get("success", 0) / float(results[legislator]["total"]))
  print(sum(temp)/ len(temp))


def train(training_set):
  model = {}
  thing = 0
  textfails = 0
  nayfails = 0
  yeafails = 0
  not_votingfails = 0
  print (textfails, nayfails, yeafails, not_votingfails)
  for vote in training_set:
    flag = 0
    if "text" not in training_set[vote]["bill"]:
      textfails += 1
      flag = 1
    if "Nay" not in training_set[vote]["votes"]:
      nayfails += 1
      flag = 1
    if "Not Voting" not in training_set[vote]["votes"]:
      not_votingfails += 1
      flag = 1
    if "Yea" not in training_set[vote]["votes"]:
      yeafails += 1
      flag = 1
    if flag == 1:
      print(training_set[vote]["bill"]["type"] + str(training_set[vote]["bill"]["number"]))
      continue
    full_text = nltk.word_tokenize(training_set[vote]["bill"]["text"])
    for word in full_text:
      word = word.lower()
      thing += 1
      if (thing % 10000 == 0):
        print (thing)
      if "Nay" in training_set[vote]["votes"]:
        for legislator in training_set[vote]["votes"]["Nay"]:
          if legislator["id"] not in model:
            model[legislator["id"]] = {}
          if "Nay" not in model[legislator["id"]]:
            model[legislator["id"]]["Nay"] = {}
          model[legislator["id"]]["Nay"][word] = model[legislator["id"]]["Nay"].get(word, 0) + 1
          model[legislator["id"]]["Nay"][1] = model[legislator["id"]]["Nay"].get(1, 0) + 1
      else:
        for legislator in training_set[vote]["votes"]["No"]:
          if legislator["id"] not in model:
            model[legislator["id"]] = {}
          if "Nay" not in model[legislator["id"]]:
            model[legislator["id"]]["Nay"] = {}
          model[legislator["id"]]["Nay"][word] = model[legislator["id"]]["Nay"].get(word, 0) + 1
          model[legislator["id"]]["Nay"][1] = model[legislator["id"]]["Nay"].get(1, 0) + 1
      if "Yea" in training_set[vote]["votes"]:
        for legislator in training_set[vote]["votes"]["Yea"]:
          if legislator["id"] not in model:
            model[legislator["id"]] = {}
          if "Yea" not in model[legislator["id"]]:
            model[legislator["id"]]["Yea"] = {}
          model[legislator["id"]]["Yea"][word] = model[legislator["id"]]["Yea"].get(word, 0) + 1
          model[legislator["id"]]["Yea"][1] = model[legislator["id"]]["Yea"].get(1, 0) + 1
      else:
        for legislator in training_set[vote]["votes"]["Aye"]:
          if legislator["id"] not in model:
            model[legislator["id"]] = {}
          if "Yea" not in model[legislator["id"]]:
            model[legislator["id"]]["Yea"] = {}
          model[legislator["id"]]["Yea"][word] = model[legislator["id"]]["Yea"].get(word, 0) + 1
          model[legislator["id"]]["Yea"][1] = model[legislator["id"]]["Yea"].get(1, 0) + 1
      for legislator in training_set[vote]["votes"]["Not Voting"]:
        if legislator["id"] not in model:
          model[legislator["id"]] = {}
        if "Not Voting" not in model[legislator["id"]]:
          model[legislator["id"]]["Not Voting"] = {}
        model[legislator["id"]]["Not Voting"][word] = model[legislator["id"]]["Not Voting"].get(word, 0) + 1
        model[legislator["id"]]["Not Voting"][1] = model[legislator["id"]]["Not Voting"].get(1, 0) + 1
  print (textfails, nayfails, yeafails, not_votingfails)
  return model

def validate(validation_set, model):
  results = {}

  count = 0
  print (len(validation_set))
  for vote in validation_set:
    count += 1
    print (count)
    if "Nay" in validation_set[vote]["votes"]:
      for legislator in validation_set[vote]["votes"]["Nay"]:
        if legislator["id"] not in model:
          continue
        label = generate_label(model[legislator["id"]], validation_set[vote]["bill"]["text"])
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        if label == 0:
          results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    else:
      for legislator in validation_set[vote]["votes"]["No"]:
        if legislator["id"] not in model:
          continue
        label = generate_label(model[legislator["id"]], validation_set[vote]["bill"]["text"])
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        if label == 0:
          results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    if "Yea" in validation_set[vote]["votes"]:
      for legislator in validation_set[vote]["votes"]["Yea"]:
        if legislator["id"] not in model:
          continue
        label = generate_label(model[legislator["id"]], validation_set[vote]["bill"]["text"])
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        if label == 1:
          results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    else:
      for legislator in validation_set[vote]["votes"]["Aye"]:
        if legislator["id"] not in model:
          continue
        label = generate_label(model[legislator["id"]], validation_set[vote]["bill"]["text"])
        if legislator["id"] not in results:
          results[legislator["id"]] = {}

        if label == 1:
          results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
        results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
    

    for legislator in validation_set[vote]["votes"]["Not Voting"]:
      if legislator["id"] not in model:
        continue
      label = generate_label(model[legislator["id"]], validation_set[vote]["bill"]["text"])
      if legislator["id"] not in results:
        results[legislator["id"]] = {}

      if label == 2:
        results[legislator["id"]]["success"] = results[legislator["id"]].get("success", 0) + 1
      results[legislator["id"]]["total"] = results[legislator["id"]].get("total", 0) + 1
        
  return results

def generate_label(legislator, billText):
  p_nay = 0.
  p_yea = 0.
  p_not_voting = 0.
  k = 1
  for word in billText:
    if "Nay" in legislator:
      p_nay += log(legislator["Nay"].get(word, 0) + k / float(legislator["Nay"].get(1, 0) + k))
    if "Yea" in legislator:
      p_yea += log(legislator["Yea"].get(word, 0) + k / float(legislator["Yea"].get(1, 0) + k))
    if "Not Voting" in legislator:
      p_not_voting += log(legislator["Not Voting"].get(word, 0) + k / float(legislator["Not Voting"].get(1, 0) + k))
  p_max = max(p_nay,p_yea,p_nay)
  if p_max == p_nay:
    return 0
  elif p_max == p_yea:
    return 1
  else:
    return 2


if __name__ == "__main__":
  main()