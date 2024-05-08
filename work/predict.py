
import torch
from PIL import Image
import torchvision.transforms as transforms
from torch.autograd import Variable
from model import resnet34
import os
import json



# 图片标准化
transform_BZ= transforms.Normalize(
    mean=[0.5, 0.5, 0.5],
    std=[0.5, 0.5, 0.5]
)
json_path = './class_indices.json'
assert os.path.exists(json_path), "file: '{}' dose not exist.".format(json_path)

with open(json_path, "r") as f:
    class_indict = json.load(f)#分类

val_tf = transforms.Compose([
                transforms.Resize(224),
                transforms.ToTensor(),
                transform_BZ#标准化操作
            ])


def padding_black(img):
    w, h = img.size
    scale = 224. / max(w, h)
    img_fg = img.resize([int(x) for x in [w * scale, h * scale]])
    size_fg = img_fg.size
    size_bg = 224
    img_bg = Image.new("RGB", (size_bg, size_bg))
    img_bg.paste(img_fg, ((size_bg - size_fg[0]) // 2,
                          (size_bg - size_fg[1]) // 2))
    img = img_bg
    return img


def predict(img_path):
    # 如果显卡可用，则用显卡进行训练
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("using {} device.".format(device))
    # print(f"Using {device} device")


    model = resnet34(num_classes=2).to(device)

    model.load_state_dict(torch.load("resnet34-pre.pth", map_location=device))

    img = Image.open(img_path)  # 打开图片
    img = img.convert('RGB')  # 转换为RGB 格式
    img = padding_black(img)
    # print(type(img))


    img_tensor = val_tf(img)
    # print(type(img_tensor))

    # 增加batch_size维度
    img_tensor = Variable(torch.unsqueeze(img_tensor, dim=0).float(), requires_grad=False).to(device)

    model.eval()
    with torch.no_grad():
        output_tensor = model(img_tensor)

        output = torch.softmax(output_tensor, dim=1)

        pred_value, pred_index = torch.max(output, 1)


        classes = ["middle","mild","normal","serious"]

        # print()
        result = "Predicted as: {}： "+str(classes[pred_index])+ " probability : "+str(pred_value * 100)+ "%"

        return result

