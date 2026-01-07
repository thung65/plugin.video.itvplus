import xbmcgui
import xbmcplugin
import sys
import urllib.request
import re

# Lấy handle của addon
HANDLE = int(sys.argv[1])

# --- DANH SÁCH MỤC (Thêm thoải mái vào đây) ---
# Thứ tự: "Tên": ["Link M3U", "Link Ảnh", "Màu chữ"]
MENU_DATA = [
    ["TỔNG HỢP - ALL", "https://raw.githubusercontent.com/thung65/Iptv-vietnam/refs/heads/main/ducnt123", "https://raw.githubusercontent.com/thung65/Iptv-vietnam/refs/heads/main/tv.png", "orange"],
    ["FPT IPTV (Chỉ mạng FPT)", "https://raw.githubusercontent.com/thung65/Iptv-vietnam/refs/heads/main/fpt", "https://raw.githubusercontent.com/thung65/Iptv-vietnam/refs/heads/main/fpt.png", "lightblue"],
    # Bạn có thể copy dòng dưới để thêm 100 mục phim nữa nếu muốn
    ["KHO PHIM HÀNH ĐỘNG", "https://link-m3u-phim-le", "https://raw.githubusercontent.com/thung65/Iptv-vietnam/refs/heads/main/tv.png", "yellow"],
    ["RADIO - INTERNATIONAL", "https://raw.githubusercontent.com/luongtamlong/DAKLAK_RADIO/refs/heads/main/RadioVietNam.m3u", "https://raw.githubusercontent.com/thung65/Iptv-vietnam/refs/heads/main/radio.png", "lightgreen"]
]

def get_content(url, color):
    xbmcplugin.setContent(HANDLE, 'videos')
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
        
        matches = re.findall(r'#EXTINF:.*?(?:tvg-logo="(.*?)")?.*?,(.*?)\n(http.*?)$', content, re.MULTILINE)
        for logo, name, link in matches:
            li = xbmcgui.ListItem(label=f"[COLOR {color}]{name.strip()}[/COLOR]")
            img = logo if (logo and logo.startswith('http')) else "DefaultVideo.png"
            li.setArt({'icon': img, 'thumb': img})
            li.setInfo('video', {'title': name.strip()})
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(HANDLE, link.strip(), li, False)
    except:
        xbmcgui.Dialog().notification("Lỗi", "Không tải được danh sách", xbmcgui.NOTIFICATION_ERROR)

def build_menu():
    xbmcplugin.setContent(HANDLE, 'folders')
    for name, url_m3u, icon, color in MENU_DATA:
        li = xbmcgui.ListItem(label=f"[B][COLOR {color}]{name}[/COLOR][/B]")
        li.setArt({'icon': icon, 'thumb': icon})
        # Tạo link điều hướng trong addon
        path = f"{sys.argv[0]}?url={url_m3u}&color={color}"
        xbmcplugin.addDirectoryItem(HANDLE, path, li, True)

# Xử lý tham số truyền vào
import urllib.parse
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))

if not params:
    build_menu()
else:
    get_content(params.get('url'), params.get('color'))

xbmcplugin.endOfDirectory(HANDLE)
