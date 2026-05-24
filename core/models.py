from django.db import models
from django.contrib.auth.models import User

class FoodRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    food_image = models.ImageField(upload_to='food_images/')
    food_name = models.CharField(max_length=200)

    calories = models.FloatField()
    
    carbs = models.FloatField(help_text="Carbohydrates (g)")
    protein = models.FloatField(help_text="Protein (g)")
    fat = models.FloatField(help_text="Fat (g)")

    diabetes_suggestion = models.CharField(max_length=200)
    fatty_liver_suggestion = models.CharField(max_length=200)
    obesity_suggestion = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    confidence = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.food_name


