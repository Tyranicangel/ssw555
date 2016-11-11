from datetime import datetime
import operator


# method to handle the dictionary of siblings to fetch the difference between their birthdates
def days_between(dictofdate , familyid):
    response = ''
    if len ( dictofdate ) >= 15:
        response += '\nERROR: US15: THERE ARE MORE THAN 15 SIBLINGS IN ' + familyid + ' FAMILY.'
    newdict = {}
    for keys in dictofdate:
        if isinstance ( dictofdate[ keys ] , dict ):
            newdict[ keys ] = dictofdate[ keys ][ 'VAL' ]
    sorted_list = sorted ( newdict.items ( ) , key=operator.itemgetter ( 1 ) )
    i = 0
    while i < len ( sorted_list ) - 1:
        j = i + 1
        while j < len ( sorted_list ):
            date1 = datetime.strptime ( newdict[ sorted_list[ i ][ 0 ] ].strftime ( '%m/%d/%Y' ) , "%m/%d/%Y" )
            date2 = datetime.strptime ( newdict[ sorted_list[ j ][ 0 ] ].strftime ( '%m/%d/%Y' ) , "%m/%d/%Y" )
            numberofdays = int ( abs ( (date1 - date2).days ) )
            if (2 > numberofdays >= 0) or numberofdays > 243:
                i += 1
                break
            else:
                response += '\nERROR: US13: THERE IS UNUSUAL DIFFERENCE IN DATE OF BIRTH OF ' + sorted_list[ i ][
                    0 ] + ' AND ' + sorted_list[ j ][ 0 ] + '.'
                j += 1
    return response


def get_descendants_list(maindict, individual_id):
    descendants_list = []
    if 'FAMC' in maindict[ 'INDI' ][ individual_id ]:
        if type ( maindict[ 'INDI' ][ individual_id ][ 'FAMC' ] ) is list:
            for d in maindict['INDI'][individual_id]['FAMC']:
                if 'HUSB' in maindict[ 'FAM' ][ d['VAL'] ]:
                    descendants_list.append (maindict[ 'FAM' ][ d['VAL'] ][ 'HUSB' ][ 'VAL' ])
                    descendants_list.extend(get_descendants_list(maindict, maindict[ 'FAM' ][ d['VAL'] ][ 'HUSB' ][ 'VAL' ]))
                if 'WIFE' in maindict[ 'FAM' ][ d['VAL'] ]:
                    descendants_list.append (maindict[ 'FAM' ][ d['VAL'] ][ 'WIFE' ][ 'VAL' ])
                    descendants_list.extend(get_descendants_list(maindict, maindict[ 'FAM' ][ d['VAL'] ][ 'WIFE' ][ 'VAL' ]))
        else:
            if 'HUSB' in maindict[ 'FAM' ][ maindict[ 'INDI' ][ individual_id ][ 'FAMC' ][ 'VAL' ] ]:
                descendants_list.append ( maindict[ 'FAM' ][ maindict[ 'INDI' ][ individual_id ][ 'FAMC' ][ 'VAL' ] ][ 'HUSB' ][ 'VAL' ] )
                descendants_list.extend (
                    get_descendants_list ( maindict , maindict[ 'FAM' ][ maindict[ 'INDI' ][ individual_id ][ 'FAMC' ][ 'VAL' ] ][ 'HUSB' ][ 'VAL' ] ) )
            if 'WIFE' in maindict[ 'FAM' ][ maindict[ 'INDI' ][ individual_id ][ 'FAMC' ][ 'VAL' ] ]:
                descendants_list.append ( maindict[ 'FAM' ][ maindict[ 'INDI' ][ individual_id ][ 'FAMC' ][ 'VAL' ] ][ 'WIFE' ][ 'VAL' ] )
                descendants_list.extend (
                    get_descendants_list ( maindict , maindict[ 'FAM' ][ maindict[ 'INDI' ][ individual_id ][ 'FAMC' ][ 'VAL' ] ][ 'WIFE' ][ 'VAL' ] ) )
    return descendants_list


# method to parse the main dictionary and generate response for user stories
def getsiblingsbdate(dict):
    # LOOP ACCORDING TO FAMILY
    siblingdict = {}
    response = ''
    famid = ''
    for key in sorted ( dict[ 'FAM' ] , key=lambda x: int ( x.replace ( '@' , "" ).replace ( 'F' , "" ) ) ):
        if siblingdict.__len__ ( ) > 0:
            response += days_between ( siblingdict , famid )
        siblingdict = {}
        if 'CHIL' in dict[ 'FAM' ][ key ]:
            if type ( dict[ 'FAM' ][ key ][ 'CHIL' ] ) is list:
                for d in dict[ 'FAM' ][ key ][ 'CHIL' ]:
                    famid = key
                    if 'BIRT' in dict[ 'INDI' ][ d[ 'VAL' ] ]:
                        if 'DATE' in dict[ 'INDI' ][ d[ 'VAL' ] ][ 'BIRT' ]:
                            siblingdict.update ( {d[ 'VAL' ]: {'VAL': dict[ 'INDI' ][ d[ 'VAL' ] ][
                                'BIRT' ][ 'DATE' ][ 'VAL' ]}} )
                        else:
                            siblingdict.update ( {d[ 'VAL' ]: 'N/A'} )
                    else:
                        siblingdict.update ( {d[ 'VAL' ]: 'N/A'} )
            else:
                if 'BIRT' in dict[ 'INDI' ][
                    dict[ 'FAM' ][ key ][ 'CHIL' ][ 'VAL' ] ]:
                    if 'DATE' not in \
                            dict[ 'INDI' ][ dict[ 'FAM' ][ key ][ 'CHIL' ][ 'VAL' ] ][
                                'BIRT' ]:
                        response += '\nWARNING: US15: THERE IS ONLY 1 SIBLING IN THE FAMILY ' + key + ' : ' + \
                                    dict[ 'FAM' ][ key ][ 'CHIL' ][ 'VAL' ] \
                                    + ' AND ITS BIRTHDATE IS NOT AVAILABLE.'
                else:
                    response += '\nWARNING: US15: THERE IS ONLY 1 SIBLING IN THE FAMILY ' + key + ' : ' + \
                                dict[ 'FAM' ][ key ][ 'CHIL' ][ 'VAL' ] \
                                + ' AND ITS BIRTHDATE IS NOT AVAILABLE.'

        husbandid = ''
        wifeid = ''
        family_id_husband_is_child_of = ''
        family_id_wife_is_child_of = ''
        husband_id_from_family_id_husband_is_child_of = ''
        wife_id_from_family_id_husband_is_child_of = ''
        husband_id_from_family_id_wife_is_child_of = ''
        wife_id_from_family_id_wife_is_child_of = ''
        family_id_husband_id_from_family_id_husband_is_child_of = ''
        family_id_wife_id_from_family_id_husband_is_child_of = ''
        family_id_husband_id_from_family_id_wife_is_child_of = ''
        family_id_wife_id_from_family_id_wife_is_child_of = ''

        value1 = 'False'
        value2 = 'False'
        value3 = 'False'
        value4 = 'False'

        if 'HUSB' in dict[ 'FAM' ][ key ]:
            husbandid = dict[ 'FAM' ][ key ][ 'HUSB' ][ 'VAL' ]
            husband_des_list = get_descendants_list(dict, husbandid)

        if 'WIFE' in dict[ 'FAM' ][ key ]:
            wifeid = dict[ 'FAM' ][ key ][ 'WIFE' ][ 'VAL' ]
            wife_des_list = get_descendants_list(dict, wifeid)

        if wifeid != '' and husbandid != '':
            if len(husband_des_list) > 0:
                if wifeid in husband_des_list:
                    response += '\nERROR : US17 : IN FAMILY ' + key + ' PARENTS ARE MARRIED WITH THEIR DESCENDANTS.'

            if len(wife_des_list) > 0:
                if husbandid in wife_des_list:
                    response += '\nERROR : US17 : IN FAMILY ' + key + ' PARENTS ARE MARRIED WITH THEIR DESCENDANTS.'

            if 'FAMC' in dict[ 'INDI' ][ husbandid ]:
                family_id_husband_is_child_of = dict[ 'INDI' ][ husbandid ][ 'FAMC' ][
                    'VAL' ]

            if 'FAMC' in dict[ 'INDI' ][ wifeid ]:
                family_id_wife_is_child_of = dict[ 'INDI' ][ wifeid ][ 'FAMC' ][
                    'VAL' ]

            if family_id_husband_is_child_of != '' and family_id_wife_is_child_of != '':
                if family_id_husband_is_child_of == family_id_wife_is_child_of:
                    response += '\nERROR : US18 : IN FAMILY ' + key + ' SIBLINGS ARE MARRIED.'

                if 'HUSB' in dict[ 'FAM' ][ family_id_husband_is_child_of ]:
                    husband_id_from_family_id_husband_is_child_of = \
                        dict[ 'FAM' ][ family_id_husband_is_child_of ][ 'HUSB' ][ 'VAL' ]

                if 'WIFE' in dict[ 'FAM' ][ family_id_husband_is_child_of ]:
                    wife_id_from_family_id_husband_is_child_of = \
                        dict[ 'FAM' ][ family_id_husband_is_child_of ][ 'WIFE' ][ 'VAL' ]

                if 'HUSB' in dict[ 'FAM' ][ family_id_wife_is_child_of ]:
                    husband_id_from_family_id_wife_is_child_of = dict[ 'FAM' ][ family_id_wife_is_child_of ][
                        'HUSB' ][ 'VAL' ]

                if 'WIFE' in dict[ 'FAM' ][ family_id_wife_is_child_of ]:
                    wife_id_from_family_id_wife_is_child_of = dict[ 'FAM' ][ family_id_wife_is_child_of ][
                        'WIFE' ][ 'VAL' ]

                if ((husband_id_from_family_id_husband_is_child_of != '' or wife_id_from_family_id_husband_is_child_of != '') and
                        (husband_id_from_family_id_wife_is_child_of != '' or wife_id_from_family_id_wife_is_child_of != '')):

                    if husband_id_from_family_id_husband_is_child_of != '':
                        if ('FAMC' in dict[ 'INDI' ][
                            husband_id_from_family_id_husband_is_child_of ]):
                            family_id_husband_id_from_family_id_husband_is_child_of = \
                               dict[ 'INDI' ][ husband_id_from_family_id_husband_is_child_of ][
                                    'FAMC' ][
                                    'VAL' ]

                    if wife_id_from_family_id_husband_is_child_of != '':
                        if 'FAMC' in dict[ 'INDI' ][
                            wife_id_from_family_id_husband_is_child_of ]:
                            family_id_wife_id_from_family_id_husband_is_child_of = \
                                dict[ 'INDI' ][ wife_id_from_family_id_husband_is_child_of ][
                                    'FAMC' ][
                                    'VAL' ]

                    if husband_id_from_family_id_wife_is_child_of != '':
                        if 'FAMC' in dict[ 'INDI' ][
                            husband_id_from_family_id_wife_is_child_of ]:
                            family_id_husband_id_from_family_id_wife_is_child_of = \
                                dict[ 'INDI' ][ husband_id_from_family_id_wife_is_child_of ][
                                    'FAMC' ][
                                    'VAL' ]

                    if wife_id_from_family_id_wife_is_child_of != '':
                        if 'FAMC' in dict[ 'INDI' ][
                            wife_id_from_family_id_wife_is_child_of ]:
                            family_id_wife_id_from_family_id_wife_is_child_of = \
                                dict[ 'INDI' ][ wife_id_from_family_id_wife_is_child_of ][
                                    'FAMC' ][
                                    'VAL' ]

                    if family_id_husband_id_from_family_id_husband_is_child_of != '' and family_id_husband_id_from_family_id_wife_is_child_of != '':
                        if family_id_husband_id_from_family_id_husband_is_child_of == family_id_husband_id_from_family_id_wife_is_child_of:
                            value1 = 'True'

                    if family_id_husband_id_from_family_id_husband_is_child_of != '' and family_id_wife_id_from_family_id_wife_is_child_of != '':
                        if family_id_husband_id_from_family_id_husband_is_child_of == family_id_wife_id_from_family_id_wife_is_child_of:
                            value2 = 'True'

                    if family_id_wife_id_from_family_id_husband_is_child_of != '' and family_id_husband_id_from_family_id_wife_is_child_of != '':
                        if family_id_wife_id_from_family_id_husband_is_child_of == family_id_husband_id_from_family_id_wife_is_child_of:
                            value3 = 'True'

                    if family_id_wife_id_from_family_id_husband_is_child_of != '' and family_id_wife_id_from_family_id_wife_is_child_of != '':
                        if family_id_wife_id_from_family_id_husband_is_child_of == family_id_wife_id_from_family_id_wife_is_child_of:
                            value4 = 'True'

                    if (value1 != 'False' or value2 != 'False') or (value3 != 'False' or value4 != 'False'):
                        response += '\nERROR : US19 : IN FAMILY ' + key + ' FIRST COUSINS ARE MARRIED.'

    return response


# method to check for unique name and birthdate in gedcom file sprint 2, user story 23
# unique names and birthdate in gedcom file

def checkuniquenameandbirthdate(maindict):
    response = ''
    namedict = {}
    for key in sorted ( maindict[ 'INDI' ] , key=lambda x: int ( x.replace ( '@' , "" ).replace ( 'I' , "" ) ) ):
        if 'BIRT' in maindict[ 'INDI' ][ key ]:
            if 'DATE' in maindict[ 'INDI' ][ key ][ 'BIRT' ]:
                key_name_date = maindict[ 'INDI' ][ key ][ 'NAME' ][ 'VAL' ] + \
                                maindict[ 'INDI' ][ key ][ 'BIRT' ][ 'DATE' ][
                                    'VAL' ].strftime ( '%m/%d/%Y' )
            else:
                key_name_date = maindict[ 'INDI' ][ key ][ 'NAME' ][ 'VAL' ]
        else:
            key_name_date = maindict[ 'INDI' ][ key ][ 'NAME' ][ 'VAL' ]

        if key_name_date in namedict:
            namedict[ key_name_date ].append ( key )
        else:
            namedict[ key_name_date ] = [ ]
            namedict[ key_name_date ].append ( key )
        if 'BIRT' in maindict[ 'INDI' ][ key ]:
            if 'DATE' in maindict[ 'INDI' ][ key ][ 'BIRT' ]:
                if 'FAMS' in maindict['INDI'][key]:
                    if isinstance(maindict['INDI'][key]['FAMS'], list):
                        for items in maindict['INDI'][key]['FAMS']:
                            if 'MARR' in maindict['FAM'][items['VAL']]:
                                if 'DATE' in maindict['FAM'][items['VAL']]['MARR']:
                                    if maindict['INDI'][key]['BIRT']['DATE']['VAL'] > maindict['FAM'][items['VAL']]['MARR']['DATE']['VAL']:
                                        response += 'ERROR: US02: BIRTH OF INDIVIDUAL ' + key + ' IS AFTER ITS MARRIAGE DATE.\n'
                    else:
                        if 'MARR' in maindict[ 'FAM' ][ maindict['INDI'][key]['FAMS']['VAL'] ]:
                            if 'DATE' in maindict[ 'FAM' ][ maindict['INDI'][key]['FAMS']['VAL'] ][ 'MARR' ]:
                                if maindict[ 'INDI' ][ key ][ 'BIRT' ][ 'DATE' ][ 'VAL' ] > \
                                        maindict[ 'FAM' ][ maindict['INDI'][key]['FAMS']['VAL'] ][ 'MARR' ][ 'DATE' ][ 'VAL' ]:
                                    response += 'ERROR: US02: BIRTH OF INDIVIDUAL ' + key + ' IS AFTER ITS MARRIAGE DATE.\n'
    for key in namedict:
        if len ( namedict[ key ] ) > 1:
            response += 'ERROR: US23: INDIVIDUALS '
            for ids in namedict[ key ]:
                if namedict[ key ].index ( ids ) == len ( namedict[ key ] ) - 1:
                    resp = ids + ' '
                else:
                    resp = ids + ', '
                response += resp
            response += 'HAVE SAME NAME AND BIRTHDATE.\n'

    return response


# method to check if response dictionary is valid or not
def run(out):
    ressponse = getsiblingsbdate ( out )
    ressponse += '\n'
    ressponse += checkuniquenameandbirthdate ( out )
    return ressponse
