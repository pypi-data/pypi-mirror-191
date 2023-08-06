'''
Date         : 2023-01-24 11:31:55
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-01-24 11:37:30
LastEditors  : BDFD
Description  : 
FilePath     : \WES_Calculation\ref_func\common_func.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''
import base64

def data_conv(data):
    if data == '':
        data = None
    else:
        data = float(data)
    return data


def data_conv_int(data):
    if data == '':
        data = None
    else:
        data = int(data)*1000
    return data

def return_img_stream(img_local_path):
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream