import datetime
from collections import defaultdict

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
def getDeathBirth(data, personId, fieldName):
    if personId is not None and fieldName in data[ 'INDI' ][ personId ] and \
       'DATE' in data[ 'INDI' ][ personId ][ fieldName ]:
        return data[ 'INDI' ][ personId ][ fieldName ][ 'DATE' ][ 'VAL' ]
    return None

# To output errors of child birth vs. parent death properly
def outputChildBirthErrors(data, errorList, errType):
    outputErrors = ''
    errorList.sort ( key=lambda x: int ( x[ 0 ].replace ( '@' , "" ).replace ( 'I' , "" ) ) )
    for childId, parentId in errorList:
        if errType == 'US09':
            outputErrors +='\nError: US09: birth of a child ' + childId + ' seems to occur after death of mother or before nine months of death of father ' + parentId
        elif errType == 'US12':
            outputErrors +='\nError: US12: Mother should be less than 60 years older than her children and father should be less than 80 years older than his children: ' + childId + ', ' + parentId
    return outputErrors

# To check that child is born before death of mother
# and before 9 months after death of father
def childBirth(data):
    errorMomsList = [ ]
    errorDadsList = [ ]
    for id, entry in data[ 'FAM' ].items():
        if 'CHIL' in entry:
            if 'WIFE' in entry:
                momId = entry[ 'WIFE' ][ 'VAL' ]
            else:
                momId = None
            momDeathDate = getDeathBirth ( data , momId , 'DEAT' )
            if 'HUSB' in entry:
                dadId = entry[ 'HUSB' ][ 'VAL' ]
            else:
                dadId = None
            dadDeathDate = getDeathBirth ( data , dadId , 'DEAT' )
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
    outputErrors += outputChildBirthErrors ( data, errorMomsList , 'US09' )
    outputErrors += outputChildBirthErrors ( data, errorDadsList , 'US09' )
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
        if 'HUSB' in entry and 'CHIL' in entry:
            dadLastName = getLastName ( data, entry[ 'HUSB' ][ 'VAL' ] )
            childrenList = getMultipleVals( entry[ 'CHIL' ] )
            for childId in childrenList:
                childLastName = getLastName ( data, childId )
                childSex = getSex ( data, childId )
                if childSex == 'M' and childLastName != dadLastName:
                    errorFamList.append ( id )
                    break
    outputErrors = ''
    for familyId in errorFamList:
        outputErrors += '\nError: US16: not all male members of a family ' + familyId + ' have the same last name'
    return outputErrors

# To check if person is alive today
def isAliveToday(data, personId):
    personEntry = data[ 'INDI' ][ personId ]
    return 'BIRT' in personEntry and personEntry[ 'BIRT' ][ 'DATE' ][ 'VAL' ] <= datetime.datetime.today() and \
           ( 'DEAT' not in personEntry or personEntry[ 'DEAT' ][ 'DATE' ][ 'VAL' ] > datetime.datetime.today() )

# To get all living descendants of a person
def getDescendants(data, personId):
    descendantSet = set()
    for familyId, entry in data[ 'FAM' ].items():
        if ( 'HUSB' in entry and entry[ 'HUSB' ][ 'VAL' ] == personId or \
           'WIFE' in entry and entry[ 'WIFE' ][ 'VAL' ] == personId ) and \
           'CHIL' in entry:
            childrenList = getMultipleVals( entry[ 'CHIL' ] )
            for childId in childrenList:
                descendantSet.add( ( childId, isAliveToday ( data, childId ) ) )
    for descendantId, status in descendantSet:
        descendantSet = descendantSet | getDescendants(data, descendantId)
    return descendantSet

def getMultipleVals(entry):
    if len ( entry ) == 1:
        return [ entry[ 'VAL' ] ]
    else:
        valList = [ ]
        for item in entry:
            valList.append ( item[ 'VAL' ] )
    return valList

# To list all living spouses and descendants of people who died in the last 30 days
def livingRelatives(data):
    relDict = { }
    for personId, personEntry in data[ 'INDI' ].items():
        if 'DEAT' in personEntry:
            deatDate = personEntry[ 'DEAT' ][ 'DATE' ][ 'VAL' ]
            if deatDate <= datetime.datetime.today() and deatDate > datetime.datetime.today() - datetime.timedelta ( days = 30 ):
                relDict.setdefault (  personId, [ ] )
                if 'FAMS' in personEntry:
                    famSList = getMultipleVals( personEntry[ 'FAMS' ] )
                for familyId in famSList:
                    familyEntry = data[ 'FAM' ]
                    if 'WIFE' in familyEntry and isAliveToday ( data, familyEntry[ 'WIFE' ][ 'VAL' ] ):
                        relDict[ personId ].append ( familyEntry[ 'WIFE' ][ 'VAL' ] )
                    elif 'HUSB' in familyEntry and isAliveToday ( data, familyEntry[ 'HUSB' ][ 'VAL' ] ):
                        relDict[ personId ].append ( familyEntry[ 'HUSB' ][ 'VAL' ] )
                descendantList = list ( getDescendants ( data, personId ) )
                descendantList.sort( key=lambda x: int ( x[ 0 ].strip ( '@I' ) ) )
                for descendantId, isAlive in descendantList:
                    if isAlive:
                        relDict[ personId ].append ( descendantId )
    outputInfo = ''
    for deceasedId, relIdList in sorted ( list ( relDict.items() ), key=lambda x: int ( x[ 0 ].strip ( '@I' ) ) ):
        if relIdList == [ ]:
            outputInfo += '\nINFO: US37: A person ' + deceasedId + ', who died in the last 30 days, had no living relatives'
        else:
            outputInfo += '\nINFO: US37: A person ' + deceasedId + ', who died in the last 30 days, had living relatives ' + ', '.join ( relIdList )
    return outputInfo 

# To detect all living couples whose marriage anniversary will occur in the next 30 days 
def upcomingAnniversaries(data):
    anniList = [ ]
    thirtyDaysFromToday = datetime.datetime.today() + datetime.timedelta ( days = 30 )
    for id, entry in data[ 'FAM' ].items():
        if 'HUSB' in entry and isAliveToday ( data, entry[ 'HUSB' ][ 'VAL' ] ) and \
           'WIFE' in entry and isAliveToday ( data, entry[ 'WIFE' ][ 'VAL' ] ) and \
           'MARR' in entry and entry[ 'MARR' ][ 'DATE' ][ 'VAL' ] < datetime.datetime.today() and \
           ( 'DIV' not in entry or entry[ 'DIV' ][ 'DATE' ][ 'VAL' ] > thirtyDaysFromToday ):
            anniDate = entry[ 'MARR' ][ 'DATE' ][ 'VAL' ].replace ( year = datetime.datetime.today().year )
            if anniDate > datetime.datetime.today() and anniDate <= thirtyDaysFromToday:
                anniList.append ( ( id, entry ) )
            else:
                anniDate = entry[ 'MARR' ][ 'DATE' ][ 'VAL' ].replace ( year = datetime.datetime.today().year + 1 )
                if anniDate > datetime.datetime.today() and anniDate <= thirtyDaysFromToday:
                    anniList.append ( ( id, entry ) )
    outputInfo = ''
    for id, entry in anniList:
        outputInfo += '\nINFO: US39: A living couple ' + id + ' (' + entry[ 'HUSB' ][ 'VAL' ] + ', ' + entry[ 'WIFE' ][ 'VAL' ] + ') discovered whose marriage anniversary is to occur in the next 30 days'
    return outputInfo

def getCheckDate(data, personId, fieldName, delta):
    birthDate = getDeathBirth ( data , personId , fieldName )
    if birthDate is not None:
        return birthDate.replace ( year = birthDate.year + delta )
    return None

# To check that mother is less than 60 years older than her children and father is less than 80 years older than his children
def checkParentsAges(data):
    errorMomsList = [ ]
    errorDadsList = [ ]
    for id, entry in data[ 'FAM' ].items():
        if 'CHIL' in entry:
            if 'WIFE' in entry:
                momId = entry[ 'WIFE' ][ 'VAL' ]
            else:
                momId = None
            momCheckDate = getCheckDate( data, momId , 'BIRT', 60)

            if 'HUSB' in entry:
                dadId = entry[ 'HUSB' ][ 'VAL' ]
            else:
                dadId = None
            dadCheckDate = getCheckDate( data, dadId , 'BIRT', 80)

            childrenList = getMultipleVals ( entry[ 'CHIL' ] )

            for childId in childrenList:
                if 'BIRT' in data[ 'INDI' ][ childId ]:
                    childBirthDate = data[ 'INDI' ][ childId ][ 'BIRT' ][ 'DATE' ][ 'VAL' ]
                    if momCheckDate is not None and momCheckDate < childBirthDate:
                        errorMomsList.append ( ( childId, momId ) )
                    if dadCheckDate is not None and dadCheckDate < childBirthDate:
                        errorDadsList.append ( ( childId, dadId ) )
    outputErrors = ''
    outputErrors += outputChildBirthErrors ( data, errorMomsList , 'US12' )
    outputErrors += outputChildBirthErrors ( data, errorDadsList , 'US12' )
    return outputErrors

# To check that no more than five siblings are born at the same time
def checkFiveSiblings(data):
    errList = [ ]
    for famId, entry in data[ 'FAM' ].items():
        if 'CHIL' in entry:
            childrenList = getMultipleVals ( entry[ 'CHIL' ] )
            birthDateDict = defaultdict(list)
            for childId in childrenList:
                if 'BIRT' in data[ 'INDI' ][ childId ]:
                    childBirthDate = data[ 'INDI' ][ childId ][ 'BIRT' ][ 'DATE' ][ 'VAL' ].strftime ( '%m/%d/%Y' )
                    birthDateDict[ childBirthDate ].append ( childId )
            for date, idList in birthDateDict.items():
                if len(idList) > 5:
                    errList.append ( ( famId , sorted ( idList, key=lambda x: int ( x.strip ( '@I' ) ) ) ) )
    outputErrors = ''
    for famId, siblingList in errList:
        outputErrors += '\nError: US14: More than five siblings in family ' + famId + ' were born at the same time: ' + ', '.join ( siblingList )
    return outputErrors
                

def run(out):
    return birthBeforeDeath ( out ) + childBirth ( out ) + marriageDivorce( out ) + lastName ( out ) + livingRelatives ( out ) + upcomingAnniversaries ( out ) + checkParentsAges ( out ) + checkFiveSiblings ( out )

