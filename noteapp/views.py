from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import SuspiciousOperation
from .models import Notes


def index(request):
    #print("in index")
    if not request.user.is_authenticated:
        return render(request, "noteapp/login.html", {"message":None})
    notes = Notes.objects.filter(user=request.user)
    context = {}
    context['notes'] = {}
    for note in notes:
        noteAsList = []
        noteAsList.append(note.notes)
        noteAsList.append(note.date)
        context['notes'][note.heading] = noteAsList
        #print(context['notes'])

    return render(request,"noteapp/index.html", context)

def login(request):
    if not request.user.is_authenticated:
        return render(request, "noteapp/login.html", {"message":None})
    return HttpResponseRedirect(reverse("index"))

def login_check(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("index"))
        return render(request, "noteapp/login.html", {"msg":"Invalid Credentials"})
    return HttpResponseRedirect(reverse("index"))

def new_user(request):
    #print("in new_user")
    if not request.user.is_authenticated:
        return render(request, "noteapp/new_user.html", {"message":"After Successfull Signup automatic login take place!"})
    return HttpResponseRedirect(reverse("index"))

def signup(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            #print("user authenticated")
            return render(request, "noteapp/index.html", {"message":None})
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        try:
            #print("in try")
            userexist = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            #print("user created")
            auth_login(request, user)
            #print("user login")
            return HttpResponseRedirect(reverse("index"))
        return render(request, "noteapp/new_user.html", {"message":"Username already exist."})
    return HttpResponseRedirect(reverse("index"))
    

def storenote(request):
    if not (request.user.is_authenticated or request.method=="POST"):
        return render(request, "noteapp/login.html", {"msg":"Login First"})
    heading = request.POST["heading"]
    notes = request.POST["note"]
    user = request.user
    try:
        notesexist = Notes.objects.get(heading=heading, user=user)
    except Notes.DoesNotExist:
        p = Notes(heading=heading, user=user, notes=notes)
        p.save()
        return HttpResponseRedirect(reverse("index"))
    raise SuspiciousOperation("Invalid request; Same heading already exist.")


def ajax(request):
    if not (request.user.is_authenticated and request.method=="POST" and request.is_ajax()):
        return render(request, "noteapp/login.html", {"msg":"Login First"})
    user = request.POST['user']
    heading = request.POST['heading']
    note = request.POST['note']
    Notes.objects.filter(user=user, heading=heading)[0].delete()

    return HttpResponse("success")

def logout(request):
    if (request.method=="POST") and (request.user.is_authenticated):
        auth_logout(request)
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("index"))
    