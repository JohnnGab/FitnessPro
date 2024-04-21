from django.urls import path
from .views import CustomLoginView, CreateAccountView
from .views import check_authentication_status


urlpatterns = [
    path('create-account/', CreateAccountView.as_view(), name="create_account"),
    path('signin/', CustomLoginView.as_view(), name='signin'),
    path('check-auth/', check_authentication_status, name='check_auth'),
]