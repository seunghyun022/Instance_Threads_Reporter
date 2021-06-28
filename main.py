import argparse
import csv
import os

name_idx=0
def format_csv(buf):
    result_buf=list()
    lbuf = ["instance name","maxThreads Valuse"]
    result_buf.append(lbuf)
    diction=dict()
    for row in buf:
        #print(row)
        ins_name=row.split()[0].split('/')
        for tomcat_idx in range(0,len(ins_name)):
            if "tomcat" == ins_name[tomcat_idx] or "tomcat9" == ins_name[tomcat_idx]:
                name_idx=tomcat_idx+1
                break
        ins_name=ins_name[name_idx]
        conf=row.split()[0].split('/')[name_idx+1]
        if "template" in ins_name or "bapi" in ins_name or conf!="conf":
            continue
        max_T=row.split()[1]
        if max_T != "maxThreads=""":
            max_T=max_T.split('"')[1]
            #print(max_T)
            #print(type(max_T))
            diction[ins_name]=max_T

    for key in diction:
        lbuf=[key,diction[key]]
        result_buf.append(lbuf)

def writecsv (result_buf,filename):
    with open("./result/"+filename,'w',encoding='utf-8-sig',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result_buf)

    csvfile.close()

def open_list_file(file):
    buf=list()
    with open(file, newline='') as mxThreads_file:
        for row in mxThreads_file:
            buf.append(row)
    mxThreads_file.close()
    return buf

def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('InputFileName', type=str, help="Input File Name to be fromatted")
    args=parser.parse_args()
    return args.InputFileName

def sub(file_name):
    input_file_name = "./mxThreads/{0}".format(file_name)
    buf=open_list_file(input_file_name)
    formatted = format_csv(buf)
    writecsv(formatted, file_name+".csv")
def main():
    #file_name = getargs()
    file_list = os.listdir(os.getcwd()+"/mxThreads")
    for i in range (0,len(file_list)):
        sub(file_list[i])
if __name__ =='__main__':
    main()