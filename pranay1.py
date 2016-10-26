#User story 05 - Marriage before death
import datetime

def run(out):	
	response = ""

	for count in out['INDI']:
		#print count
		
		# if 'BIRT' in out['INDI'][count]:
		# 	val = out['INDI'][count]['BIRT']['DATE']['VAL']
		# 	if val > today:
				
		# 		response += "Error: US01: Birth date of " + count + " greater than today\n"
				
		if 'DEAT' in out['INDI'][count]:
			if 'DATE' in out['INDI'][count]['DEAT']:
				death_val = out['INDI'][count]['DEAT']['DATE']['VAL']
				print '\n\n\n'
				print 'Death date -> ' + str(death_val) + '\n'
				print 'Name of Individual who died -> ' + str(out['INDI'][count]['NAME']['VAL']) +'\n'
				print 'Individual id ->' +count +'\n'
				print 'Family-id of the individual who died -> ' + str(out['INDI'][count]['FAMS']['VAL']) +'\n'
				

	for count in out['FAM']:

		if 'MARR' in out['FAM'][count]:
			if 'DATE' in out['FAM'][count]['MARR']:
				marriage_val = out['FAM'][count]['MARR']['DATE']['VAL']
				husb_val = out['FAM'][count]['HUSB']['VAL']
				wife_val = out['FAM'][count]['WIFE']['VAL']
				print 'Marriage date -> ' + str(marriage_val) + '\n'
				print 'Husband-ID ->' +str(husb_val)+' Wife-ID ->' +str(wife_val)+'\n'
				print '------------------------------------------------------------\n'
		# if 'DIV' in out['FAM'][count]:
		# 	if 'DATE' in out['FAM'][count]['DIV']:
		# 		val = out['FAM'][count]['DIV']['DATE']['VAL']
		# 		if val > today:
		# 			response += "Error: US01: Divorce date of "+ count + " greater than today\n"

		# if 'HUSB' in out['FAM'][count]:

		# 	val = out['FAM'][count]['HUSB']['VAL']
		# 	gender = out['INDI'][val]['SEX']['VAL']

		# 	if gender != 'M':
		# 		response += "Warning: US21: " +val+ " Gender is not correct\n"

		# if 'WIFE' in out['FAM'][count]:

		# 	val = out['FAM'][count]['WIFE']['VAL']
		# 	gender = out['INDI'][val]['SEX']['VAL']

		# 	if gender != 'F':
		# 		response += "Warning: US21: " +val+ " Gender is not correct\n"

	return response