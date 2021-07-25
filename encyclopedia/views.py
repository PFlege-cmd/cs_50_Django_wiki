from django.shortcuts import render
from django.core.files import File
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from markdown2 import Markdown
from random import choice
from . import MarkDown2Html
from . import util
import re

class CreationForm(forms.Form):
    title = forms.CharField(label="title");
    textarea= forms.CharField(widget=forms.Textarea)
    

markdowner = Markdown()
md2html = MarkDown2Html.MarkDown2Html()
    

def index(request):

    #if "entries" not in request.session:
    #    request.session["entries"] = util.list_entries()

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def get_entry(request, site):
    try:
        
        md = markdowner.convert(util.get_entry(site.capitalize())); 
        testmd = "<h1>Test von neuem Markdown</h1>"
        
        
        htmlString = md2html.convertMarkdown2Html(util.get_entry(site.capitalize()))
        
        return render(request, "encyclopedia/Git.html", 
                    {
                        "entry" : htmlString,
                        "page" : site
                     })

    except TypeError:
            return error(request)

   
def error(request):
    return HttpResponse("500\n Page not found!");
    
def search(request):

    if request.method=="GET":        
        page = request.GET.get("q")
        
        if page.capitalize() in util.list_entries():          
           return get_entry(request, page);
           
        else:
            return createSuggestions(request);    
    
def createSuggestions(request):
    
    searchString = request.GET.get("q")
    containingPages = []
    
    for pages in util.list_entries():
        if searchString in pages.lower():
            containingPages.append(pages)
            
    return render(request, "encyclopedia/suggestions.html", {
        "suggestions": containingPages
    })


def createPage(request):
    if request.method=="POST":
    
        createForm = CreationForm(request.POST)
        if createForm.is_valid():
            
            # - checks if the title of the new pages matches already existing one - if so, throw error!
            if (checkIfFileExists(createForm.cleaned_data["title"])):
                return HttpResponse("Page already exists!")
            # - if all good: return some message to view
            else:
                util.save_entry(createForm.cleaned_data["title"], createForm.cleaned_data["textarea"])
                return get_entry(request, createForm.cleaned_data["title"])                

    else:
        return render(request, 'encyclopedia/createPage.html', {
            "createForm": CreationForm()
        })
    

def checkIfFileExists(fileName):
    for entry in util.list_entries():
        if fileName.lower() ==  entry.lower():
            return True
          
            
def editPage(request, site):

    if request.method == "GET":
   
        path = f"entries/{site}.md"
        f = open(path, "r");
        content = f.read();
               
        data = { 'title': site,
                    'textarea': content}
        
        form = CreationForm(data)
        
        return render(request, 'encyclopedia/editPage.html', {
                "form" : form,
                "page" : site
            })
    
    else:
        
        form = CreationForm(request.POST)
        if form.is_valid():
        
            util.save_entry(form.cleaned_data['title'], form.cleaned_data['textarea'])
            return HttpResponseRedirect(reverse("encyclopedia:test", args=(site,)))
            
        else:
            return HttpResponse("Does not work so fine!")
        
def getRandomPage(request):
    
    page = choice(util.list_entries());
    return get_entry(request, page);