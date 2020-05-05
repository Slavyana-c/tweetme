from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


# Create your views here.
def login_view(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST or None)

    # if you have your own form
    # form = MyModelForm(request.POST or None )
    if form.is_valid():
        # username = form.cleaned_data.get('username')
        # user_ = authenticate(username, password)
        user_ = form.get_user()
        login(request, user_)
        return redirect('/')

    # user = authenticate(request, username=username, password=password)
    context = {
        'form': form,
        'btn_label': 'Login',
        'title': 'Login'
    }
    return render(request, 'accounts/auth.html', context)


def logout_view(request, *args, **kwargs):
    if request.method == 'POST':
        logout(request)
        return redirect('/login')

    context = {

        'form': None,
        'description': 'Are you sure you want to logout?',
        'btn_label': 'Click to confirm',
        'title': 'Logout'
    }

    return render(request, 'accounts/auth.html', context)


def register_view(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)

    print(form.is_valid())
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return redirect('/')
        # print(form.cleaned_data)
        # username = form.cleaned_data.get('username')
        # User.objects.create(username=username)

    context = {
        'form': form,
        'btn_label': 'Register',
        'title': 'Register'
    }
    return render(request, 'accounts/auth.html', context)
