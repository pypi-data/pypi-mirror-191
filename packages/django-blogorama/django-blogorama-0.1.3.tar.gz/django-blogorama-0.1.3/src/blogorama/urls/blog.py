from django.urls import path

from blogorama.views import blog

urlpatterns = [
    path("posts/", blog.PostlListAPIView.as_view(), name="blogorama_post-list"),
    path("post-create/", blog.PostCreate.as_view(), name="blogorama_post-create"),
    path("post/<slug:slug>/update/", blog.PostUpdate.as_view(), name="blogorama_post-update"),
    path(
        "post/<slug:slug>/",
        blog.PostDetailView.as_view(),
        name="blogorama_post",
    ),
]
