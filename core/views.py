from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import FoodRecord
from django.core.files.storage import FileSystemStorage
from .models import FoodRecord
from .ml.predict import predict_food
import os
import uuid
from django.conf import settings
from .utils.nutrition import get_nutrition
from .utils.disease_rules import diabetes_rule, fatty_liver_rule, obesity_rule
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 🔐 Hardcoded admin credentials
        if username == "admin" and password == "admin":
            request.session['admin_logged_in'] = True
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid Admin Credentials")

    return render(request, "admin/admin_login.html")


def admin_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect("admin_login")

    records = FoodRecord.objects.select_related('user').order_by('-created_at')

    context = {
        "records": records,
        "total_records": records.count(),
    }
    return render(request, "admin/admin_dashboard.html", context)



def admin_logout(request):
    request.session.flush()
    return redirect("landing")


def landing_page(request):
    return render(request, 'landing.html')


def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'register.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid login credentials")

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('landing')


@login_required(login_url='login')
def user_dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url='login')
def upload_food(request):

    if request.method == "POST" and request.FILES.get("food_image"):

        image = request.FILES["food_image"]

        # 🔹 Generate unique filename (VERY IMPORTANT)
        unique_filename = str(uuid.uuid4()) + "_" + image.name

        fs = FileSystemStorage()
        filename = fs.save(unique_filename, image)
        image_path = os.path.join(settings.MEDIA_ROOT, filename)

        # 🔹 ML prediction
        try:
            food_name, confidence = predict_food(image_path)
        except Exception as e:
            print("Prediction Error:", e)
            return render(request, "upload.html", {
                "error": "Model prediction failed. Try again."
            })

        # 🔹 Nutrition values
        nutrition = get_nutrition(food_name)

        calories = nutrition.get("calories", 0)
        carbs = nutrition.get("carbs", 0)
        protein = nutrition.get("protein", 0)
        fat = nutrition.get("fat", 0)

        # 🔹 Disease rules
        diabetes_msg = diabetes_rule(carbs)
        fatty_liver_msg = fatty_liver_rule(fat)
        obesity_msg = obesity_rule(calories)

        # 🔹 Save to DB
        record = FoodRecord.objects.create(
            user=request.user,
            food_image=filename,
            food_name=food_name,
            calories=calories,
            carbs=carbs,
            protein=protein,
            fat=fat,
            diabetes_suggestion=diabetes_msg,
            fatty_liver_suggestion=fatty_liver_msg,
            obesity_suggestion=obesity_msg,
            confidence=confidence
        )

        # 🔥 Instead of session → pass id in URL (better)
        return redirect("result_page", record_id=record.id)

    return render(request, "upload.html")
    
    
@login_required(login_url='login')
def result_page(request, record_id):

    try:
        record = FoodRecord.objects.get(id=record_id, user=request.user)
    except FoodRecord.DoesNotExist:
        return redirect("upload_food")

    return render(request, "result.html", {
        "record": record
    })
