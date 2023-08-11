# -*- coding: utf-8 -*-
# Author : xy_cloud
import concurrent.futures
import os
import shutil
import argparse
import yaml
import api.mod
import api.modrinth
import api.view
from tkinter import filedialog
from tqdm import tqdm
import gettext

print(r''' __       __ __                                               ______    __          __       __                __      ________ __ __   __
|  \     /  \  \                                             /      \  |  \        |  \     /  \              |  \    |        \  \  \ |  \
| ▓▓\   /  ▓▓\▓▓_______   ______   _______  ______   ______ |  ▓▓▓▓▓▓\_| ▓▓_       | ▓▓\   /  ▓▓ ______   ____| ▓▓    | ▓▓▓▓▓▓▓▓\▓▓ ▓▓_| ▓▓_    ______   ______
| ▓▓▓\ /  ▓▓▓  \       \ /      \ /       \/      \ |      \| ▓▓_  \▓▓   ▓▓ \      | ▓▓▓\ /  ▓▓▓/      \ /      ▓▓    | ▓▓__   |  \ ▓▓   ▓▓ \  /      \ /      \
| ▓▓▓▓\  ▓▓▓▓ ▓▓ ▓▓▓▓▓▓▓\  ▓▓▓▓▓▓\  ▓▓▓▓▓▓▓  ▓▓▓▓▓▓\ \▓▓▓▓▓▓\ ▓▓ \    \▓▓▓▓▓▓      | ▓▓▓▓\  ▓▓▓▓  ▓▓▓▓▓▓\  ▓▓▓▓▓▓▓    | ▓▓  \  | ▓▓ ▓▓\▓▓▓▓▓▓ |  ▓▓▓▓▓▓\  ▓▓▓▓▓▓\
| ▓▓\▓▓ ▓▓ ▓▓ ▓▓ ▓▓  | ▓▓ ▓▓    ▓▓ ▓▓     | ▓▓   \▓▓/      ▓▓ ▓▓▓▓     | ▓▓ __     | ▓▓\▓▓ ▓▓ ▓▓ ▓▓  | ▓▓ ▓▓  | ▓▓    | ▓▓▓▓▓  | ▓▓ ▓▓ | ▓▓ __| ▓▓    ▓▓ ▓▓   \▓▓
| ▓▓ \▓▓▓| ▓▓ ▓▓ ▓▓  | ▓▓ ▓▓▓▓▓▓▓▓ ▓▓_____| ▓▓     |  ▓▓▓▓▓▓▓ ▓▓       | ▓▓|  \    | ▓▓ \▓▓▓| ▓▓ ▓▓__/ ▓▓ ▓▓__| ▓▓    | ▓▓     | ▓▓ ▓▓ | ▓▓|  \ ▓▓▓▓▓▓▓▓ ▓▓
| ▓▓  \▓ | ▓▓ ▓▓ ▓▓  | ▓▓\▓▓     \\▓▓     \ ▓▓      \▓▓    ▓▓ ▓▓        \▓▓  ▓▓    | ▓▓  \▓ | ▓▓\▓▓    ▓▓\▓▓    ▓▓    | ▓▓     | ▓▓ ▓▓  \▓▓  ▓▓\▓▓     \ ▓▓
 \▓▓      \▓▓\▓▓\▓▓   \▓▓ \▓▓▓▓▓▓▓ \▓▓▓▓▓▓▓\▓▓       \▓▓▓▓▓▓▓\▓▓         \▓▓▓▓      \▓▓      \▓▓ \▓▓▓▓▓▓  \▓▓▓▓▓▓▓     \▓▓      \▓▓\▓▓   \▓▓▓▓  \▓▓▓▓▓▓▓\▓▓



''')



parser = argparse.ArgumentParser()
parser.add_argument('--gui', required=False, action='store_true', default=False, help='Use GUI')
parser.add_argument('-l', '--locate', type=str, choices=['zh-CN', 'en'], default='en', required=False,
                    help='Your language')
arg = parser.parse_args()

lang = gettext.translation('mcmodfilter', localedir='i18n', languages=[arg.locate],)
lang.install('mcmodfilter')
_ = lang.gettext

mods_path = filedialog.askdirectory(initialdir=os.getcwd()) + '/'
if os.path.samefile(mods_path, '/') or os.path.samefile(mods_path, os.getcwd()):
    exit(1)
with open('config/config.yml') as f:
    cfg = yaml.safe_load(f.read())
modlist = os.listdir(mods_path)
modlist_view = {}
modinfolist = []
output_path = 'temp/'
if os.path.exists(output_path):
    shutil.rmtree(output_path)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    to_do = []
    for i in modlist:
        future = executor.submit(api.mod.read_modinfo, mods_path + i, output_path)
        to_do.append(future)
    for future in tqdm(concurrent.futures.as_completed(to_do), total=len(modlist)):
        r = future.result()
        if not r[0] == 'ERROR':
            r[0]['localpath'] = r[1]
            modinfolist.append(r[0])
            modlist_view[r[1]] = [r[0]['name']]
        else:
            modlist_view[r[1]] = ['Unknown', 'Unknown', 'Unknown', 'Unknown']
modrinth_api = api.modrinth.ModrinthAPI(cfg['version'])
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    to_do = []
    opi = {}
    for i in modinfolist:
        future = executor.submit(modrinth_api.find_mod, i['name'], i['modid'])
        to_do.append(future)
        opi[future] = i
    for future in tqdm(concurrent.futures.as_completed(to_do), total=len(modinfolist)):
        projinfo = future.result()
        if projinfo == 'ERROR':
            modlist_view[opi[future]['localpath']].extend(['Unknown', 'Unknown', 'Unknown'])
        else:
            modlist_view[opi[future]['localpath']].extend(
                [projinfo['client_side'], projinfo['server_side'], projinfo['icon_url']])
if arg.gui:
    api.view.start_view(sorted(list(modlist_view.items()), key=lambda x: x[0]))
else:
    api.view.start_cli(sorted(list(modlist_view.items()), key=lambda x: x[0]))
