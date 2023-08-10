# -*- coding: utf-8 -*-
# Author : xy_cloud
import os
import shutil
import zipfile
import json
import api.exception


def read_modinfo(jar_path, output_path='temp/'):
    info = 'ERROR'
    try:
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        output_path += os.path.splitext(jar_path.split('/')[-1])[0] + '/'
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        zip_ref = zipfile.ZipFile(jar_path)
        zip_ref.extractall(output_path)
        tempname = '未找到mod配置文件'
        for i in os.listdir(output_path):
            if os.path.splitext(i)[1] == '.info':
                tempname = i
                break
        with open(output_path + tempname, 'r', encoding='utf-8') as f:
            file = f.read().replace('\n', '')
            try:
                info = json.loads(file)[0]
            except KeyError:
                info = json.loads(file)['modList'][0]
    except FileNotFoundError as e:
        api.exception.throw(e, ':未找到mod配置文件 ' + jar_path)
    except KeyError as e:
        api.exception.throw(e, ':未找到mod配置文件 ' + jar_path)
    finally:
        shutil.rmtree(output_path)
    return [info, os.path.splitext(jar_path.split('/')[-1])[0]]
