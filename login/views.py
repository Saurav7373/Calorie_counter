from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from login.forms import LoginForm

def register(request):
    if request.method == 'POST':
        username = request.POST[ 'username' ]
        fname = request.POST[ 'fname' ]
        lname = request.POST[ 'lname' ]
        email = request.POST[ 'email' ]
        pass1 = request.POST[ 'pass1' ]
        pass2 = request.POST[ 'pass2' ]

        if len( username ) > 10:
            messages.error( request, 'Enter valid name.Your name should be within 10 character', extra_tags='alert' )
            return redirect( 'login_index' )
        if not username.isalnum():
            messages.error( request, 'Enter Valid Name.Your name should be in letter and numbers', extra_tags='alert' )
            return redirect( 'login_index' )

        if pass1 != pass2:
            if User.objects.filter( username=username ).exists():
                messages.error( request, 'Username Taken', extra_tags='alert' )
                return redirect( 'login_index' )
            elif User.objects.filter( email=email ).exists():
                messages.error( request, 'Email Taken', extra_tags='alert' )
                return redirect( 'login_index' )

            messages.error( request, 'Enter match password', extra_tags='alert' )
            return redirect( 'login_index' )

        if len( pass1 ) < 8:
            messages.error( request, 'Enter atleast eight character', extra_tags='alert' )
            return redirect( 'login_index' )

        else:
            user = User.objects.create_user( username=username, first_name=fname, email=email, password=pass1,
                                             last_name=lname )
        user.save();
        messages.success( request, "Your account is successfully created.", extra_tags='success' )
        return redirect( "/login" )

    else:
        return render( request, 'login/login.html' )
    # if request.method == "POST":
    #     login_form = LoginForm(data=request.POST)
    #
    #     if login_form.is_valid():
    #         user = login_form.save()
    #         print(user.password)
    #         user.set_password(user.password)
    #         user.save()
    #
    #         messages.success(request, "Successfully registered")
    #         return HttpResponseRedirect("/login")
    #
    # messages.error(request, "Error while registering")
    # return HttpResponseRedirect("/login")

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out")
    return HttpResponseRedirect("/login")

def login_attempt(request):
    success = False

    if "demo" in request.POST:
        username = password = "demo"
    else:
        username = request.POST["username"]
        password = request.POST["password"]

    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            login(request, user)
            success = True

    return success

def login_index(request):
    if request.method == "POST":
        result = login_attempt(request)

        if result:
            messages.success(request, "Successfully logged in")
        else:
            messages.error(request, "Error logging in")

        return HttpResponseRedirect("/")

    form_responses = messages.get_messages(request)
    response_message = None

    for response in form_responses:
        response_message = response
        break

    form_responses.used = True

    return render(request, "login/login.html", {"response_message": response_message})