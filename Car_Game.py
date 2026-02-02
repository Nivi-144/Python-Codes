import tkinter as tk
import random
#Window   
root = tk.Tk()
root.title("Red Ferrari Snow Catcher")
root.geometry("700x500")
canvas = tk.Canvas(root, width=700, height=500, bg="skyblue")
canvas.pack()
#Road
canvas.create_rectangle(0, 380, 700, 500, fill="gray")
#Ferrari Car 
car_x = 300
car_y = 340
car_body = canvas.create_rectangle(
    car_x, car_y,
    car_x + 140, car_y + 45,
    fill="red", outline="black", width=2
)
car_top = canvas.create_rectangle(
    car_x + 30, car_y - 30,
    car_x + 110, car_y,
    fill="red", outline="black", width=2
)
wheel1 = canvas.create_oval(
    car_x + 20, car_y + 35,
    car_x + 50, car_y + 65,
    fill="black"
)
wheel2 = canvas.create_oval(
    car_x + 90, car_y + 35,
    car_x + 120, car_y + 65,
    fill="black"
)
car_parts = [car_body, car_top, wheel1, wheel2]
#Score
score = 0
score_text = canvas.create_text(
    10, 10, anchor="nw",
    text="Score: 0",
    font=("Arial", 14, "bold")
)
#Snowflakes
snowflakes = []
def create_snowflake():
    x = random.randint(20, 650)
    flake = canvas.create_oval(
        x, 0,
        x + 20, 20, 
        fill="magenta", outline=""
    )
    snowflakes.append(flake)
def move_snowflakes():
    global score
    for flake in snowflakes[:]:
        canvas.move(flake, 0, 6)
        fx1, fy1, fx2, fy2 = canvas.coords(flake)
        cx1, cy1, cx2, cy2 = canvas.coords(car_body)
        # Collision detection
        if fx2 > cx1 and fx1 < cx2 and fy2 > cy1 and fy1 < cy2:
            canvas.delete(flake)
            snowflakes.remove(flake)
            score += 1
            canvas.itemconfig(score_text, text=f"Score: {score}")
        elif fy1 > 500:
            canvas.delete(flake)
            snowflakes.remove(flake)
    if random.randint(1, 8) == 1:
        create_snowflake()
    root.after(40, move_snowflakes)
# Car Movement
def move_left(event):
    if canvas.coords(car_body)[0] > 0:
        for part in car_parts:
            canvas.move(part, -25, 0)
def move_right(event):
    if canvas.coords(car_body)[2] < 700:
        for part in car_parts:
            canvas.move(part, 25, 0)
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
#Start Game
move_snowflakes()
root.mainloop()
