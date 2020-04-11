from django.shortcuts import render
from myapp.forms import UserForm, UserProfileInfoForm

# for Login
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


# Create your views here.
def index(request):
    return render(request, 'myapp/index.html')


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)

        # check for validity of both the forms
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            # set_password will take in the raw_password and applies hashing
            user.set_password(user.password)
            # save the above change
            user.save()

            # contains website link and profile_pic
            profile = profile_form.save(commit = False)  # creates object but don't persist into db
            profile.user = user


            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'myapp/registration.html',
                    {'registered':registered, 'user_form': user_form, 'profile_form': profile_form})


def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)

        if user:
            if user.is_active:
                login(request, user)

                # redirect to a success page
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("Login failed!")
            print(f'Username: {username} and Password: {password}')

            return HttpResponse('Invalid login details!')

    else:
        return render(request, 'myapp/login.html', {})


# you can logout only if you are logged in
@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect(reverse('index'))


@login_required
def special(request):
    return HttpResponse('You\'re logged in!')
