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
        outputErrors = '\nError: birth of a person seems to occur after death in entries:\n'
        for id, entry in errorEntriesList:
             outputErrors += id.ljust ( 10 ) + briefEntry ( entry )  + '\n'
        outputErrors += '\n'
    else:
        outputErrors = ''
    return outputErrors

# To get death date if any
def getDeath(data, personId):
    if 'DEAT' in data[ 'INDI' ][ personId ]:
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
            outputErrors += 'Child:    ' + childId.ljust ( 10 ) + briefEntry ( data[ 'INDI' ][ childId ] )  + '\n'
            outputErrors += parentCaption + parentId.ljust ( 10 ) + briefEntry ( data[ 'INDI' ][ parentId ] )  + '\n\n'
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
    outputErrors += outputChildBirthErrors ( data, errorMomsList, 'Mother:   ', '\nError: birth of a child seems to occur after death of mother in entries:\n' )
    outputErrors += outputChildBirthErrors ( data, errorDadsList, 'Father:   ', '\nError: birth of a child seems to occur later than 9 months after death of father in entries:\n' )
    return outputErrors

def run(out):
	return birthBeforeDeath ( out ) + childBirth ( out )

