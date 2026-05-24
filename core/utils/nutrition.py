# Nutrition values per 100g (approximate, standard references)

NUTRITION_DATA = {

    # 🍕 Fast / Junk Foods
    "pizza": {"calories": 266, "carbs": 33, "protein": 11, "fat": 10},
    "hamburger": {"calories": 295, "carbs": 30, "protein": 17, "fat": 14},
    "french_fries": {"calories": 312, "carbs": 41, "protein": 3.4, "fat": 15},
    "hot_dog": {"calories": 290, "carbs": 4, "protein": 11, "fat": 26},
    "fried_rice": {"calories": 163, "carbs": 20, "protein": 4.3, "fat": 6},

    # 🍰 Desserts / Sweets
    "apple_pie": {"calories": 237, "carbs": 34, "protein": 2.4, "fat": 11},
    "cheesecake": {"calories": 321, "carbs": 22, "protein": 6, "fat": 25},
    "chocolate_cake": {"calories": 371, "carbs": 58, "protein": 5, "fat": 15},
    "cup_cakes": {"calories": 305, "carbs": 45, "protein": 3.8, "fat": 14},
    "donuts": {"calories": 452, "carbs": 51, "protein": 4.9, "fat": 25},
    "ice_cream": {"calories": 207, "carbs": 24, "protein": 3.5, "fat": 11},
    "waffles": {"calories": 291, "carbs": 33, "protein": 7.9, "fat": 14},
    "pancakes": {"calories": 227, "carbs": 28, "protein": 6, "fat": 9},

    # 🥗 Healthy / Low Fat Foods
    "greek_salad": {"calories": 106, "carbs": 4, "protein": 2, "fat": 9},
    "caesar_salad": {"calories": 190, "carbs": 7, "protein": 6, "fat": 16},
    "grilled_salmon": {"calories": 208, "carbs": 0, "protein": 20, "fat": 13},
    "omelette": {"calories": 154, "carbs": 1.6, "protein": 11, "fat": 12},
    "sushi": {"calories": 130, "carbs": 28, "protein": 3, "fat": 0.5},

    # 🇮🇳 Indian Food (BIG PLUS)
    "samosa": {"calories": 262, "carbs": 32, "protein": 5, "fat": 14},

    # 🍞 General
    "bread": {"calories": 265, "carbs": 49, "protein": 9, "fat": 3},
}

def get_nutrition(food_name):
    food_name = food_name.lower()

    return NUTRITION_DATA.get(
        food_name,
        {
            "calories": 200,
            "carbs": 30,
            "protein": 6,
            "fat": 5
        }
    )
