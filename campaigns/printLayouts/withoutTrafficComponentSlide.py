from .getImages import getSiteImage
from .getTable import getTable

def printSlideWOTrafficData(pdfDocument, siteData):
    print(siteData, "printSlideWOTrafficData")
    pdfDocument.set_font('Arial', '', 18)
    pdfDocument.cell(500, 20, f"Site ID:   {siteData["siteDetail"]["location"]}")
    getSiteImage(pdfDocument, siteData["siteImage"])
    getTable(pdfDocument, siteData["siteDetail"], siteData["sitePricing"])

    #pdfDocument.multi_cell(200, 20, siteData["siteDetail"]["siteTag"], fill=True)
        
    