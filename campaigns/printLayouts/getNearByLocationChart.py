import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg (non-interactive)

import matplotlib.pyplot as plt
from io import BytesIO

def create_bar_chart(data, categories, colors):
    plt.figure(figsize=(11,6))
    bars = plt.barh(categories, data,color=colors, edgecolor='none', linewidth=0)    
    plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    for bar, value in zip(bars, data):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{value}', ha='left', va='center', fontsize=21)

    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    plt.close()
    img_bytes.seek(0)
    return img_bytes


def getNearbyPOIChartsImage(pdfDocument, data):
    print(data, "getNearbyPOIChartsImage")
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
    
    nearByPlacesMap = {}

    for item in data:
        if item["type"] in nearByPlacesMap:
            nearByPlacesMap[item["type"]] = nearByPlacesMap[item["type"]]+1
        else:
            nearByPlacesMap[item["type"]] = 1

    data1 = list(nearByPlacesMap.values())
    labels = list(nearByPlacesMap.keys())
    colorsPassed = colors[0:len(data1)]

    img_bytes = create_bar_chart(data1, labels, colorsPassed)
    pdfDocument.image(img_bytes, x=530, y=210, w=200, h=150)

    
    for index, item in enumerate(labels):
        pdfDocument.set_xy(730, 250 + index*15)
        pdfDocument.set_fill_color(colorsPassed[index])
        pdfDocument.cell(10, 10, "", fill=True)
        pdfDocument.cell(90, 10, item)

    
    
    