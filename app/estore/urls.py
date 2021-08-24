from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('login/',views.login_veiw,name='login'),
    path('profile/',views.dashboard,name='dashboard'),
    path('logout/',views.logout_view,name='logout'),
    path('code/<str:ref_code>',views.signup,name='signup'),
    path('network/',views.network, name = 'network'),
    path('help/up', views.helper_up, name='helper_up'),
    path('help/down', views.helper_down, name='helper_down'),
    path('edit-info/',views.UserInfoEditView,name='edit_info'),
    path('sharing_increase',views.sharing_increase,name = 'sharing_increase'),
]
