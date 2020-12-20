import telebot
import datetime

def convertDate(date):
    splittedDateString = [int(x) for x in date.split(".")]
    return datetime.date(
        int(splittedDateString[2]),
        int(splittedDateString[1]),
        int(splittedDateString[0])
    )

def generate_keyboards(days = ['20.12.2020', '22.12.2020', '25.12.2020', '1.1.2021'], nameArg = "tasklist", additional = "_0"):
    previousDay = 0
    weeks = []
    keyboardWeek = []
    for date in days:
        currentDate = convertDate(date)
        if currentDate.weekday() > previousDay:
            keyboardWeek.append(date)
        else:
            if len(keyboardWeek) > 0:
                weeks.append(keyboardWeek.copy())
                keyboardWeek.clear()
            keyboardWeek.append(date)
        previousDay = currentDate.weekday()
    if len(keyboardWeek) > 0:
        weeks.append(keyboardWeek.copy())


    if len(weeks) > 1:
        for i in range(len(weeks)):
            if i < len(weeks) - 1:
                weeks[i].append("👉🏿")
            if i > 0:
                weeks[i].insert(0, "👈🏿")


    keyboards = []
    for i in range(len(weeks)):
        keyboard = telebot.types.InlineKeyboardMarkup()
        for day in weeks[i]:
            keyboard.add(telebot.types.InlineKeyboardButton(text=str(day), callback_data=f"{nameArg}_{str(day)}_{i}{additional}"))
        keyboards.append(keyboard)

    return keyboards