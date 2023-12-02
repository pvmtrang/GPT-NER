from simcse import SimCSE
import json
import numpy as np
import os
import faiss
import random

# where can i get this data nhi??
def read_feature(dir_, prefix):
    print("------>HERE AT read_feature " + os.path.join(dir_, f"{prefix}.start_word_feature_info.json"))
    info_file = json.load(open(os.path.join(dir_, f"{prefix}.start_word_feature_info.json")))
    features = np.memmap(os.path.join(dir_, f"{prefix}.start_word_feature.npy"), 
                         dtype=np.float32,
                         mode="r",
                         shape=(info_file["entity_num"], info_file["hidden_size"]))
    index_file = []
    file = open(os.path.join(dir_, f"{prefix}.start_word_feature_index.json"), "r")
    for line in file:
        index_file.append(int(line.strip()))
    file.close()
    return info_file, features, index_file

def read_mrc_data(dir_, prefix):
    file_name = os.path.join(dir_, f"mrc-ner.{prefix}")
    print("------>HERE AT read_mrc_data " + file_name) 
    with open(file_name, encoding="utf-8") as file:
        data = json.load(file)
    #return json.load(open(file_name, encoding="utf-8"))
    return data

def read_idx(dir_, prefix="test"):
    print("------>HERE AT read_idx " + dir_)
    print("reading ...")
    file_name = os.path.join(dir_, f"{prefix}.knn.jsonl")
    example_idx = []
    file = open(file_name, "r")
    for line in file:
        example_idx.append(json.loads(line.strip()))
    file.close()
    return example_idx

def compute_mrc_knn(test_info, test_features, train_info, train_features, train_index, knn_num=32):
    print("------>HERE AT compute_mrc_knn")
    quantizer = faiss.IndexFlatIP(train_info["hidden_size"])
    index = quantizer
    index.add(train_features.astype(np.float32))
    # 10 is a default setting in simcse
    index.nprobe = min(10, train_info["entity_num"])
    # index = faiss.index_gpu_to_cpu(index) mtrang: hiding this to use faiss-cpu

    top_value, top_index = index.search(test_features.astype(np.float32), knn_num)

    sum_ = 0
    vis_index = {}
    for idx_, value in enumerate(train_index):
        if value == 0:
            continue
        for i in range(sum_, value+sum_):
            vis_index[i] = idx_
        sum_ += value

    example_idx = [[vis_index[int(i)] for i in top_index[idx_]] for idx_ in range(test_info["entity_num"])]
    example_value = [[float(value) for value in top_value[idx_]] for idx_ in range(test_info["entity_num"])]

    return example_idx, example_value

def compute_simcse_knn(test_mrc_data, train_mrc_data, knn_num, test_index=None):
    print("------>HERE AT compute_simcse_knn")
    # to download model
    # sim_model = SimCSE("princeton-nlp/sup-simcse-roberta-large")
    # but i downloaded the model roi, nen la thui
    sim_model = SimCSE("data/models/simcse-roberta-large")

    train_sentence = {} #train_sentence[entity_label][a list of its contexts in the training set]
    train_sentence_index = {} #train_sentence_index[entity_label][list of the above corresponding index in the training set]
    print("re-arrange context by entity type")
    for idx_, item in enumerate(train_mrc_data):
        label = item["entity_label"]
        # print("this is label " + label)
        context = item["context"]
        # if len(item["start_position"]) == 0:
        #     if label not in train_sentence:
        #         train_sentence[label] = []
        #         train_sentence_index[label] = []
        #     train_sentence[label].append(context)
        #     train_sentence_index[label].append(idx_)
        if item["impossible"] == False: #chi duoc record cai context nao ma thuc su chua cai label day thoi chu????
            if label not in train_sentence:     
                train_sentence[label] = []
                train_sentence_index[label] = []
            train_sentence[label].append(context) #group train samples by label
            train_sentence_index[label].append(idx_)    #and note lai index cua no
    
    print("encode embedding for all contexts of each label type")
    train_index = {}
    for key, _ in train_sentence.items(): #for each entity label
        print("--for type = " + str(key) + ": " + str(len(train_sentence[key])))
        #lam cai gi day ta?? huhu gio phai di doc code cua simcse a?? idk, calculate the embedding of all contexts?
        embeddings = sim_model.encode(train_sentence[key], batch_size=128, normalize_to_unit=True, return_numpy=True)
        print("----done encoding")
        quantizer = faiss.IndexFlatIP(embeddings.shape[1])
        index = quantizer #?? lmao
        index.add(embeddings.astype(np.float32))
        # 10 is a default setting in simcse
        index.nprobe = min(10, len(train_sentence[key])) #number of clusters to explore while finding neighbor
        # since i'm using faiss-cpu already, no need to move it to cpu memory
        # index = faiss.index_gpu_to_cpu(index)

        train_index[key] = index 
    #-> loop thru all entity label -> calculate embedding of each entity label's list of contexts
    #train_index vs train_sentence align in index
    
    print ("In test set")

    example_idx = []
    example_value = []
    if test_index is None: #test_index la gi ta?? the result?!?? 0.0 what??
        for idx_ in range(len(test_mrc_data)): # ua sao ko enumerate(test_mrc_data) nua di
            # print("-test sample id = " + str(idx_))
            context = test_mrc_data[idx_]["context"]
            label = test_mrc_data[idx_]["entity_label"]
           # print("this test set co label " + label)
            # for each test sample -> get the embedding of its context
            # -> search for knn_num nearest neighbor of that sample's label's context in the training set?
            embedding = sim_model.encode([context], batch_size=128, normalize_to_unit=True, keepdim=True, return_numpy=True)
            # print("---done encode context")
            top_value, top_index = train_index[label].search(embedding.astype(np.float32), knn_num)
            # get the k nearest contexts with the values of contexts and their indices in the training set

            #why [0] only?? the nearest neighbor thui ha? or maybe that's how .search result is formatted??
            example_idx.append([train_sentence_index[label][int(i)] for i in top_index[0]]) #[0] gi vay??
            # maybe [0] stores all k neighbor 
            #-> loop through [0], foreach neighbor -> add its index in the train_set and its embedding value?
            example_value.append([float(value) for value in top_value[0]])
        
        #return test_set[index] -> example_value[index]((a list of k neighbor's embedding context))
        # example_idx[index]((a list of the neighbors' index in the train set[label]))
        # print(str(example_idx))
        # print(str(example_value))
        return example_idx, example_value
    #to pass in another test set other than the mrc-ner.test a???
    for idx_, sub_index in enumerate(test_index):
        if sub_index != 0: #hmm??
            continue
        context = test_mrc_data[idx_]["context"]
        label = test_mrc_data[idx_]["entity_label"]

        embedding = sim_model.encode([context], batch_size=128, normalize_to_unit=True, keepdim=True, return_numpy=True)
        top_value, top_index = train_index[label].search(embedding.astype(np.float32), knn_num)

        example_idx.append([train_sentence_index[label][int(i)] for i in top_index[0]])
        example_value.append([float(value) for value in top_value[0]])
    
    return example_idx, example_value

def combine_full_knn(test_index, mrc_knn_index, simcse_knn_index):
    print("------>HERE AT combine_full_knn")
    results = []
    mrc_idx = 0
    simcse_idx = 0
    for idx_, num in enumerate(test_index):
        if num == 0:
            results.append(simcse_knn_index[simcse_idx])
            simcse_idx += 1
        else:
            knn_num = len(mrc_knn_index[mrc_idx])
            span_ = int(knn_num // num)
            if span_ * num != knn_num:
                span_ += 1
            sub_results = []
            for sub_idx in range(mrc_idx, mrc_idx+num):
                sub_results = sub_results + mrc_knn_index[sub_idx][:span_]
            sub_results = sub_results[:knn_num]
            results.append(sub_results)
            mrc_idx += num
    
    return results

def random_knn(test_mrc_data, train_mrc_data, knn_num):
    print("------>HERE AT random_knn")
    train_sentence = {}
    train_sentence_index = {}
    print("done group train data")
    for idx_, item in enumerate(train_mrc_data):
        label = item["entity_label"]
        context = item["context"]
        if item["impossible"] == False:
            if label not in train_sentence:
                train_sentence[label] = []
                train_sentence_index[label] = []
            train_sentence[label].append(context)
            train_sentence_index[label].append(idx_)

    example_idx = []
    print("test data")
    for idx_ in range(len(test_mrc_data)):
        context = test_mrc_data[idx_]["context"]
        label = test_mrc_data[idx_]["entity_label"]

        random.shuffle(train_sentence_index[label])

        example_idx.append(train_sentence_index[label][:knn_num])
    
    return example_idx, None

def write_file(dir_, data):
    file = open(dir_, "w")
    for item in data:
        file.write(json.dumps(item, ensure_ascii=False)+'\n')
    file.close()

if __name__ == '__main__':

    cwd = os.getcwd() # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory"

    test_mrc_data = read_mrc_data(dir_="data\\phoNER_COVID19", prefix="test_500_converted")
    train_mrc_data = read_mrc_data(dir_="data\\phoNER_COVID19", prefix="train_converted")
    index_, value_ = compute_simcse_knn(test_mrc_data=test_mrc_data, train_mrc_data=train_mrc_data, knn_num=10)
    # index_, value = random_knn(test_mrc_data=test_mrc_data, train_mrc_data=train_mrc_data,knn_num=10)
    write_file(dir_="data\\phoNER_COVID19\\test_500_simsce_10.knn.jsonl", data=index_) #only store the indices matrix thui
    
    train_sentence = {} #train_sentence[entity_label][a list of its contexts in the training set]
    train_sentence_index = {} #train_sentence_index[entity_label][list of the above corresponding index in the training set]
    for idx_, item in enumerate(train_mrc_data):
        label = item["entity_label"]
        context = item["context"]
        if label not in train_sentence:     
            train_sentence[label] = []
            train_sentence_index[label] = []
        train_sentence[label].append(context) #group train samples by label
        train_sentence_index[label].append(idx_)    #and note lai index cua no

    print("max index of test_data = " + str(len(test_mrc_data)))
    for i in range(10):
        test_label = test_mrc_data[i]["entity_label"]
        print("the test sentence is: " + test_mrc_data[i]["context"] + " of label " + test_label)
        list_index = index_[i]
        print("list id of neighbor is " + str(list_index))
        for idx_ in range (3):
            print("neighbor #"+str(idx_)+": " + train_mrc_data[list_index[idx_]]["context"])
        print("----------")
   
