from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from blogging.models import Post


def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join([f"\t{arg}" for arg in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join([f"\t{key}: {val}" for key, val in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")


class PostListView(ListView):
    model = Post
    template_name = "blogging/list.html"

    def get(self, request, *args, **kwargs):
        posts = self.get_queryset()
        published = posts.exclude(published_date__exact=None).order_by(
            "-published_date"
        )
        context = {"posts": published}
        return render(request, "blogging/list.html", context)


class PostDetailView(DetailView):
    model = Post
    template_name = "blogging/detail.html"

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        if post.published_date:
            context = {"post": post}
            return render(request, "blogging/detail.html", context)
        # found a post, but it is not published
        raise Http404
