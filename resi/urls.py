from django.urls import path
from . import views

app_name = "resi"

urlpatterns = [
    path("", views.index, name="home"),
    path(
        "verification_account/", views.verification_account, name="verification_account"
    ),
    path("login", views.log_in, name="log_in"),
    path("signup/", views.sign_up, name="sign_up"),
    path("number-verification/", views.confirm_account, name="confirm_account"),
    path("logout/", views.log_out, name="log_out"),
    path("customer/account/", views.account_details, name="account_details"),
    path("get_rooms/<int:department_pk>", views.get_rooms, name="get_rooms"),
]
