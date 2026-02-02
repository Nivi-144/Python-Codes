import tkinter as tk
root=tk.Tk()
root.title("Left & Right Car Model")
root.geometry("600x300")
canvas = tk.Canvas(root, width=600, height=300, bg="skyblue")
canvas.pack()
# Road
canvas.create_rectangle(0, 200, 600, 300, fill="gray")
#Car Parts
car_body = canvas.create_rectangle(100, 150, 300, 200, fill="red", outline="black")
car_top = canvas.create_rectangle(140, 120, 260, 150, fill="red", outline="black")
window1 = canvas.create_rectangle(150, 125, 190, 145, fill="lightblue")
window2 = canvas.create_rectangle(210, 125, 250, 145, fill="lightblue")
wheel1 = canvas.create_oval(130, 190, 170, 230, fill="black")
wheel2 = canvas.create_oval(230, 190, 270, 230, fill="black")
car_parts = [car_body, car_top, window1, window2, wheel1, wheel2]
#Movement Functions
def move_left(event=None):
    for part in car_parts:
        canvas.move(part, -10, 0)
def move_right(event=None):
    for part in car_parts:
        canvas.move(part, 10, 0)
#Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="⬅ Left", width=10, command=move_left).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Right ➡", width=10, command=move_right).grid(row=0, column=1, padx=10)
#Keyboard Bindings
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.mainloop()
