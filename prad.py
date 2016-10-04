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
	return response