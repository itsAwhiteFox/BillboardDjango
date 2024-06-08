from .getImages import getSiteImage
from .getTable import getTable
from .getSECCChartGroup import getSECCChartsImage
from .getNearByLocationChart import getNearbyPOIChartsImage
from .getMap import getMapImage
from .getTrafficStatsChart import getTrafficStatsChartsImage


def printPageWOAnyGoogleData(pdfDocument, siteData):
    pdfDocument.set_font('Arial', '', 18)
    pdfDocument.cell(500, 20, f"Site ID:   {siteData["siteDetail"]["location"]}")
    getSiteImage(pdfDocument, siteData["siteImage"])
    getTable(pdfDocument, siteData["siteDetail"], siteData["sitePricing"])
    getSECCChartsImage(pdfDocument, siteData["seccData"], "full")
    getMapImage(pdfDocument, siteData["siteDetail"], "full")