from django.urls import path
from home import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', views.mainhome, name = 'home'),
    path('list', views.listhome, name = 'list'),
    path('list/<str:loai>', views.sortlisthome, name='sortlist'),
    path('detail/<int:pk>', views.detailhome, name = 'detail'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('add/<int:id>', views.add_to_cart, name='add'),
    path('upsoluong/<int:id>', views.upsoluong, name='upsoluong'),
    path('downsoluong/<int:id>', views.downsoluong, name='downsoluong'),
    path('xoadonhang/<int:id>', views.xoadonhang, name='xoadonhang'),
    path('xoa_item/<int:id>/<int:don>', views.xoa_item, name='xoa_item'),
    path('user', views.profile, name='profile'),
    path('buy/<int:id>', views.buyhome, name = 'buy')
]