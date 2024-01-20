from async_study.challenges.models import ChallengeFlashcard
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Category, Flashcard


@login_required(login_url="sign_in")
def flashcards(request):
    difficulties = [{"value": d[0], "label": d[1]} for d in Flashcard.difficulty_choices]
    categories = Category.objects.all()

    if request.method == "GET":
        filter_category = request.GET.get("filter_category") or ""
        filter_difficulty = request.GET.get("filter_difficulty") or ""

        flashcards = Flashcard.objects.filter(user=request.user)
        if filter_category:
            flashcards = flashcards.filter(category_id=filter_category)
        if filter_difficulty:
            flashcards = flashcards.filter(difficulty=filter_difficulty)
        return render(
            request,
            "flashcards.html",
            {
                "categories": categories,
                "flashcards": flashcards,
                "difficulties": difficulties,
                "filter_category": filter_category,
                "filter_difficulty": filter_difficulty,
            },
        )
    elif request.method == "POST":
        question = request.POST.get("question") or ""
        response = request.POST.get("response") or ""
        category = request.POST.get("category") or ""
        difficulty = request.POST.get("difficulty") or ""

        if (
            len(question.strip()) == 0
            or len(response.strip()) == 0
            or len(category.strip()) == 0
            or len(difficulty.strip()) == 0
        ):
            messages.error(request, "All fields are required")
            return redirect("flashcards")
        if True not in [d["value"] == difficulty for d in difficulties]:
            messages.error(request, "Invalid difficulty")
            return redirect("flashcards")
        category = categories.filter(id=category)
        if not category.exists():
            messages.error(request, "Category not found")
            return redirect("flashcards")
        category = category.first()

        Flashcard.objects.create(
            user=request.user, question=question, answer=response, category=category, difficulty=difficulty
        )

        messages.success(request, "Flashcard created successfully")
        return redirect("flashcards")


@login_required(login_url="sign_in")
def reply_flashcard(request, id):
    try:
        flashcard = ChallengeFlashcard.objects.get(id=id)
        challenge_id = request.GET.get("challenge_id")
        is_correct = request.GET.get("is_correct")
        is_answered = request.GET.get("is_answered") or "True"

        if flashcard.flashcard.user == request.user:
            flashcard.is_answered = is_answered == "True"
            flashcard.is_correct = is_correct == "True"
            flashcard.save()
            messages.success(request, "Reply submitted successfully")
        else:
            messages.error(request, "You are not authorized to reply to this flashcard")
        return redirect("challenge", id=challenge_id)
    except ChallengeFlashcard.DoesNotExist:
        messages.error(request, "Flashcard not found")
        return redirect("challenges")
    except Exception:
        messages.error(request, "An error occurred")
        return redirect("challenges")


@login_required(login_url="sign_in")
def remove_flashcard(request, id):
    try:
        flashcard = Flashcard.objects.get(id=id)
        if flashcard.user == request.user:
            flashcard.delete()
            messages.success(request, "Flashcard removed successfully")
        else:
            messages.error(request, "You are not authorized to remove this flashcard")
        return redirect("flashcards")
    except Flashcard.DoesNotExist:
        messages.error(request, "Flashcard not found")
        return redirect("flashcards")
