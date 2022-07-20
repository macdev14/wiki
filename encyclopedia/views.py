from django.shortcuts import render
from django import forms
from . import util
from django.contrib import messages
from django.http import HttpResponseRedirect as redirect
from django.urls import reverse
from markdown2 import Markdown
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import random
class wikiNewForm(forms.Form):
    wikiTitle = forms.CharField(label="", widget=forms.TextInput(attrs={'class' : 'form-control my-2', 'id' : 'wikiTitle'}))
    wikiContent = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control my-2 mr-5'}), label="")
class wikiEditForm(forms.Form):
    wikiTitle = forms.CharField(label="", widget=forms.TextInput(attrs={'readonly': 'readonly', 'class' : 'form-control my-2', 'id' : 'wikiTitle'}))
    wikiContent = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control my-2 mr-5'}), label="")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
markdowner = Markdown()

def entryPage(request, entry=None):
    renderPage = None
    if not entry and request.GET.get('q'):
        button = True
        renderPage = 'index.html'
        srch = request.GET.get('q')
        entries = checkEntry(srch)
        
    elif util.get_entry(entry):
        entries = markdowner.convert(util.get_entry(entry))
        renderPage = 'entry.html'
        button = True
    if renderPage:
        return render(request, "encyclopedia/"+renderPage, {
            "pageTitle" : entry,
            "entries" : entries,
            "button" : button
        })
    return entryNotFound()
    

    

def wikiNewPage(request):                   
    if request.method == 'POST':
        form = wikiNewForm(request.POST)
        if form.is_valid():
            wikiTitle = form.cleaned_data["wikiTitle"]
            if util.get_entry(wikiTitle):
                messages.add_message(request, messages.ERROR, 'Entry Already Exists.')
                return render(request, "encyclopedia/wiki.html", {
                "form": form})
            wikiContent = form.cleaned_data["wikiContent"]
            util.save_entry(wikiTitle, wikiContent)
            return redirect(reverse("entryPage", kwargs={"entry":wikiTitle} ))
        else:
            return render(request, "encyclopedia/wiki.html", {
        "form": form,
        "pageTitle" : "New Entry"
    })

    return render(request, "encyclopedia/wiki.html", {
        "form": wikiNewForm()
    })

def wikiEditPage(request):
    # Edit Entry View
    if request.method == "GET":
        # Case GET retrieve passed title
        wikiTitle = request.GET.get("title")
        if not util.get_entry(wikiTitle):
            # Check if exists & return not found 
            return entryNotFound()
        wikiContent = util.get_entry(wikiTitle)
        # Pass wikicontent to data dict and create form
        data = {'wikiTitle': wikiTitle ,'wikiContent': wikiContent }
        form = wikiEditForm(data)
        return render(request, "encyclopedia/wiki.html", {"form": form, "edit": True})
       
    if request.method == "POST":
        form = wikiEditForm(request.POST)
        if form.is_valid():
            wikiTitle = form.cleaned_data["wikiTitle"]
            wikiContent = form.cleaned_data["wikiContent"]
            util.save_entry(wikiTitle, wikiContent)
            return redirect(reverse("entryPage", kwargs={"entry":wikiTitle} ))
        return render(request, "encyclopedia/wiki.html", {"form": form, "edit": True } )
 
def checkEntry(srch):
    # Function to check if entry exists
    entries = []
    if util.get_entry(srch):
        entries.append(srch)
    else:
        for char in srch:
            for item in util.list_entries():
                if char in item or char.capitalize() in item:      
                    if item not in entries:
                        entries.append(item)
                
  
    return entries

def randomPage(request):
    # Function to return random entry
    entries = util.list_entries()
    return redirect(reverse("entryPage", kwargs={"entry": random.choice(entries)} ))


def entryNotFound():
    # Function to return 'not Found' Entry
    entry = "Not Found"
    entries = markdowner.convert('#**Oops!**  <br> <h3>Entry not found</h3>')
    return render(request, "encyclopedia/entry.html", {
        "pageTitle" : entry,
        "entries" : entries
            
    })