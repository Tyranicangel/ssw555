import datetime
import functools
import collections
import calendar

import common
import akshay
import prad
import prabhjot3
import pranay3
import pranay4
import pranay
from prettytable import PrettyTable


# To convert string into Datetime
def getDate(dateVal):
    if len ( dateVal ) == 3:
        if len ( dateVal[ 0 ] ) == 1:
            dateVal[ 0 ] = '0' + dateVal[ 0 ]
    elif len ( dateVal ) == 2:
        dateVal.insert ( 0 , '01' )
    else:
        dateVal.insert ( 0 , 'JAN' )
        dateVal.insert ( 0 , '01' )
    return datetime.datetime.strptime ( ' '.join ( dateVal ) , '%d %b %Y' )
    return " ".join ( dateVal )


# To get data from dictonary
def getData(mdict , mlist):
    return functools.reduce ( lambda d , k: d[ k ] , mlist , mdict )


# To insert data into dictonary
def setData(mdict , mlist , key , val):
    if key in getData ( mdict , mlist[ :-1 ] )[ mlist[ -1 ] ]:
        if type ( getData ( mdict , mlist[ :-1 ] )[ mlist[ -1 ] ][ key ] ) is list:
            getData ( mdict , mlist[ :-1 ] )[ mlist[ -1 ] ][ key ].append ( val )
        else:
            getData ( mdict , mlist[ :-1 ] )[ mlist[ -1 ] ][ key ] = [
                getData ( mdict , mlist[ :-1 ] )[ mlist[ -1 ] ][ key ] ]
            getData ( mdict , mlist[ :-1 ] )[ mlist[ -1 ] ][ key ].append ( val )
    else:
        getData ( mdict , mlist[ :-1 ] )[ mlist[ -1 ] ][ key ] = val


months = {v: k for k , v in enumerate ( calendar.month_abbr )}

# user_name=raw_input("Hello!What is your name:")
# fname=raw_input("Well "+user_name+' please enter file name:')

# Tags which are relevant
taglist = [ 'INDI' , 'NAME' , 'SEX' , 'BIRT' , 'DEAT' , 'FAMC' , 'FAMS' , 'FAM' , 'MARR' , 'HUSB' , 'WIFE' , 'CHIL' ,
            'DIV' , 'DATE' ,
            'HEAD' , 'TRLR' , 'NOTE' ]
# Tags necessary for parsing
readable = [ 'INDI' , 'NAME' , 'SEX' , 'BIRT' , 'DEAT' , 'FAMC' , 'FAMS' , 'FAM' , 'MARR' , 'HUSB' , 'WIFE' , 'CHIL' ,
             'DIV' , 'DATE' ]
#fname = "prad.ged"
# fname = "prabhjot.ged"
fname = "akshay.ged"
# fname = "prabhjotsprint2.ged"

# Holds the complete parsed file
maindict = {}
# Holds data of the previous link
prev = [ ]
# Holds the reponse to be written to the output
response = ""

duplicates={'FAM':[],'INDI':[]}

try:
    filehandler = open ( fname , 'r' )
    for line in filehandler:
        dat = line.replace ( "/" , "" ).split ( )
        if len ( dat ) >= 2:
            # Putting Level 0 tags in
            if dat[ 0 ] == '0':
                if len ( dat ) >= 3 and dat[ 2 ] in readable:
                    if not dat[ 2 ] in maindict:
                        maindict[ dat[ 2 ] ] = {}
                    if dat[1] in maindict[dat[2]]:
                        duplicates[dat[2]].append(dat[1])
                    maindict[ dat[ 2 ] ][ dat[ 1 ] ] = {}
                    prev = [ dat[ 2 ] , dat[ 1 ] ]
            else:
                # Other tags
                if dat[ 1 ] in readable:
                    # Verying if correct level of tag
                    if int ( dat[ 0 ] ) != len ( prev ) - 1:
                        prev = prev[ 0:int ( dat[ 0 ] ) + 1 ]
                    if prev[ -1 ] != False:
                        if len ( dat ) == 2:
                            setData ( maindict , prev , dat[ 1 ] , {} )
                        else:
                            if dat[ 1 ] == 'DATE':
                                setData ( maindict , prev , dat[ 1 ] , {'VAL': getDate ( dat[ 2: ] )} )
                            else:
                                setData ( maindict , prev , dat[ 1 ] , {'VAL': ' '.join ( dat[ 2: ] )} )
                        prev.append ( dat[ 1 ] )
                else:
                    if int ( dat[ 0 ] ) != len ( prev ) - 1:
                        prev = prev[ 0:int ( dat[ 0 ] ) + 1 ]
                    prev.append ( False )
    filehandler.close ( )
except IOError:
    print ( 'This file does not exist.' )
maindict['DUP']=duplicates

# List of people with their details to response
pretty_response = PrettyTable()
pretty_response.field_names = ['Id', 'Name', 'Gender', 'Age', 'Birthday', 'Alive', 'Death', 'Spouse', 'Children']
pretty_response.align = 'l'
pretty_response.padding_width = 1
for key in sorted ( maindict[ 'INDI' ] , key=lambda x: int ( x.replace ( '@' , "" ).replace ( 'I' , "" ) ) ):
    person_id = key
    name = maindict[ 'INDI' ][ key ][ 'NAME' ][ 'VAL' ]
    if 'SEX' in maindict[ 'INDI' ][ key ]:
        sex = maindict[ 'INDI' ][ key ][ 'SEX' ][ 'VAL' ]
    else:
        sex = 'N/A'
    if 'BIRT' in maindict[ 'INDI' ][ key ]:
        if 'DATE' in maindict[ 'INDI' ][ key ][ 'BIRT' ]:
            age = str(common.getage(maindict['INDI'][key]))
            birth_date = maindict[ 'INDI' ][ key ][ 'BIRT' ][ 'DATE' ][ 'VAL' ].strftime ( '%m/%d/%Y' )
        else:
            age = 'N/A'
            birth_date = 'N/A'
    else:
        age = 'N/A'
        birth_date = 'N/A'
    if 'DEAT' in maindict[ 'INDI' ][ key ]:
        if maindict[ 'INDI' ][ key ][ 'DEAT' ][ 'VAL' ] == 'Y':
            alive = 'Dead'
            if 'DATE' in maindict[ 'INDI' ][ key ][ 'DEAT' ]:
                death_date = maindict[ 'INDI' ][ key ][ 'DEAT' ][ 'DATE' ][ 'VAL' ].strftime ( '%m/%d/%Y' )
            else:
                death_date = 'N/A'
        else:
            alive = 'Alive'
            death_date = 'N/A'
    else:
        alive = 'Alive'
        death_date = 'N/A'
    if 'FAMS' in maindict[ 'INDI' ][ key ]:
        if type ( maindict[ 'INDI' ][ key ][ 'FAMS' ] ) is list:
            spouse = ','.join ( [ d[ 'VAL' ] for d in maindict[ 'INDI' ][ key ][ 'FAMS' ] ] )
        else:
            spouse = maindict[ 'INDI' ][ key ][ 'FAMS' ][ 'VAL' ]
    else:
        spouse = 'N/A'
    if 'FAMC' in maindict[ 'INDI' ][ key ]:
        if type ( maindict[ 'INDI' ][ key ][ 'FAMC' ] ) is list:
            child = ','.join ( [ d[ 'VAL' ] for d in maindict[ 'INDI' ][ key ][ 'FAMC' ] ] )
        else:
            child = maindict[ 'INDI' ][ key ][ 'FAMC' ][ 'VAL' ]
    else:
        child = 'N/A'
    pretty_response.add_row([person_id, name, sex, age, birth_date, alive, death_date, spouse, child])

# List of families with their details to response
pretty_response_fam = PrettyTable()
pretty_response_fam.field_names = ['Id', 'Marriage', 'Divorce', 'Husband', 'Wife', 'Children']
pretty_response_fam.align = 'l'
pretty_response_fam.padding_width = 1
for key in sorted ( maindict[ 'FAM' ] , key=lambda x: int ( x.replace ( '@' , "" ).replace ( 'F' , "" ) ) ):
    fam_id = key
    if 'MARR' in maindict[ 'FAM' ][ key ]:
        marriage_date = maindict[ 'FAM' ][ key ][ 'MARR' ][ 'DATE' ][ 'VAL' ].strftime ( '%m/%d/%Y' )
    else:
        marriage_date = 'N/A'
    if 'DIV' in maindict[ 'FAM' ][ key ]:
        divorce_date = maindict[ 'FAM' ][ key ][ 'DIV' ][ 'DATE' ][ 'VAL' ].strftime ( '%m/%d/%Y' )
    else:
        divorce_date = 'N/A'
    if 'HUSB' in maindict[ 'FAM' ][ key ]:
        husband = (maindict[ 'FAM' ][ key ][ 'HUSB' ][ 'VAL' ] + ", " +
                     maindict[ 'INDI' ][ maindict[ 'FAM' ][ key ][ 'HUSB' ][ 'VAL' ] ][ 'NAME' ][ 'VAL' ])
    else:
        husband = 'N/A'
    if 'WIFE' in maindict[ 'FAM' ][ key ]:
        wife = (maindict[ 'FAM' ][ key ][ 'WIFE' ][ 'VAL' ] + ", " +
                     maindict[ 'INDI' ][ maindict[ 'FAM' ][ key ][ 'WIFE' ][ 'VAL' ] ][ 'NAME' ][ 'VAL' ])
    else:
        wife = 'N/A'
    if 'CHIL' in maindict[ 'FAM' ][ key ]:
        if type ( maindict[ 'FAM' ][ key ][ 'CHIL' ] ) is list:
            children = ','.join ( [ d[ 'VAL' ] for d in maindict[ 'FAM' ][ key ][ 'CHIL' ] ] )
        else:
            children = maindict[ 'FAM' ][ key ][ 'CHIL' ][ 'VAL' ]
    else:
        children = 'N/A'
    pretty_response_fam.add_row ( [ fam_id , marriage_date , divorce_date , husband , wife , children] )

# Executing all scripts and combining maindictputs
response += prad.run ( maindict ) + akshay.run ( maindict ) + prabhjot3.run ( maindict ) + pranay3.run ( maindict ) + pranay4.run ( maindict ) + pranay.run (maindict)

# Response file
writer = open ( 'reponse_' + fname + '.txt' , 'w' )
writer.write('People\n\n')
writer.write(str(pretty_response))
writer.write('\n\n\nFamilies\n\n')
writer.write(str(pretty_response_fam))
writer.write('\n')
writer.write ( response )
writer.close ( )
