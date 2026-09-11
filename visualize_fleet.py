import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

fleet_data = [
    {"id": "Лок-1", "mileage": 15000, "defects": 1},
    {"id": "Лок-2", "mileage": 125000, "defects": 5},
    {"id": "Лок-3", "mileage": 82000, "defects": 3},
    {"id": "Лок-4", "mileage": 45000, "defects": 1},
    {"id": "Лок-5", "mileage": 115000, "defects": 4},
    {"id": "Лок-6", "mileage": 20000, "defects": 0},
    {"id": "Лок-7", "mileage": 150000, "defects": 6},
    {"id": "Лок-8", "mileage": 60000, "defects": 2},
    {"id": "Лок-9", "mileage": 95000, "defects": 4},
    {"id": "Лок-10", "mileage": 5000, "defects": 0},
]
df = pd.DataFrame(fleet_data)

sns.regplot(data=df, x="mileage", y="defects", color="darkred")
plt.title("Прогноз дефектаций подвижного состава")
plt.xlabel("Пробег (км)")
plt.ylabel("Количество выявленных дефектов")
plt.show()
