import main


# method to check if response dictionary is valid or not
def run(out):
    print ( out )
    return ""


def gethusbandandwifedict(dict):
    husbwifedict = {}
    husblist = []
    wifelist = []
    for key in sorted ( dict[ 'FAM' ] , key=lambda x: int ( x.replace ( '@' , "" ).replace ( 'F' , "" ) ) ):
        if 'HUSB' in dict['FAM'][key]:
            if dict['FAM'][key]['HUSB']['VAL'] not in husblist:
                husblist.append(dict['FAM'][key]['HUSB']['VAL'])
        if 'WIFE' in dict['FAM'][key]:
            if dict['FAM'][key]['WIFE']['VAL'] not in wifelist:
                wifelist.append(dict['FAM'][key]['WIFE']['VAL'])

    husbwifedict['HUSB'] = husblist
    husbwifedict['WIFE'] = wifelist
    return husbwifedict



def getsiblingsbdate(dict):
    siblingdict = []
    # hubwifdict = gethusbandandwifedict(dict)
    # husbdict = hubwifdict['HUSB']
    # wifedict = hubwifdict['WIFE']
    hubdict = []
    wifdict = []

    #LOOP ACCORDING TO INDIVIDUAL
    for key in sorted ( dict[ 'INDI' ] , key=lambda x: int ( x.replace ( '@' , "" ).replace ( 'F' , "" ) ) ):
        if 'FAMS' in dict['INDI'][key]:
            if type(dict['INDI'][key]['FAMS']) is list:
                for d in dict['INDI'][key]['FAMS']:

            else:
                response += maindict['INDI'][key]['FAMS']['VAL'].ljust(20)
        else:
            response += 'N/A'.ljust(20)



    # LOOP ACCORDING TO FAMILY
    for key in sorted ( dict[ 'FAM' ] , key=lambda x: int ( x.replace ( '@' , "" ).replace ( 'F' , "" ) ) ):
        if dict['FAM'][key]['HUSB']['VAL'] not in hubdict:
            hubdict.append(dict['FAM'][key]['HUSB']['VAL'])
        else:
            print()
        if dict['FAM'][key]['WIFE']['VAL'] not in wifdict:
            wifdict.append(dict['FAM'][key]['WIFE']['VAL'])
        else:
            print()
        if 'CHIL' in dict[ 'FAM' ][ key ]:
            if type ( dict[ 'FAM' ][ key ][ 'CHIL' ] ) is list:
                for d in dict[ 'FAM' ][ key ][ 'CHIL' ]:
                    if 'BIRT' in dict[ 'INDI' ][ d[ 'VAL' ] ]:
                        if 'DATE' in dict[ 'INDI' ][ d[ 'VAL' ] ][ 'BIRT' ]:
                            print ( 'id : ' , d[ 'VAL' ] , 'birthdate : ' ,
                                    dict[ 'INDI' ][ d[ 'VAL' ] ][ 'BIRT' ][ 'DATE' ][ 'VAL' ] )
                        else:
                            print ( 'id : ' , d[ 'VAL' ] , 'birthdate : N/A' )
                    else:
                        print ( 'id : ' , d[ 'VAL' ] , 'birthdate : N/A' )
            else:
                if 'BIRT' in dict[ 'INDI' ][ dict[ 'FAM' ][ key ][ 'CHIL' ][ 'VAL' ] ]:
                    if 'DATE' in dict[ 'INDI' ][ dict[ 'FAM' ][ key ][ 'CHIL' ][ 'VAL' ] ][ 'BIRT' ]:
                        print ( 'id : ' , dict[ 'FAM' ][ key ][ 'CHIL' ][ 'VAL' ] ,
                                'birthdate : ' ,
                                dict[ 'INDI' ][ dict[ 'FAM' ][ key ][ 'CHIL' ][ 'VAL' ] ][ 'BIRT' ][ 'DATE' ][ 'VAL' ] )
                    else:
                        print ( 'id : ' , dict[ 'FAM' ][ key ][ 'CHIL' ][ 'VAL' ] , 'birthdate : N/A' )
                else:
                    print ( 'id : ' , dict[ 'FAM' ][ key ][ 'CHIL' ][ 'VAL' ] , 'birthdate : N/A' )
        else:
            print ( 'no childs available.' )


filename = "akshay.ged"
maindict = main.parsergedcomfile ( filename )
run ( maindict )

getsiblingsbdate ( maindict )
