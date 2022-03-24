"""vipnamesproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from vipapi import views
from vipapi.views import VipWinnerAPI, RegisterNewAPI, UpdateRegistrationAPI, LoginView, PersonalInfoAPI, GetPersonalInfoAPI, EditPersonalInfoAPI, PhotoPortfolioAPI, GetPhotoPortfolioAPI, DescribeYourselfAPI, GetDescribeYourselfAPT, ApplicantStatusAPI, MessagesAPI, DeleteUserAPI, CheckUserPasswordAPI, PhotoStoryAPI
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^accounts', include('django.contrib.auth.urls')), #used by password reset url under rest-auth
    url(r'^photostory/$', PhotoStoryAPI.as_view(), name="photostory"),
    url(r'^vipwinner/$', VipWinnerAPI.as_view(), name="vipwinner"),
    url(r'^registernew/$', RegisterNewAPI.as_view(), name="registernew"),
    url(r'^updateregistration/(?P<pk>\d+)/$', UpdateRegistrationAPI.as_view(), name="updateregistration"),
    url(r'^api-auth/', include('rest_framework.urls')), #this creates LogIN link in the api browseable page.the url tag api-auth can be any name.
    url(r'^rest-auth/', include('rest_auth.urls')), #from package django-rest-auth
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')), #from package django-rest-auth[with_social]
    url(r'^auth/login/', LoginView.as_view(), name="auth-login"),
    url(r'^personalinfo/$', PersonalInfoAPI.as_view(), name="personalinfo"),
    url(r'^getpersonalinfo/$', GetPersonalInfoAPI.as_view(), name="getpersonalinfo"),
    url(r'^editpersonalinfo/(?P<pk>\d+)/$', EditPersonalInfoAPI.as_view(), name="editpersonalinfo"),
    url(r'^photoportfolio/$', PhotoPortfolioAPI.as_view(), name="photoportfolio"),
    url(r'^getphotoportfolio/$', GetPhotoPortfolioAPI.as_view(), name="getphotoportfolio"),
    url(r'^describeyourself/$', DescribeYourselfAPI.as_view(), name="describeyourself"),
    url(r'^getdescribeyourself/$', GetDescribeYourselfAPT.as_view(), name="getdescribeyourself"),
    url(r'^status/$', ApplicantStatusAPI.as_view(), name="applicantstatusapi"),
    url(r'^messages/$', MessagesAPI.as_view(), name="messagesapi"),
    url(r'^deleteuser/$', DeleteUserAPI.as_view(), name="deleteuserapi"),
    url(r'^checkuserpassword/$', CheckUserPasswordAPI.as_view(), name="checkuserpassword"),
    url(r'^checkapplicants/$', views.checkapplicants, name="checkapplicants"),
    url(r'^checkapplicantsbyyear/$', views.checkapplicantsbyyear, name="checkapplicantsbyyear"),
    url(r'^applicantdetails/(\d+)/$', views.applicantdetails, name="applicantdetails"),
    url(r'^markaschecked/$', views.markaschecked, name="markaschecked"),
    url(r'^sendmessage/$', views.sendmessage, name="sendmessage"),
    url(r'^sendemail/$', views.sendemail, name="sendemail"),  
    url(r'^deleteapplicantaccount/$', views.deleteapplicantaccount, name="deleteapplicantaccount"),   
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
