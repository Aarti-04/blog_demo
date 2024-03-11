from django.urls import path
from .views import UserApiView,UserLoginApiView,UserLogoutView,PostApiView
urlpatterns = [
    path("user/",UserApiView.as_view(),name="user_api"),
    path("login/",UserLoginApiView.as_view(),name="user_login"),
    path("logout/",UserLogoutView.as_view(),name="logout"),
    path("post/",PostApiView.as_view(),name="post_api"),
     path("post/<int:param>",PostApiView.as_view(),name="post_api")

]
