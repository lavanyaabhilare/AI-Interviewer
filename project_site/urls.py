from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    # created paths urls and using actively
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('user_login', views.user_login, name='user_login'),
    path('create_account', views.create_account, name='create_account'),
    path('otp_verification', views.otp_verification, name='otp_verification'),
    path('short_reviwes', views.short_reviwes, name='short_reviwes'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('user_logout', views.user_logout, name='forgot_password'),
    path('start_interview', views.start_interview, name='start_interview'),
    # path('final_report', views.final_report, name='final_report'),
    # path('store_data', views.store_data, name='store_data'),
    path('update_user_info', views.update_user_info, name='update_user_info'),
    path('pp', views.pp, name='pp'),
    path('tc', views.tc, name='tc'),
    path('next_q', views.next_q, name='next_q'),
    path('ex', views.ex, name='ex'),
    path('ex2', views.ex2, name='ex2'),
    path('save_image', views.save_image, name='save_image'),
    

    

    # feature testing paths
    #path('tp', views.tp, name='tp'),
    # path('bi', views.bi, name='bi'),
    # path('f1', views.f1, name='f1'),



]


