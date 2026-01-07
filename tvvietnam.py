import xbmcgui
import xbmcplugin
import sys
import urllib.request
import re
import json
import urllib.parse

HANDLE = int(sys.argv[1])
# LINK FILE DATA.JSON CỦA BẠN
DATA_URL = "https://raw.githubusercontent.com/thung65/Iptv-vietnam/refs/heads/main/data.json"

def get_content(url, color):
    xbmcplugin.setContent(HANDLE, 'videos')
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
        
        # Regex bóc tách kênh từ file M3U
        matches = re.findall(r'#EXTINF:.*?(?:tvg-logo="(.*?)")?.*?,(.*?)\n(http.*?)$', content, re.MULTILINE)
        for logo, name, link in matches:
            li = xbmcgui.ListItem(label=f"[COLOR {color}]{name.strip()}[/COLOR]")
            img = logo if (logo and logo.startswith('http')) else "DefaultVideo.png"
            li.setArt({'icon': img, 'thumb': img, 'poster': img})
            li.setInfo('video', {'title': name.strip()})
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(HANDLE, link.strip(), li, False)
    except:
        xbmcgui.Dialog().notification("Lỗi", "Không thể nạp danh sách kênh")

def build_menu():
    xbmcplugin.setContent(HANDLE, 'folders')
    try:
        # Tải file data.json để dựng Menu chính
        req = urllib.request.Request(DATA_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        for item in data:
            # Tạo label theo màu và thêm chú thích (như mục FPT)
            label = f"[B][COLOR {item['color']}]{item['name']}[/COLOR][/B]"
            if 'note' in item:
                label += f" [COLOR red]{item['note']}[/COLOR]"
                
            li = xbmcgui.ListItem(label=label)
            li.setArt({'icon': item['icon'], 'thumb': item['icon']})
            
            # Đóng gói tham số gửi vào URL điều hướng
            query = urllib.parse.urlencode({'url': item['url'], 'color': item['color']})
            path = f"{sys.argv[0]}?{query}"
            xbmcplugin.addDirectoryItem(HANDLE, path, li, True)
    except:
        xbmcgui.Dialog().ok("Lỗi kết nối", "Kiểm tra lại link file data.json trên GitHub")

# Xử lý tham số từ Kodi
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
if not params:
    build_menu()
else:
    get_content(params.get('url'), params.get('color'))

xbmcplugin.endOfDirectory(HANDLE)

