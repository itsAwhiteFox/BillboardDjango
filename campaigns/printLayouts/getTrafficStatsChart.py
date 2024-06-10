import matplotlib
import math 

matplotlib.use('Agg')  # Set the backend to Agg (non-interactive)

import matplotlib.pyplot as plt
from io import BytesIO

def create_bar_chart(data, categories, colors):
    print(data, "create_bar_chart")
    plt.figure(figsize=(11,6))
    bars = plt.bar(categories, data,color=colors, edgecolor='none', linewidth=0)    
    plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)    
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    index = 0
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, data[index], ha='center', va='bottom', fontsize=15)
        index=index+1

    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    plt.close()
    img_bytes.seek(0)
    return img_bytes


def getTrafficStatsChartsImage(pdfDocument, data):
    
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
    
    dataDetail = {"Monday":{
            "morningPeak":0,
            "noonHours":0,
            "eveningPeak":0,
            "nightHours":0
            }, 
            "Tuesday":{
                "morningPeak":0,
                "noonHours":0,
                "eveningPeak":0,
                "nightHours":0
            }, 
            "Wednesday": {
                "morningPeak":0,
                "noonHours":0,
                "eveningPeak":0,
                "nightHours":0
            },
            "Thursday":{
                "morningPeak":0,
                "noonHours":0,
                "eveningPeak":0,
                "nightHours":0
            }, 
            "Friday": {
                "morningPeak":0,
                "noonHours":0,
                "eveningPeak":0,
                "nightHours":0
            }, 
            "Saturday" : {
                "morningPeak":0,
                "noonHours":0,
                "eveningPeak":0,
                "nightHours":0
            }, 
            "Sunday":{
                "morningPeak":0,
                "noonHours":0,
                "eveningPeak":0,
                "nightHours":0
            }
        }


    for element in data:
        averageSpeed = (float(element["distance"])/1000)/(float(element["traffic_time"])/3600)
        completeTraffic = math.floor(((float(element["distance"])*7)/(3.5*2.5))*(float(element["distance"])/float(element["traffic_time"])))
        if averageSpeed < 10 :
            dataDetail[element["day"]][element["daySection"]] = math.floor((dataDetail[element["day"]][element["daySection"]] + completeTraffic*1.25 if element["daySection"] == "morningPeak" else dataDetail[element["day"]][element["daySection"]] + completeTraffic)*(0.65 if element["day"]=="Saturday" or element["day"]=="Sunday" else 1))
        elif averageSpeed >= 10 and averageSpeed < 20:
            dataDetail[element["day"]][element["daySection"]] = math.floor((dataDetail[element["day"]][element["daySection"]] + completeTraffic*0.8*1.25 if element["daySection"] == "morningPeak" else dataDetail[element["day"]][element["daySection"]] + completeTraffic*0.8)*(0.65 if element["day"]=="Saturday" or element["day"]=="Sunday" else 1))
        elif averageSpeed >= 20 and averageSpeed < 25:
            dataDetail[element["day"]][element["daySection"]] = math.floor((dataDetail[element["day"]][element["daySection"]] + completeTraffic*0.7*1.25 if element["daySection"] == "morningPeak" else dataDetail[element["day"]][element["daySection"]] + completeTraffic*0.7)*(0.65 if element["day"]=="Saturday" or element["day"]=="Sunday" else 1))    
        elif averageSpeed >= 25 and averageSpeed < 30:
            dataDetail[element["day"]][element["daySection"]] = math.floor((dataDetail[element["day"]][element["daySection"]] + completeTraffic*0.5*1.25 if element["daySection"] == "morningPeak" else dataDetail[element["day"]][element["daySection"]] + completeTraffic*0.5)*(0.65 if element["day"]=="Saturday" or element["day"]=="Sunday" else 1))
        elif averageSpeed >= 30 and averageSpeed < 40:
            dataDetail[element["day"]][element["daySection"]] = math.floor((dataDetail[element["day"]][element["daySection"]] + completeTraffic*0.3*1.25 if element["daySection"] == "morningPeak" else dataDetail[element["day"]][element["daySection"]] + completeTraffic*0.3)*(0.65 if element["day"]=="Saturday" or element["day"]=="Sunday" else 1))    
        elif averageSpeed >= 40:
            dataDetail[element["day"]][element["daySection"]] = math.floor((dataDetail[element["day"]][element["daySection"]] + completeTraffic*0.2*1.25 if element["daySection"] == "morningPeak" else dataDetail[element["day"]][element["daySection"]] + completeTraffic*0.2)*(0.65 if element["day"]=="Saturday" or element["day"]=="Sunday" else 1))    
                
    print(dataDetail, "getTrafficStatsChartsImage")
    i = 0
    for key, value in dataDetail.items():
        img_bytes = create_bar_chart(list(value.values()), list(value.keys()), colors[0:4])
        pdfDocument.image(img_bytes, x=310+i*70, y=390, w=70, h=180)
        i=i+1

    j=0
    
    for item in dataDetail.keys():
        pdfDocument.set_xy(310+j*70, y=400)
        pdfDocument.cell(70,10,item,0, 1, 'C')
        j=j+1
    
