# -*- coding: utf-8 -*-
# Author : xy_cloud
import concurrent.futures
import os
import yaml
import api.mod
import api.modrinth
import api.view
from tkinter import filedialog
from tqdm import tqdm

mods_path = filedialog.askdirectory(initialdir=os.getcwd())+'/'
with open('config/config.yml') as f:
    cfg = yaml.safe_load(f.read())
modlist = os.listdir(mods_path)
modlist_view = {}
modinfolist = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    to_do = []
    for i in modlist:
        future = executor.submit(api.mod.read_modinfo, mods_path + i)
        to_do.append(future)
    for future in tqdm(concurrent.futures.as_completed(to_do)):
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
    for future in tqdm(concurrent.futures.as_completed(to_do)):
        projinfo = future.result()
        if projinfo == 'ERROR':
            modlist_view[opi[future]['localpath']].extend(['Unknown', 'Unknown', 'Unknown'])
        else:
            modlist_view[opi[future]['localpath']].extend(
                [projinfo['client_side'], projinfo['server_side'], projinfo['icon_url']])
api.view.start_view(sorted(list(modlist_view.items()), key=lambda x: x[0]))
