import datetime

def datediff(date1,date2):
	return date1-date2

def getage(indi):
	if 'DEAT' in indi:
		if indi[ 'DEAT' ][ 'VAL' ] == 'Y':
			return 'N/A'.ljust ( 10 )
		else:
			return (datetime.datetime.today ( ) - indi[ 'BIRT' ][ 'DATE' ][
				'VAL' ]).days // 365
	else:
		return (datetime.datetime.today ( ) - indi[ 'BIRT' ][ 'DATE' ][
			'VAL' ]).days // 365 
