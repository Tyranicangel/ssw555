import datetime

# To output essential parts of entry
def briefEntry(entry):
    output = entry[ 'NAME' ][ 'VAL' ].ljust ( 30 ) + entry[ 'BIRT' ][ 'DATE' ][ 'VAL' ].strftime ( '%m/%d/%Y' ).ljust ( 15 )
    if 'DEAT' in entry:
        output += entry[ 'DEAT' ][ 'DATE' ][ 'VAL' ].strftime ( '%m/%d/%Y' ).ljust ( 15 )
    else:
        output += 'N/A'.ljust ( 15 )
    return output

# To check that birth occurs before death of an individual
def birthBeforeDeath(data):
    errorEntriesList = [ ]
    for id, entry in data[ 'INDI' ].items():
        if 'BIRT' in entry and 'DEAT' in entry:
            if entry[ 'BIRT' ][ 'DATE' ][ 'VAL' ] > entry[ 'DEAT' ][ 'DATE' ][ 'VAL' ]:
                errorEntriesList.append ( ( id , entry ) )
    if errorEntriesList != [ ]:
        errorEntriesList.sort ( key=lambda x: int ( x[ 0 ].replace ( '@' , "" ).replace ( 'I' , "" ) ) )
        outputErrors = '';
        for id, entry in errorEntriesList:
             outputErrors += '\nError: US03: birth of a person '+id+' seems to occur after death'
        # outputErrors += '\n'
    else:
        outputErrors = ''
    return outputErrors

# To get death date if any
def getDeath(data, personId):
    if 'DEAT' in data[ 'INDI' ][ personId ]:
    	if 'DATE' in data['INDI'][personId]['DEAT']:
        	return data[ 'INDI' ][ personId ][ 'DEAT' ][ 'DATE' ][ 'VAL' ]
    else:
        return None

# To output errors of child birth vs. parent death properly
def outputChildBirthErrors(data, errorList, parentCaption, errorCaption):
    outputErrors = ''
    if errorList != [ ]:
        errorList.sort ( key=lambda x: int ( x[ 0 ].replace ( '@' , "" ).replace ( 'I' , "" ) ) )
        outputErrors += errorCaption
        for childId, parentId in errorList:
        	outputErrors +='\nError: US09: Birth of a child'+childId+'seems to occur after death of mother or before nine months of death of father '+parentId+'\n'
    return outputErrors

# To check that child is born before death of mother
# and before 9 months after death of father
def childBirth(data):
    errorMomsList = [ ]
    errorDadsList = [ ]
    for id, entry in data[ 'FAM' ].items():
        if 'CHIL' in entry:
            momId = entry[ 'WIFE' ][ 'VAL' ]
            momDeathDate = getDeath ( data , momId )
            dadId = entry[ 'HUSB' ][ 'VAL' ]
            dadDeathDate = getDeath ( data , dadId )
            if len ( entry[ 'CHIL' ] ) == 1:
                childrenList = [ entry[ 'CHIL' ] ]
            else:
                childrenList = entry[ 'CHIL' ]
            for child in childrenList:
                childId = child[ 'VAL' ]
                if 'BIRT' in data[ 'INDI' ][ childId ]:
                    childBirthDate = data[ 'INDI' ][ childId ][ 'BIRT' ][ 'DATE' ][ 'VAL' ]
                    if momDeathDate is not None and momDeathDate < childBirthDate:
                        errorMomsList.append ( ( childId, momId ) )
                    if dadDeathDate is not None and dadDeathDate + datetime.timedelta ( days = 275 ) < childBirthDate:
                        errorDadsList.append ( ( childId, dadId ) )
    outputErrors = ''
    outputErrors += outputChildBirthErrors ( data, errorMomsList, 'Mother:   ', '' )
    outputErrors += outputChildBirthErrors ( data, errorDadsList, 'Father:   ', '' )
    return outputErrors

def run(out):
	return birthBeforeDeath ( out ) + childBirth ( out )
	
