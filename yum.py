import pandas as pd
import random

data = []

# -------- SAFE (80 rows) --------
for _ in range(80):
    data.append({
        "mq2": random.randint(100, 400),   # heavy overlap
        "mq7": random.randint(50, 220),
        "mq135": random.randint(120, 380),
        "flame": random.choice([1,1,1,1,0]),  # small sensor error
        "temperature": random.randint(22, 45),
        "humidity": random.randint(30, 80),
        "status": "SAFE"
    })

# -------- WARNING (70 rows) --------
for _ in range(70):
    data.append({
        "mq2": random.randint(250, 600),
        "mq7": random.randint(150, 350),
        "mq135": random.randint(250, 600),
        "flame": random.choice([1,1,0]),    # noisy flame
        "temperature": random.randint(35, 60),
        "humidity": random.randint(20, 85),
        "status": "WARNING"
    })

# -------- FIRE (50 rows) --------
for _ in range(50):
    data.append({
        "mq2": random.randint(300, 900),
        "mq7": random.randint(200, 500),
        "mq135": random.randint(400, 1000),
        "flame": random.choice([0,0,0,1]),  # occasional miss detection
        "temperature": random.randint(45, 75),
        "humidity": random.randint(15, 70),
        "status": "FIRE"
    })

# ---------- Label Noise (Important) ----------
# Randomly change 10% labels to simulate real-world mistakes
for i in range(int(len(data) * 0.10)):
    idx = random.randint(0, len(data)-1)
    data[idx]["status"] = random.choice(["SAFE", "WARNING", "FIRE"])

df = pd.DataFrame(data)
df.to_csv("fire_dataset_200.csv", index=False)

print("Dataset created with strong noise and overlap")
