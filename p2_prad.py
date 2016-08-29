user_name=raw_input("Hello!What is your name:")
fname=raw_input("Well "+user_name+' please enter file name:')
try:
	filehandler=open(fname,'r')
	writer=open(fname+'.txt','w')
	taglist=['INDI','NAME','INDI','SEX','BIRT','DEAT','FAMC','FAMS','FAM','MARR','HUSB','WIFE','CHIL','DIV','DATE','HEAD','TRLR','NOTE']
	for line in filehandler:
		print line.strip()
		writer.write(line.strip()+"\n")
		dat=line.split()
		print dat[0]
		writer.write(dat[0]+"\n")
		if dat[1] in taglist:
			print dat[1]
			writer.write(dat[1]+"\n")
		else:
			print "Invalid Tag"
			writer.write("Invalid Tag"+"\n")
		print '===='
		writer.write("===="+"\n")
	filehandler.close()
except IOError:
	print 'This file does not exist.'