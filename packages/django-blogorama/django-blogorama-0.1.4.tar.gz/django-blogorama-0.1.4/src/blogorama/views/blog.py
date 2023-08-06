from django.views.generic import ListView, DetailView, UpdateView, CreateView
from blogorama.settings import Config
from blogorama.models import Post, StateChoices, Comment
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormMixin
from blogorama.forms import CommentModelForm
from django.urls import reverse
from django.utils.translation import get_language
from collections import OrderedDict
from django.contrib.sites.shortcuts import get_current_site


def toc_generator(request):
    work = OrderedDict()

    for post in Post.objects.active().filter(sites=get_current_site(request)):
        year, month, month_int = post.created.strftime("%Y-%B-%m").split("-")

        if not year in work:
            work[year] = {"months": {}, "int": int(year)}

        if not month in work[year]["months"]:
            work[year]["months"][month] = {"int": int(month_int), "posts": []}

        work[year]["months"][month]["posts"].append(
            {"title": post.title, "author": post.author, "url": post.get_absolute_url()}
        )

    return work


def get_available_language():
    thread_language = get_language()

    ldict = {v[0]: v[1] for v in settings.LANGUAGES}

    # Check if the available language is in the list of languages

    if thread_language in ldict:
        return thread_language

    short_language_code = thread_language.split("_")[0]

    if short_language_code in ldict:
        return short_language_code

    if settings.LANGUAGE_CODE in ldict:
        return settings.LANGUAGE_CODE

    short_system_language_code = settings.LANGUAGE_CODE.split("_")[0]

    if short_system_language_code in ldict:
        return short_system_language_code

    return Config.DEFAULT_LANGUAGE_CODE


class PostlListAPIView(ListView):
    queryset = Post.objects.active()
    paginate_by = Config.BLOG_PAGINATION

    def get_context_data(self, *args, **kwargs):
        context = super(PostlListAPIView, self).get_context_data(*args, **kwargs)
        context["drafts"] = Post.objects.all().filter(
            author=self.request.user.id, state=StateChoices.DRAFT, sites=get_current_site(self.request)
        )
        context["toc"] = toc_generator(self.request)
        return context

    def get_queryset(self):
        return self.queryset.filter(sites=get_current_site(self.request))


class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentModelForm

    # TODO: add check that the post is available on the given site

    # def get

    # Form Processing for Comments
    def get_success_url(self):
        return reverse("blogorama_post", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["form"] = self.form_class(initial={"post": self.object})
        context["comments"] = Comment.objects.active().filter(post=self.object)
        get_available_language()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        form.instance.post = self.object
        form.instance.language = get_available_language()
        form.instance.state = StateChoices.PUBLISHED

        form.save()
        return super(PostDetailView, self).form_valid(form)


@method_decorator(login_required, name="dispatch")
class PostCreate(PermissionRequiredMixin, CreateView):
    """Creates a Blgorama Post"""

    permission_required = "blogorama.add_post"

    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        form.instance.site = get_current_site(self.request)
        form.instance.language = get_available_language()
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class PostUpdate(PermissionRequiredMixin, UpdateView):
    """Edits an existing Blgorama Post"""

    permission_required = "blogorama.change_post"

    model = Post
    fields = ["title", "content", "state"]
    template_name = "blogorama/post_update.html"
