from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth.models import User

from .forms import StudentForm, UserForm
from .models import Student, Post
from django.core.paginator import Paginator, EmptyPage
from django.template.loader import render_to_string

PAGE_COUNT = 2


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        response_data = {}
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                response_data['result'] = 'Success!'
                response_data['message'] = 'You"re logged in'
            else:
                response_data['result'] = 'Failed!'
                response_data['message'] = 'Login Failed, Please check your credentials'
        else:
            response_data['message'] = 'Login Failed, Please check your credentials'
            response_data['result'] = 'Failed!'

        return JsonResponse(response_data)

    return render(request, 'login.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({"success": True})
            else:
                errors = form.errors.get_json_data()
                print(errors)
                return JsonResponse({"errors": errors})
        form = UserForm()
        return render(request, 'signup.html', {'form': form})


def logout_view(request):
    auth.logout(request)
    return redirect('login')


def home(request):
    students = Student.objects.all().order_by('id').distinct()
    form = StudentForm()
    query = request.GET.get(
        'query')

    data = {}
    ajax = False
    if query:
        students = students.filter(
            Q(email__icontains=query) | Q(phone__icontains=query) | Q(name__icontains=query))
        ajax = True

    page = request.GET.get('page')
    has_next = True
    if page:
        ajax = True
        paginator = Paginator(students, PAGE_COUNT)

        try:
            students = paginator.page(page)
            has_next = students.has_next()
        except EmptyPage:
            has_next = False
    if ajax:
        html = render_to_string('partial_students.html', context={"students": students})
        data = {"html": html, "has_next": has_next}
        return JsonResponse(data)

    if request.method == 'POST':
        id = request.POST.get('update')
        instance = Student.objects.get(id=id) if id else None
        form = StudentForm(request.POST or None, instance=instance)
        if form.is_valid():
            print('form is valid')
            student = form.save()
            return render(request, 'student_data.html', {'student': student, 'update': id})

    return render(request, 'index.html', {'students': students[:PAGE_COUNT], 'form': form, "guery": query})


def delete(request, id):
    delt = Student.objects.get(id=id)
    delt.delete()
    return JsonResponse({'id': id})


def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse('Page not found', status=404)

    return render(request, 'user.html', {'user': user})