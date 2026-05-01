from tkinter import *
import math, sys, os

YELLOW = "#FFF1D3"
ORANGE = "#FFB090"
PINK = "#CA5995"
PURPLE = "#5D1C6A"

FONT_NAME = "Courier"

WORK_MINS = 25
BREAK_MINS = 5
LONG_BREAK_MINS = 20
SEC_PER_ROUND = 60

pomodoro_time = 0
pomodoro_round = 0
pomodoro_round_type = "Idle"
timer = None

def run_timer():
    global pomodoro_time, timer
    update_ui()
    pomodoro_time -= 1
    if not timer == None:
        window.after_cancel(timer)
    timer = window.after(1000, run_timer)

def start_round():
    global pomodoro_time, pomodoro_round, pomodoro_round_type
    if pomodoro_round_type == "Idle" or pomodoro_round_type == "Break" \
        or pomodoro_round_type == "Long Break":
        pomodoro_round_type = "Work"
    elif pomodoro_round_type == "Work":
        if pomodoro_round % 8 == 0:
            pomodoro_round = "Long Break"
        else:
            pomodoro_round_type = "Break"

    pomodoro_round += 1
    if pomodoro_round_type == "Work":
        pomodoro_time = WORK_MINS * SEC_PER_ROUND
    if pomodoro_round_type == "Break":
        pomodoro_time = BREAK_MINS * SEC_PER_ROUND
    if pomodoro_round_type == "Long Break":
        pomodoro_time = LONG_BREAK_MINS * SEC_PER_ROUND

    ticks = int((pomodoro_round-1)/2)
    canvas.itemconfig(lbl_ticks,text=f"{'✔'*ticks}")
    # print(pomodoro_round, pomodoro_round_type, f"{'✔'*ticks}")

    run_timer()

def reset_round():
    global pomodoro_time, pomodoro_round, pomodoro_round_type
    pomodoro_round_type = "Idle"
    pomodoro_round = 0
    pomodoro_time = 0
    update_ui()

def update_ui():
    mins = math.floor(pomodoro_time / 60)
    sec = math.floor(pomodoro_time % 60)

    if mins <= 0 and sec <= 0:
        start_round()
        return 

    if sec <= 9:
        sec = '0' + str(sec)
    
    if mins <= 9:
        mins = '0' + str(mins)

    canvas.itemconfig(lbl_timer,text=f"{mins}:{sec}")
    canvas.itemconfig(lbl_title,text=pomodoro_round_type)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

window = Tk()
window.minsize(width=400, height=400)
window.configure(bg=YELLOW) 
window.title("Pomodoro Timer")



canvas = Canvas(width=400, height=400, bg=PINK, highlightthickness=0)
image = PhotoImage(file=resource_path("tomato.png"))

canvas.create_image(200,200, image=image)
lbl_title = canvas.create_text(200,50,text=pomodoro_round_type, font=(FONT_NAME,30,"bold"),fill="white")
lbl_timer = canvas.create_text(200,220,text="00:00", font=(FONT_NAME,35,"bold"),fill="white")
lbl_ticks = canvas.create_text(200,265,text="", font=(FONT_NAME,14,"bold"),fill="green")
canvas.place(x=200, y=200, anchor="center")

btn_start = Button(text=" Start ", bg=PURPLE, font=(FONT_NAME,12), fg="white", command=start_round)
btn_restart = Button(text="Restart", bg=PURPLE, font=(FONT_NAME,12), fg="white", command=reset_round)
btn_start.place(x=100, y=350, anchor="center")
btn_restart.place(x=300, y=350, anchor="center")



window.mainloop()