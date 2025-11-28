#Taking input from user.
gender = str(input("What's your gender : "))
age = float(input("How old are you : "))
weight = float(input("Enter your weight(KG) : "))
height = float(input("Enter your height(m) : "))
print("\nchoose you goal")   #asking user whats their goal.
print("1.weight loss")
print("2.weight gain")
print("3.muscle gain")
print("4.maintaince")
goals = [["weight loss", 1], ["weight gain", 2],
             ["muscle gain", 3], ["maintaince", 4]]     

enter_goal = int(input("enter number of specified goal : "))    #input for user to enter their specific goal

BMI = weight/(height**2)    # calculation of BMI

height_in_cm = 100*height      #converted height in cm.

if gender.lower() == "male":     #BMR IS  differnt for male and female. calculated bmr    
    BMR = (10*weight) + (6.25*height_in_cm) - (5*age) + 5
elif gender.lower() == "female":
    BMR = (10*weight) + (6.25*height_in_cm) - (5*age) - 161
else:
    print("none")               #for other than male and female
activity_levels = [["1.sedentary(little/no excercise)",1],
                  ["2.Lightly active(light excercise (1-3)Days/week)", 2],
                  ["3.Moderately Excercise(Exercise (3-5)Days/week", 3],
                  ["4.very active(Hard exercise (6-7)days/week)", 4],
                  ["5.super active (Very hard training / athlete)", 5]]
print("\nActivity levels")
for level in range(0,len(activity_levels)):
    activity_level = activity_levels[level]

    print(activity_level[0])
activity_type = int(input("\nenter your activity type(enter No.) : "))
if activity_type == 1:
    activity_multiplier = 1.2
elif activity_type == 2:
    activity_multiplier = 1.375
elif activity_type == 3:
    activity_multiplier = 1.55
elif activity_type == 4:
    activity_multiplier = 1.725
else:
    activity_multiplier = 1.9
tdee = BMR * activity_multiplier       #appox how much calorie we burn in aday
# print("your body mass index : ", BMI)
# print("your body metabolic rate : ", BMR)
print("\nyour total energy expenditure is (TDEE) : ", tdee)


def goal_for_fitness():
    for val in range(0,len(goals)):
        goal = goals[val]
        if enter_goal == goal[1]:
            return goal[0]
user_goal = goal_for_fitness()      #this for understand whats the user goal

def calculations(tdee,user_goal,goal_dataframes):
    user_goal = user_goal.lower()
    row = goal_dataframes[goal_dataframes["goal"].str.lower() == user_goal]
    protien_percent = float(row["protien"].iloc[0])
    carb_percent = float(row["carb"].iloc[0])
    fat_percent = float(row["fat"].iloc[0])
    
#according to user goal how much calories required for user per day.
    if enter_goal == 1:
        calories_required = tdee - 300
    
    elif enter_goal == 2 :
        calories_required = tdee + 300

    elif enter_goal == 3:
        calories_required = tdee + 150
    else:
        calories_required = tdee

    protien_grams = (calories_required * (protien_percent)/100)/4
    carb_grams = (calories_required * (carb_percent)/100)/4
    fat_grams = (calories_required * (fat_percent)/100)/9
    return calories_required, protien_grams, carb_grams, fat_grams


from data_loader import goal_dataframes      #this is for taking data from data loader file.


total_required_calories = calculations(tdee,user_goal,goal_dataframes)    
cal, protien_g, carb_g, fat_g = total_required_calories    #converting tupple format to string format
print("\n~~~~~~~~ Total you requires ~~~~~~~~")
print(f"\nTotal calories required per day to {user_goal} : {round(cal)} kcal")
print(f"Total grams of protien required per day to {user_goal} : {round(protien_g)} g")
print(f"Total grams of carb required per day to {user_goal} : {round(carb_g)} g")
print(f"Total grams of fat required per day to {user_goal} : {round(fat_g)} g")



        

        











