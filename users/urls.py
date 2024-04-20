from django.urls import path
from .views import CustomLoginView, CreateAccountView


urlpatterns = [
    path('create-account/', CreateAccountView.as_view(), name="create_account"),
    path('signin/', CustomLoginView.as_view(), name='signin'),
]