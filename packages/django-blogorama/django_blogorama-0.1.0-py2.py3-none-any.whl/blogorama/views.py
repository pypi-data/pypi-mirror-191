from django.views.generic import ListView, DetailView
from .settings import Config
from .models import Post


def toc_generator():
    # TODO: Update this format with real data
    return [{"year": "2023", "months": [{"name": "January", "posts": [{"title": "post1", "url": "/blog/"}]}]}]


class PostConsolidatedView(ListView):
    queryset = Post.objects.active()
    template_name = "blogorama/post_consolidated_view.html"
    extra_context = {"toc": toc_generator()}
    paginate_by = Config.BLOG_PAGINATION


class PostlListAPIView(ListView):
    queryset = Post.objects.active()


class PostDetailView(DetailView):
    model = Post
