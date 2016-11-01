import datetime


def run(out):
    # print out

    today = datetime.datetime.today ( )
    response = ""
    birthdict = {}  # Dictionary which maintains the {Key,Val} as {Indi-id, Birthdates}

    for count in out[ 'INDI' ]:
        if 'BIRT' in out[ 'INDI' ][ count ]:
            val = out[ 'INDI' ][ count ][ 'BIRT' ][ 'DATE' ][ 'VAL' ]
            birthdict[ count ] = val.date ( )  # Stores {Key,Val} as {Indi-id, Birthdates}

            if val > today:
                response += "\nERROR: US01: Birth date of " + count + " greater than today\n"

        # US35 - List individuals born in last thirty days.
        tdelta = datetime.timedelta ( days=30 )
        diff = today - tdelta  # Gives date before 30 days starting from today.
        if (val >= diff and val <= today):
            response += '\nINFO: US35: ' + count + ' is born in last 30 days.\n'

        if 'DEAT' in out[ 'INDI' ][ count ]:
            if 'DATE' in out[ 'INDI' ][ count ][ 'DEAT' ]:
                val = out[ 'INDI' ][ count ][ 'DEAT' ][ 'DATE' ][ 'VAL' ]
                if val > today:
                    response += "\nERROR: US01: Death date of " + count + " greater than today\n"

    for count in out[ 'FAM' ]:
        if 'MARR' in out[ 'FAM' ][ count ]:
            if 'DATE' in out[ 'FAM' ][ count ][ 'MARR' ]:
                val = out[ 'FAM' ][ count ][ 'MARR' ][ 'DATE' ][ 'VAL' ]
                if val > today:
                    response += "\nERROR: US01: Marriage date of " + count + " greater than today\n"

        if 'DIV' in out[ 'FAM' ][ count ]:
            if 'DATE' in out[ 'FAM' ][ count ][ 'DIV' ]:
                val = out[ 'FAM' ][ count ][ 'DIV' ][ 'DATE' ][ 'VAL' ]
                if val > today:
                    response += "\nERROR: US01: Divorce date of " + count + " greater than today\n"

        if 'HUSB' in out[ 'FAM' ][ count ]:

            val = out[ 'FAM' ][ count ][ 'HUSB' ][ 'VAL' ]
            gender = out[ 'INDI' ][ val ][ 'SEX' ][ 'VAL' ]

            if gender != 'M':
                response += "\nWARNING: US21: " + val + " Gender is not correct\n"

        if 'WIFE' in out[ 'FAM' ][ count ]:

            val = out[ 'FAM' ][ count ][ 'WIFE' ][ 'VAL' ]
            gender = out[ 'INDI' ][ val ][ 'SEX' ][ 'VAL' ]

            if gender != 'F':
                response += "\nWARNING: US21: " + val + " Gender is not correct\n"

    out_US33 = US33 ( out , birthdict )  # Calling US33() function for user-story 33
    response += out_US33
    
    return response


# Method for user-story 33
def US33(out , birthdict):
    result = ""
    deathvals = [ ]  # Stores ID's of family members who are dead
    child_id = [ ]  # Temp list TBD that stores Child-id's
    tday = datetime.date.today ( )

    for count in out[ 'INDI' ]:
        if 'DEAT' in out[ 'INDI' ][ count ]:
            deathvals.append ( count )
            if 'DATE' in out[ 'INDI' ][ count ][ 'DEAT' ]:
                deathvals.append ( count )  # Stores Individual-ID's of persons who are dead

    deathvals = list ( set ( deathvals ) )  # Remove duplicates using SET and converting SET back to LIST
    # print 'IDs in Deathvals.\n',deathvals

    for count in out[ 'FAM' ]:
        # print 'Family-id at start of For loop.',count

        husbtag = out[ 'FAM' ][ count ].get ( 'HUSB' )  # If HUSB is not present in a family
        wifetag = out[ 'FAM' ][ count ].get ( 'WIFE' )  # If WIFE is not present in a family

        # If CHIL tag is a list
        if 'CHIL' in out[ 'FAM' ][ count ]:
            if type ( out[ 'FAM' ][ count ][ 'CHIL' ] ) is list:
                for n in range ( len ( out[ 'FAM' ][ count ][ 'CHIL' ] ) ):
                    childval = out[ 'FAM' ][ count ][ 'CHIL' ][ n ][ 'VAL' ]
                    if childval not in deathvals and husbtag != None and wifetag != None:  # husbval in deathvals and wifeval in deathvals:
                        husbval = out[ 'FAM' ][ count ][ 'HUSB' ][ 'VAL' ]  # ID of father
                        wifeval = out[ 'FAM' ][ count ][ 'WIFE' ][ 'VAL' ]  # ID of mother
                        if husbval in deathvals and wifeval in deathvals:
                            for I , D in birthdict.items ( ):  # I-> Indi-id, D->Birthdates
                                if childval == I:  # Check for child-id in birthdict
                                    if D > tday:  # Birthdate greater than today, Future birthdate not acceptable, skip it
                                        continue
                                    else:
                                        age = tday.year - D.year  # birthdict[D]
                                        if age < 18 and age >= 1:
                                            result += '\nINFO: US33: ' + childval + ' Child is orphan.\n'
            else:
                childval = out[ 'FAM' ][ count ][ 'CHIL' ][ 'VAL' ]
                if childval not in deathvals and husbtag != None and wifetag != None:  # husbval in deathvals and wifeval in deathvals:
                    husbval = out[ 'FAM' ][ count ][ 'HUSB' ][ 'VAL' ]  # ID of father
                    wifeval = out[ 'FAM' ][ count ][ 'WIFE' ][ 'VAL' ]  # ID of mother
                    if husbval in deathvals and wifeval in deathvals:
                        for I , D in birthdict.items ( ):  # I-> Indi-id, D->Birthdates
                            if childval == I:
                                if D > tday:  # Birthdate greater than today, Future birthdate not acceptable, skip it
                                    continue
                                else:
                                    age = tday.year - D.year  # birthdict[D]
                                    if age < 18 and age >= 1:
                                        result += '\nINFO: US33: ' + childval + ' Child is orphan.\n'

    return result
