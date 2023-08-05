from django.urls import path

from blogorama import views

urlpatterns = [
    path("posts/", views.PostlListAPIView.as_view(), name="blogorama-post-list"),
    path(
        "post/<slug:slug>/",
        views.PostDetailView.as_view(),
        name="blogorama-post",
    ),
]
