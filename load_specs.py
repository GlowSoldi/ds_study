import pandas as pd
from sqlalchemy import create_engine

loco_specs = [
    {"id": "ВЛ80с-101", "route_type": "freight", "year": 1989},
    {"id": "ЭП1М-201", "route_type": "suburban", "year": 2007},
    {"id": "ЧС4Т-301", "route_type": "suburban", "year": 1978},
    {"id": "2ТЭ25КМ-401", "route_type": "freight", "year": 2015},
    {"id": "ВЛ80с-102", "route_type": "freight", "year": 1990},
    {"id": "ЭД9М-0134", "route_type": "suburban", "year": 2003},
]

engine = create_engine("postgresql://postgres:mentor@localhost:5432/railway")
df = pd.DataFrame(loco_specs)
df.to_sql("locomotives", engine, if_exists="replace", index=False)
print("Таблица спецификаций локомотивов успешно загружена в базу данных!")
