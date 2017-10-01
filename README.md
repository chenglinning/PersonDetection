## 1.项目简介
给定一张图片，使用合适的方法把图片中的人检测出来，然后统计图片中总的人数，与真实人数作对比。这里我直接使用的是YOLOV2的模型yolo.weights（没有自己训练模型），通过对图片里人的检测，从而实现计算有多少个人。
   ### 1.1基本思路
   * 去YOLO官网或是在github上下载YOLOv2的源码。
   * 本项目没有自己训练模型，而是直接使用官网训练好的模型yolo.weights.
   * 由于该模型是对20类物体进行检测识别，但这个项目只需要对人进行检测，因此需要先对YOLOv2的源码进行修改，使其只检测并输出人的bounding box位置。
   * 由于YOLOv2对小物体或是比较密集的人群检测得不是很理想，因此根据情况先对原图片做分割，然后对分割后的图片单独进行检测。
   * 由于分割图片然后检测会导致在分割线处会出现重复检测的情况，因此设计了一个算法，使得在分割线处，如果是属于同一个人的框都合并在一起。
   * 为了提高精度，把一些比较大的框所覆盖的原图区域提取出来，重新放进网络中进行检测。
   * 最后整合上述的处理结果，在原图上把检测到的人都用红框标记出来。

## 2.YOLOv2简介
YOLO全称是：You Only Look Once：Unified, Real-Time Object Detection，是一种支持端到端训练和测试的卷积神经网络，在保证一定准确率的前提下能图像中多目标的检测与识别,YOLO是一个可以一次性预测多个Box位置和类别的卷积神经网络，能够实现端到端的目标检测和识别，其最大的优势就是速度快。事实上，目标检测的本质就是回归，因此一个实现回归功能的CNN并不需要复杂的设计过程。YOLO没有选择滑窗或提取proposal的方式训练网络，而是直接选用整图训练模型，这样做的好处在于可以更好的区分目标和背景区域，相比之下，采用proposal训练方式的Fast-R-CNN常常把背景区域误检为特定目标，但YOLO在提升检测速度的同时牺牲了一些精度。<br>
具体的可以去 [YOLO官网](https://pjreddie.com/darknet/yolo/)查看。
## 3.运行环境
* ubuntu 14.04
* 最好安装GPU和安转CUDA，CPU下也可以运行，但是比较慢。
* 编程语言是Python和C,python推荐安装Anaconda,需要安装的python库：
    * opencv
    * numpy

## 4.使用方式

* 将项目clone到你的本地：`git clone https://github.com/Lihit/PersonDetection.git`
* 到下载后的文件夹`：cd PersonDetection`。
* 首先需要把`yolo.weights`的模型下载下来，打开文件`yolo.weights.download`里面有百度网盘的下载链接，你也可以自己去官网下载。
* 打开终端，运行`make`，先对项目进行编译。
* 在终端输入`sudo ./run.sh [your imagepath] [SplitRow] [SplitCol]`，`your imagepath`是你需要检测的图片路径，`SplitRow`是
需要将图片的行分成几份，同理`SplitCol`需要将图片的列分成几份，如果不设置，默认是2*2,分割的原因是yolo对小物体检测的效果并不是很好，合理分割参数可以
使准确率有很大的提升。
* 然后在项目的根目录下会生成检测后的图片，`ImageUnited.png`。

## 5.运行结果
我测试的结果放在项目的文件`testResult`下。下面贴出几张训练的结果：
* 测试1：<br>
   * 原图：<br>
   ![image](https://github.com/Lihit/PersonDetection/blob/master/TestResult/图片/b3.jpg)
   * 检测图：<br>
   ![image](https://github.com/Lihit/PersonDetection/blob/master/TestResult/result/b3_18.png)
* 测试2：<br>
   * 原图：<br>
   ![image](https://github.com/Lihit/PersonDetection/blob/master/TestResult/图片/f2.jpg)
   * 检测图：<br>
   ![image](https://github.com/Lihit/PersonDetection/blob/master/TestResult/result/f2_42.png)
