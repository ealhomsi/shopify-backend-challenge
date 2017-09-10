#!/usr/bin/python

#import jason lib and url
import urllib, json


#define main
def main():
	#initialize log file
	log = open("log.txt", "w")

	#open url and read data
	url = "https://backend-challenge-winter-2017.herokuapp.com/customers.json"
	response = urllib.urlopen(url)
	data = json.loads(response.read())

	#find total number of pages
	total = data["pagination"]["total"]

	log.write("the total number of pages is " + str(total))
	results = dict()
	#loop through all pages
	for i in range(1,total+1):
		url = "https://backend-challenge-winter-2017.herokuapp.com/customers.json?page=" + str(i)
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		log.write("\n response " + str(i))
		log.write(str(response))
		log.write("\n");

		validations = data["validations"]
		customers = data["customers"]

		results.update(violations(validations, customers, log))

	print(results)
	log.close()


#define violations
def violations(validaitons, customers, log):
	results = dict()
	for customer in customers:
		for condition in validaitons:
			#for each customer try all problems
			if not validateCustomer(customer, condition, log):
				customerID = customer['id']
				field = key = list(condition)[0]

				log.write("customer number " + str(customerID) + " has a violation in " + str(key) + " \n")
				log.write("condition is " + str(condition) + " customer attribute is " + str(customer[key]) + "\n")
				if customerID in results:
					results[customerID].append(field)
				else:
					results[customerID] = [field]

	return results



#define validation for one customer condition
def validateCustomer(customer, condition, log):
	key = list(condition)[0]
	value = condition[key]

	#fetch conditions
	req = False
	t = None
	minimum = -1
	maximum = -1
	length = None
	if("required" in value): 
		req = value["required"]
	
	if("type" in value): 
		t = value["type"]
	
	if("length" in value):
		length = value["length"]
		minimum = length["min"] if ("min" in length) else -1
		maximum = length["max"] if ("max" in length) else -1

	#test conditions against customer
	if(req):
		if not(key in customer):
			return False

	if(t != None):
		if(t == "boolean" and (key in customer) and not (type(customer[key]) is bool)):
			return False
		if(t == "number" and (key in customer) and not (type(customer[key]) is int)):
			return False
		if(t == "string" and (key in customer) and not (type(customer[key]) is unicode)):
			return False 

	if(minimum != -1 or maximum != -1):
		propertyString = customer[key]
		propertyStringLength = len(propertyString)
		if(propertyStringLength < minimum):
			return False
		elif (propertyStringLength > maximum and maximum != -1):
			return False

	return True

#call main if we are running this program
if __name__ == "__main__":
	main()