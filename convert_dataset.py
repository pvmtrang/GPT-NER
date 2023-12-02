import os
import re
from openai_access.dataset_name import FULL_DATA
import json

dataset_name = "phoNER_COVID19_vie"
dataset_source_path = "data\\phoNER_COVID19\\mrc-ner.train"

# dataset_source_path = "data\\phoNER_COVID19\\mrc-ner.dev"

# dataset_source_path = "data\\phoNER_COVID19\\mrc-ner.test_500"
dataset_dest_path = dataset_source_path+"_converted"

entity_type_set = list(FULL_DATA["phoNER_COVID19"].keys()) #list of all entity types in this dataset

#1 sentence: repeat n times for n tags
# phoNER_covid19 is flat NER, khong can lo ve nested -> get duoc 1 tag != 0 -> tao sentence luon va auto fill cac tag khac??
#some modification: skip nhung cai setence format cho cac tag ma no ko co (impossible = true) di, du sao cung ko dung, kinda useless
# only exist to prove that random retrieval of knn is random
# "query" to store definition of entity_label is useless not, vi anyway no se lay tu FULL_DAT[data_type][entity_tag]
# qas_id is useless also, never used

def process_data(dataset_source_path, dataset_dest_path):
    dataset_list = [] #break dataset into smaller dataset and concat later due to memory error if store all at once
    dataset = [] # a list store all sentences. each sentence is a dict of all required fields: context, entity_type, ...
    def process_sentence(word_seq, tag_seq, sentence_id):
        sentence_set = []
        for i in range (len(entity_type_set)):
            current_type = entity_type_set[i]
            # print ("at entity type of " + str(current_type))
            one_sentence = {}
            start_position = []
            end_position = []
            span_position = [] #list of string maching start;end position
            token_id = 0
            while token_id < len(tag_seq): #process the whole sentence to extract entity span
                if tag_seq[token_id] == ("B-" + current_type): #begin an entity span
                    # print("begin a span of " + current_type + " at token id=" + str(token_id))
                    start_position.append(token_id)
                    for j in range(token_id, len(tag_seq)):
                        if tag_seq[j] == "O": #out of entity span or reach the end
                            end_position.append(j - 1)
                            span_position.append(str(token_id)+";"+str(j-1))
                            token_id = j
                            break
                        if j == len(tag_seq) - 1: #or reach the end
                            end_position.append(j)
                            span_position.append(str(token_id)+";"+str(j))
                            token_id = j
                            break
                token_id += 1
            one_sentence["context"] = " ".join(word_seq)
            one_sentence["entity_label"] = current_type
            one_sentence["start_position"] = start_position
            one_sentence["end_position"] = end_position
            if (len(start_position) != len(end_position)):
                print("vcl start end ko match in sentence number" + str(count_sentence))
                print("context: " + one_sentence["context"] + ". of label " + one_sentence["entity_label"])
                print("word:"+str(word_seq))
                print("tag: " + str(tag_seq))
                return
            one_sentence["span_position"] = span_position
            one_sentence["qas_id"] = str(sentence_id)+"."+str(i)
            one_sentence["impossible"] = False if len(start_position) > 0 else True
#                print (one_sentence["context"])
            sentence_set.append(one_sentence)
        #sentence_set.append(" ".join(word_seq))
        return sentence_set
    
    with open(dataset_source_path, 'r', encoding='utf-8') as input_file:
        print("opening file")
        count_sentence = 0
        word_seq = []
        tag_seq = []
        for line in input_file:
            line = line.strip()     
            if not line: #reach the blank line between 2 sentence
                if (len(word_seq) > 0):
                    count_sentence += 1
                    # print("sentence number: " + str(count_sentence) +" with length = " + str(len(tag_seq)))
                    sentence = process_sentence(word_seq, tag_seq, count_sentence-1) # a set of sentences for different entity labels
                    dataset.extend(sentence)
                    # if (len(dataset) > 1000): #split dataset every 70 training sample
                    #     print ("split new dataset")
                    #     #dataset_list.append(dataset)
                    #     with open(dataset_dest_path + str(count_dataset), 'w', encoding='utf-8') as out_file:
                    #         json.dump(dataset, out_file, ensure_ascii=False, indent=4)
                    #         count_dataset += 1
                    #     dataset = []
                    # #json.dump(sentence, out_file, ensure_ascii=False, indent=4)
                    word_seq = []
                    tag_seq = []
                continue
            word_seq.append(line.split()[0])
            if word_seq[-1] == '"': word_seq[-1] = "\""
            tag_seq.append(line.split()[-1])   
    print("total sentence: " + str(count_sentence))
    print("total gen: " + str(len(dataset)))
    with open(dataset_dest_path, 'w', encoding='utf-8') as out_file:
        json.dump(dataset, out_file, ensure_ascii=False, indent=4)
            

# print ("total entity types = " + str(len(entity_type_set)))
process_data(dataset_source_path, dataset_dest_path)
            

           

    # Write the processed data to the output file
    
