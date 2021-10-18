def recommend(age, budget, action, comedy):
    if (age < 18) or (budget < 10):
        return "T"
    elif action == +1:
        return "T"
    else:
        return "AH"