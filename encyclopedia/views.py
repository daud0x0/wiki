from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from markdown import markdown
from random import choice
import re

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def get_page(request,title):
	content = util.get_entry(title)
	if content != None:
		return render(request, "encyclopedia/view.html",{
			"content": markdown(content),
			"title": title})
	return render(request, "encyclopedia/404.html",{
		"message": "Page Not Found",
		"title": title
		})

def search(request):
	title = request.GET.get("q")
	r = re.compile(f".*{title}.*", re.IGNORECASE)
	matchlist = list(filter(r.match, util.list_entries()))
	content = util.get_entry(title)
	if content != None:
		return render(request, "encyclopedia/view.html",{
			"content": markdown(content),
			"title": title})
	elif len(matchlist) > 0:
		return render(request, "encyclopedia/index.html", {
			"entries": matchlist
			})
	return render(request, "encyclopedia/404.html",{
		"message": "Page Not Found",
		"title": title
		})

def random(request):
	title = choice(util.list_entries())
	content = util.get_entry(title)
	return render(request, "encyclopedia/view.html", {
			"content": markdown(content),
			"title": title
			})

def create(request):
	if request.method == "POST":
		title = request.POST.get("title", "")
		content = request.POST.get("content", "")
		if title in util.list_entries():
			return render(request, "encyclopedia/404.html", {
				"message": "Page aleary exists",
				"title": title
				})
		else:
			util.save_entry(title, content)
			return render(request, "encyclopedia/view.html", {
				"content": markdown(content),
				"title": title
				})

	return render(request, "encyclopedia/create.html")

def edit(request, entry):
	if request.method == "POST":
		title = request.POST.get("title", "")
		content = request.POST.get("content", "")
		util.save_entry(title, content)
		return render(request, "encyclopedia/view.html", {
			"content": markdown(content),
			"title": title
			})
	else:
		return render(request, "encyclopedia/edit.html", {
			"content": util.get_entry(entry),
			"title": entry
			})
