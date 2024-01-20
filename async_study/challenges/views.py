from async_study.flashcards.models import Category, Flashcard
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Challenge, ChallengeFlashcard


@login_required(login_url="sign_in")
def challenges(request):
    difficulties = [{"value": d[0], "label": d[1]} for d in Flashcard.difficulty_choices]
    categories = Category.objects.all()
    challenges = Challenge.objects.filter(user=request.user)

    category = request.GET.get("category") or ""
    difficulty = request.GET.get("difficulty") or ""
    status = request.GET.get("status") or ""
    if category:
        challenges = challenges.filter(categories__id=category)
    if difficulty:
        challenges = challenges.filter(difficulty=difficulty)
    if status:
        status = status == "True"
        challenges = [c for c in challenges if c.is_answered() == status]
    return render(
        request,
        "challenges.html",
        {
            "challenges": challenges,
            "categories": categories,
            "difficulties": difficulties,
            "f": {
                "category": category,
                "difficulty": difficulty,
                "status": status,
            },
        },
    )


@login_required(login_url="sign_in")
def start_challenge(request):
    difficulties = [{"value": d[0], "label": d[1]} for d in Flashcard.difficulty_choices]
    categories = Category.objects.all()
    if request.method == "POST":
        title = request.POST.get("title") or ""
        post_categories = request.POST.getlist("categories") or []
        difficulty = request.POST.get("difficulty") or ""
        questions_qt = request.POST.get("questions_qt") or ""
        questions_qt = int(questions_qt) if questions_qt.isdigit() else 0

        if len(title.strip()) == 0 or len(post_categories) == 0 or len(difficulty.strip()) == 0:
            messages.error(request, "All fields are required")
            return redirect("start_challenge")
        if questions_qt < 1:
            messages.error(request, "Invalid number of questions")
            return redirect("start_challenge")
        if True not in [d["value"] == difficulty for d in difficulties]:
            messages.error(request, "Invalid difficulty")
            return redirect("start_challenge")
        post_categories = categories.filter(id__in=post_categories)
        if not post_categories.exists():
            messages.error(request, "Category not found")
            return redirect("start_challenge")

        flashcards = Flashcard.objects.filter(
            user=request.user, category__in=post_categories, difficulty=difficulty
        ).order_by("?")[:questions_qt]
        if not flashcards.exists():
            messages.error(request, "No flashcards found")
            return redirect("start_challenge")
        if flashcards.count() < questions_qt:
            messages.warning(request, "Not enough flashcards found")

        try:
            challenge = Challenge.objects.create(
                user=request.user,
                title=title,
                questions_qt=flashcards.count(),
                difficulty=difficulty,
            )
            for flashcard in flashcards:
                challenge.categories.add(flashcard.category)
                ChallengeFlashcard.objects.create(challenge=challenge, flashcard=flashcard)
        except Exception:
            messages.error(request, "Error creating challenge")
            return redirect("start_challenge")
        messages.success(request, "Challenge created successfully")
        return redirect("challenge", id=challenge.id)
    return render(request, "start_challenge.html", {"categories": categories, "difficulties": difficulties})


@login_required(login_url="sign_in")
def challenge(request, id):
    try:
        challenge = Challenge.objects.get(id=id, user=request.user)
        flashcards = ChallengeFlashcard.objects.filter(challenge=challenge)
        answered_flashcards = flashcards.filter(is_answered=True)
        not_answered_flashcards = flashcards.filter(is_answered=False).count()
        correct = answered_flashcards.filter(is_correct=True).count()
        incorrect = answered_flashcards.filter(is_correct=False).count()
        return render(
            request,
            "challenge.html",
            {
                "challenge": challenge,
                "flashcards": flashcards,
                "correct": correct,
                "incorrect": incorrect,
                "not_answered_flashcards": not_answered_flashcards,
            },
        )
    except Challenge.DoesNotExist:
        messages.error(request, "Challenge not found")
        return redirect("challenges")
    except Exception as e:
        print(e)
        messages.error(request, "Error loading challenge")
        return redirect("challenges")


@login_required(login_url="sign_in")
def remove_challenge(request, id):
    try:
        challenge = Challenge.objects.get(id=id, user=request.user)
        challenge.delete()
        messages.success(request, "Challenge removed successfully")
        return redirect("challenges")
    except Challenge.DoesNotExist:
        messages.error(request, "Challenge not found")
        return redirect("challenges")
    except Exception:
        messages.error(request, "Error removing challenge")
        return redirect("challenges")


@login_required(login_url="sign_in")
def report(request, challenge_id):
    try:
        challenge = Challenge.objects.get(id=challenge_id, user=request.user)

        flashcards = ChallengeFlashcard.objects.filter(challenge=challenge)
        answered_flashcards = flashcards.filter(is_answered=True)
        not_answered_flashcards = flashcards.filter(is_answered=False).count()
        correct = answered_flashcards.filter(is_correct=True).count()
        incorrect = answered_flashcards.filter(is_correct=False).count()
        data = [correct, incorrect, not_answered_flashcards]

        categories = challenge.categories.all()
        category_names = [category.name for category in categories]
        data2 = [flashcards.filter(flashcard__category=category, is_correct=True).count() for category in categories]
        data2_incorrect = [
            answered_flashcards.filter(flashcard__category=category, is_correct=False).count()
            for category in categories
        ]

        def category_object(category):
            index = category_names.index(category.name)
            return {
                "name": category.name,
                "correct": data2[index],
                "incorrect": data2_incorrect[index],
            }

        worst_categories = [
            categories[i] for i in range(len(categories)) if data2[i] == 0 or data2_incorrect[i] >= data2[i] * 0.5
        ]
        best_categories = [category_object(category) for category in categories if category not in worst_categories]
        worst_categories = [category_object(category) for category in worst_categories]

        return render(
            request,
            "report.html",
            {
                "challenge": challenge,
                "data": data,
                "data2": data2,
                "category_names": category_names,
                "worst_categories": worst_categories,
                "best_categories": best_categories,
            },
        )
    except Challenge.DoesNotExist:
        messages.error(request, "Challenge not found")
        return redirect("challenge", id=challenge_id)
    except Exception:
        messages.error(request, "Error loading challenge")
        return redirect("challenge", id=challenge_id)
