import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

exam_data = [
    {"id": "ВЛ80с-101", "type": "freight", "mileage": 50000, "cost": 120},
    {"id": "ВЛ80с-102", "type": "freight", "mileage": None, "cost": 150},
    {"id": "ЭП1М-201", "type": "suburban", "mileage": 120000, "cost": 300},
    {"id": "ЭП1М-202", "type": "suburban", "mileage": 85000, "cost": 210},
    {"id": "ЧС4Т-301", "type": "suburban", "mileage": 30000, "cost": 90},
    {"id": "2ТЭ25КМ-401", "type": "freight", "mileage": 110000, "cost": None},
    {"id": "2ТЭ25КМ-402", "type": "freight", "mileage": 15000, "cost": 40},
]
df = pd.DataFrame(exam_data)
df = df.dropna()
df = df.reset_index(drop=True)
df = df[df["mileage"] > 20000]
mean_cost = df.groupby("type")["cost"].mean()
print("Финальная информация о локомотивах:")
print(mean_cost)
sns.regplot(data=df, x="mileage", y="cost", color="blue")
plt.title("Зависимость стоимости ремонта от пробега")
plt.xlabel("Пробег (км)")
plt.ylabel("Стоимость ремонта (тыс. руб.)")
plt.show()
