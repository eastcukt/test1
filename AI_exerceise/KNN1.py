import numpy as np
from numpy import *
import matplotlib
import matplotlib.pyplot as plt
import operator


# 解析文本文件
def file2matrix(filename):
    # 打开文件
    fr = open(filename)
    # 获得行数
    numberOfLines = len(fr.readlines())
    # 生成空矩阵1000行3列
    returnMat = zeros((numberOfLines, 3))
    # 生成标签列表，每条数据的标记，喜欢or一般
    classLableVector = []       # prepare lables return

    # 下一步非常非常非常重要，少了这步则提取不了文件内容！！！！！！！！！
    fr = open(filename)         # 这步可以注释掉我觉得

    # 设置下标
    index = 0
    for line in fr.readlines():     # 1000行循环
        # str.strip([chars]) - -返回以移除字符串头尾指定字符所生成新字符串。//这是原始注释,不懂
        line = line.strip()
        # 以/t切割字符串
        listFromLine = line.split('\t')
        # 每列的属性数据 //将0，1，2列的数据放到returnMat矩阵中
        returnMat[index, :] = listFromLine[0:3]
        # 将第3列的数据放入标记容器中
        classLableVector.append(int(listFromLine[-1]))
        # 下标+1继续循环
        index += 1
    # 返回提取的矩阵数据和标记容器
    return returnMat, classLableVector


# 分析数据，画图  //下面scatter好像有问题
def draw(datingDataMat, datingLabels):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:, 0], datingDataMat[:, 1], 15.0 * array(datingLabels), 15.0 * array(datingLabels))
    plt.show()


# 归一化,立一个统一标准
def autoNorm(dataSet):
    """
    Desc:
        归一化特征值，消除特征之间量级不同导致的影响
    parameter:
        dataSet: 数据集
    return:
        归一化后的数据集 normDataSet. ranges和minVals即最小值与范围，并没有用到

    归一化公式：
        Y = (X-Xmin)/(Xmax-Xmin)
        其中的 min 和 max 分别是数据集中的最小特征值和最大特征值。该函数可以自动将数字特征值转化为0到1的区间。
    """
    # 计算每种属性的最大值、最小值(为某一行数据)
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    # 极差，最大减最小
    ranges = maxVals - minVals
    # 按照dataset建立一个矩阵但元素都为0
    normDataSet = zeros(shape(dataSet))
    # 得到数据集的行数
    m = dataSet.shape[0]
    # 生成与最小值之差组成的矩阵
    # tile():将minvals作为模板复制m行列数不变组成矩阵 ，下一tile同理
    normDataSet = dataSet - tile(minVals, (m, 1))
    # 将最小值之差除以范围组成归一化矩阵
    normDataSet = normDataSet / tile(ranges, (m, 1))  # element wise divide
    # 返回归一化矩阵，极差，最小矩阵
    return normDataSet, ranges, minVals


# 测试代码
def classify0(inX, dataSet, labels, k):
    """
    :param inX: 归一化的数据--输入数据与最小的行数据差与极差的比值
    :param dataSet:数据集
    :param labels:标记集
    :param k:knn核心k
    :return:分类结果
    """
    # 得到行数
    dataSetSize = dataSet.shape[0]
    # 距离度量 度量公式为欧氏距离
    # 将输入数据做成1000行的标准矩阵 /然后与数据集相减
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    # 将新的数据集平方
    sqDiffMat = diffMat ** 2
    # 将待测数据集按行相加 即[[0,1,2],[0,2,2]]变成[3,4]
    sqDistances = sqDiffMat.sum(axis=1)
    # 待测数据开方
    distances = sqDistances ** 0.5

    # 将距离排序：从小到大。返回值为数组下标
    sortedDistIndicies = distances.argsort()
    # 创建分类字典
    # classCount = []是不行的，[]只能做到数组不能做到矩阵
    classCount = {}
    # 选取前K个最短距离， 选取这K个中最多的分类类别
    for i in range(k):
        # 取出前k个数据的label并保存
        voteIlabel = labels[sortedDistIndicies[i]]
        # 为字典添加元素[value:key]  /value代表label,key代表出现的次数
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    # 将字典按key排序
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    # 返回分类结果label
    return sortedClassCount[0][0]


# 测试约会代码
def datingClassTest():
    """
    Desc:
        对约会网站的测试方法
    parameters:
        none
    return:
        错误数
    """
    # 设置测试数据的的一个比例（训练数据集比例=1-hoRatio）
    hoRatio = 0.1  # 测试范围,一部分测试一部分作为样本
    # 从文件中加载数据,进而处理为标准格式
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')  # load data setfrom file
    # 归一化数据
    normMat, ranges, minVals = autoNorm(datingDataMat)
    # m 表示数据的行数，即矩阵的第一维
    m = normMat.shape[0]
    # 设置测试的样本数量， numTestVecs:m表示训练样本的数量
    numTestVecs = int(m * hoRatio)
    print('numTestVecs=', numTestVecs)
    errorCount = 0.0
    for i in range(numTestVecs):
        # 对数据测试
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
        print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i]))
        if classifierResult != datingLabels[i]:
            errorCount += 1.0
    print("the total error rate is: %f" % (errorCount / float(numTestVecs)))
    print(errorCount)


# 预测函数
def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(input("percentage of time spent playing video games ?"))
    ffMiles = float(input("frequent filer miles earned per year?"))
    iceCream = float(input("liters of ice cream consumed per year?"))
    datingDataMat, datingLabels = file2matrix('./datingTestSet2.txt')
    # draw(datingDataMat, datingLabels)
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = classify0((inArr-minVals)/ranges, normMat, datingLabels, 3)
    print("You will probably like this person: ", resultList[classifierResult - 1])


def main():
    # 测试准确率
    datingClassTest()
    # 测试你的数据
    # classifyPerson()


if __name__ == '__main__':
    main()
