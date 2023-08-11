# -*- coding: utf-8 -*-
# Author : xy_cloud
import webview
from prettytable import PrettyTable

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
    """
    shtml += f'<tr><td>{_("icon")}</td><td>{_("title")}</td><td>{_("filename")}</td><td>{_("client")}</td><td>{_("server")}</td></tr>\n'
    for i in modlist_view:
        img_url = i[1][3]
        if img_url == 'Unknown':
            img_url = 'https://www.minecraft.net/etc.clientlibs/minecraft/clientlibs/main/resources/favicon.ico'
        client = i[1][1]
        server = i[1][2]
        mod_dict = {'required': _('需装'), 'optional': _('可选'), 'unsupported': _('无效'), 'Unknown': _('未知')}
        client = _('client ') + mod_dict[client]
        server = _('server ') + mod_dict[server]

        shtml += f'<tr><td><img src="{img_url}" alt="{i[1][0]}" height=50px width=50px></img></td><td>{i[1][0]}</td><td>{i[0]}</td><td>{client}</td><td>{server}</td></tr>\n'

    shtml += """
            </table>
        </body>
        </html>
    """
    webview.create_window('Mod Filter', html=shtml)
    webview.start()


def start_cli(modlist_view):
    table = PrettyTable([_('title'), _('path'), _('client'), _('server')])
    for i in modlist_view:
        img_url = i[1][3]
        if img_url == 'Unknown':
            img_url = 'https://www.minecraft.net/etc.clientlibs/minecraft/clientlibs/main/resources/favicon.ico'
        client = i[1][1]
        server = i[1][2]
        mod_dict = {'required': _('required'), 'optional': _('optional'), 'unsupported': _('unsupported'),
                    'Unknown': _('unknown')}
        client = _('client ') + mod_dict[client]
        server = _('server ') + mod_dict[server]
        table.add_row([i[1][0], i[0], client, server])
    print(table)
