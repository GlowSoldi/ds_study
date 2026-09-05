import pandas as pd

train_fleet = [
    {"id": "ЧС4Т-210", "route_type": "suburban", "mileage": 15000, "defects": 0},
    {"id": "ВЛ80с-104", "route_type": "freight", "mileage": 125000, "defects": 3},
    {"id": "ЭП1М-645", "route_type": "suburban", "mileage": 82000, "defects": 1},
    {"id": "2ТЭ25КМ-012", "route_type": "freight", "mileage": 45000, "defects": 0},
    {"id": "ЭД9М-0134", "route_type": "suburban", "mileage": 115000, "defects": 4},
]
df = pd.DataFrame(train_fleet)
depot_data = [
    {
        "route_type": "suburban",
        "depot_name": "ТЧ-1 (Моторвагонное)",
        "manager": "Иванов А.В.",
    },
    {
        "route_type": "freight",
        "depot_name": "ТЧ-4 (Эксплуатационное)",
        "manager": "Петров В.С.",
    },
]
depots_df = pd.DataFrame(depot_data)
full_fleet_info = pd.merge(df, depots_df, on="route_type", how="left")
print("Полная информация о локомотивах и депо:")
print(full_fleet_info)
