import datetime


def run(out):

    today = datetime.datetime.today ( )
    response = ""
    birthdict = {}  # Dictionary which maintains the {Key,Val} as {Indi-id, Birth-dates}
    marrdict = {}   # Dictionary which maintains {Key,Val} as {Fam-id, Marriage-dates}
    deathdict = {}  # Dictionary which maintains {Key,Val} as {Indi-id, Death-dates}

    for count in out[ 'INDI' ]:
        if 'BIRT' in out[ 'INDI' ][ count ]:
            val = out[ 'INDI' ][ count ][ 'BIRT' ][ 'DATE' ][ 'VAL' ]
            birthdict[ count ] = val.date( )  # Stores {Key,Val} as {Indi-id, Birthdates}
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
                deathdict[count] = val.date() # Stores {Key,Val} as {Indi-id, Deathdates}
                if val > today:
                    response += "\nERROR: US01: Death date of " + count + " greater than today\n" 


    for count in out[ 'FAM' ]:
        if 'MARR' in out[ 'FAM' ][ count ]:
            if 'DATE' in out[ 'FAM' ][ count ][ 'MARR' ]:
                val = out[ 'FAM' ][ count ][ 'MARR' ][ 'DATE' ][ 'VAL' ]
                marrdict[count] = val.date() # Stores {Key,Val} as {Fam-id, Marriagedates}
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


    out_US08 = ChildPostMarr (out, birthdict, marrdict) 

    out_US10 = CheckMarriage(out,birthdict,marrdict,deathdict) # Includes US10, US05

    out_US07 = CheckAge(out,birthdict,deathdict) 

    out_US33 = ListOrphans(out, birthdict, deathdict)

    response += out_US33 + out_US08 + out_US10 + out_US07

    return response


#US08 -> Child should be born after marriage
def ChildPostMarr(out,birthdict,marrdict):
    result = ""
    
    for count in out['FAM']: # var count contains all the family-id's
        if 'CHIL' in out['FAM'][count]:
            if type ( out[ 'FAM' ][ count ][ 'CHIL' ] ) is list:
                for n in range ( len ( out[ 'FAM' ][ count ][ 'CHIL' ] ) ):
                    childval = out[ 'FAM' ][ count ][ 'CHIL' ][ n ][ 'VAL' ]
                    if childval in birthdict and count in marrdict:
                        if marrdict[count] < birthdict[childval]:
                            result += '\nINFO: US08: ' + childval + ' is born after parents marriage.\n'
                        else:
                            result += '\nWARNING: US08: ' + childval + ' is born before parents marriage.\n'
            else:
                childval = out[ 'FAM' ][ count ][ 'CHIL' ][ 'VAL' ]
                if childval in birthdict and count in marrdict:
                    if marrdict[count] < birthdict[childval]:
                        result += '\nINFO: US08: ' + childval + ' is born after parents marriage.\n'
                    else:
                        result += '\nWARNING: US08: ' + childval + ' is born before parents marriage.\n'

    return result
    
# US10 -> Marriage after 14 years, US05 -> Marriage should happen before death
def CheckMarriage(out, birthdict, marrdict, deathdict):
    result = ""

    for count in out['FAM']:
        

        if 'MARR' in out['FAM'][count]:        
            husbval = out[ 'FAM' ][ count ][ 'HUSB' ][ 'VAL' ]  # ID of HUSB
            wifeval = out[ 'FAM' ][ count ][ 'WIFE' ][ 'VAL' ]  # ID of WIFE
            marrdate = marrdict[count]

            if husbval in birthdict and wifeval in birthdict and count in marrdict:
                #marrdate = marrdict[count]
                husbdate = birthdict[husbval]
                wifedate = birthdict[wifeval]
                if (marrdate.year - husbdate.year) >= 14 and (marrdate.year - wifedate.year) >= 14:
                    result += '\nINFO: US10: Both spouses ' +husbval+ ', ' +wifeval+' were more than 14 years old at the time of their marriage.\n'

            if husbval in deathdict: # or wifeval in deathdict:
                #marrdate = marrdict[count]
                husbddate = deathdict[husbval]
                if husbddate < marrdate:
                    result += '\nERROR: US05: Marriage cannot happen after death of either spouse, family-id:'+ count +'\n'

            elif wifeval in deathdict: # or wifeval in deathdict:
                #marrdate = marrdict[count]
                wifeddate = deathdict[wifeval]
                if wifeddate < marrdate:
                    result += '\nERROR: US05: Marriage cannot happen after death of either spouse, family-id:'+ count + '\n'

    return result

# US07 -> Age less than 150 years
def CheckAge(out, birthdict, deathdict):
    result = ""
    today = datetime.date.today ( )

    for kb,vb in sorted(birthdict.items()):
        bdate = vb
        age = today.year - bdate.year

        if age < 0: # Future birth date for individual   
            continue
        elif age >= 0 and age < 150:
            result += '\nINFO: US07: Age is less than 150 years for individual '+ kb
        else:
            result += '\nWARNING: US07: Age is more than 150 years for individual '+ kb

    for kd,vd in sorted(deathdict.items()):
        if kd in sorted(birthdict):  #Indi-id's in deathdict equals Indi-id in birthdict

            if vd > today: # Future death date for individual
                continue
            else:
                vb = birthdict[kd]
                deathage = vd.year - vb.year
                if deathage >= 0 and deathage < 150:
                    result += '\nINFO: US07: Age at time of death less than 150 years for individual '+ kd
    return result

# US33 -> List orphans
def ListOrphans(out, birthdict, deathdict):
    result = ""
    today = datetime.date.today()

    for count in out['FAM']:
        husbtag = out[ 'FAM' ][ count ].get ( 'HUSB' )  # If HUSB is not present in a family
        wifetag = out[ 'FAM' ][ count ].get ( 'WIFE' )  # If WIFE is not present in a family
        

        # If CHIL tag is a list
        if 'CHIL' in out[ 'FAM' ][ count ]:
            if type ( out[ 'FAM' ][ count ][ 'CHIL' ] ) is list:
                for n in range ( len ( out[ 'FAM' ][ count ][ 'CHIL' ] ) ):
                    childval = out[ 'FAM' ][ count ][ 'CHIL' ][ n ][ 'VAL' ]
                    if childval not in deathdict and husbtag != None and wifetag != None:
                        husbval = out[ 'FAM' ][ count ][ 'HUSB' ][ 'VAL' ]  # ID of HUSB
                        wifeval = out[ 'FAM' ][ count ][ 'WIFE' ][ 'VAL' ]  # ID of WIFE
                        if husbval in deathdict and wifeval in deathdict:
                            childbdate = birthdict[childval]
                            age = today.year - childbdate.year
                            if age < 18 and age >= 1: # age >= 1 to skip future birth-dates
                                result += '\nINFO: US33: ' + childval + ' Child is orphan.\n'
            
            else:
                childval = out[ 'FAM' ][ count ][ 'CHIL' ][ 'VAL' ]
                if childval not in deathdict and husbtag != None and wifetag != None:
                    husbval = out[ 'FAM' ][ count ][ 'HUSB' ][ 'VAL' ]  # ID of HUSB
                    wifeval = out[ 'FAM' ][ count ][ 'WIFE' ][ 'VAL' ]  # ID of WIFE
                    if husbval in deathdict and wifeval in deathdict:
                        childbdate = birthdict[childval]
                        age = today.year - childbdate.year
                        if age < 18 and age >= 1: # age >= 1 to skip future birth-dates
                            result += '\nINFO: US33: ' + childval + ' Child is orphan.\n'

    return result