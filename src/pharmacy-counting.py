## This function will parse through the text data and 
## generate list of dictionaries. 
### don't forget to set the dirctory where the input data is (itcont.txt)

import os
import csv

DATADIR = "/home/oem/pharmacy_counting/input/"
DATAFILE = "itcont.txt"


def parse_file(datafile):
    data = []
    with open(datafile, "r") as f:
        header = f.readline().split(',')
        counter = 0
        for line in f:
            if counter == 1000:
                break
            fields = line.split(',')
            entry = {}
            for i,value in enumerate(fields):
                entry[header[i].strip()] = value.strip()
            data.append(entry)
            counter +=1
            

    return data
###  The  next fuction will extract data for drug_name, num_prescriber and
## num_prescriber from the whole given data which is a python dictionary

datafile = os.path.join(DATADIR, DATAFILE)
dic = parse_file(datafile)

def drug_prescr_cost(dic):
    drug_name_list = []
    num_prescriber_list = []
    total_cost_list =[]
    for i in range(len(dic)):
        drug_name_list.append(dic[i]['drug_name'])
        num_prescriber_list.append(dic[i]['id'])
        total_cost_list.append(dic[i]['drug_cost'])
    ## lets collect unique drug name lists
    myset = list(set(drug_name_list))
 
    data = []
    for j in range(len(drug_name_list)):
        for k in range(len(myset)):
            entry = {}
            if drug_name_list[j] == myset[k]: 
                entry[myset[k]] = total_cost_list[j] #,num_prescriber_list[j] 
                data.append(entry)
    dic2 = {"data": data}
    
    return dic2
dic3 = drug_prescr_cost(dic)

### After obtaining information for durg list and cost of each drug list,
## lets calcuate the total cost for each drug list
# and the total number of presccriber 

def total_costandprec(dic3):
    total = {}
    subs  = {}
    for item in dic3['data']:
        for key,val in item.items(): 
            if key in total:
                total[key] +=float(val)
                subs[key] += 1     
            else:
                total[key] = float(val)
                subs[key] = 1
    ### now after computing total cost and number of 
    ### prescriber for each drug lets collect the information
    ## for drug_name,num_prescriber and total_cost in a dictionary
    la = list(subs.values())
    for i in range(len(la)):
        entry = {}
        entry['drug_name'] = list(total.keys())
        entry['num_prescriber'] = list(subs.values())
        entry['total_cost'] = list(total.values())
    return entry
entry = total_costandprec(dic3) 
## Finally lets write the out put into a text file


def zipped(entry):
    """
    This function will creates sets from values of
    each key in the dictionary entry so that is easy to write 
    the out put in the required format and sorts in decending order
    based on the total cost and based on drug_name if there is a tie 
    in total cost
    """
    for i in range(len(entry['drug_name'])-1):
        if entry['total_cost'][i] != entry['total_cost'][i+1]:
            zipped = sorted(zip(entry['drug_name'], entry['num_prescriber'], entry['total_cost']), key=lambda x: x[2], reverse=True)
        if entry['total_cost'][i] == entry['total_cost'][i+1]:
            zipped = sorted(zip(entry['drug_name'], entry['num_prescriber'], entry['total_cost']), key=lambda x: x[0], reverse=False)
        
    return zipped
zipped = zipped(entry)


with open("/home/oem/pharmacy_counting/output/top_cost_drug.txt", 'w') as fp:
    root = csv.writer(fp, delimiter=',')
    root.writerow(['drug_name', 'num_prescriber', 'total_cost'])
    for i in range(len(zipped)):
        root.writerow(zipped[i])



