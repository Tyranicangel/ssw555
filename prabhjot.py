import datetime

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
             outputErrors += '\nError: US03: birth of a person ' + id + ' seems to occur after death'
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
def outputChildBirthErrors(data, errorList):
    outputErrors = ''
    errorList.sort ( key=lambda x: int ( x[ 0 ].replace ( '@' , "" ).replace ( 'I' , "" ) ) )
    for childId, parentId in errorList:
        outputErrors +='\nError: US09: birth of a child ' + childId + ' seems to occur after death of mother or before nine months of death of father ' + parentId
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
    outputErrors += outputChildBirthErrors ( data, errorMomsList )
    outputErrors += outputChildBirthErrors ( data, errorDadsList )
    return outputErrors

# To check that marriage occurs before divorce and divorce occurs only after marriage
def marriageDivorce(data):
    errorFamList = [ ]
    for id, entry in data[ 'FAM' ].items():
        if 'DIV' in entry:
            if 'MARR' not in entry:
                errorFamList.append ( id )
            elif entry[ 'DIV' ][ 'DATE' ][ 'VAL' ] < entry[ 'MARR' ][ 'DATE' ][ 'VAL' ]:
                errorFamList.append ( id )
    outputErrors = ''
    for familyId in errorFamList:
        outputErrors += '\nError: US04: marriage does not occur before divorce of spouses or divorce occurs before marriage in family ' + familyId
    return outputErrors

# To get the last name of the individual
def getLastName(data, personId):
    return data[ 'INDI' ][ personId ][ 'NAME' ][ 'VAL' ].split(' ')[1]

# To get sex of the individual
def getSex(data, personId):
    return data[ 'INDI' ][ personId ][ 'SEX' ][ 'VAL' ]

# To check that all male members of the family have the same last name
def lastName(data):
    errorFamList = [ ]
    for id, entry in data[ 'FAM' ].items():
        if 'CHIL' in entry:
            dadLastName = getLastName ( data, entry[ 'HUSB' ][ 'VAL' ] )
            if len ( entry[ 'CHIL' ] ) == 1:
                childrenList = [ entry[ 'CHIL' ] ]
            else:
                childrenList = entry[ 'CHIL' ]
            for child in childrenList:
                childLastName = getLastName ( data, child[ 'VAL' ] )
                childSex = getSex ( data, child[ 'VAL' ] )
                if childSex == 'M' and childLastName != dadLastName:
                    errorFamList.append ( id )
                    break
    outputErrors = ''
    for familyId in errorFamList:
        outputErrors += '\nError: US16: not all male members of a family ' + familyId + ' have the same last name'
    return outputErrors

def run(out):
    return birthBeforeDeath ( out ) + childBirth ( out ) + marriageDivorce( out ) + lastName ( out )

