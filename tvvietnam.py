import xbmcgui
import xbmcplugin
import sys
import urllib.request
import re

# --- CẤU HÌNH LINK ẢNH TỪ GITHUB ---
ICON_TV = "https://raw.githubusercontent.com/thung65/Iptv-vietnam/refs/heads/main/tv.png"
ICON_FPT = "https://raw.githubusercontent.com/thung65/Iptv-vietnam/refs/heads/main/fpt.png"
ICON_RADIO = "https://raw.githubusercontent.com/thung65/Iptv-vietnam/refs/heads/main/radio.png"

# --- NGUỒN DỮ LIỆU ---
SOURCES = {
    "ALL": "https://raw.githubusercontent.com/thung65/Iptv-vietnam/refs/heads/main/ducnt123",
    "FPT": "https://raw.githubusercontent.com/thung65/Iptv-vietnam/refs/heads/main/fpt",
    "RADIO": "https://raw.githubusercontent.com/luongtamlong/DAKLAK_RADIO/refs/heads/main/RadioVietNam.m3u"
}

handle = int(sys.argv[1])

def get_content(url):
    xbmcplugin.setContent(handle, 'videos')
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        content = urllib.request.urlopen(req).read().decode('utf-8')
        matches = re.findall(r'#EXTINF:.*?(?:tvg-logo="(.*?)")?.*?,(.*?)\n(http.*?)$', content, re.MULTILINE)
        
        for logo, name, link in matches:
            li = xbmcgui.ListItem(label="[B]" + name.strip() + "[/B]")
            img = logo if logo else "DefaultVideo.png"
            li.setArt({'icon': img, 'thumb': img})
            li.setInfo('video', {'title': name.strip()})
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle=handle, url=link.strip(), listitem=li, isFolder=False)
    except:
        xbmcgui.Dialog().notification("Lỗi", "Không thể tải danh sách kênh", xbmcgui.NOTIFICATION_ERROR)

def build_menu():
    xbmcplugin.setContent(handle, 'files')

    # 1. Kênh tổng hợp (Mục All luôn ở đầu)
    item_all = xbmcgui.ListItem(label="[B][COLOR orange]Kênh tổng hợp[/COLOR][/B]")
    item_all.setArt({'icon': ICON_TV, 'thumb': ICON_TV})
    xbmcplugin.addDirectoryItem(handle, sys.argv[0] + "?mode=all", item_all, True)

    # 2. Kênh truyền hình FPT (Kèm cảnh báo mạng FPT)
    label_fpt = "[B][COLOR lightblue]Kênh truyền hình FPT[/COLOR] [COLOR red](Chỉ dùng cho mạng FPT)[/COLOR][/B]"
    item_fpt = xbmcgui.ListItem(label=label_fpt)
    item_fpt.setArt({'icon': ICON_FPT, 'thumb': ICON_FPT})
    xbmcplugin.addDirectoryItem(handle, sys.argv[0] + "?mode=fpt", item_fpt, True)

    # 3. Radio_FM (Mục International đặt ở cuối)
    item_radio = xbmcgui.ListItem(label="[B][COLOR lightgreen]Radio_FM[/COLOR][/B]")
    item_radio.setArt({'icon': ICON_RADIO, 'thumb': ICON_RADIO})
    xbmcplugin.addDirectoryItem(handle, sys.argv[0] + "?mode=radio", item_radio, True)

# ĐIỀU HƯỚNG
params = sys.argv[2]
if not params:
    build_menu()
else:
    if "?mode=all" in params: get_content(SOURCES["ALL"])
    if "?mode=fpt" in params: get_content(SOURCES["FPT"])
    if "?mode=radio" in params: get_content(SOURCES["RADIO"])

xbmcplugin.endOfDirectory(handle)
