from django.shortcuts import render

from . import util

from markdown2 import Markdown

from django import forms

from django.shortcuts import render

import random

markdowner=Markdown()

class Search(forms.Form):
    item=forms.CharField(widget=forms.TextInput(attrs={
        "class": "myfieldclass",
        "placeholder": "Search"
        }))

class Post(forms.Form):
    Title= forms.CharField()
    textarea=forms.CharField(widget=forms.Textarea())

class Edit(forms.Form):
    textarea=forms.CharField(widget=forms.Textarea())


def index(request):
    entries= util.list_entries()
    searched=[]
    if request.method == "POST":
        form=Search(request.POST)
        if form.is_valid():
            item= form.cleaned_data["item"]
            for x in entries:
                if item in entries:
                    page=util.get_entry(item)
                    converted_page=markdowner.convert(page)
                    context={
                        "page":converted_page,
                        "Title":item,
                        "form": Search()
                    }
                    return render(request, "encyclopedia/entry.html", context)
                if item.lower() in x.lower():
                    searched.append(x)
                    context={
                        "searched": searched,
                        "form": Search()
                    }
            return render(request, "encyclopedia/search.html", context)
        else:
            return render(request, "encyclopedia/index.html", {
                "form": form
             })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": Search()
        })

def entry(request, Title):
    entries=util.list_entries()
    if Title in entries:
        page=util.get_entry(Title)
        converted_page=markdowner.convert(page)
        context={
            "page": converted_page,
            "Title": Title,
            "form":Search()
        }
        return render(request,"encyclopedia/entry.html", context)
    else:
        return render(request,"encyclopedia/ERROR.html", {
            "error_message": "Page not found"
            })

def create(request):
    if request.method==POST:
        form=Post(request.POST)
        if form.is_valid():
            Title=form.cleaned_data["Title"]
            textarea=form.cleaned_data["textarea"]
            entries=util.list_entries()
            if Title in entries:
                return render(request, "encyclopedia/ERROR.html",{
                    "form": Search(),
                    "error_message": "This page already exists"
                })
            else:
                util.save_entry(Title, textarea)
                page=util.get_entry(Title)
                converted_page=markdowner.convert(page)
                context={
                    "form": Search(),
                    "page": converted_page,
                    "Title": Title
                }
                return render(request, "encyclopedia/entry.html", context)
        else:
            return render(request, "encyclopedia/create.html", {
                "form": Search(),
                "post": Post()
            })
            
