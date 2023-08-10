# -*- coding: utf-8 -*-
# Author : xy_cloud
import time

import requests
import json
import api.exception
from fuzzywuzzy import fuzz


class ModrinthAPI(object):
    def __init__(self, version):
        self.api_url = 'https://api.modrinth.com/v2/'
        self.UA = r'User-Agent: xy-cloud-cn/minecraft-mod-filter/' + version

    def search(self, keyword):
        try:
            temp = json.loads(requests.get(self.api_url + 'search?query=' + keyword).text)['hits'][0]
        except json.decoder.JSONDecodeError:
            return 'ERROR'
        except IndexError:
            return 'ERROR'
        except requests.exceptions.ConnectionError:
            time.sleep(5)
            try:
                temp = json.loads(requests.get(self.api_url + 'search?query=' + keyword).text)['hits'][0]
            except json.decoder.JSONDecodeError:
                return 'ERROR'
            except requests.exceptions.ConnectionError:
                time.sleep(10)
                try:
                    temp = json.loads(requests.get(self.api_url + 'search?query=' + keyword).text)['hits'][0]
                except json.decoder.JSONDecodeError:
                    return 'ERROR'
                except requests.exceptions.ConnectionError:
                    time.sleep(15)
                    try:
                        temp = json.loads(requests.get(self.api_url + 'search?query=' + keyword).text)['hits'][0]
                    except json.decoder.JSONDecodeError:
                        return 'ERROR'
                    except requests.exceptions.ConnectionError:
                        time.sleep(20)
                        try:
                            temp = json.loads(requests.get(self.api_url + 'search?query=' + keyword).text)['hits'][0]
                        except json.decoder.JSONDecodeError:
                            return 'ERROR'
                        except requests.exceptions.ConnectionError as e:
                            api.exception.throw(e, '服务器断开了连接，请过一会再试')
                            return 'ERROR'
        if fuzz.ratio(temp['title'].lower().replace(' ', ''), keyword.lower().replace(' ', '')) >= 70:
            return temp
        else:
            return 'ERROR'

    def project(self, modid):
        try:
            temp = json.loads(requests.get(self.api_url + 'project/' + modid).text)
        except json.decoder.JSONDecodeError:
            return 'ERROR'
        except requests.exceptions.ConnectionError:
            time.sleep(5)
            try:
                temp = json.loads(requests.get(self.api_url + 'project/' + modid).text)
            except json.decoder.JSONDecodeError:
                return 'ERROR'
            except requests.exceptions.ConnectionError:
                time.sleep(10)
                try:
                    temp = json.loads(requests.get(self.api_url + 'project/' + modid).text)
                except json.decoder.JSONDecodeError:
                    return 'ERROR'
                except requests.exceptions.ConnectionError:
                    time.sleep(15)
                    try:
                        temp = json.loads(requests.get(self.api_url + 'project/' + modid).text)
                    except json.decoder.JSONDecodeError:
                        return 'ERROR'
                    except requests.exceptions.ConnectionError:
                        time.sleep(20)
                        try:
                            temp = json.loads(requests.get(self.api_url + 'project/' + modid).text)
                        except json.decoder.JSONDecodeError:
                            return 'ERROR'
                        except requests.exceptions.ConnectionError as e:
                            api.exception.throw(e, '服务器断开了连接，请过一会再试')
                            return 'ERROR'
        if fuzz.ratio(temp['slug'].lower(),modid.lower()) >= 70:
            return temp
        else:
            return 'ERROR'

    def find_mod(self, keyword, modid):
        project_result = self.project(modid)
        if project_result == 'ERROR':
            search_result = self.search(keyword)
            if search_result == 'ERROR':
                return 'ERROR'
            else:
                return search_result
        else:
            return project_result
