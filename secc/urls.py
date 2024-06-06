from django.urls import include, path
from sites.views import get_bookings_by_customer, post_booking, get_self_bookings, get_site_images, upload_image_data, images_from_ppt, post_site_pricing, get_site_price, post_new_site, site_search_view, get_site_detail, get_sites_list, post_state_entities, get_state_entities, get_all_bookings, get_nearby_assets, get_image_id, map_image_site, get_first_distance, start_traffic_collection, get_traffic_count_collection, get_site_traffic
from customers.views import customer_detail, customer_list, create_customer, search_customer, customer_detail_by_code
from users.views import users_list, user_detail, staff_list, reset_password, get_user_images, upload_user_image, edit_user
from seccdata.views import search_area, create_area, region_list, stateSECCData, districtSECCData
from campaigns.views import get_campaign_detail, get_campaign_list, post_new_campaign, add_site_to_campaign, print_campaign_data, remove_site_from_campaign
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('gettoken/', obtain_auth_token),
    path('uploadSECCData/', create_area),
    path('getSECCData/', search_area),
    path('getStateData/', stateSECCData),
    path('getDistrictData/', districtSECCData),
    path('getRegions/', region_list),
    path('users/', users_list),
    path('uploadUserImage/', upload_user_image),
    path('getUserImage/', get_user_images),
    path('userDetail/', user_detail),
    path('editUser/<str:pk>/', edit_user),
    path('resetPassword/',reset_password),
    path('staffList/', staff_list),
    path('customerDetail/', customer_detail),
    path('customerDetailById/<str:pk>/', customer_detail_by_code),
    path('customersList/', customer_list),
    path('createCustomer/', create_customer),
    path('customers/search/', search_customer),
    path('getStateEntitiesList/', get_state_entities),
    path('createStateEntity/', post_state_entities),
    path('createCampaign/', post_new_campaign),
    path('listCampaigns/', get_campaign_list),
    path('campaignDetail/<str:pk>/', get_campaign_detail),
    path('addSiteToCampaign/<str:pk>/', add_site_to_campaign),
    path('removeSiteFromCampaign/<str:pk>/', remove_site_from_campaign),
    
    path('printCampaignData/<str:pk>/', print_campaign_data),
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
    path('getImageByID/<str:pk>/', get_image_id),
    path('mapSiteImage/', map_image_site),
    path('getFirstDistance/',get_first_distance),
    path('startTrafficCollection/', start_traffic_collection),
    path('processTrafficCount/', get_traffic_count_collection),
    path('getAllTrafficCalculations/', get_site_traffic)    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
