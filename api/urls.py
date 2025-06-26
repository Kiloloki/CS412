from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import HistoryListView

urlpatterns = [
    path('', views.home_view, name='home'),
    path('history/', HistoryListView.as_view(), name='history'),  # ✅ 用 class-based view
    path('search/', views.search_view, name='search'),

    path('api/upload/', views.upload_image, name='upload'),
    path('api/full_process/', views.process_full_image, name='full_process'),
    path('api/crop_process/', views.process_crop_region, name='crop_process'),
    path('api/add_tag/', views.add_tag_to_image, name='add_tag'),
    path('api/search_by_tag/', views.search_by_tag, name='search_by_tag'),

    path('api/delete_image/', views.delete_image, name='delete_image'),  # ✅ 删除功能

    path('accounts/logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('accounts/register/', views.register_view, name='register'),  # 注册页面

    path('image/<int:image_id>/', views.image_detail_view, name='image_detail'),  # 图片详情
    path('update_tag/<int:image_id>/', views.update_tag_view, name='update_tag'),  # 标签更新
]

