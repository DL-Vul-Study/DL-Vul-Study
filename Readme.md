##  实验的主要核心为main.py，其中和核心函数为main()和main_test

- main(): 主要用于模型的训练和结果保存
- main_test(): 主要用于将训练好的模型在交叉数据集上进行测试并保存结果

## 实验主要分如下几步：

- 1、静态分析处理，不同模型的处理方式不同，通过joern等工具进行数据预处理
- 2、划分训练集测试集，十折交叉等
- 3、运行main.py进行运行和测试

## 从不同模型介绍

### bert & codebert & LSTM & GRU & TextCNN & astgru

- 1、通过generate_pkl.py中的相应部分进行静态处理，将.c文件处理并整合为.pkl文件
- 2、运行main.py中的模型相应部分

###  vulcnn

- 参考vulcnn开源代码 （ https://gitee.com/QISANSAN/vulcnn ）

### vulroberta

- 1、通过generate_pkl.py中的相应部分进行静态处理，将.c文件处理并整合为.pkl文件
- 2、通过generate_vulberta_data.py生成vulberta需要的数据文件
- 3、运行main.py中的模型相应部分

### code2vec

- 1、通过astminer（可以参考 https://gitee.com/QISANSAN/astminer ）结合官方文档运行yaml文件
- 2、运行astminer_to_c2v.py文件将astminer数据文件生成code2vec数据文件
- 3、运行main.py中的模型相应部分

### devign & reveal

- 1、通过joern_graph_gen.py 使用joern工具将.c文件生成对应的bin中间文件，然后生成ast和pdg图
- 2、通过joern_to_devign.py 将joern生成的图转化为json文件
- 3、通过main.py中的prepare_devign_reveal()函数将json文件整合为dataset文件
- 4、运行main.py中的模型相应部分
