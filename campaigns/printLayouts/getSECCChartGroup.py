import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg (non-interactive)

import matplotlib.pyplot as plt
from io import BytesIO

def create_pie_chart(data, colors):
    plt.figure(figsize=(3,3))
    plt.pie(data, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    plt.close()
    img_bytes.seek(0)
    return img_bytes


def getSECCChartsImage(pdfDocument, data):
    pdfDocument.set_font('Arial', '', 9)
    colors = [
    "#f0f0f0",  # Light Gray
    "#add8e6",  # Light Blue
    "#90ee90",  # Light Green
    "#ffffe0",  # Light Yellow
    "#ffdab9",  # Light Orange
    "#ffb6c1",  # Light Pink
    "#e6e6fa",  # Light Purple
    "#ffcccb",  # Light Red
    "#d2b48c",  # Light Brown
    "#e0ffff"   # Light Cyan
    ]
    
    data1 = [30, 30, 40]
    labels = ["Label Passed 1", "Label Passed 2", "Label Passed 3"]
    colorsPassed = colors[0:len(data1)]

    img_bytes = create_pie_chart(data1, colorsPassed)
    pdfDocument.image(img_bytes, x=20, y=210, w=170, h=150)
    pdfDocument.image(img_bytes, x=190, y=210, w=170, h=150)
    pdfDocument.image(img_bytes, x=360, y=210, w=170, h=150)
    
    pdfDocument.set_xy((520-len(data1)*60)/2, 360)
    for index, item in enumerate(labels):
        pdfDocument.set_fill_color(colorsPassed[index])
        pdfDocument.cell(10, 10, "", fill=True)
        pdfDocument.cell(70, 10, item)
    