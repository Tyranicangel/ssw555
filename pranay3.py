# User story 05 - Marriage before death

import datetime


def run(out):
    response = ""
    dlist = [ ]  # Store individual-id
    deathlist = [ ]  # Store death date of the corresponding individual who died
    deathdict = {}  # Dictionary to store Individual-id as Key and death date as its value

    for count in out[ 'INDI' ]:
        # print count
        if 'DEAT' in out[ 'INDI' ][ count ]:
            if 'DATE' in out[ 'INDI' ][ count ][ 'DEAT' ]:
                death_val = out[ 'INDI' ][ count ][ 'DEAT' ][ 'DATE' ][ 'VAL' ]  # Get death date value
                if type ( out[ 'INDI' ][ count ][ 'FAMS' ] ) is list:                    
                    for fid in range(len(out[ 'INDI' ][ count ][ 'FAMS' ])):
                        fidval = out[ 'INDI' ][ count ][ 'FAMS' ][fid]['VAL']                        
                        fam_id = fidval # Get family-id of the individual
                        deathdict[ fam_id ] =  str ( death_val )
                else:
                    fam_id = out[ 'INDI' ][ count ][ 'FAMS' ][ 'VAL' ]  # Get family-id of the individual
                    deathdict[ fam_id ] =  str ( death_val )
                    # dlist.append(count) #Store INDI-ID
                    # deathlist.append(str(death_val)) #Store death dates in string format
                    # [Key, Value] => [Family-ID, Deathdate], Family id with their death dates stored in deathdict dictonary

                    # print '\nDictionary of family-ids with death dates ->' ,deathdict

    fdlist = [ ]
    marrdict = {}
    for count in out[ 'FAM' ]:
        if 'HUSB' in out[ 'FAM' ][ count ] and 'WIFE' in out[ 'FAM' ][ count ] and 'MARR' in out[ 'FAM' ][ count ]:
            fdlist.append ( count )  # Stores family-ids
            marrdate = out[ 'FAM' ][ count ][ 'MARR' ][ 'DATE' ][ 'VAL' ]  # Marriage date
            for k , v in deathdict.items():
                if k == count:  # Key's(Family-id's) in deathdict equals to count(Family-id)
                    if v < str ( marrdate ):
                        # print 'Failure, Marriage date ->',str(marrdate), '\n'
                        # print 'Death date ->', v, '\n'
                        # print 'Family-id ->', k, '\n'
                        response += '\nError: US05: Marriage cannot happen after death.\n'
                    else:
                        continue
        else:
            continue

    return response
