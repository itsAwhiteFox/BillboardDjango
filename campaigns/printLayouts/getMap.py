import urllib.parse

def getMapImage(pdfDocument, data):
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    params = {
        "center": f"{28.550488},{77.272764}",
        "zoom": 12,
        "size": "800x400",
        "markers": f"{28.550488},{77.272764}",
        "key": "AIzaSyAmnjoE7eFekledKAqF8ctrMoNBk3w0Xm8"
    }

    url = base_url + urllib.parse.urlencode(params)

    pdfDocument.image(url, x=20, y=390, w=350, h=180)

