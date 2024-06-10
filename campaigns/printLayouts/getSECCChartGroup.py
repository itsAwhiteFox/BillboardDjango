import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg (non-interactive)

import matplotlib.pyplot as plt
from io import BytesIO

def create_pie_chart(data, colors, size):
    if size == "normal":
        plt.figure(figsize=(3,3))
    else:
        plt.figure(figsize=(4,3))
    plt.pie(data, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    plt.close()
    img_bytes.seek(0)
    return img_bytes


def getSECCChartsImage(pdfDocument, data, size = "normal"):
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
    
    print(data, "getSECCChartsImage")

    seccDataMap = {"No_HH":{}, "P_LIT":{}, "TOT_WORK_P":{}}
    labels = []
    for item in data:
        seccDataMap["No_HH"] = {**seccDataMap["No_HH"], item["SubDistrict"]:item["No_HH"]}
        seccDataMap["P_LIT"] = {**seccDataMap["P_LIT"], item["SubDistrict"]:item["P_LIT"]}
        seccDataMap["TOT_WORK_P"] = {**seccDataMap["TOT_WORK_P"], item["SubDistrict"]:item["TOT_WORK_P"]}
        if item["SubDistrict"] not in labels:
            labels.append(item["SubDistrict"])

    
    colorsPassed = colors[0:len(labels)]

    img_bytes_house_hold = create_pie_chart(seccDataMap["No_HH"].values(), colorsPassed, size)
    img_bytes_literate_persons = create_pie_chart(seccDataMap["P_LIT"].values(), colorsPassed, size)
    img_bytes_working_person = create_pie_chart(seccDataMap["TOT_WORK_P"].values(), colorsPassed, size)
    if size == "normal":
        pdfDocument.image(img_bytes_house_hold, x=20, y=210, w=170, h=150)
        pdfDocument.set_xy(20+60, 350)
        pdfDocument.cell(50,10,"Household")
        pdfDocument.image(img_bytes_literate_persons, x=190, y=210, w=170, h=150)
        pdfDocument.set_xy(190+60, 350)
        pdfDocument.cell(50,10,"Literate")
        pdfDocument.image(img_bytes_working_person, x=360, y=210, w=170, h=150)    
        pdfDocument.set_xy(360+60, 350)
        pdfDocument.cell(50,10,"Working")
        pdfDocument.set_xy((520-len(labels)*60)/2, 360)

    if size == "full":
        pdfDocument.image(img_bytes_house_hold, x=20, y=210, w=250, h=150)
        pdfDocument.image(img_bytes_literate_persons, x=270, y=210, w=250, h=150)
        pdfDocument.image(img_bytes_working_person, x=520, y=210, w=250, h=150)    
        pdfDocument.set_xy((750-len(labels)*60)/2, 360)
    
    for index, item in enumerate(labels):
        pdfDocument.set_fill_color(colorsPassed[index])
        pdfDocument.cell(10, 10, "", fill=True)
        pdfDocument.cell(70, 10, item)
    