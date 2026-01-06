import sys, re, urllib.request, xbmcgui, xbmcplugin, xbmc, ssl

# Link nguồn từ GitHub của thung65
M3U_URL = "https://raw.githubusercontent.com/thung65/Iptv-vietnam/refs/heads/main/fpt"

def list_channels():
    handle = int(sys.argv[1])
    try:
        # Bỏ qua lỗi SSL trên Android 10
        context = ssl._create_unverified_context()
        req = urllib.request.Request(M3U_URL, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, context=context)
        data = response.read().decode('utf-8')
        
        # Tìm logo, tên kênh và link
        matches = re.findall(r'#EXTINF:.*?(?:tvg-logo="(.*?)")?.*?,(.*?)\n(http.*)', data)
        
        for logo, name, url in matches:
            name = name.strip()
            url = url.strip()
            
            list_item = xbmcgui.ListItem(label=name)
            list_item.setInfo('video', {'title': name, 'mediatype': 'video'})
            
            if logo:
                list_item.setArt({'thumb': logo.strip(), 'icon': logo.strip()})
            
            # Cài đặt để bấm là phát ngay
            list_item.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=list_item, isFolder=False)
            
    except Exception as e:
        xbmc.log(f"Loi tai list: {str(e)}", xbmc.LOGERROR)
        
    xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    list_channels()
