from django.urls import include, path
from . views import UserViewSet, FollowViewSet, FollowToView
from rest_framework.routers import SimpleRouter

app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet, 'users')

urlpatterns = [
    path('users/subscriptions/', FollowViewSet.as_view()),
    path('users/<int:pk>/subscribe/', FollowToView.as_view()),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
