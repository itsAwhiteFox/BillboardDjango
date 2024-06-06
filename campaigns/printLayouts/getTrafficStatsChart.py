import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg (non-interactive)

import matplotlib.pyplot as plt
from io import BytesIO

def create_bar_chart(data, categories):
    plt.figure(figsize=(11,6))
    plt.bar(categories, data, edgecolor='none', linewidth=0)    
    
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    plt.close()
    img_bytes.seek(0)
    return img_bytes


def getTrafficStatsChartsImage(pdfDocument, data):
    
    pdfDocument.set_font('Arial', '', 9)
    
    data1 = [30, 30, 40, 10, 20, 40, 20, 30, 50, 10, 30, 20, 30, 40, 50, 20, 30, 50, 10, 30, 20, 30, 40, 50]
    labels = ["Label1", "Label2", "Label3", "Label4", "Label5", "Label6", "Label7", "Label8", "Label9", "Label10", "Label11", "Label12", "Label13", "Label14", "Label15", "Label16", "Label17", "Label18", "Label19", "Label20", "Label21", "Label22", "Label23", "Label24" ]
    

    img_bytes = create_bar_chart(data1, labels)
    pdfDocument.image(img_bytes, x=370, y=390, w=500, h=180)

    
    
    
