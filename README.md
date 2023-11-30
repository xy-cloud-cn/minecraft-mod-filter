<p align="center">
    <img src="./icon.png">
</p>

<h1 align="center">Minecraft mod filter</h1>
<p align="center">English | <a href="https://github.com/xy-cloud-cn/minecraft-mod-filter/blob/master/README_zh-hans.md">简体中文</a></p>

Quickly filter the minecraft modpack to see if any of its mods are client-side/server-side.
## Features
👻 Quickly scans your mods and tells you their server/client compatibility.  
💎 Support for cli and gui, default is cli  
🎃 i18n support
## Todo
✨ Support Java reflection to read @mod annotations  
✨ Faster file processing with rust  
✨ ~~Add a CLI for terminal users~~  
✨ Auto-generate server modpack (including auto-installation of modloader cores, etc.)  
✨ Make a server-side launcher  
✨ Make a server-side launcher-cli  
✨ Optimize the UI  
✨ Debug  
✨ ~~i18n support~~  
✨ Make a terminal UI using curses  
## Known issues
Currently, I've only tested forge version 1.12, I hope you can help me test other mod loaders and other versions.
## How to use
### For Developer
    pip install -r requirements.txt
    python main.py

args:-h,--gui,[-l/--locate]  
Recommended to use python 3.10
### For customer
https://github.com/xy-cloud-cn/minecraft-mod-filter/releases
### You are welcome to pull requests to help me finish Todo or fix bugs.
##### If you like this project, please give me a free star⭐!

Powered by python and ❤️

``Poor English, you can translate the Chinese readme for yourself``
