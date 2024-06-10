import urllib.parse

def getMapImage(pdfDocument, data, size = "normal"):
    print(data, "getMapImage")
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"

    if size == "normal":
        params = {
            "center": f"{data["site_lat"]},{data["site_long"]}",
            "zoom": 12,
            "size": "300x180",
            "markers": f"{data["site_lat"]},{data["site_long"]}",
            "key": "AIzaSyAmnjoE7eFekledKAqF8ctrMoNBk3w0Xm8"
        }

        url = base_url + urllib.parse.urlencode(params)

        pdfDocument.image(url, x=20, y=390, w=300, h=180)
    
    if size == "full":
        params = {
            "center": f"{data["site_lat"]},{data["site_long"]}",
            "zoom": 12,
            "size": "720x180",
            "markers": f"{data["site_lat"]},{data["site_long"]}",
            "key": "AIzaSyAmnjoE7eFekledKAqF8ctrMoNBk3w0Xm8"
        }

        url = base_url + urllib.parse.urlencode(params)

        pdfDocument.image(url, x=20, y=390, w=720, h=180)

