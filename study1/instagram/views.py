from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Post

post_list = ListView.as_view(model=Post)

# def post_list(request):
#     qs = Post.objects.all()
#     q = request.GET.get('q', '')
#     if q:
#         qs = qs.filter(message__icontains=q)
#     # instagram/templates/instagram/post_list.html
#     return render(request, 'instagram/post_list.html',{
#         'post_list': qs,
#         'q': q,
#     })

def post_detail(request: HttpResponse, pk: int) -> HttpResponse:
    response = HttpResponse()
    response.write("Hello World")
    return response
