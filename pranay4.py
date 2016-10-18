#User story 07 - Less then 150 years old
#Death should be less than 150 years after birth for dead people, 
#and current date should be less than 150 years after birth for all living people
# to get only date => t = datetime.date.today()
# 					  t.year => returns YEAR

import datetime

def run(out):
	#print out
	today = datetime.datetime.today()
	response = ""

	birthdict = {}
	for count in out['INDI']:
		#Print Individual-ID's present in the family
		#print out['INDI']

		if 'BIRT' in out['INDI'][count]:
			#Value of birth date
			val = out['INDI'][count]['BIRT']['DATE']['VAL']		

			#Calculate age
			age = (today.year) - (val.year)
			if age < 0:
				print 'Anomaly: US07: - Future birth date of individual-id ' +count + ' Birth year -> ', (val.year), '\n'
			elif age >= 0 and age < 150:
				birthdict[count] = [str(val)] #Store individual-id and birthdate in dictionary
				print 'Success'
				print 'Individual id BD->',count
				print 'Birth date ->',val.date()
				print 'Age ->',age, ' years.\n'
			else:
				print 'Error: US07: - Age is more than 150 years, individual-id ' + count + ' Birth year -> ', (val.year), '\n'
		#print birthdict, '\n'

				
		if 'DEAT' in out['INDI'][count]:
			print str(out['INDI'][count]['DEAT']['VAL'])			
			if 'DATE' in out['INDI'][count]['DEAT']:
				dval = out['INDI'][count]['DEAT']['DATE']['VAL']

				for x,y in birthdict.iteritems():
					if x == count: #IF Individual-id's are same then get birth date 
						birth = str(birthdict[x]) # Store the value for key in variable birth in string format
						birthyear = birth[2:6] # Stores only the year value
						#print 'In death block , birth date -',birth, '\n' 
						#print 'Type of birth ', type(birth), '\n'				
						deathyear = str(dval.year)
						age = int(deathyear) - int(birthyear)

						if age >= 0 and age < 150:
							print 'Success, Individual id- ' + count + 'Death year - ', (dval.year), '\n'
						else: # age < 0:
						 	print 'Anomaly: US07: - Future birth date of individual-id ' +count + ' Birth year -> ', (birthyear), '\n'
				
				#print 'Individual id DD ->',count
				#print 'Death date ->',val.date()
				#print '\n'

	return response
				#if val > today:
				#	response += "Error: US01: Death date of " + count + " greater than today\n"