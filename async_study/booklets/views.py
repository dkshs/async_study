from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Booklet, BookletView


@login_required(login_url="sign_in")
def add_booklet(request):
    if request.method == "GET":
        booklets = Booklet.objects.filter(user=request.user)
        total_views = BookletView.objects.filter(booklet__user=request.user).count()
        return render(request, "add_booklet.html", {"booklets": booklets, "total_views": total_views})
    elif request.method == "POST":
        title = request.POST.get("title") or ""
        file = request.FILES.get("file") or None

        if len(title.strip()) == 0:
            messages.error(request, "Title is required!")
            return redirect("add_booklet")
        if file is None:
            messages.error(request, "File is required!")
            return redirect("add_booklet")
        booklet = Booklet(user=request.user, title=title, file=file)
        booklet.save()
        messages.success(request, "Booklet added successfully!")
        return redirect("add_booklet")


@login_required(login_url="sign_in")
def booklet(request, booklet_id):
    try:
        booklet = Booklet.objects.get(id=booklet_id)
    except Booklet.DoesNotExist:
        messages.error(request, "Booklet not found!")
        return redirect("add_booklet")
    if request.method == "GET":
        booklet_view = BookletView(booklet=booklet, ip=request.META.get("REMOTE_ADDR"), user=request.user)
        booklet_view.save()
        views = BookletView.objects.filter(booklet=booklet)
        unique_views = views.values("ip").distinct().count()
        total_views = views.count()
        return render(
            request, "booklet.html", {"booklet": booklet, "unique_views": unique_views, "total_views": total_views}
        )
