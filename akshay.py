from datetime import datetime
import operator

key_individual = 'INDI'
key_individual_name = 'NAME'
key_individual_sex = 'SEX'
key_individual_birthdate = 'BIRT'
key_individual_deathdate = 'DEAT'
key_individual_child_of_family = 'FAMC'
key_individual_spouse_of_family = 'FAMS'
key_family = 'FAM'
key_family_marriagedate = 'MARR'
key_family_husbid = 'HUSB'
key_family_wifeid = 'WIFE'
key_family_child = 'CHIL'
key_family_divorce = 'DIV'
key_date = 'DATE'
key_value = 'VAL'


# method to handle the dictionary of siblings to fetch the difference between their birthdates
def days_between(dictofdate , familyid):
    response = ''
    if len ( dictofdate ) >= 15:
        response += '\nERROR: US15: THERE ARE MORE THAN 15 SIBLINGS IN ' + familyid + ' FAMILY.'
    newdict = {}
    for keys in dictofdate:
        if isinstance ( dictofdate[ keys ] , dict ):
            newdict[ keys ] = dictofdate[ keys ][ key_value ]
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


# method to parse the main dictionary and generate response for user stories
def getsiblingsbdate(dict):
    # LOOP ACCORDING TO FAMILY
    siblingdict = {}
    response = ''
    famid = ''
    for key in sorted ( dict[ key_family ] , key=lambda x: int ( x.replace ( '@' , "" ).replace ( 'F' , "" ) ) ):
        if siblingdict.__len__ ( ) > 0:
            response += days_between ( siblingdict , famid )
        siblingdict = {}
        if key_family_child in dict[ key_family ][ key ]:
            if type ( dict[ key_family ][ key ][ key_family_child ] ) is list:
                for d in dict[ key_family ][ key ][ key_family_child ]:
                    famid = key
                    if key_individual_birthdate in dict[ key_individual ][ d[ key_value ] ]:
                        if key_date in dict[ key_individual ][ d[ key_value ] ][ key_individual_birthdate ]:
                            siblingdict.update ( {d[ key_value ]: {key_value: dict[ key_individual ][ d[ key_value ] ][
                                key_individual_birthdate ][ key_date ][ key_value ]}} )
                        else:
                            siblingdict.update ( {d[ key_value ]: 'N/A'} )
                    else:
                        siblingdict.update ( {d[ key_value ]: 'N/A'} )
            else:
                if key_individual_birthdate in dict[ key_individual ][
                    dict[ key_family ][ key ][ key_family_child ][ key_value ] ]:
                    if key_date not in \
                            dict[ key_individual ][ dict[ key_family ][ key ][ key_family_child ][ key_value ] ][
                                key_individual_birthdate ]:
                        response += '\nWARNING: US15: THERE IS ONLY 1 SIBLING IN THE FAMILY ' + key + ' : ' + \
                                    dict[ key_family ][ key ][ key_family_child ][ key_value ] \
                                    + ' AND ITS BIRTHDATE IS NOT AVAILABLE.'
                else:
                    response += '\nWARNING: US15: THERE IS ONLY 1 SIBLING IN THE FAMILY ' + key + ' : ' + \
                                dict[ key_family ][ key ][ key_family_child ][ key_value ] \
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

        if key_family_husbid in dict[ key_family ][ key ]:
            husbandid = dict[ key_family ][ key ][ key_family_husbid ][ key_value ]

        if key_family_wifeid in dict[ key_family ][ key ]:
            wifeid = dict[ key_family ][ key ][ key_family_wifeid ][ key_value ]

        if wifeid != '' and husbandid != '':
            if key_individual_child_of_family in dict[ key_individual ][ husbandid ]:
                family_id_husband_is_child_of = dict[ key_individual ][ husbandid ][ key_individual_child_of_family ][
                    key_value ]

            if key_individual_child_of_family in dict[ key_individual ][ wifeid ]:
                family_id_wife_is_child_of = dict[ key_individual ][ wifeid ][ key_individual_child_of_family ][
                    key_value ]

            if family_id_husband_is_child_of != '' and family_id_wife_is_child_of != '':

                if key_family_husbid in dict[ key_family ][ family_id_husband_is_child_of ]:
                    husband_id_from_family_id_husband_is_child_of = \
                        dict[ key_family ][ family_id_husband_is_child_of ][ key_family_husbid ][ key_value ]

                if key_family_wifeid in dict[ key_family ][ family_id_husband_is_child_of ]:
                    wife_id_from_family_id_husband_is_child_of = \
                        dict[ key_family ][ family_id_husband_is_child_of ][ key_family_wifeid ][ key_value ]

                if key_family_husbid in dict[ key_family ][ family_id_wife_is_child_of ]:
                    husband_id_from_family_id_wife_is_child_of = dict[ key_family ][ family_id_wife_is_child_of ][
                        key_family_husbid ][ key_value ]

                if key_family_wifeid in dict[ key_family ][ family_id_wife_is_child_of ]:
                    wife_id_from_family_id_wife_is_child_of = dict[ key_family ][ family_id_wife_is_child_of ][
                        key_family_wifeid ][ key_value ]

                if ((husband_id_from_family_id_husband_is_child_of != '' or wife_id_from_family_id_husband_is_child_of != '') and
                        (husband_id_from_family_id_wife_is_child_of != '' or wife_id_from_family_id_wife_is_child_of != '')):

                    if husband_id_from_family_id_husband_is_child_of != '':
                        if (key_individual_child_of_family in dict[ key_individual ][
                            husband_id_from_family_id_husband_is_child_of ]):
                            family_id_husband_id_from_family_id_husband_is_child_of = \
                               dict[ key_individual ][ husband_id_from_family_id_husband_is_child_of ][
                                    key_individual_child_of_family ][
                                    key_value ]

                    if wife_id_from_family_id_husband_is_child_of != '':
                        if key_individual_child_of_family in dict[ key_individual ][
                            wife_id_from_family_id_husband_is_child_of ]:
                            family_id_wife_id_from_family_id_husband_is_child_of = \
                                dict[ key_individual ][ wife_id_from_family_id_husband_is_child_of ][
                                    key_individual_child_of_family ][
                                    key_value ]

                    if husband_id_from_family_id_wife_is_child_of != '':
                        if key_individual_child_of_family in dict[ key_individual ][
                            husband_id_from_family_id_wife_is_child_of ]:
                            family_id_husband_id_from_family_id_wife_is_child_of = \
                                dict[ key_individual ][ husband_id_from_family_id_wife_is_child_of ][
                                    key_individual_child_of_family ][
                                    key_value ]

                    if wife_id_from_family_id_wife_is_child_of != '':
                        if key_individual_child_of_family in dict[ key_individual ][
                            wife_id_from_family_id_wife_is_child_of ]:
                            family_id_wife_id_from_family_id_wife_is_child_of = \
                                dict[ key_individual ][ wife_id_from_family_id_wife_is_child_of ][
                                    key_individual_child_of_family ][
                                    key_value ]

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
    for key in sorted ( maindict[ key_individual ] , key=lambda x: int ( x.replace ( '@' , "" ).replace ( 'I' , "" ) ) ):
        if key_individual_birthdate in maindict[ key_individual ][ key ]:
            if key_date in maindict[ key_individual ][ key ][ key_individual_birthdate ]:
                key_name_date = maindict[ key_individual ][ key ][ key_individual_name ][ key_value ] + \
                                maindict[ key_individual ][ key ][ key_individual_birthdate ][ key_date ][
                                    key_value ].strftime ( '%m/%d/%Y' )
            else:
                key_name_date = maindict[ key_individual ][ key ][ key_individual_name ][ key_value ]
        else:
            key_name_date = maindict[ key_individual ][ key ][ key_individual_name ][ key_value ]

        if key_name_date in namedict:
            namedict[ key_name_date ].append ( key )
        else:
            namedict[ key_name_date ] = [ ]
            namedict[ key_name_date ].append ( key )
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
