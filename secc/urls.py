from django.contrib import admin
from django.urls import include, path
from sites.views import SitesAPIView, BookingAPIView, PPTUploadView, ImageView, GetPlacesGoogle, PlaceDetailAPI, SitesSearchView, ImagesSearchView, SitePricingAPIView, ImagesFetchSiteTagView, PriceFetchSite
from customers.views import CustomersAPIView, CustomerSearchView
from users.views import UsersAPIView, TokenAPIView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', CustomersAPIView.as_view()),
    path('customers/<int:pk>/', CustomersAPIView.as_view()),
    path('customers/search/', CustomerSearchView.as_view()),
    path('sites/', SitesAPIView.as_view()),
    path('sites/<int:pk>/', SitesAPIView.as_view()),
    path('sites/search/', SitesSearchView.as_view()),
    path('sites/pricing/', SitePricingAPIView.as_view()),
    path('sites/pricing/search/', PriceFetchSite.as_view()),
    
    path('sites/pricing/<int:pk>/', SitePricingAPIView.as_view()),
    path('bookings/', BookingAPIView.as_view()),
    path('bookings/<int:pk>/', BookingAPIView.as_view()),
    path('process_ppt/', PPTUploadView.as_view()),
    path('getImages/<int:pk>/', ImageView.as_view()),
    path('getImages/', ImageView.as_view()),
    path('uploadImage/', ImageView.as_view()),
    path('getGooglePlaces/', GetPlacesGoogle.as_view()),
    path('getPlaceDetail/', PlaceDetailAPI.as_view()),
    path('images/search/', ImagesSearchView.as_view()),
    path('images/searchTag/', ImagesFetchSiteTagView.as_view()),
    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
