from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *


urlpatterns = [

    #JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('api/books/', BookViewSet.as_view({'get': 'list'})),
    path('api/genres/', GenericViewSet.as_view({'get': 'list'})),
    path('api/review/add', add_review),
    path('api/review/delete/<int:review_id>/', delete_review),
    path('suggest/api/', suggest_books),
]
