from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

class Response(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    # Store responses to each question
    answers = models.ManyToManyField(Question, through='Answer')

    def __str__(self):
        return f"{self.name} {self.surname}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self):
        return f"{self.response.name}'s answer to {self.question.question_text}"
