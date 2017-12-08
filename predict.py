import sys
import json
import nltk
from heapq import heappush, heappop, heappushpop, nsmallest
from math import log

def main():
  # Usage 
  # python predict.py bill.txt

  with open('model.json') as d:
    model = json.load(d)
  with open("idf.json") as d:
    idf = json.load(d)
  with open("names.json") as d:
    names = json.load(d)

  bill = sys.argv[1]
  c = 9
  k = 3

  with open(bill) as f:
    billText = f.read()


  vote_count = [0,0,0]
  billText = tfidf(nltk.word_tokenize(billText), idf, c)
  for legislator in model:
    result = generate_label(model[legislator], billText)
    if result == 0:
      print ("Legislator " + names.get(legislator, legislator) + " predicted to vote Nay")
    if result == 1:
      print ("Legislator " + names.get(legislator, legislator) + " predicted to vote Yea")
    if result == 2:
      print ("Legislator " + names.get(legislator, legislator) + " predicted to vote Abstain")
    vote_count[result] += 1

  print ("Number of predicted Yeas: " + str(vote_count[1]))
  print ("Number of predicted Nays: " + str(vote_count[0]))
  print ("Number of predicted Abstains: " + str(vote_count[2]))

#Generate predictions for bills given the legislator(Congressman)
def generate_label(legislator, billText):
  #Probability of votes being Nay vs Yea, as well as not voting
  p_nay = 0.
  p_yea = 0.
  p_not_voting = 0.
  k = 1
  unique_words = len(set([word for (word, _) in billText]))
  for (word, count) in billText:
  #Modifying Nay vs Yeah probabilities given each word
    word = word.lower()
    if "Nay" in legislator:
      p_nay += log((legislator["Nay"].get(word, 0) + k) / (float(legislator["Nay"].get("total_wc !@#", 0) + k * unique_words)))
    if "Yea" in legislator:
      p_yea += log((legislator["Yea"].get(word, 0) + k) / (float(legislator["Yea"].get("total_wc !@#", 0) + k * unique_words)))
    if "Not Voting" in legislator:
      p_not_voting += log((legislator["Not Voting"].get(word, 0) + k) / (float(legislator["Not Voting"].get("total_wc !@#", 0) + k * unique_words)))
  #Choose the highest probability label
  p_max = max(p_nay,p_yea,p_not_voting)
  if p_max == p_nay:
    return 0
  elif p_max == p_yea:
    return 1
  else:
    return 2

#The TF-IDF algorithm with hyperparameters
def tfidf(billText, idf, c):
  word_count = {}
  for word in billText:
    word = word.lower()
    word_count[word] = word_count.get(word, 0) + 1
  length = len(billText)
  heap = []
  #Obtain the most important words using TF-IDF with min-heap
  for word in word_count:
    tfidf_val = (word_count[word] / float(length)) * (log(idf["total_wc !@#"]) / idf.get(word, 1))
    if len(heap) < c:
      heappush(heap, (tfidf_val, word))
    elif heap[0][0] < tfidf_val:
      heappushpop(heap, (tfidf_val, word))
  return [(word, word_count[word]) for (_, word) in heap]

if __name__ == "__main__":
  main()