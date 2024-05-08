from PIL import ImageEnhance
import os
import numpy as np
from PIL import Image


def brightnessEnhancement(root_path, img_name):  # 亮度增强
    image = Image.open(os.path.join(root_path, img_name))
    enh_bri = ImageEnhance.Brightness(image)
    brightness = 1.1+0.4*np.random.random()#取值范围1.1-1.5
    # brightness = 1.5
    image_brightened = enh_bri.enhance(brightness)
    return image_brightened


def contrastEnhancement(root_path, img_name):  # 对比度增强
    image = Image.open(os.path.join(root_path, img_name))
    enh_con = ImageEnhance.Contrast(image)
    contrast = 1.1+0.4*np.random.random()#取值范围1.1-1.5
    # contrast = 1.5
    image_contrasted = enh_con.enhance(contrast)
    return image_contrasted


def rotation(root_path, img_name):
    img = Image.open(os.path.join(root_path, img_name))
    random_angle = np.random.randint(-2, 2) * 90
    if random_angle == 0:
        rotation_img = img.rotate(-90)  # 旋转角度
    else:
        rotation_img = img.rotate(random_angle)  # 旋转角度
    # rotation_img.save(os.path.join(root_path,img_name.split('.')[0] + '_rotation.jpg'))
    return rotation_img


def flip(root_path, img_name):  # 翻转图像
    img = Image.open(os.path.join(root_path, img_name))
    filp_img = img.transpose(Image.FLIP_LEFT_RIGHT)

    return filp_img


def createImage(imageDir, saveDir):
    i = 0
    for name in os.listdir(imageDir):
        i = i + 1
        saveName = "cesun" + str(i) + ".jpg"
        saveImage = contrastEnhancement(imageDir, name)
        saveImage.save(os.path.join(saveDir, saveName))
        saveName1 = "flip" + str(i) + ".jpg"
        saveImage1 = flip(imageDir, name)
        saveImage1.save(os.path.join(saveDir, saveName1))
        saveName2 = "brightnessE" + str(i) + ".jpg"
        saveImage2 = brightnessEnhancement(imageDir, name)
        saveImage2.save(os.path.join(saveDir, saveName2))
        saveName3 = "rotate" + str(i) + ".jpg"
        saveImage = rotation(imageDir, name)
        saveImage.save(os.path.join(saveDir, saveName3))

        _saveName = "_cesun" + str(i) + ".jpg"
        _saveImage = contrastEnhancement(imageDir, name)
        _saveImage.save(os.path.join(saveDir, _saveName))

        _saveName2 = "_brightnessE" + str(i) + ".jpg"
        _saveImage2 = brightnessEnhancement(imageDir, name)
        _saveImage2.save(os.path.join(saveDir, _saveName2))
        _saveName3 = "_rotate" + str(i) + ".jpg"
        _saveImage = rotation(imageDir, name)
        _saveImage.save(os.path.join(saveDir, _saveName3))


imageDir = "F:/learning/design/deep-learning-for-image-processing-master/fat/serious_ori"  # 要改变的图片的路径文件夹
saveDir = "F:/learning/design/deep-learning-for-image-processing-master/fat/serious2"  # 数据增强生成图片的路径文件夹
createImage(imageDir, saveDir)
