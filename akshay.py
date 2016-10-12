from datetime import datetime
import operator


# method to handle the dictionary of siblings to fetch the difference between their birthdates
def days_between(dictofdate, familyid):
    length = len(dictofdate)
    response = ''
    if length >= 15:
        response += '\nERROR: US15: THERE ARE MORE THAN 15 SIBLINGS IN ' + familyid + ' FAMILY.'
    newdict = {}
    for keys in dictofdate:
        if isinstance(dictofdate[keys], dict):
            newdict[keys] = dictofdate[keys]['VAL']
    sorted_list = sorted(newdict.items(), key=operator.itemgetter(1))
    i = 0
    while i < len(sorted_list)-1:
        j = i + 1
        while j < len(sorted_list):
            d1 = newdict[sorted_list[i][0]]
            d2 = newdict[sorted_list[j][0]]
            date1 = datetime.strptime ( d1.strftime('%m/%d/%Y') , "%m/%d/%Y" )
            date2 = datetime.strptime ( d2.strftime('%m/%d/%Y') , "%m/%d/%Y" )
            numberofdays = int(abs((date1 - date2).days))
            if (2 > numberofdays >= 0) or numberofdays > 243:
                i += 1
                break
            else:
                response += '\nERROR: US13: THERE IS UNUSUAL DIFFERENCE IN DATE OF BIRTH OF ' + sorted_list[i][0] + ' AND ' + sorted_list[j][0] +'.'
                j += 1
    return response


# method to parse the main dictionary and generate response for user stories
def getsiblingsbdate(dict):
    # LOOP ACCORDING TO FAMILY
    siblingdict = {}
    response = ''
    famid = ''
    for key in sorted ( dict[ 'FAM' ] , key=lambda x: int ( x.replace ( '@' , "" ).replace ( 'F' , "" ) ) ):
        if siblingdict.__len__() > 0:
            response += days_between (siblingdict , famid)
        siblingdict = {}
        if 'CHIL' in dict[ 'FAM' ][ key ]:
            if type ( dict[ 'FAM' ][ key ][ 'CHIL' ] ) is list:
                for d in dict[ 'FAM' ][ key ][ 'CHIL' ]:
                    famid = key
                    if 'BIRT' in dict[ 'INDI' ][ d[ 'VAL' ] ]:
                        if 'DATE' in dict[ 'INDI' ][ d[ 'VAL' ] ][ 'BIRT' ]:
                            siblingdict.update({d['VAL'] : {'VAL' : dict['INDI'][d['VAL']]['BIRT']['DATE']['VAL']}})
                        else:
                            siblingdict.update({d['VAL'] : 'N/A'})
                    else:
                        siblingdict.update ( {d[ 'VAL' ]: 'N/A'} )
            else:
                if 'BIRT' in dict[ 'INDI' ][ dict[ 'FAM' ][ key ][ 'CHIL' ][ 'VAL' ] ]:
                    if 'DATE' not in dict[ 'INDI' ][ dict[ 'FAM' ][ key ][ 'CHIL' ][ 'VAL' ] ][ 'BIRT' ]:
                        response += '\nWARNING: US15: THERE IS ONLY 1 SIBLING IN THE FAMILY ' + key + ' : ' +\
                                            dict[ 'FAM' ][ key ][ 'CHIL' ][ 'VAL' ]\
                                            + ' AND ITS BIRTHDATE IS NOT AVAILABLE.'
                else:
                    response += '\nWARNING: US15: THERE IS ONLY 1 SIBLING IN THE FAMILY ' + key + ' : ' + \
                                        dict[ 'FAM' ][ key ][ 'CHIL' ][ 'VAL' ] \
                                        + ' AND ITS BIRTHDATE IS NOT AVAILABLE.'
    return response



# method to check for unique name and birthdate in gedcom file sprint 2, user story 23
# unique names and birthdate in gedcom file

def checkuniquenameandbirthdate(maindict):
    response = ''
    namelist = []
    birthdatelist = []
    idlist = []
    for key in sorted ( maindict[ 'INDI' ] , key=lambda x: int ( x.replace ( '@' , "" ).replace ( 'I' , "" ) ) ):
        namelist.append(maindict['INDI'][key]['NAME']['VAL'])
        idlist.append(key)
        if 'BIRT' in maindict[ 'INDI' ][ key ]:
            if 'DATE' in maindict[ 'INDI' ][ key ][ 'BIRT' ]:
                birthdatelist.append(maindict['INDI'][key]['BIRT']['DATE']['VAL'])
            else:
                birthdatelist.append('N/A')
        else:
            birthdatelist.append ( 'N/A' )

    count = 0
    for names in namelist:
        indexs = list_duplicates_of(namelist, names)
        # print ( 'name : ' , names , 'index : ', namelist.index(names) )
        # print ( 'same name index : ' , indexs )
        if len(indexs) > 1:
            indexs_birthdate = list_duplicates_of(birthdatelist, birthdatelist[count])
            if len(indexs_birthdate) > 1:
                # print('same birthdate index : ', indexs_birthdate)
                commonindexes = set(indexs) & set(indexs_birthdate)
                sorted_common_indexes = sorted(commonindexes)
                # print('common indexes : ', sorted_common_indexes)
        count += 1

    # print()


def list_duplicates_of(list,item_to_check):
    start_from = -1
    duplicate_locs = []
    while True:
        try:
            location = list.index(item_to_check,start_from+1)
        except ValueError:
            break
        else:
            duplicate_locs.append(location)
            start_from = location
    return duplicate_locs



# method to check if response dictionary is valid or not
def run(out):
    ressponse = getsiblingsbdate(out)
    # print(checkuniquenameandbirthdate(out))
#    ressponse += checkuniquenameandbirthdate(out)
    return ressponse
