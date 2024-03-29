#encoding=utf-8
import tensorflow as tf
import argparse
from skimage import measure as m
import numpy as np
import os
from PIL import Image
from utils import load_image_test
import scipy


np.set_printoptions(suppress=True)

def image_to_tensor(image):
    image = tf.expand_dims(image,0)
    image = tf.expand_dims(image,-1)
    return image

def get_image_names(file_path, with_gt=True,epoch='test'):
    L1 = []
    if with_gt:
        L2 = []
    for root,dirs,files in os.walk(file_path): #Changed Here
        for file in files:
            if epoch == 'test':
                if (os.path.splitext(file)[1] == '.jpg' or os.path.splitext(file)[1] == '.png'):
                    L1.append(os.path.join(root,file))
                    if with_gt:
                        L2.append(os.path.join('datasets/super/test/gt/', file))
            else:
                if epoch in file and (os.path.splitext(file)[1] == '.jpg' or os.path.splitext(file)[1] == '.png'):
                    L1.append(os.path.join(root,file))
                    if with_gt:
                        L2.append(os.path.join('datasets/super/test/gt/',file))
    if with_gt:
        return L1,L2
    else:
        return L1

def evaluate_val(dataset_name,epoch='0000'):
    for k,data_name in enumerate(dataset_name):
        print(data_name)
        sample_files1 = get_image_names(data_name,with_gt = False,epoch=epoch)
        value_g = [0.0]*4
        value_g_13 = [0.0] * 4
        value_g_14 = [0.0] * 4
        for i in range(0,len(sample_files1)):
            image1,image2 = load_image_test(sample_files1[i])
            image1 = image1.astype(np.float32)
            image2 = image2.astype(np.float32)
            image3 = image3.astype(np.float32)
            image4 = image4.astype(np.float32)
            value_g[0] += m.compare_mse(image2,image1)
            value_g[1] += m.compare_nrmse(image2,image1)
            value_g[2] += m.compare_psnr(image2,image1,data_range=255)
            value_g[3] += m.compare_ssim(image2,image1,K1=0.01,K2=0.03,win_size=11,data_range=255,multichannel=True)

            value_g_13[0] += m.compare_mse(image3, image1)
            value_g_13[1] += m.compare_nrmse(image3, image1)
            value_g_13[2] += m.compare_psnr(image3, image1, data_range=255)
            value_g_13[3] += m.compare_ssim(image3, image1, K1=0.01, K2=0.03, win_size=11, data_range=255,
                                            multichannel=True)

            value_g_14[0] += m.compare_mse(image4, image1)
            value_g_14[1] += m.compare_nrmse(image4, image1)
            value_g_14[2] += m.compare_psnr(image4, image1, data_range=255)
            value_g_14[3] += m.compare_ssim(image4, image1, K1=0.01, K2=0.03, win_size=11, data_range=255,
                                            multichannel=True)

            print(sample_files1[i],m.compare_psnr(image2,image1,data_range=255),m.compare_ssim(image2,image1,K1=0.01,K2=0.03,win_size=11,data_range=255,multichannel=True))

        print(np.array(value_g)/len(sample_files1))

def evaluate_test(dataset_name,epoch='test'):
    for k,data_name in enumerate(dataset_name):
        print(data_name)
        sample_files1,sample_files2 = get_image_names(data_name,with_gt = True,epoch=epoch)
        value_g = [0.0]*4
        for i in range(0,len(sample_files1)):
            image1 = Image.open(sample_files1[i])
            image2 = Image.open(sample_files2[i])
            image1 = np.array(image1)
            image2 = np.array(image2)
            # print np.shape(image1),np.shape(image2)
            image1 = image1.astype(np.float32)
            image2 = image2.astype(np.float32)
            value_g[0] += m.compare_mse(image2,image1)
            value_g[1] += m.compare_nrmse(image2,image1)
            value_g[2] += m.compare_psnr(image2,image1,data_range=255)
            value_g[3] += m.compare_ssim(image2,image1,K1=0.01,K2=0.03,win_size=11,data_range=255,multichannel=True)
            # print(sample_files1[i],m.compare_psnr(image2,image1,data_range=255),m.compare_ssim(image2,image1,K1=0.01,K2=0.03,win_size=11,data_range=255,multichannel=True))
        print(np.array(value_g)/len(sample_files1))


def eval(img,logger_val ,image_name,epoch):
    value_g = [0.0] * 4
    value_g_13 = [0.0] * 4
    value_g_14 = [0.0] * 4
    width = img.shape[1]
    h = 4

    img[:, :, 0] = (img[:, :, 0] + img[:, :, 1] + img[:, :, 2]) / 3.0
    img[:, :, 1] = 0
    img[:, :, 2] = 0

    # img_A = img[:,width//h:width//h*(h-3),:]
    # img_A = img[:,(width-15)//h*(h - 3):width//h*(h-1),:]
    image1 = img[:, 0: (width - 15) // h * (h - 3), :]
    image2 = img[:, (width - 15) // h * (h - 3) + 5:(width - 15) // h * (h - 2) + 5, :]
    image3 = img[:, (width - 15) // h * (h - 2) + 10:(width - 15) // h * (h - 1) + 10, :]
    image4 = img[:, (width - 15) // h * (h - 1) + 15:(width - 15) // h * (h - 0) + 15, :]
    image1 = image1.astype(np.float32)
    image2 = image2.astype(np.float32)
    image3 = image3.astype(np.float32)
    image4 = image4.astype(np.float32)
    print(image1.shape)
    print(image2.shape)
    print(image3.shape)
    print(image4.shape)
    value_g[0] += m.compare_mse(image2, image1)
    value_g[1] += m.compare_nrmse(image2, image1)
    value_g[2] += m.compare_psnr(image2, image1, data_range=255)
    value_g[3] += m.compare_ssim(image2, image1, K1=0.01, K2=0.03, win_size=11, data_range=255, multichannel=True)

    value_g_13[0] += m.compare_mse(image3, image1)
    value_g_13[1] += m.compare_nrmse(image3, image1)
    value_g_13[2] += m.compare_psnr(image3, image1, data_range=255)
    value_g_13[3] += m.compare_ssim(image3, image1, K1=0.01, K2=0.03, win_size=11, data_range=255, multichannel=True)

    value_g_14[0] += m.compare_mse(image4, image1)
    value_g_14[1] += m.compare_nrmse(image4, image1)
    value_g_14[2] += m.compare_psnr(image4, image1, data_range=255)
    value_g_14[3] += m.compare_ssim(image4, image1, K1=0.01, K2=0.03, win_size=11, data_range=255, multichannel=True)
    print('epoch:{}'.format(epoch))
    print('the eval of image :{}'.format(image_name))
    print('the gt compare with w1 :')
    print('mse  : {}   ,  nrmse : {}'.format(value_g[0], value_g[1]))
    print('psnr : {}   ,  ssim  : {}'.format(value_g[2], value_g[3]))
    print('the gt compare with w2 :')
    print('mse  : {}   ,  nrmse : {}'.format(value_g_13[0], value_g_13[1]))
    print('psnr : {}   ,  ssim  : {}'.format(value_g_13[2], value_g_13[3]))
    print('the gt compare with fusion :')
    print('mse  : {}   ,  nrmse : {}'.format(value_g_14[0], value_g_14[1]))
    print('psnr : {}   ,  ssim  : {}'.format(value_g_14[2], value_g_14[3]))
    logger_val.info('epoch:{}'.format(epoch))
    logger_val.info('the eval of image :{}'.format(image_name))
    logger_val.info('the gt compare with w1 :')
    logger_val.info('mse  : {}   ,  nrmse : {}'.format(value_g[0], value_g[1]))
    logger_val.info('psnr : {}   ,  ssim  : {}'.format(value_g[2], value_g[3]))
    logger_val.info('the gt compare with w2 :')
    logger_val.info('mse  : {}   ,  nrmse : {}'.format(value_g_13[0], value_g_13[1]))
    logger_val.info('psnr : {}   ,  ssim  : {}'.format(value_g_13[2], value_g_13[3]))
    logger_val.info('the gt compare with fusion :')
    logger_val.info('mse  : {}   ,  nrmse : {}'.format(value_g_14[0], value_g_14[1]))
    logger_val.info('psnr : {}   ,  ssim  : {}'.format(value_g_14[2], value_g_14[3]))
    return value_g_14[3]

def eval_test(test_dir,logger_val,image_name,epoch):
    path_gt = test_dir+'gt//'+image_name+'.tif'
    path_a = test_dir + 'a//' + image_name + '.tif'
    path_b = test_dir + 'b//' + image_name + '.tif'
    path_f = test_dir + 'f//' + image_name + '.tif'
    value_g = [0.0] * 4
    value_g_13 = [0.0] * 4
    value_g_14 = [0.0] * 4
    image1 = scipy.misc.imread(path_gt)
    image2 = scipy.misc.imread(path_a)
    image3 = scipy.misc.imread(path_b)
    image4 = scipy.misc.imread(path_f)
    image1 = image1.astype(np.float32)
    image2 = image2.astype(np.float32)
    image3 = image3.astype(np.float32)
    image4 = image4.astype(np.float32)
    print(image1.shape)
    print(image2.shape)
    print(image3.shape)
    print(image4.shape)
    value_g[0] += m.compare_mse(image2, image1)
    value_g[1] += m.compare_nrmse(image2, image1)
    value_g[2] += m.compare_psnr(image2, image1, data_range=255)
    value_g[3] += m.compare_ssim(image2, image1, K1=0.01, K2=0.03, win_size=11, data_range=255, multichannel=True)

    value_g_13[0] += m.compare_mse(image3, image1)
    value_g_13[1] += m.compare_nrmse(image3, image1)
    value_g_13[2] += m.compare_psnr(image3, image1, data_range=255)
    value_g_13[3] += m.compare_ssim(image3, image1, K1=0.01, K2=0.03, win_size=11, data_range=255, multichannel=True)

    value_g_14[0] += m.compare_mse(image4, image1)
    value_g_14[1] += m.compare_nrmse(image4, image1)
    value_g_14[2] += m.compare_psnr(image4, image1, data_range=255)
    value_g_14[3] += m.compare_ssim(image4, image1, K1=0.01, K2=0.03, win_size=11, data_range=255, multichannel=True)
    print('epoch:{}'.format(epoch))
    print('the eval of image :{}'.format(image_name))
    print('the gt compare with w1 :')
    print('mse  : {}   ,  nrmse : {}'.format(value_g[0], value_g[1]))
    print('psnr : {}   ,  ssim  : {}'.format(value_g[2], value_g[3]))
    print('the gt compare with w2 :')
    print('mse  : {}   ,  nrmse : {}'.format(value_g_13[0], value_g_13[1]))
    print('psnr : {}   ,  ssim  : {}'.format(value_g_13[2], value_g_13[3]))
    print('the gt compare with fusion :')
    print('mse  : {}   ,  nrmse : {}'.format(value_g_14[0], value_g_14[1]))
    print('psnr : {}   ,  ssim  : {}'.format(value_g_14[2], value_g_14[3]))
    logger_val.info('epoch:{}'.format(epoch))
    logger_val.info('the eval of image :{}'.format(image_name))
    logger_val.info('the gt compare with w1 :')
    logger_val.info('mse  : {}   ,  nrmse : {}'.format(value_g[0], value_g[1]))
    logger_val.info('psnr : {}   ,  ssim  : {}'.format(value_g[2], value_g[3]))
    logger_val.info('the gt compare with w2 :')
    logger_val.info('mse  : {}   ,  nrmse : {}'.format(value_g_13[0], value_g_13[1]))
    logger_val.info('psnr : {}   ,  ssim  : {}'.format(value_g_13[2], value_g_13[3]))
    logger_val.info('the gt compare with fusion :')
    logger_val.info('mse  : {}   ,  nrmse : {}'.format(value_g_14[0], value_g_14[1]))
    logger_val.info('psnr : {}   ,  ssim  : {}'.format(value_g_14[2], value_g_14[3]))
    return value_g_14[3]
parser = argparse.ArgumentParser(description='')
parser.add_argument('--epoch', dest='epoch', default='test', help='evaluate which epoch')
args = parser.parse_args()

if __name__ == '__main__':
    if args.epoch != 'test':
        val_dataset_name = ['base_super/sample_super/']#,'base_haze/sample_base_ssim_l1_1000/']
        evaluate_val(dataset_name=val_dataset_name,epoch=args.epoch)
    else:
        test_dataset_name =['base_super/test_super/']
        evaluate_test(dataset_name=test_dataset_name,epoch=args.epoch)