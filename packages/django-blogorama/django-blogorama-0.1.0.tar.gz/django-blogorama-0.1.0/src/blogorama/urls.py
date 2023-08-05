from django.urls import path

from blogorama import views

urlpatterns = [
    path("", views.PostConsolidatedView.as_view(), name="blogorama-post-overview"),
    path("posts/", views.PostlListAPIView.as_view(), name="blogorama-post-list"),
    path(
        "post/<slug:slug>/",
        views.PostDetailView.as_view(),
        name="blogorama-post",
    ),
]
