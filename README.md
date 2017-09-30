## 1.项目简介
给定一张图片，使用合适的方法把图片中的人检测出来，然后统计图片中总的人数，与真实人数作对比。这里我直接使用的是YOLOV2的模型yolo.weights（没有自己训练模型），通过对图片里人的检测，从而实现计算有多少个人。
## 2.YOLOv2简介
YOLO全称是：You Only Look Once：Unified, Real-Time Object Detection，是一种支持端到端训练和测试的卷积神经网络，在保证一定准确率的前提下能图像中多目标的检测与识别,YOLO是一个可以一次性预测多个Box位置和类别的卷积神经网络，能够实现端到端的目标检测和识别，其最大的优势就是速度快。事实上，目标检测的本质就是回归，因此一个实现回归功能的CNN并不需要复杂的设计过程。YOLO没有选择滑窗或提取proposal的方式训练网络，而是直接选用整图训练模型，这样做的好处在于可以更好的区分目标和背景区域，相比之下，采用proposal训练方式的Fast-R-CNN常常把背景区域误检为特定目标，但YOLO在提升检测速度的同时牺牲了一些精度。

![iamge](https://github.com/Lihit/FaceRecognition/blob/master/ResultImage/AlexNet.png)
## 3.运行环境
* ubuntu 14.04
* 需要有GPU和安转CUDA。
* 编程语言是Python，推荐安装Anaconda,需要安装的python库：
    * opencv
    * tensorflow
    * numpy

## 4.使用方式

* 将项目clone到你的本地：`git clone https://github.com/Lihit/FaceRecognition.git`
* 到下载后的文件夹`：cd FaceRecognition`。
* 文件`AlexNet.py`是AlexNet的具体实现，讲它写成了一个类。
* 打开终端，运行`python AlexnetTrain.py`，即可进行训练，但是由于训练数据太大，无法上传，需要自己准备数据或是联系我。
* 如果你是自己准备数据，可以使用`python ExpandImageSample.py`来扩充你的数据集，具体的做法以及要修改的一些地方（如文件路径），请 
看`ExpandImageSample.py` 的代码。
* 如果能够正常训练，那么文件夹`MyModel`将会保存你训练的模型（如果你想下载我训练模型，请联系我），而文件夹`LogFIle`将会保存你的训练日志。
* `AlexnetTest.ipynb`用来测试准确率，`LossAndAccuracy.ipynb`用来绘制损失和准确率函数。

## 5.运行结果

* 训练时的训练误差和验证误差：<br>
![iamge](https://github.com/Lihit/FaceRecognition/blob/master/ResultImage/traingingErro.png)
* 单人的测试结果：<br>
![iamge](https://github.com/Lihit/FaceRecognition/blob/master/ResultImage/testResult.png)
* 随机抽取20人的测试结果：<br>
![iamge](https://github.com/Lihit/FaceRecognition/blob/master/ResultImage/testResult(20pictures).png)
* loss和Accuracy曲线的绘制：<br>
![iamge](https://github.com/Lihit/FaceRecognition/blob/master/ResultImage/lossAndAccuracy.png)
