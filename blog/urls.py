from django.urls import include, path, re_path

from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *

router = routers.DefaultRouter()
router.register(r'authorpost', AuthorPostViewSet, basename='authorpost')


urlpatterns = [
    path('register', register, name='register'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('create_post', create_post, name="create_post"),
    path('post_detail/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', update_post, name='update_post'),
    path('post_list', PostListView.as_view(), name='post_list'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user_posts'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('password/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('logout/', logout_view, name='logout'),

    path('api/drf/drf-auth/', include('rest_framework.urls')),
    path('api/drf/postlist/', PostDRFAPI.as_view(), name='DRF GET'),   # Basic API Views
    path('api/drf/postlist/<int:pk>', PostDRFAPI.as_view(), name='DRF POST'),
    path('api/drf/postup/<int:pk>', PostUpdateDRFAPI.as_view(), name='DRF PUT and PATCH'),
    path('api/drf/postupdel/<int:pk>', PostUpdateDelDRFAPI.as_view(), name='DRF PUT,PATCH, DEL'),

    path('api/drf/', include(router.urls)),   # ViewSet

    path('api/drf/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   # JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
