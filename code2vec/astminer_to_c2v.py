import os
import shutil
import pickle
from tqdm import tqdm

def get_data(input_path):
    data = []
    for i in range(len(os.listdir(input_path))):
        INPUT_PATH = os.path.join(input_path, str(i+1), "c")
        c2s_path = os.path.join(INPUT_PATH, "data/path_contexts.c2s")
        node_types_path = os.path.join(INPUT_PATH, "node_types.csv")
        paths_path = os.path.join(INPUT_PATH, "paths.csv")
        tokens_path = os.path.join(INPUT_PATH, "tokens.csv")

        node_types_dict = {}
        paths_dict = {}
        tokens_dict = {}
        with open(node_types_path) as f:
            f.readline()
            for line in tqdm(f.readlines()):
                line = line.strip()
                strs = line.split(",")
                strs[1] = strs[1].replace(" ", "|")
                node_types_dict[strs[0]] = strs[1]
        print(len(node_types_dict))

        with open(tokens_path) as f:
            f.readline()
            for line in tqdm(f.readlines()):
                line = line.strip()
                strs = line.split(",")
                tokens_dict[strs[0]] = strs[1]
        print(len(tokens_dict))

        with open(paths_path) as f:
            f.readline()
            for line in tqdm(f.readlines()):
                line = line.strip()
                strs = line.split(",")
                pid = strs[0]
                nodes = strs[1].split()
                paths_dict[pid] = nodes
        print(len(paths_dict))

        with open(c2s_path) as f:
            for line in tqdm(f.readlines()):
                strs = line.split()
                if len(strs) == 1:
                    continue
                fn = strs[0]
                Target = 'NoVul'
                if fn[0] == "1":
                    Target = 'Vul'
                strs = strs[1:]
                path_list = []
                for path in strs:
                    apath = path.split(",")
                    token1 = apath[0]
                    token2 = apath[2]
                    pathid = apath[1]
                    ppath = paths_dict[pathid]
                    pathstr = ""
                    for node in ppath:
                        pathstr = pathstr + node_types_dict[node] + " "
                    pathstr = pathstr.strip()
                    path_list.append([tokens_dict[token1], pathstr, tokens_dict[token2]])
                data.append([Target, path_list, fn])
    return data

def dataset_generation(INPUT_PATH, OUTPUT_PATH, DATASET, dataset_type):
    SEED = 1234
    if not os.path.exists(OUTPUT_PATH): os.makedirs(OUTPUT_PATH)
    data = get_data(INPUT_PATH)
    path2index = {}
    for d in tqdm(data):
        for path in d[1]:
            if path[1] not in path2index:
                path2index[path[1]] = len(path2index)

    print(len(path2index))
    word2count = {}
    path2count = {}
    target2count = {}
    n_training_examples = 0

    for d in tqdm(data):
        target = d[0]
        target2count[target] = target2count.get(target, 0) + 1
        for path in d[1]:
            word1 = path[0]
            word2 = path[2]
            pathstr = path[1]
            word2count[word1] = word2count.get(word1, 0) + 1
            word2count[word2] = word2count.get(word2, 0) + 1
            path2count[path2index[pathstr]] = path2count.get(path2index[pathstr], 0) + 1
        n_training_examples += 1
    

    with open(os.path.join(OUTPUT_PATH, DATASET + '.dict.c2v'), 'wb') as f:
        pickle.dump(word2count, f)
        pickle.dump(path2index, f)
        pickle.dump(target2count, f)
        pickle.dump(n_training_examples, f)

    
    def load_data(filename):
        print("开始读取数据于：", filename)
        f = open(filename, 'rb')
        data = pickle.load(f)
        f.close()
        return data
    def sava_data(filename, data):
        print("saving data to:", filename)
        f = open(filename, 'wb')
        pickle.dump(data, f)
        f.close()
    def save_data_file(data, filename):
        print("Saving to ", filename, "...")
        with open(os.path.join(OUTPUT_PATH, filename), 'w') as f:
            for d in tqdm(data):
                line = d[0] + ' ' + d[2] + ' '
                examples = []
                for path in d[1]:
                    tem_path = [i for i in path]
                    tem_path[1] = str(path2index[path[1]])
                    # path[1] = str(path2index[path[1]])
                    example = ','.join(tem_path)
                    examples.append(example)
                line = line + ' '.join(examples)
                f.write(line + '\n')
    # train_all = load_data("./issta2022/data/pkl/original_dataset/" + DATASET + "/train.pkl")
    # test_all = load_data("./issta2022/data/pkl/original_dataset/" + DATASET +"/test.pkl")
    # train_tem = {}
    # test_tem = {}
    # for cnt in range(10):
    #     train_tem[cnt] = [i for i in tqdm(data) if i[2].split(".")[0] in list(train_all[cnt].filename.apply(lambda x: x.split(".")[0]))]
    #     test_tem[cnt] = [i for i in tqdm(data) if i[2].split(".")[0] in list(test_all[cnt].filename.apply(lambda x: x.split(".")[0]))]
       
    #     save_data_file(train_tem[cnt], DATASET + "_" + str(cnt) + '.train.c2v')
    #     save_data_file(test_tem[cnt], DATASET  + "_" + str(cnt) + '.test.c2v')
    #     save_data_file([], DATASET + "_" + str(cnt) + '.val.c2v')

    save_data_file(data, DATASET + '.data.c2v')
    # sava_data(os.path.join(OUTPUT_PATH, "train_final.pkl") , train_tem)
    # sava_data(os.path.join(OUTPUT_PATH, "test_final.pkl") , test_tem)

    # from sklearn.model_selection import train_test_split
    # train_data, test_data = train_test_split(data, test_size=0.2, random_state=SEED)
    # test_data, val_data = train_test_split(test_data, test_size=0.5, random_state=SEED)

    

def split_data(source_path, save_path):
    a = 0
    b = 0
    for file in tqdm(os.listdir(source_path)):
        if a % 10000 == 0:
            b += 1
            p = save_path + "/" + str(b)
            if not os.path.exists(p): os.makedirs(p)
        shutil.copy(source_path + "/" + str(file), p + r"/")
        a += 1

def main():
    # 这俩是将数据划分为10000个一组用的
    # source_path = "./issta2022/data/source_code"
    # save_path = "/root/data/code2vec/source_code"

    # 这俩是将astminer的数据整合起来用的
    source_path = "/root/data/code2vec/data"
    # save_path = "./code2vec/data_final"
    save_path = "./code2vec/data_2"
    # save_path = "./issta2022/data/pkl/code2vec"
    for dataset_type in["sub_mutation_dataset"]:
    # for dataset_type in["sub_original_dataset", "sub_mutation_dataset"]:
        for file_val in ["qemu", "reveal"]:
        # for file_val in ["ffmpeg", "qemu", "reveal"]:
            # split_data(os.path.join(source_path, dataset_type, file_val), \
            #     os.path.join(save_path, dataset_type, file_val))

            dataset_generation(os.path.join(source_path, dataset_type, file_val), \
                os.path.join(save_path, dataset_type, file_val), file_val, dataset_type)

if __name__ == "__main__":
    main()