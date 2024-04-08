from django.urls import path
from .views import SigninView, CreateAccountView


urlpatterns = [
    path('create-account/', CreateAccountView.as_view(), name="create_account"),
    path('signin/', SigninView, name='signin'),
]