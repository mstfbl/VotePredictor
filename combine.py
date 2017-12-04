import os
import json
import datetime

def main():
	with open('mergedData.json') as json_data:
		votes = json.load(json_data)
	print (len(votes))
	with open('billText.json') as json_data:
		print ("hi")
		billText = json.load(json_data)
	print ("rip")

	count = 0
	for vote in votes:
		count += 1
		bill_id = vote[14:]
		vote_date = datetime.datetime.strptime(vote[0:10], "%Y-%m-%d")
		maxDate = None
		maxVersion = None
		for version in billText[bill_id]:
			version_date = datetime.datetime.strptime(billText[bill_id][version]["issued_on"], "%Y-%m-%d")
			if maxDate == None or (version_date > maxDate and version_date < vote_date):
				maxDate = version_date
				maxVersion = version
		votes[vote]['bill']['text'] = billText[bill_id][maxVersion]['text']

		if count % 10 == 0:
			print (count)

	with open('complete.json', 'w') as f:
		json.dump(votes, f)

if __name__ == "__main__":
	main()