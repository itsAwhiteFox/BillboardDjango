from django.urls import include, path
from sites.views import get_bookings_by_customer, post_booking, get_self_bookings, get_site_images, upload_image_data, images_from_ppt, post_site_pricing, get_site_price, post_new_site, site_search_view, get_site_detail, get_sites_list, post_state_entities, get_state_entities, get_all_bookings, get_nearby_assets
from customers.views import customer_detail, customer_list, create_customer, search_customer
from users.views import users_list, user_detail, staff_list, reset_password
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('gettoken/', obtain_auth_token),
    path('users/', users_list),
    path('userDetail/', user_detail),
    path('resetPassword/',reset_password),
    path('staffList/', staff_list),
    path('customerDetail/', customer_detail),
    path('customersList/', customer_list),
    path('createCustomer/', create_customer),
    path('customers/search/', search_customer),
    path('getStateEntitiesList/', get_state_entities),
    path('createStateEntity/', post_state_entities),
    path('createSite/', post_new_site),
    path('getSitesList/', get_sites_list),
    path('getSiteDetail/<str:pk>/', get_site_detail),
    path('sites/search/', site_search_view),
    path('getGooglePlaces/', get_nearby_assets),
    path('sites/pricing/', get_site_price),
    path('addPricing/', post_site_pricing),
    path('createBooking/', post_booking),
    path('bookingsForSelf/', get_self_bookings),
    path('bookingByCustomer/', get_bookings_by_customer),
    path('getAllBookings/', get_all_bookings),
    path('process_ppt/', images_from_ppt),
    path('getSiteImages/', get_site_images),
    path('uploadImage/', upload_image_data),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
