from async_study.flashcards.models import Category, Flashcard
from django.contrib.auth.models import User
from django.db import models


class Challenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    difficulty = models.CharField(max_length=1, choices=Flashcard.difficulty_choices)
    questions_qt = models.PositiveIntegerField(default=1)
    flashcards = models.ManyToManyField(Flashcard, through="ChallengeFlashcard")

    def is_answered(self):
        return ChallengeFlashcard.objects.filter(challenge=self, is_answered=True).count() == self.questions_qt

    def __str__(self):
        return self.title


class ChallengeFlashcard(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    is_answered = models.BooleanField(default=False)

    class Meta:
        unique_together = ("challenge", "flashcard")
        verbose_name = "Challenge Flashcard"
        verbose_name_plural = "Challenge Flashcards"
        constraints = [models.UniqueConstraint(fields=["challenge", "flashcard"], name="unique_challenge_flashcard")]

    def __str__(self):
        return f"{self.challenge} - {self.flashcard}"
