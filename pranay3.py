#User story 05 - Marriage before death
import datetime

def run(out):	
	response = ""
	dlist = [] #Store individual-id
	deathlist = [] #Store death date of the corresponding individual who died
	deathdict = {} #Dictionary to store Individual-id as Key and death date as its value

	for count in out['INDI']:
		#print count					
		if 'DEAT' in out['INDI'][count]:			
			if 'DATE' in out['INDI'][count]['DEAT']:
				death_val = out['INDI'][count]['DEAT']['DATE']['VAL']
				fam_id = out['INDI'][count]['FAMS']['VAL']
				dlist.append(count)
				deathlist.append(str(death_val))
				deathdict[fam_id] = [str(death_val)] #Family id with their death dates stored in deathdict dictonary
				#print 'Death date -> ' + str(death_val) + '\n'
				#print 'Name of Individual who died -> ' + str(out['INDI'][count]['NAME']['VAL']) +'\n'
				#print 'Individual id ->' + count +'\n'
				#print 'Family-id of the individual who died -> ' + str(fam_id) +'\n'
	
	#print dlist
	#print deathlist
	print '\nDictionary of family-ids with death dates ->' ,deathdict
	#print '\n Death dict - ', deathdict.keys()[0]

	fdlist = []	
	marrdict = {}
	for count in out['FAM']:
		if 'HUSB' in out['FAM'][count] and 'WIFE' in out['FAM'][count] and 'MARR' in out['FAM'][count]:			
			fdlist.append(count)
			marrdate = out['FAM'][count]['MARR']['DATE']['VAL']
			for k,v in deathdict.iteritems():
				if k == count:
					if v > str(marrdate):
						print 'Success'
						print 'Marriage date ->',str(marrdate)
					else:
						print 'Failure'
						print 'Marriage date ->',str(marrdate)
		else:
			print '\nNo one is married in this GEDCOM file data.'

	return response