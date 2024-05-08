# -*- coding = utf-8 -*-
# @Time :2024/4/17 16:53
import os
import shutil
import random

def split_dataset(dataset_dir, train_dir, val_dir, test_dir, split_ratio=(0.8, 0.1, 0.1), seed=42):
    # 创建目标目录
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # 获取数据集中所有文件的路径
    file_paths = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir) if os.path.isfile(os.path.join(dataset_dir, f))]
    random.seed(seed)
    random.shuffle(file_paths)

    # 计算划分数量
    num_files = len(file_paths)
    num_train = int(num_files * split_ratio[0])
    num_val = int(num_files * split_ratio[1])
    num_test = num_files - num_train - num_val

    # 划分数据集
    train_files = file_paths[:num_train]
    val_files = file_paths[num_train:num_train+num_val]
    test_files = file_paths[num_train+num_val:]

    # 将文件复制到目标目录
    copy_files(train_files, train_dir)
    copy_files(val_files, val_dir)
    copy_files(test_files, test_dir)

def copy_files(file_paths, target_dir):
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        shutil.copy(file_path, os.path.join(target_dir, file_name))

# 示例用法
dataset_dir = "F:/learning/design/deep-learning-for-image-processing-master/image_data"
train_dir = "/path/to/train"
val_dir = "/path/to/validation"
test_dir = "/path/to/test"
split_ratio = (0.8, 0.1, 0.1)  # 训练集、验证集、测试集的划分比例
seed = 42  # 随机种子

split_dataset(dataset_dir, train_dir, val_dir, test_dir, split_ratio, seed)
