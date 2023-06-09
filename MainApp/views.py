from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet, Comment
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib import auth
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def snippets_page(request):
    snippets = Snippet.objects.all()
    users = User.objects.annotate(num_snippets=Count('snippets')).exclude(num_snippets=0)
    lang = request.GET.get('lang')
    sort = request.GET.get('sort')
    if lang:
        snippets = snippets.filter(lang=lang)
    if sort:
        snippets = snippets.order_by(sort)
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets,
        'lang': lang,
        'users': users,
        'sort': sort,
    }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    comment_form = CommentForm()
    context = {
        'pagename': 'Информация о сниппете',
        'snippet': snippet,
        'comment_form': comment_form
    }
    return render(request, 'pages/snippet_detail.html', context)


def add_snippet(request):
    if request.method == 'GET':   # получили страницу с формой заполнения
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)
    elif request.method == 'POST':  # получили данные из формы для добавления нового сниппета
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False) # атрибут указывает на "отложенное" сохранение в БД
            snippet.user = request.user
            snippet.save()
        return redirect('snippets-list')


def snippet_delete(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    snippet.delete()
    return redirect('snippets-list')


def login(request):
   if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
       # print("username =", username)
       # print("password =", password)
       user = auth.authenticate(request, username=username, password=password)
       if user is not None:
           auth.login(request, user)
       else:
           # Return error message
           pass
   return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect('home')


def registration(request):
    form = UserRegistrationForm()
    if request.method == 'GET':
        context = {
            'pagename': 'Регистрация',
            'form': form
        }
        return render(request, 'pages/registration.html', context)
    elif request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context = {
                'form': form,
                'pagename': 'Регистрация',
            }
            return render(request, 'pages/registration.html', context)

@login_required()       # декоратор для блокирования входа неавторизованным пользователям
def snippets_my(request):
    my_snippet = Snippet.objects.filter(user=request.user)
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': my_snippet,
    }
    return render(request, 'pages/view_snippets.html', context)


def comment_add(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            snippet_id = request.POST.get('snippet_id')
            snippet = Snippet.objects.get(id=snippet_id)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))


def users_rate(request):
    users = User.objects.all().annotate(num_snippets=Count('snippets'))
    context = {
        'pagename': 'Рейтинг пользователей',
        'users': users,
    }
    return render(request, 'pages/users_rate.html', context)


















