import os
from django.conf import settings

def getSiteImage(pdfDocument, data):
    if(data):
        image_path = os.path.join(settings.STATIC_ROOT, 'ppt_images', data["path"].split("\\")[-1])
        print(image_path, "getSiteImage")
        try:
            if os.path.exists(image_path):
                pdfDocument.image(image_path, x=20, y=50, w=250, h=160)
                
                print(image_path, "getSiteImage")
            else:
                print(f"Image file not found: {image_path}")
        except Exception as e:
            print(f"Error embedding image: {e}")
    