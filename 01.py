#!/usr/bin/python3
# !/usr/bin/env python
import re
import sys
import io
import linecache

import argparse

a = argparse.ArgumentParser(description='test')
a.add_argument('--a', type=int, default=0)
a.add_argument('--source_gff', type=str, default="")
a.add_argument('--type', type=str, default="")
a.add_argument('--attribute', type=str, default="")
a.add_argument('--value', type=str, default="")
args = a.parse_args()
def reverse_seq(sequence):
    basepair = {
        "A": "T",
        "G": "C",
        "T": "A",
        "C": "G",
        "a": "t",
        "g": "c",
        "t": "a",
        "c": "g",
        '\n':'\n'
    }
    seq = list(sequence)
    revseq = [basepair[bp] for bp in seq]
    output = "".join(revseq)
    return output



def readGFF3(source, type, attribute, value):
    GFF3File = open(source)
    selected_type_list = list()
    ID_list = list()
    seleted_line_list=list()
    attribute_dic={"gene":'ID=([\w.-]+?);',
                   "name":'[Nn]ame=([\w.-]+?);',
                   "Ontology_term":'Ontology_term=([\w.-:,]+?);',
                   "Note":'Note=([\w.-:,%]+?);'}
    seq={'start':0,'end':0,'chrom':"",'seq_content':"","chain":""}
    search_key=attribute+"="+value
    i = 0
    for line in GFF3File:
        if re.match('###',line):
            break
        if re.match('(#{1,2}?)',line):
            continue
        else:
            tableList = line.strip().split()
            # tablelist is the table that store the table in GFF
            if tableList[2] == type:
                selected_type_list.append(tableList)
                # selected_type_list is the table store the selected type lines in the tableList
        i += 1
    for tableList in selected_type_list:
        attribute_str = tableList[8]
        if re.search(search_key, attribute_str):
            seleted_line_list=tableList
            seq['start']=int(tableList[3])
            seq['end']=int(tableList[4])
            seq['chrom']=tableList[0].strip()
            seq["chain"]=str(tableList[6])

            ID_obj = re.search(search_key, attribute_str)
            ID_list.append(ID_obj.group())
    line_start_count=0;line_end_count=0;line_count=0
    temp=list()
    start=False
    for line in GFF3File:
        if re.search(">",line) and start==True:
            line_end_count=line_count
            start=False
        if start==True:
            temp.append(line)
        if re.search((">"+seq["chrom"])+'[\s]',line):
            line_start_count=line_count
            start=True
            fasta_name=line.strip().split(">"+value)
        if line_count==i and start==True:
            line_end_count = line_count
        line_count=line_count+1

    seq["seq_content"] = [""]
    # temp = linecache.getlines("C:/Users/QiHY/Desktop/JHU/gff.txt")[line_start_count + 1:line_end_count]
    seq["seq_content"] = "".join(temp)
    seq["seq_content"].strip()
    seq["seq_content"] = seq["seq_content"][seq["start"]:seq["end"]]



    if seq["chain"]=="+":
        seq["seq_content"] = seq["seq_content"].split('\n', int(len(seq["seq_content"]) / 60))
        output = ">" + str(type) + ":" + str(attribute) + ":" + str(value) + '\n'
        for key in seq["seq_content"]:
            output = output + key + '\n'
    if seq["chain"]=="-":
        seq["seq_content"] = reverse_seq(seq["seq_content"])
        seq["seq_content"] = seq["seq_content"].split('\n', int(len(seq["seq_content"]) / 60))
        output = ">" + str(type) + ":" + str(attribute) + ":" + str(value) + '\n' 
        for key in seq["seq_content"]:
            output = output + key + '\n'







    #
    # print(len(ID_list))
    # print(seq['chrom'])
    # print(ID_list[0])
    print(output)

readGFF3(args.source_gff, args.type, args.attribute, args.value)
