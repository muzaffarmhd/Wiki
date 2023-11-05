from django.shortcuts import render
import markdown2
import requests
import random
import os
import re
from django.urls import reverse
from . import util
from django.http import Http404, HttpResponseRedirect,HttpResponse
from django.conf import settings


def index(request):
    if request.method == "POST":
        search_query=request.POST.get('q','')
        url = request.build_absolute_uri(reverse('encyclopedia:getByTitle', kwargs={'title': search_query}))
        response = requests.head(url)
        pages= util.list_entries()
        if search_query in pages:
            return HttpResponseRedirect(url)
        else:
            search=util.list_search_entries(search_query)
            return render(request,"encyclopedia/index.html",{
                "entries":search
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
    })

def get(request,title):
    if request.method=="POST":
        search_query=request.POST.get('q','')
        url = request.build_absolute_uri(reverse('encyclopedia:getByTitle',kwargs={'title':search_query}))
        response = requests.head(url)
        pages= util.list_entries()
        if search_query in pages:
            return HttpResponseRedirect(url)
        else:
            search=util.list_search_entries(search_query)
            return render(request,"encyclopedia/index.html",{
                "entries":search
            })
    if title in util.list_entries():
        entry=util.get_entry(title)
        html_content=markdown2.markdown(entry)
        return render(request,'encyclopedia/display.html',{'html_content':html_content,"title":title})
    else:
        return render(request,'encyclopedia/notfound.html')
    

def create(request):
    if request.method=='POST':
        title=request.POST.get('title','')
        content = request.POST.get('markdowncontent','')
        if util.list_search_entries(title):
            abc= True
            return render(request, 'encyclopedia/create.html',{"exists":abc})
        else:
            entries_directory = os.path.join(settings.BASE_DIR, 'entries')

            # Ensure the "entries" directory exists
            if not os.path.exists(entries_directory):
                os.makedirs(entries_directory)

            # Construct the full path to the file you want to create in the "entries" directory
            file_path = os.path.join(entries_directory, f'{title}.md')
            with open(file_path,'w+') as file:
                file.write(content)
                file.close()
                return HttpResponseRedirect(reverse('encyclopedia:index'))
    return render(request,'encyclopedia/create.html')
def normalize_newlines(text):
  """Normalizes newline characters to Unix-style (LF)."""
  return re.sub(r"\r\n", "\n", text)
def edit(request,title):
    if request.method=="POST":
        markdowncontent = request.POST.get('markdowncontent')
        markdowncontent = normalize_newlines(markdowncontent)
        util.save_entry(title,markdowncontent)
        url = request.build_absolute_uri(reverse("encyclopedia:getByTitle",kwargs={'title':title}))
        return HttpResponseRedirect(url)
    entry=util.get_entry(title)
    return render(request,'encyclopedia/edit.html',{
        "title":title,
        "content":entry
    })
def randomm(request):
    if request.method=="POST":
        search_query=request.POST.get('q','')
        url = request.build_absolute_uri(reverse('encyclopedia:getByTitle',kwargs={'title':search_query}))
        response = requests.head(url)
        pages= util.list_entries()
        if search_query in pages:
            return HttpResponseRedirect(url)
        else:
            search=util.list_search_entries(search_query)
            return render(request,"encyclopedia/index.html",{
                "entries":search
            })
    entries= util.list_entries()
    random_entry = random.choice(entries)
    entry=util.get_entry(random_entry)
    html_content = markdown2.markdown(entry)
    return render(request,'encyclopedia/display.html',{'html_content': html_content,'title':random_entry})
    

            