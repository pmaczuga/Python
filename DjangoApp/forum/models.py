from django.db import models

class Category(models.Model):
    category_text = models.CharField(max_length = 200)

    def __str__(self):
        return self.category_text

class Thread(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thread_text = models.CharField(max_length = 200)
    thread_date = models.DateTimeField()
    thread_author = models.CharField(max_length = 200)

    def __str__(self):
        return self.thread_text

class Answer(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length = 1000)
    answer_date = models.DateTimeField()
    answer_author = models.CharField(max_length = 200)

    def __str__(self):
        return self.answer_text
