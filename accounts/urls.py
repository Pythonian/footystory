from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from . import views as accounts_views

urlpatterns = [
    path('', RedirectView.as_view(url='login', permanent=True),
         name='account'),
    path('signup/', account_views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(
        template_name='account/login.html'),
        name='login'),

    url(r'^activation/sent/$',
        accounts_views.account_activation_sent,
        name='account_activation_sent'),

    url(r'^activate/resend/$',
        accounts_views.resend_activation,
        name='resend_activation'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        accounts_views.activate, 
        name='activate'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='account/password_reset.html',
             email_template_name='account/email/password_reset_email.html',
             subject_template_name='account/email/password_reset_subject.txt'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done')

]


urlpatterns += [

    url(r'^(?P<username>[\w.@+-]+)/$', 
        accounts_views.profile,
        name='profile'),
    
    url(r'^(?P<username>[\w.@+-]+)/comments/$',
        accounts_views.comments,
        name='comments'),

    url(r'^(?P<username>[\w.@+-]+)/settings/$', 
        accounts_views.settings,
        name='settings'),

    url(r'^(?P<username>[\w.@+-]+)/settings/disable/$',
        accounts_views.disable,
        name='disable'),

    url(r'^(?P<username>[\w.@+-]+)/follow/$', 
        accounts_views.follow, 
        name='follow'),

    url(r'^(?P<username>[\w.@+-]+)/unfollow/$', 
        accounts_views.unfollow, 
        name='unfollow'),

    url(r'^(?P<username>[\w.@+-]+)/followers/$', 
        accounts_views.followers,
        name='followers'),

    url(r'^(?P<username>[\w.@+-]+)/following/$', 
        accounts_views.following,
        name='following'),

    url(r'^(?P<username>[\w.@+-]+)/notifications/$', 
        accounts_views.notifications,
        name='notifications'),

]

# urlpatterns += [
#     path('<username>/', accounts_views.profile, name='profile'),
#    	path('<username>/comments/', accounts_views.comments, name='comments'),
#     path('<username>/settings/', accounts_views.settings, name='settings'),
#    	path('<username>/settings/disable/', accounts_views.disable, name='disable'),
#     path('<username>/following/', accounts_views.following, name='following'),
#     path('<username>/followers/', accounts_views.followers, name='followers'),
#     # path('<username>/follow/',
#     path('users/follow/', accounts_views.user_follow, name='user_follow'),
#     path('<username>/notifications/',
#          accounts_views.notifications, name='notifications'),

#    	url(r'^(?P<username>[\w.@+-]+)/follow/$',
#         accounts_views.follow,
#         name='follow'),

#     url(r'^(?P<username>[\w.@+-]+)/unfollow/$',
#         accounts_views.unfollow,
#         name='unfollow'),

# ]
