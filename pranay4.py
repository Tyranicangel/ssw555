# User story 07 - Less then 150 years old
# Death should be less than 150 years after birth for dead people,
# and current date should be less than 150 years after birth for all living people

import datetime


def run(out):
    # print out
    today = datetime.datetime.today ( )
    response = ""
    birthdict = {}  # Dictionary to store [Key, Value] => [Individual-Id, Birthdate]

    for count in out[ 'INDI' ]:
        # print out['INDI'] #Print individual-ID's present in family
        if 'BIRT' in out[ 'INDI' ][ count ]:
            # Value of birth date
            val = out[ 'INDI' ][ count ][ 'BIRT' ][ 'DATE' ][ 'VAL' ]
            # Calculate age
            age = (today.year) - (val.year)
            if age < 0:
                # print '\nBIRTH:: Anomaly: US07: - Future birth date of individual-id ' +count + ' Birth year -> ', (val.year), '\n'
                response += '\nERROR: US07: Future birth date of individual-id ' + count
            elif age >= 0 and age < 150:
                birthdict[ count ] = [ str ( val ) ]  # Stores [Key, Value] => [Individual-id, Birthdate]
            # print '\nBIRTH:: -->Success, Individual id in BD-> ',count, ' and Birth date ->',val.date(), ' and Age ->',age, ' years.\n'
            else:
                # print '\nBIRTH:: Error: US07: - Age is more than 150 years, individual-id ' + count + ' Birth year -> ', (val.year), '\n'
                response += '\nERROR: US07: Age is more than 150 years, individual-id ' + count
        # print birthdict, '\n'


        if 'DEAT' in out[ 'INDI' ][ count ]:
            if 'DATE' in out[ 'INDI' ][ count ][ 'DEAT' ]:
                deathval = out[ 'INDI' ][ count ][ 'DEAT' ][ 'DATE' ][ 'VAL' ]  # Gets the death date value

                for x , y in birthdict.items ( ):
                    if x == count:  # If Individual-id's are same then get birth date
                        birth = str ( birthdict[ x ] )  # Store the value for key in variable birth in string format
                        birthyear = birth[ 2:6 ]  # Stores only the year value
                        deathyear = str ( deathval.year )

                        if deathval.date ( ) > today.date ( ):  # Check if death date is a future date.
                            # print '\nDEATH:: Error: US07: Death date is future date - ' + str(deathval.date()) + ' for individual-id - '+ count + '\n'
                            response += '\nERROR: US07: Death date is future date ' + str (
                                deathval.date ( ) ) + ' for individual-id ' + count + '\n'
                        else:
                            age = int ( deathyear ) - int ( birthyear )  # Calculate age in years
                            if age >= 0 and age < 150:
                                continue
                            # print '\nDEATH:: -->Success, Individual id in DD-> ' + count + ' and Death year - ', (deathval.year), '\n'
                            else:  # age < 0:
                                # print '\nDEATH:: Error: US07: - Death before birth or Future birth date of individual-id ' +count + ' Birth year -> ', (birthyear), '\n'
                                response += '\nERROR: US07: - Death before birth or future birth date of individual-id ' + count + '\n'
    return response
