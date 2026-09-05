train_fleet = [
    {"id": "ЧС4Т-210", "route_type": "suburban", "mileage": 15000, "defects": 0},
    {"id": "ВЛ80с-104", "route_type": "freight", "mileage": 125000, "defects": 3},
    {"id": "ЭП1М-645", "route_type": "suburban", "mileage": 82000, "defects": 1},
    {"id": "2ТЭ25КМ-012", "route_type": "freight", "mileage": 45000, "defects": 0},
    {"id": "ЭД9М-0134", "route_type": "suburban", "mileage": 115000, "defects": 4},
]


def analyze_fleet(fleet_data):
    bad_trains = []
    for train in fleet_data:
        if train["route_type"] == "suburban" and train["mileage"] > 50000:
            bad_trains.append(train["id"])
    return bad_trains


bad_trains = analyze_fleet(train_fleet)
print("Локомотивы требующие проверки:")
for train_id in bad_trains:
    print(f"Наименование: {train_id}")
