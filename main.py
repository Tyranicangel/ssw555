import datetime
import functools
import akshay
import prad
import prabhjot
import pranay


def getDate(dateVal):
    if len(dateVal[0]) == 1:
        dateVal[0] = '0' + dateVal[0]
    return " ".join(dateVal)
#    return datetime.datetime.strptime(' '.join(dateVal), '%d %b %Y')


def getData(mdict, mlist):
    return functools.reduce(lambda d, k: d[k], mlist, mdict)


def setData(mdict, mlist, key, val):
    if key in getData(mdict, mlist[:-1])[mlist[-1]]:
        if type(getData(mdict, mlist[:-1])[mlist[-1]][key]) is list:
            getData(mdict, mlist[:-1])[mlist[-1]][key].append(val)
        else:
            getData(mdict, mlist[:-1])[mlist[-1]][key] = [getData(mdict, mlist[:-1])[mlist[-1]][key]]
            getData(mdict, mlist[:-1])[mlist[-1]][key].append(val)
    else:
        getData(mdict, mlist[:-1])[mlist[-1]][key] = val


# user_name=raw_input("Hello!What is your name:")
# fname=raw_input("Well "+user_name+' please enter file name:')

taglist = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE',
           'HEAD', 'TRLR', 'NOTE']
readable = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE']
fname = "prabhjot.ged"

out = {}
prev = []

try:
    filehandler = open(fname, 'r')
    for line in filehandler:
        dat = line.replace("/", "").split()
        if dat[0] == '0':
            if len(dat) >= 3 and dat[2] in readable:
                if dat[2] in out:
                    out[dat[2]][dat[1]] = {}
                else:
                    out[dat[2]] = {}
                    out[dat[2]][dat[1]] = {}
                prev = [dat[2], dat[1]]
        else:
            if dat[1] in readable:
                if prev[-1] != False:
                    if int(dat[0]) != len(prev) - 1:
                        prev = prev[0:int(dat[0]) + 1]
                    if len(dat) == 2:
                        setData(out, prev, dat[1], {})
                    else:
                        if dat[1] == 'DATE':
                            setData(out, prev, dat[1], {'VAL': getDate(dat[2:])})
                        else:
                            setData(out, prev, dat[1], {'VAL': ' '.join(dat[2:])})
                    prev.append(dat[1])
            else:
                prev.append(False)
    filehandler.close()
except IOError:
    print('This file does not exist.')



response=prad.run(out)+akshay.run(out)+prabhjot.run(out)+pranay.run(out)

writer=open('reponse_'+fname+'.txt','w')
writer.write(response)
writer.close()


print("Families : ")
fam_list = out["FAM"]
a=sorted(list(fam_list.keys()))
print(a)
