from django.forms.models import model_to_dict
from django.db.models import Q
from io import BytesIO

from .allComponentsSlide import printSlideWithAllComponents
from .withoutNearbyPlacesSlide import printSlideWONearbyData
from .withoutTrafficComponentSlide import printSlideWOTrafficData
from .withoutAnyGoogleDataSlide import printPageWOAnyGoogleData

from sites.models import Site, SitePricing, SiteImages, GoogleStats, GoogleTrafficStats
from seccdata.models import SeccData

from fpdf import FPDF

class GetSiteData():
    def __init__(self, siteTag):
        self.siteTag = siteTag
        self.siteDetail = None
        self.siteImage = None
        self.sitePricing = None
        self.siteSECC = None
        self.nearByLocation = None
        self.trafficData = None
        self.siteSlideType = "woGoolgeData"

        self.getSiteData()
        self.getSiteImage()
        self.getSitePricing()
        self.getGoogleStats()
        self.getSECCData()  
        self.getTrafficData()
        self.getSlideType()

    def getSiteData(self):
        try:
            siteData = Site.objects.get(siteTag=self.siteTag)
            if siteData:
                self.siteDetail = model_to_dict(siteData)
        except:
            print("error")

    def getSiteImage(self):
        try:
            siteData = SiteImages.objects.filter(site=self.siteTag).last()
            print(siteData, self.siteTag, "getSiteImage")
            if siteData:
                self.siteImage = model_to_dict(siteData)
        except:
            print("error")
    
    def getSitePricing(self):
        try:
            siteData = SitePricing.objects.get(site=self.siteTag)
            if siteData:
                self.sitePricing = model_to_dict(siteData)
        except:
            print("error")

    def getGoogleStats(self):
        try:
            siteData = GoogleStats.objects.filter(grid=self.siteDetail["grid"])
            if siteData:
                self.nearByLocation = siteData.values()
                pass
        except:
            print("error")

    def getSECCData(self):
        try:
            subDistrictData = SeccData.objects.filter(Q(State=self.siteDetail["state"]) & Q(District=self.siteDetail["district"]))
            if subDistrictData:
                self.siteSECC = subDistrictData.values()
        except:
            print("error")

    def getTrafficData(self):
        try:
            siteData = GoogleTrafficStats.objects.filter(Q(site=self.siteTag))
            print(siteData, "getTrafficData")
            if siteData:
                self.trafficData = siteData.values()
        except:
            print("error")

    def getSlideType(self):
        if(self.nearByLocation and self.trafficData):
            self.siteSlideType = "allComponentSlide" 
        elif(not self.nearByLocation and self.trafficData):
            self.siteSlideType = "woNearbyPlaces" 
        elif(self.nearByLocation and not self.trafficData):
            self.siteSlideType = "woTrafficData"
        elif(not self.nearByLocation and not self.trafficData): 
            self.siteSlideType = "woGoolgeData"



class PDF(FPDF):

    def __init__(self, orientation='L', unit='pt', format='A4'):
        super().__init__(orientation, unit, format)
        self.set_margins(20, 30)

    def draw_table_from_dict(self, data, column_width=100, row_height=20, x_offset=0, y_offset=0):
        self.set_font('Arial', '', 16)
        i=0
        
        for key, item in data.items():
            if key != "assignedSites":
                print(key, item, "passedValues")
                self.set_xy(x_offset, y_offset+row_height*i)        
                self.cell(column_width, row_height, key)
                self.cell(column_width, row_height, item)
                self.ln(row_height)
                i=i+1
    
    def draw_site_page(self, data):
        self.set_font('Arial', '', 16)
        if data["slideType"] == "allComponentSlide":
            printSlideWithAllComponents(self, data)
        if data["slideType"] == "woNearbyPlaces":
            printSlideWONearbyData(self, data)
        if data["slideType"] == "woTrafficData":
            printSlideWOTrafficData(self, data)
        if data["slideType"] == "woGoolgeData":
            printPageWOAnyGoogleData(self, data)


    def draw_table_from_list(self, data, column_widths, row_height=20, x_offset=0, y_offset=0):
        self.set_font('Arial', 'B', 12)

        for row in data:
            for i, item in enumerate(row):
                self.cell(column_widths[i]+x_offset, row_height+y_offset, str(item), border=1)
            self.ln(row_height)


    
def printReportData(campaign):
    
    #get the sites inside and store them
    sites = campaign["assignedSites"]
    sitesCount = len(sites)
    campaign["sitesCount"] = str(sitesCount)

    siteDetails = []
    for item in sites:
        siteObject = GetSiteData(item)
        siteDetails.append({
                            "slideType" : siteObject.siteSlideType,
                            "siteDetail": siteObject.siteDetail, 
                            "siteImage": siteObject.siteImage,
                            "sitePricing": siteObject.sitePricing,
                            "nearByLocations": siteObject.nearByLocation,
                            "seccData": siteObject.siteSECC,
                            "trafficData":siteObject.trafficData    
                            })


    # Create instance of PDF class
    pdf = PDF()

    # Add a page
    pdf.add_page()

    # Add a border less table with Campaign Data
    pdf.draw_table_from_dict(campaign, 200, 20, 50, 100)
    # print(sites)
    for item in siteDetails:
        pdf.add_page()
        pdf.draw_site_page(item)
    

    pdf_output = BytesIO()
    pdf.output(pdf_output)

    # Return the PDF content
    return pdf_output.getvalue()
    