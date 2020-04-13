from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
from django.contrib.auth import login, authenticate
# Create your views here.


def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if response.method == "POST":
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get("c" + str(item.id)) == "clicked":
                    item.complete = True
                else:
                    item.complete = False

                item.save()

        elif response.POST.get("newItem"):
            txt = response.POST.get("new")
            if len(txt) > 0:
                ls.item_set.create(text=txt, complete=False)
            else:
                print("invalid")

        elif response.POST.get("deleteItem"):  # change it , not working
            for item in ls.item_set.all():
                if response.POST.get("d" + str(item.id)) == "clicked":
                    item.delete()
                else:
                    print("invalid1")

    return render(response, "home/list.html", {"ls": ls})


def home(response):
    return render(response, "home/homepage.html", {})


def create(response):
    if response.user.is_active:
        if response.method == "POST":
            form = CreateNewList(response.POST)
            if form.is_valid():
                n = form.cleaned_data["name"]
                t = ToDoList(name=n)
                t.save()
                response.user.todolist.add(t)
            return HttpResponseRedirect("/home/%i" % t.id)
        else:
            form = CreateNewList()
        return render(response, "home/create.html", {'form': form})
    else:
        return HttpResponseRedirect("/login")


def view(response):
    if response.user.is_active:
        return render(response, "home/view.html", {})
    else:
        return HttpResponseRedirect("/login")

