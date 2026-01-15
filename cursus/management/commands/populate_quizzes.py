from django.core.management.base import BaseCommand
from cursus.models import Course, Quiz, Question, Choice
import random

class Command(BaseCommand):
    help = 'Populate database with dummy quizzes if none exist'

    def handle(self, *args, **kwargs):
        courses = Course.objects.all()
        if not courses.exists():
            self.stdout.write(self.style.WARNING("Aucun cours trouvé. Veuillez d'abord créer des cours."))
            return

        for course in courses:
            if Quiz.objects.filter(course=course).exists():
                self.stdout.write(self.style.SUCCESS(f"Quiz déjà existant pour {course.titre}"))
                continue

            self.stdout.write(f"Création d'un quiz pour {course.titre}...")
            
            # Create Quiz
            quiz = Quiz.objects.create(
                course=course,
                title=f"Quiz de base - {course.titre}",
                description="Un petit quiz pour tester vos connaissances de base sur ce cours."
            )
            
            # Create Questions
            questions_data = [
                {
                    "text": "Quelle est la caractéristique principale de ce sujet ?",
                    "choices": [("C'est complexe", True), ("C'est simple", False), ("Aucune idée", False)]
                },
                {
                    "text": "En quelle année cette technologie est-elle devenue populaire ?",
                    "choices": [("2020", False), ("2010", True), ("1990", False)]
                },
                {
                    "text": "Qu'est-ce qui est vrai parmi ces affirmations ?",
                    "choices": [("A est vrai", True), ("B est vrai", False), ("Tout est faux", False)]
                }
            ]
            
            for q_data in questions_data:
                question = Question.objects.create(quiz=quiz, text=q_data["text"])
                choices = q_data["choices"]
                random.shuffle(choices)
                
                for choice_text, is_correct in choices:
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        is_correct=is_correct
                    )
            
            self.stdout.write(self.style.SUCCESS(f"Quiz créé pour {course.titre}"))

        self.stdout.write(self.style.SUCCESS("Opération terminée."))
