import common
import datetime

def run(out):
	response="\n\n"
	for fam in out['FAM']:
		if 'CHIL' in out['FAM'][fam]:
			if type(out['FAM'][fam]['CHIL']) is list:
				checkarr={}
				for chil in out['FAM'][fam]['CHIL']:
					if 'BIRT' in out['INDI'][chil['VAL']]:
						if 'DATE' in out['INDI'][chil['VAL']]['BIRT']:
							dictkey=out['INDI'][chil['VAL']]['NAME']['VAL']+out['INDI'][chil['VAL']]['BIRT']['DATE']['VAL'].strftime('%m/%d/%Y')
						else:
							dictkey=out['INDI'][chil['VAL']]['NAME']['VAL']
					else:
						dictkey=out['INDI'][chil['VAL']]['NAME']['VAL']
					if dictkey in checkarr:
						checkarr[dictkey].append(chil['VAL'])
					else:
						checkarr[dictkey]=[]
						checkarr[dictkey].append(chil['VAL'])
				for key in checkarr:
					if len(checkarr[key])>1:
						response+='\nError: US25: There are '+str(len(checkarr[key]))+' children in family '+fam+' with the same name and birthday,'+','.join(checkarr[key])
		if 'DIV' in out['FAM'][fam]:
			if 'DATE' in out['FAM'][fam]['DIV']:
				if 'DEAT' in out['INDI'][out['FAM'][fam]['HUSB']['VAL']]:
					if 'DATE' in out['INDI'][out['FAM'][fam]['HUSB']['VAL']]['DEAT']:
						if common.datediff(out['INDI'][out['FAM'][fam]['HUSB']['VAL']]['DEAT']['DATE']['VAL'],out['FAM'][fam]['DIV']['DATE']['VAL']).days<0:
							response+='\nWARNING: US06: DIVORCE DATE is before Marriage date for '+out['FAM'][fam]['HUSB']['VAL']+' in family '+fam
				if 'DEAT' in out['INDI'][out['FAM'][fam]['WIFE']['VAL']]:
					if 'DATE' in out['INDI'][out['FAM'][fam]['WIFE']['VAL']]['DEAT']:
						if common.datediff(out['INDI'][out['FAM'][fam]['WIFE']['VAL']]['DEAT']['DATE']['VAL'],out['FAM'][fam]['DIV']['DATE']['VAL']).days<0:
							response+='\nWARNING: US06: DIVORCE DATE is before Marriage date for '+out['FAM'][fam]['WIFE']['VAL']+' in family '+fam
	for indi in out['INDI']:
		if 'DEAT' in out['INDI'][indi]:
			response+='\nINFO: US29: Individual '+out['INDI'][indi]['NAME']['VAL']+'('+indi+')'+' is deceased.'
		elif 'FAMS' not in out['INDI'][indi]:
			if 'BIRT' in out['INDI'][indi]:
				if 'DATE' in out['INDI'][indi]['BIRT']:
					if common.getage(out['INDI'][indi])!='N/A' and common.getage(out['INDI'][indi])>30:
						response+='\nINFO: US31: Individual '+out['INDI'][indi]['NAME']['VAL']+'('+indi+')'+' is living single.'
		if 'FAMS' in out['INDI'][indi]:
			if type(out['INDI'][indi]['FAMS']) is list:
				famdict={}
				for fams in out['INDI'][indi]['FAMS']:
					if 'MARR' in out['FAM'][fams['VAL']] or 'DIV' in out['FAM'][fams['VAL']]:
						famdict[fams['VAL']]={}
						if 'MARR' in out['FAM'][fams['VAL']]:
							famdict[fams['VAL']]['STRT']=out['FAM'][fams['VAL']]['MARR']['DATE']['VAL']
						else:
							famdict[fams['VAL']]['STRT']=datetime.datetime.min
						if 'DIV' in out['FAM'][fams['VAL']]:
							famdict[fams['VAL']]['END']=out['FAM'][fams['VAL']]['DIV']['DATE']['VAL']
						else:
							if out['FAM'][fams['VAL']]['HUSB']['VAL']==indi:
								if 'DEAT' in out['INDI'][out['FAM'][fams['VAL']]['HUSB']['VAL']]:
									if 'DATE' in out['INDI'][out['FAM'][fams['VAL']]['HUSB']['VAL']]['DEAT']:
										famdict[fams['VAL']]['END']=out['INDI'][out['FAM'][fams['VAL']]['HUSB']['VAL']]['DEAT']['DATE']['VAL']
							else:
								if 'DEAT' in out['INDI'][out['FAM'][fams['VAL']]['WIFE']['VAL']]:
									if 'DATE' in out['INDI'][out['FAM'][fams['VAL']]['WIFE']['VAL']]['DEAT']:
										famdict[fams['VAL']]['END']=out['INDI'][out['FAM'][fams['VAL']]['WIFE']['VAL']]['DEAT']['DATE']['VAL']
							if not 'END' in famdict[fams['VAL']]:
								famdict[fams['VAL']]['END']=datetime.datetime.max
				if len(famdict)>1:
					sortedfam=sorted(famdict, key=lambda k: famdict[k]['STRT'])
					for i in range(0,len(sortedfam)):
						if i!=0:
							if common.datediff(famdict[sortedfam[i]]['STRT'],famdict[sortedfam[i-1]]['END']).days<0:
								response+='\nWARNING: US11: Individual '+indi+' is involved in bigamy'
								break
	return response