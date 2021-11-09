import sys
import os

if len(sys.argv) < 2:
  print("add file name")
  exit()
filename=os.path.splitext(sys.argv[1])[0]
filetype=os.path.splitext(sys.argv[1])[1].lower()

# Using readlines()
file1 = open(sys.argv[1], 'r')
Lines = file1.readlines()
 
count = 0
mode = 0
header = {}
qsos = []
countqso = 0
if filetype==".stf":    # converter for STF format
  print("STF format")
# Strips the newline character
  for line in Lines:
    if count == 0:
      if line.strip()=="STF1":
        print("format OK")
      else:
        print("wrong file format")
        exit()
    if mode == 0:
      if line.strip()=="HEADER":
        mode = 1
      if line.strip()=="QSOLIST":
        mode = 2

    if mode == 1:  # HEADER
      if line.strip()=="ENDHEADER":
        mode = 0
      key=line.strip().split()
      value=line[len(key[0]):].strip()
      if key[0]=="QSOORDER":
        print("qsoorder:" + value)
        qsokeys=value.split()
      elif key[0]=="HEADER":
        print("header")
      elif key[0]=="ENDHEADER":
        print("endheader")
      else:
#        print("key: {}, value: {}".format(key[0], value))
        oldvalue=header.pop(key[0],False)
        if oldvalue:
          value = oldvalue + " " + value
        header.update({key[0]:value})

    if mode == 2:  # QSOLIST
      if line.strip()=="ENDQSOLIST":
        mode = 0
      elem=line.strip().split()
      if elem[0]=="QSOLIST":
        print("qsolist")
      elif elem[0]=="ENDQSOLIST":
        print("endqsolist")
      else:
#        print(qsokeys)
        print(elem)
        qsos.append(elem)
        countqso += 1

#  if mode != 1:  
    if mode == 0:  
      print("Line{}-Mode{}: {}".format(count, mode, line.strip()))
    count += 1
elif filetype==".csv":    # converter for SOTA csv format
  print("SOTA csv format")
# Strips the newline character
  for line in Lines:
    print(line)
    elem=line.strip().split(',')
    qsos.append(elem)
    countqso += 1

  print(qsos)
else:    # no correct format detected
  print("wrong format!!!")
  exit()

#generate adif file
#print(header)
#print(qsos)
#write content to new file
logfilename = filename + ".adi"
#f = open("log.adi", "w")
f = open(logfilename, "w")
if filetype==".stf":
  f.write("generated on 2021-11-05 for {}\n\n".format(header.get("MYCALL")));
elif filetype==".csv":
  f.write("generated on 2021-11-05\n\n");
f.write("<adif_ver:5>3.0.5\n");
f.write("<programid:12>converter.py\n");
f.write("\n");
f.write("<eoh>\n");
for i in qsos:
#  print(i)
#  print("<qso_date:{}>{}<time_on:{}>{}<call:{}>{}<band:{}>{}<mode:{}>{}<rst_sent:{}>{}<my_gridsquare:{}>{}<rst_rcvd:{}>{}<darc_doc:{}>{}<gridsquare:{}>{}<eor>".format(len(i[0]),i[0],len(i[1]),i[1],len(i[4]),i[4],len(i[2]),i[2],len(i[3]),i[3],len(i[5]),i[5],len(i[7]),i[7],len(i[8]),i[8],len(i[9]),i[9],len(i[10]),i[10]))
  if filetype==".stf":
    f.write("<qso_date:{}>{}<time_on:{}>{}<call:{}>{}<band:{}>{}<mode:{}>{}<rst_sent:{}>{}<my_gridsquare:{}>{}<rst_rcvd:{}>{}<darc_doc:{}>{}<gridsquare:{}>{}<eor>\n".format(len(i[0]),i[0],len(i[1]),i[1],len(i[4]),i[4],len(i[2]),i[2],len(i[3]),i[3],len(i[5]),i[5],len(i[7]),i[7],len(i[8]),i[8],len(i[9]),i[9],len(i[10]),i[10]))
  if filetype==".csv":
    datestr="20"+i[3][6]+i[3][7]+i[3][3]+i[3][4]+i[3][0]+i[3][1]
    timestr=i[4]
    if len(timestr)==3:
      timestr="0" + timestr
    f.write("<qso_date:{}>{}<time_on:{}>{}<call:{}>{}<freq:{}>{}<mode:{}>{}<my_sota_ref:{}>{}".format(len(datestr),datestr,len(timestr),timestr,len(i[7]),i[7],len(i[5]),i[5],len(i[6]),i[6],len(i[2]),i[2]))
    if len(i)>=9:
      f.write("<sota_ref:{}>{}<eor>\n".format(len(i[8]),i[8]))
    else:
      f.write("<eor>\n")
f.close()

