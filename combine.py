import os
import json
import datetime


def main():
	with open('mergedData.json') as json_data:
		votes = json.load(json_data)

	with open('billText.json') as json_data:
		print "hi"
		billText = json.load(json_data)
	print "rip"

	count = 0
	for bill in votes:
		count += 1
		votes[bill]['bill']['text'] = billText[bill]['text']
		if count % 10:
			print count

	with open('complete.json', 'w') as f:
		json.dump(mergedData, f)    


if __name__ == "__main__":
	main()