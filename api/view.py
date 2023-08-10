# -*- coding: utf-8 -*-
# Author : xy_cloud
import webview


def start_view(modlist_view):
    shtml = """
        <html>
        <head>
            <style>
                table {
                    border-collapse: collapse;
                    width: 100%;
                }
                th, td {
                    border: 1px solid black;
                    padding: 10px;
                    text-align: left;
                }
                tr:hover {
                    background-color: #f5f5f5;
                }
            </style>
        </head>
        <body>
            <table id="table">
            <tr><td>图标</td><td>名称</td><td>文件名</td><td>客户端</td><td>服务端</td></tr>
    """
    for i in modlist_view:
        img_url = i[1][3]
        if img_url=='Unknown':
            img_url='https://www.minecraft.net/etc.clientlibs/minecraft/clientlibs/main/resources/favicon.ico'
        client=i[1][1]
        server=i[1][2]
        mod_dict={'required':'需装','optional':'可选','unsupported':'无效','Unknown':'未知'}
        client='客户端'+mod_dict[client]
        server='服务端'+mod_dict[server]


        shtml += f'<tr><td><img src="{img_url}" alt="{i[1][0]}" height=50px width=50px></img></td><td>{i[1][0]}</td><td>{i[0]}</td><td>{client}</td><td>{server}</td></tr>'

    shtml += """
            </table>
        </body>
        </html>
    """
    webview.create_window('Mod Filter', html=shtml)
    webview.start()
