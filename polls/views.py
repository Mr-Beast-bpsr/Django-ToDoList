from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import ToDoList, Item
from .forms import  CreateNewList
# Create your views here.

def home(response):
    return render(response, "polls/home.html", {})
def index(response,id):
    ls = ToDoList.objects.get(id=id)
    if response.user.todolist.all():

        # item = ls.item_set.get()
        if response.method == "POST":

            if response.POST.get("save"):
                for item in ls.item_set.all():
                    p= response.POST
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete =True
                    else :
                        item.complete = False
                    item.save()

            elif response.POST.get("newItem"):
                txt =response.POST.get("new")
                if len(txt) >2:
                    ls.item_set.create(text = txt, complete= False)
                else:
                    print("Invalid")
        return render(response, "polls/list.html", {"ls":ls})



def create(response):
    if response.method == "POST":
        form = CreateNewList((response.POST))

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            response.user.todolist.add(t)
            return HttpResponseRedirect("%i" %t.id)
    else:
        form = CreateNewList()

    return render(response, "polls/create.html", {"form":form})
def view(response):
    l = ToDoList.objects.all()
    return render(response, "polls/view.html", {"lists":l})
