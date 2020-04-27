from numpy import *
from os import listdir
import operator


# 图片转化为矩阵
def img2vector(filename):
    # 建立一行1024列空矩阵
    returnVect = zeros((1, 1024))
    # 打开文件
    fr = open(filename)
    for i in range(32):
        # 从第i行开始
        lineStr = fr.readline()
        for j in range(32):
            # 列数 将32*32矩阵每一行数据赋值给1*1024矩阵内
            returnVect[0, 32*i+j] = int(lineStr[j])
    # 返回从像素到矩阵的矩阵
    return returnVect


# KNN心脏函数
def classify0(inX, dataSet, labels, k):
    """
    :param inX: 单独一个测试数据矩阵
    :param dataSet:训练数据集
    :param labels:标记集
    :param k:knn核心k
    :return:分类结果
    """
    # 得到行数
    dataSetSize = dataSet.shape[0]
    # 距离度量 度量公式为欧氏距离
    # 将测试数据做成数据集的行的标准矩阵 /然后与数据集相减
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


def handwritingClassTest():
    # 建立标签数组
    hwLabels = []
    # 1. 导入训练数据 listdir：列出目录内的文件名
    trainingFileList = listdir('D:/PY_AIfile/trainingDigits')  # load the training set
    # 得到文件名数量
    m = len(trainingFileList)
    # 建立m行1024（32*32）列的矩阵  m：训练数据个数  1024：0，1表示像素图像像素点
    trainingMat = zeros((m, 1024))
    # hwLabels存储0～9对应的index位置， trainingMat存放的每个位置对应的图片向量
    for i in range(m):
        # 第i个文件名
        fileNameStr = trainingFileList[i]
        # 去掉.txt后缀
        fileStr = fileNameStr.split('.')[0]  # take off .txt
        # 拿取标记值
        classNumStr = int(fileStr.split('_')[0])
        # 将标记值加入标记数组
        hwLabels.append(classNumStr)
        # 使用img2vector函数将训练文件内32*32的矩阵转化1*1024的矩阵
        # 并保存到统一矩阵trainingMat（m行1024列）内，从而包含所有训练数据
        trainingMat[i, :] = img2vector('D:/PY_AIfile/trainingDigits/%s' % fileNameStr)
    # 打印训练数据第一行 ///可有可无
    # #################################print(trainingMat[0])

    # 2. 导入测试数据
    testFileList = listdir('D:/PY_AIfile/testDigits')  # iterate through the test set
    # 设立错误次数计数器
    errorCount = 0.0
    # 得到测试数据行数
    mTest = len(testFileList)
    for i in range(mTest):
        # 得到第一个文件名
        fileNameStr = testFileList[i]
        # 去掉.txt
        fileStr = fileNameStr.split('.')[0]  # take off .txt
        # 得到标签值
        classNumStr = int(fileStr.split('_')[0])
        # 将文件矩阵导入统一测试矩阵内
        vectorUnderTest = img2vector('D:/PY_AIfile/testDigits/%s' % fileNameStr)
        # 进行分类，返回分类后结果
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        # 输出分类结果和真实结果
        # print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr))
        # 尝试每隔100次输出一次
        if i % 100 == 0:
            print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr))
        # 比较分类结果和真是结果，若不相等则错误数加1
        if classifierResult != classNumStr:
            errorCount += 1.0
    print("\nthe total number of errors is: %d" % errorCount)
    print("\nthe total error rate is: %f" % (errorCount / float(mTest)))


def main():
    # 测试正确率
    handwritingClassTest()


if __name__ == '__main__':
    main()
