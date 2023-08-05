from django.views.generic import ListView, DetailView
from .settings import Config
from .models import Post


def toc_generator():
    # TODO: Update this format with real data
    return [{"year": "2023", "months": [{"name": "January", "posts": [{"title": "post1", "url": "/blog/"}]}]}]


class PostlListAPIView(ListView):
    queryset = Post.objects.active()
    # extra_context = {"toc": toc_generator()}
    paginate_by = Config.BLOG_PAGINATION


class PostDetailView(DetailView):
    model = Post
