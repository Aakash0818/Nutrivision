def diabetes_rule(carbs):
    if carbs > 40:
        return "Not suitable for diabetic patients"
    return "Can be consumed in moderation"

def fatty_liver_rule(fat):
    if fat > 12:
        return "Avoid or consume very rarely"
    return "Suitable in limited quantity"

def obesity_rule(calories):
    if calories > 300:
        return "High calorie food – avoid frequent intake"
    return "Moderate calorie food"
