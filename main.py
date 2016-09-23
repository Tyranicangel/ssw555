import datetime
import functools
import collections

import akshay
import prad
import prabhjot
import pranay


# To convert string into Datetime
def getDate(dateVal):
	if len(dateVal[0]) == 1:
		dateVal[0] = '0' + dateVal[0]
	return " ".join(dateVal)


# return datetime.datetime.strptime(' '.join(dateVal), '%d %b %Y')

# To get data from dictonary
def getData(mdict, mlist):
	return functools.reduce(lambda d, k: d[k], mlist, mdict)


# To insert data into dictonary
def setData(mdict, mlist, key, val):
	if key in getData(mdict, mlist[:-1])[mlist[-1]]:
		if type(getData(mdict, mlist[:-1])[mlist[-1]][key]) is list:
			getData(mdict, mlist[:-1])[mlist[-1]][key].append(val)
		else:
			getData(mdict, mlist[:-1])[mlist[-1]][key] = [getData(mdict, mlist[:-1])[mlist[-1]][key]]
			getData(mdict, mlist[:-1])[mlist[-1]][key].append(val)
	else:
		getData(mdict, mlist[:-1])[mlist[-1]][key] = val


# user_name=raw_input("Hello!What is your name:")
# fname=raw_input("Well "+user_name+' please enter file name:')

# Tags which are relevant
taglist = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE',
		   'HEAD', 'TRLR', 'NOTE']
# Tags necessary for parsing
readable = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE']
# fname = "akshay.ged"
# fname = "prabhjot.ged"
fname = "prad.ged"


# Holds the complete parsed file
maindict = {}
# Holds data of the previous link
prev = []
# Holds the reponse to be written to the output
response = ""

try:
	filehandler = open(fname, 'r')
	for line in filehandler:
		dat = line.replace("/", "").split()
		if len(dat) >= 2:
			# Putting Level 0 tags in
			if dat[0] == '0':
				if len(dat) >= 3 and dat[2] in readable:
					if dat[2] in maindict:
						maindict[dat[2]][dat[1]] = {}
					else:
						maindict[dat[2]] = {}
						maindict[dat[2]][dat[1]] = {}
					prev = [dat[2], dat[1]]
			else:
				# Other tags
				if dat[1] in readable:
					# Verying if correct level of tag
					if int(dat[0]) != len(prev) - 1:
						prev = prev[0:int(dat[0]) + 1]
					if prev[-1] != False:
						if len(dat) == 2:
							setData(maindict, prev, dat[1], {})
						else:
							if dat[1] == 'DATE':
								setData(maindict, prev, dat[1], {'VAL': getDate(dat[2:])})
							else:
								setData(maindict, prev, dat[1], {'VAL': ' '.join(dat[2:])})
						prev.append(dat[1])
				else:
					if int(dat[0]) != len(prev) - 1:
						prev = prev[0:int(dat[0]) + 1]
					prev.append(False)
	filehandler.close()
except IOError:
	print('This file does not exist.')

# List of people with their details to response
response += "People:\n"
response += "Id".ljust(10) + 'Name'.ljust(30) + 'Gender'.ljust(10) + 'Birthday'.ljust(15) + 'Alive'.ljust(
	10) + 'Death'.ljust(15) + 'Spouse'.ljust(20) + 'Children\n'

for key in sorted(maindict['INDI'], key=lambda x: int(x.replace('@', "").replace('I', ""))):
	response += key.ljust(10) + maindict['INDI'][key]['NAME']['VAL'].ljust(30)
	if 'SEX' in maindict['INDI'][key]:
		response += maindict['INDI'][key]['SEX']['VAL'].ljust(10)
	else:
		response += 'N/A'.ljust(10)
	if 'BIRT' in maindict['INDI'][key]:
		if 'DATE' in maindict['INDI'][key]['BIRT']:
			response += maindict['INDI'][key]['BIRT']['DATE']['VAL'].ljust(15)
		else:
			response += 'N/A'.ljust(15)
	else:
		response += 'N/A'.ljust(15)
	if 'DEAT' in maindict['INDI'][key]:
		if maindict['INDI'][key]['DEAT']['VAL'] == 'Y':
			response += 'Dead'.ljust(10)
			if 'DATE' in maindict['INDI'][key]['DEAT']:
				response += maindict['INDI'][key]['DEAT']['DATE']['VAL'].ljust(15)
			else:
				response += 'N/A'.ljust(15)
		else:
			response += 'Alive'.ljust(10)
			response += 'N/A'.ljust(15)
	else:
		response += 'Alive'.ljust(10)
		response += 'N/A'.ljust(15)
	if 'FAMS' in maindict['INDI'][key]:
		if type(maindict['INDI'][key]['FAMS']) is list:
			response += ','.join([d['VAL'] for d in maindict['INDI'][key]['FAMS']]).ljust(20)
		else:
			response += maindict['INDI'][key]['FAMS']['VAL'].ljust(20)
	else:
		response += 'N/A'.ljust(20)
	if 'FAMC' in maindict['INDI'][key]:
		if type(maindict['INDI'][key]['FAMC']) is list:
			response += ','.join([d['VAL'] for d in maindict['INDI'][key]['FAMC']]) + '\n'
		else:
			response += maindict['INDI'][key]['FAMC']['VAL'] + '\n'
	else:
		response += 'N/A' + '\n'

# List of families with their details to response
response += '\n\n\nFamilies:\n'
response += "Id".ljust(10) + 'Marriage'.ljust(15) + 'Divorce'.ljust(15) + 'Husband'.ljust(60) + 'Wife'.ljust(
    60) + 'Children\n'
for key in sorted(maindict['FAM'], key=lambda x: int(x.replace('@', "").replace('F', ""))):
    response += key.ljust(10)
    if 'MARR' in maindict['FAM'][key]:
        response += maindict['FAM'][key]['MARR']['DATE']['VAL'].ljust(15)
    else:
        response += 'N/A'.ljust(15)
    if 'DIV' in maindict['FAM'][key]:
        response += maindict['FAM'][key]['DIV']['DATE']['VAL'].ljust(15)
    else:
        response += 'N/A'.ljust(15)
    if 'HUSB' in maindict['FAM'][key]:
        response += (maindict['FAM'][key]['HUSB']['VAL'] + ", " + maindict['INDI'][maindict['FAM'][key]['HUSB']['VAL']]['NAME']['VAL']).ljust(60)
    else:
        response += 'N/A'.ljust(40)
    if 'WIFE' in maindict['FAM'][key]:
        response += (maindict['FAM'][key]['WIFE']['VAL'] + ", " + maindict['INDI'][maindict['FAM'][key]['WIFE']['VAL']]['NAME']['VAL']).ljust(60)
    else:
        response += 'N/A'.ljust(40)
    if 'CHIL' in maindict['FAM'][key]:
        if type(maindict['FAM'][key]['CHIL']) is list:
            response += ','.join([d['VAL'] for d in maindict['FAM'][key]['CHIL']]) + '\n'
        else:
            response += maindict['FAM'][key]['CHIL']['VAL'] + '\n'
    else:
        response += 'N/A' + '\n'

# Executing all scripts and combining maindictputs
response += prad.run(maindict) + akshay.run(maindict) + prabhjot.run(maindict) + pranay.run(maindict)

# Response file
writer = open('reponse_' + fname + '.txt', 'w')
writer.write(response)
writer.close()
