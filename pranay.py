import datetime

def run(out):
	today = datetime.datetime.today()
	response = ""

	for count in out['INDI']:

		if 'BIRT' in out['INDI'][count]:
			val = out['INDI'][count]['BIRT']['DATE']['VAL']
			if val > today:
				
				response += "Error: Birth date of " + count + " greater than today\n"
				# print "Birth date of ", count, " greater than today"	
				
		if 'DEAT' in out['INDI'][count]:
			if 'DATE' in out['INDI'][count]['DEAT']:
				val = out['INDI'][count]['DEAT']['DATE']['VAL']
				if val > today:
					response += "Error: Death date of " + count + " greater than today\n"

	for count in out['FAM']:

		if 'MARR' in out['FAM'][count]:
			if 'DATE' in out['FAM'][count]['MARR']:
				val = out['FAM'][count]['MARR']['DATE']['VAL']
				if val > today:
					response += "Error: Marriage date of "+ count + " greater than today\n"	
				# print "Birth date of ", count, " greater than today"	
				
		if 'DIV' in out['FAM'][count]:
			if 'DATE' in out['FAM'][count]['DIV']:
				val = out['FAM'][count]['DIV']['DATE']['VAL']
				if val > today:
					response += "Error: Divorce date of "+ count + " greater than today\n"

		if 'HUSB' in out['FAM'][count]:

			val = out['FAM'][count]['HUSB']['VAL']
			gender = out['INDI'][val]['SEX']['VAL']

			if gender != 'M':
				response += "Warning: " +val+ " Gender is not correct\n"

		if 'WIFE' in out['FAM'][count]:

			val = out['FAM'][count]['WIFE']['VAL']
			gender = out['INDI'][val]['SEX']['VAL']

			if gender != 'F':
				response += "Warning: " +val+ " Gender is not correct\n"

	return response