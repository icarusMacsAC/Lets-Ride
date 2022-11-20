from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static
from .views import SignUpView

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.index, name='index'),
    path('about_me', views.about_me, name='about_me'),
    path('result', views.result, name='result'),
    path('find_article', views.find_article, name='find_article'),
    path('technology', views.technology, name='technology'),
    path('projects', views.projects, name='projects'),
    path('login', views.login, name='login'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('asset_transportation_request', views.asset_transportation_request,
         name='asset_transportation_request'),
    path('share_travel_info', views.share_travel_info,
         name='share_travel_info'),
    path('my_asset_transportation_requests', views.my_asset_transportation_requests,
         name='my_asset_transportation_requests'),
    path('my_travel_info', views.my_travel_info,
         name='my_travel_info'),
    path('matched_asset_transportation_requests', views.matched_asset_transportation_requests,
         name='matched_asset_transportation_requests'),
    path('selected_asset_transportation_requests', views.selected_asset_transportation_requests,
         name='selected_asset_transportation_requests'),
    # path('sign_up', views.sign_up, name='sign_up'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signup/signin", views.signin, name="signup/signin"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
