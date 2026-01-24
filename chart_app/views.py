from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from chart_app.forms import MessageForm
from chart_app.models import Message


@login_required
def chat_view(request, room_name):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.member = request.user
            message.save()
            return redirect("chat")
    else:
        form = MessageForm()

    messages = Message.objects.order_by("-created_at")
    return render(
        request,
        "chat.html",
        {"form": form, "messages": messages, "room_name": room_name},
    )
