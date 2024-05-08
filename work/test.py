# -*- coding = utf-8 -*-
# @Time :2024/2/20 16:39
import os
import sys
import json
import torch
from PIL import Image
import matplotlib.pyplot as plt
from torchvision import transforms, datasets, utils
from tqdm import tqdm
from model import resnet34

def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    data_transform = transforms.Compose(
        [transforms.Resize(256),
         transforms.CenterCrop(224),
         transforms.ToTensor(),
         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    data_root = os.path.abspath(os.path.join(os.getcwd(), ".."))  # get data root path
    image_path = os.path.join(data_root, "data_set", "liver_data")  # flower data set path
    assert os.path.exists(image_path), "{} path does not exist.".format(image_path)
    test_dataset = datasets.ImageFolder(root=os.path.join(image_path, "test"),
                                         transform=data_transform)
    test_num = len(test_dataset)

    test_loader = torch.utils.data.DataLoader(test_dataset,
                                                  batch_size=1, shuffle=False,
                                                  num_workers=0)

    print(" {} images for testing.".format(test_num))
    test_data_iter = iter(test_loader)

    test_image, test_label = next(test_data_iter)

    # read class_indict
    json_path = './class_indices.json'
    assert os.path.exists(json_path), "file: '{}' dose not exist.".format(json_path)

    with open(json_path, "r") as f:
        class_indict = json.load(f)

    # create model
    model = resnet34(num_classes=2).to(device)

    # load model weights,训练出来的参数
    weights_path = "./resnet34-pre.pth"
    assert os.path.exists(weights_path), "file: '{}' dose not exist.".format(weights_path)
    model.load_state_dict(torch.load(weights_path))

    model.eval()#关闭训练模式

    acc = 0.0  # accumulate accurate number / epoch搞到这里，还没搞完
    with torch.no_grad():
        test_bar = tqdm(test_loader, file=sys.stdout)
        for test_data in test_bar:
            test_images, test_labels = test_data
            outputs = model(test_images.to(device))
            predict_y = torch.max(outputs, dim=1)[1]
            acc += torch.eq(predict_y, test_labels.to(device)).sum().item()
            # print(predict_y)
    test_accurate = acc / test_num
    print('test_accuracy: %.3f' %
           test_accurate)

if __name__ == '__main__':
    main()
