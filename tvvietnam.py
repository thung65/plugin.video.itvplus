import sys
import re
import urllib.request
import xbmcgui
import xbmcplugin
import xbmc
import ssl

# Link danh sách của bạn
M3U_URL = "https://raw.githubusercontent.com/thung65/Iptv-vietnam/refs/heads/main/fpt"

def get_m3u_data():
    try:
        context = ssl._create_unverified_context()
        req = urllib.request.Request(M3U_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=context) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        xbmc.log(f"Loi tai du lieu: {str(e)}", xbmc.LOGERROR)
        return ""

def list_channels():
    handle = int(sys.argv[1])
    data = get_m3u_data()
    
    # Regex này sẽ lấy: Logo, Tên kênh và Link phát
    # Hỗ trợ cấu trúc: #EXTINF:-1 tvg-logo="link_anh",Tên Kênh
    matches = re.findall(r'#EXTINF:.*?(?:tvg-logo="(.*?)")?.*?,(.*?)\n(http.*)', data)
    
    for logo, name, url in matches:
        name = name.strip()
        url = url.strip()
        logo = logo.strip() if logo else ""
        
        # Tạo đối tượng Item
        list_item = xbmcgui.ListItem(label=name)
        
        # Cấu hình để Kodi hiểu đây là Video và tự động mở trình phát
        list_item.setInfo('video', {'title': name, 'mediatype': 'video'})
        
        # Thêm Logo nếu có trong link GitHub
        if logo:
            list_item.setArt({'thumb': logo, 'icon': logo})
        
        # QUAN TRỌNG: Cấu hình để bấm là phát ngay (IsPlayable = true)
        list_item.setProperty('IsPlayable', 'true')
        
        # Đưa vào danh sách (isFolder=False nghĩa là không vào thư mục con nữa)
        xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=list_item, isFolder=False)
        
    xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    list_channels()
