import os
from tqdm import tqdm
from base_access import AccessBase

import json
import argparse
from dataset_name import FULL_DATA
import random

random.seed(1)

#use custom logger
from logger import get_logger 
logger = get_logger(__name__) 

#use pythonjsonlogger
# import logging
# logger = logging.getLogger(__name__)

def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--source-dir", type=str, help="directory for the input")
    parser.add_argument("--source-name", type=str, help="file name for the input")
    parser.add_argument("--train-name", type=str, default="None", help="file name for the training set")
    parser.add_argument("--data-name", type=str, help="dataset name for the input")
    parser.add_argument("--example-dir", type=str, default="None", help="directory for the example")
    parser.add_argument("--example-name", type=str, default="None", help="file name for the example")
    parser.add_argument("--example-num", type=int, default=16, help="numebr for examples")
    parser.add_argument("--last-results", type=str, default="None", help="unfinished file")
    parser.add_argument("--write-dir", type=str, help="directory for the output")
    parser.add_argument("--write-name", type=str, help="file name for the output")
    
    return parser

def read_mrc_data(dir_, prefix="test"):
    file_name = os.path.join(dir_, f"mrc-ner.{prefix}")
    return json.load(open(file_name, encoding="utf-8"))

def read_results(dir_):
    file = open(dir_, "r")
    resulst = file.readlines()
    file.close()
    return resulst

def read_examples(dir_, prefix="dev"):
    print("reading ...")
    file_name = os.path.join(dir_, f"mrc-ner.{prefix}")
    return json.load(open(file_name, encoding="utf-8"))

def read_idx(dir_, prefix="test"):
    print("reading ...")
    file_name = os.path.join(dir_, f"{prefix}.knn.jsonl") #read the output of sentence-level embed 
    example_idx = []
    file = open(file_name, "r")
    for line in file:
        example_idx.append(json.loads(line.strip()))
    file.close()
    return example_idx

#mrc_data: test set. what a stupid name =_=
#example_idx -> store indices of k neighbor of each test sample
def mrc2prompt(mrc_data, data_name="CONLL", example_idx=None, train_mrc_data=None, example_num=16, last_results=None):
    print("mrc2prompt ...")
    
    #return the sentence + special tokens around its entities
    #get_example(): Few-shot demonstration part
    # given a test sample -> retrieve k neighbors in the train set 
    # -> for each neighbor, add special tokens around entity -> construct the prompt with original and new neighbor sentence
    # -> return that set of k prompts of those k neighbors
    def get_example(index): #is to process the sample context -> adding special token to make prompt
        exampel_prompt = ""
        for idx_ in example_idx[index][:example_num]: #example_idx[index][:example_num] -> example_num nearest neighbor out of k?
            #what if example_num > k -> array out of bound ha??
            context = train_mrc_data[idx_]["context"] #get the corresponding context of that neighbor from train set
            context_list = context.strip().split() #split to list of words
            labels = "" #the final context after being processed to add special tokens

            last_ = 0 #where the last entity to process was
            for span_idx in range(len(train_mrc_data[idx_]["start_position"])): #loop thru each word entity position
                start_ = train_mrc_data[idx_]["start_position"][span_idx] #for each starting position of entity 
                end_ = train_mrc_data[idx_]["end_position"][span_idx] + 1 #entity only has 1 word thui ha??
                #this is not looping thru each word in the context nhe. Don't be confuse
                if labels != "":
                    labels += " " #adding space between words thui
                if last_ == start_: #if the first word is an entity -> @@first_word##
                    labels += "@@" + " ".join(context_list[start_:end_]) + "##"
                else:
                    #copy the part from the last entity to this current entity + @@current_entity##
                    labels += " ".join(context_list[last_:start_]) + " @@" + " ".join(context_list[start_:end_]) + "##"
                last_ = end_ #update the last entity position thui

            if labels != "" and last_ != len(context_list): #copy the rest of sentence if any
                labels += " "
            labels += " ".join(context_list[last_:])

            exampel_prompt += f"The given sentence: {context}\n"
            
            # exampel_prompt += f"{prompt_label_name} entities: {labels}\n"
            exampel_prompt += f"The labeled sentence: {labels}\n"
        return exampel_prompt
        
    results = []
    for item_idx in tqdm(range(len(mrc_data))): #foreach test sample

        if last_results is not None and last_results[item_idx].strip() != "FRIDAY-ERROR-ErrorType.unknown":
            continue

        item_ = mrc_data[item_idx]
        context = item_["context"]
        origin_label = item_["entity_label"]
        #FULL_DATA is for the description of entity label
        #create the prompt for each test sample?
        transfered_label, sub_prompt = FULL_DATA[data_name][origin_label]
        prompt_label_name = transfered_label[0].upper() + transfered_label[1:]
        # prompt = f"I want to extract {transfered_label} entities that {sub_prompt}, and if that does not exist output \"none\". Below are some examples.\n"
        # prompt = f"I want to extract {transfered_label} entities that {sub_prompt}. Below are some examples.\n"
        prompt = f"You are an excellent linguist. Within the OntoNotes5.0 dataset, the task is to label {transfered_label} entities that {sub_prompt}. Below are some examples, and you should make the same prediction as the examples.\n"
        # prompt = f"You are an excellent linguist. The task is to label {transfered_label} entities in the given sentence. {prompt_label_name} entities {sub_prompt}. Noted that if the given sentence does not contain any {transfered_label} entities, just output the same sentence, or surround the extracted entities by @@ and ## if there exist {transfered_label} entities. Below are some examples."
        # prompt = f"You are an excellent linguistic. The task is to label {transfered_label} entities that {sub_prompt}. First, articulate the clues and reasoning process for determining {transfered_label} entities in the sentence. Next, based on the clues and your reasoning process, label {transfered_label} entities in the sentence. Below are some examples.\n"
        # prompt += get_knn(test_sentence=context, nums=example_false, label_name=transfered_label, positive_idx=0)
        # prompt += get_knn(test_sentence=context, nums=example_true, label_name=transfered_label, positive_idx=1)
        #adding the demonstration to the prompt
        prompt += get_example(index=item_idx)

        # context_list = context.strip().split()
        # index_string = ""
        # for sub_idx in range(len(context_list)):
        #     index_string += f"{context_list[sub_idx]} {sub_idx}\n"
        # prompt += f"The given sentence: {context}\n{index_string}{prompt_label_name} entities:"
        prompt += f"The given sentence: {context}\nThe labeled sentence:"
        # prompt += f"The given sentence: {context}\nThe labeled sentence:"

        # print(prompt)
        results.append(prompt)
    
    return results

def ner_access(openai_access, ner_pairs, batch=16):
    print("tagging ...")
    results = []
    start_ = 0
    pbar = tqdm(total=len(ner_pairs))
    while start_ < len(ner_pairs):
        end_ = min(start_+batch, len(ner_pairs))
        results = results + openai_access.get_multiple_sample(ner_pairs[start_:end_])
        pbar.update(end_-start_)
        start_ = end_
    pbar.close()
    return results

def write_file(labels, dir_, last_name):
    print("writing ...")
    file_name = os.path.join(dir_, last_name)
    file = open(file_name, "w")
    for line in labels:
        file.write(line.strip()+'\n')
    file.close()
    # json.dump(labels, open(file_name, "w"), ensure_ascii=False)

def test():
    openai_access = AccessBase(
        engine="text-davinci-003",
        temperature=0.0,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        best_of=1
    )

    ner_test = read_mrc_data("data\conll_mrc", prefix="test")[:20]
    mrc_train = read_mrc_data("data/conll_mrc", prefix="train")
    example_idx = read_idx("data\conll_mrc", prefix="test.100.simcse.32")

    prompts = mrc2prompt(mrc_data=ner_test, data_name="CONLL", example_idx=example_idx, train_mrc_data=mrc_train, example_num=4)
    results = ner_access(openai_access=openai_access, ner_pairs=prompts, batch=16)
    print(results)

if __name__ == '__main__':
    # test()


    parser = get_parser()
    args = parser.parse_args()

    openai_access = AccessBase(
        engine="text-davinci-003",
        temperature=0.0,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        best_of=1
    )

    # read source_dir.prefix file. why split into two parts??
    ner_test = read_mrc_data(args.source_dir, prefix=args.source_name) #mrc-ner.text
    mrc_train = read_mrc_data(dir_=args.source_dir, prefix=args.train_name) #mrc-ner.train
    #example_idx is the full set of test_set after done all calculation to find the k neighbor
    example_idx = read_idx(args.example_dir, args.example_name) #test.100.simcse.32.knn.jsonl

    last_results = None
    if args.last_results != "None":
        last_results = read_results(dir_=args.last_results)

    prompts = mrc2prompt(mrc_data=ner_test, data_name=args.data_name, example_idx=example_idx, train_mrc_data=mrc_train, example_num=args.example_num, last_results=last_results)
    results = ner_access(openai_access=openai_access, ner_pairs=prompts, batch=4)
    # print(results)
    write_file(results, args.write_dir, args.write_name)