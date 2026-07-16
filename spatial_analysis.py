import pandas as pd
import geopandas as gpd
from shapely import wkt

df = pd.read_csv("data/works.csv")

# даты
df["start_dt"] = pd.to_datetime(df["start_dt"], dayfirst=True)
df["end_dt"] = pd.to_datetime(df["end_dt"], dayfirst=True)

# поле geometry
df["geometry"] = (df["geom_a_wkt"]
    .fillna(df["geom_b_wkt"])
    .fillna(df["geom_c_wkt"])
)

# удаление записей без геометрии
df = df[df["geometry"].notna()].copy()

# Преобразуем WKT в геометрию
df["geometry"] = df["geometry"].apply(wkt.loads)

# GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

# проверка геометрии
gdf = gdf[gdf.geometry.is_valid].copy()

# три слоя
layer_A = gdf[gdf["dataset_code"] == "A"]
layer_B = gdf[gdf["dataset_code"] == "B"]
layer_C = gdf[gdf["dataset_code"] == "C"]

# веса приоритетов
priority_weights = {
    1: 4,
    2: 3,
    3: 2,
    4: 1
}

def priority_weight(p1, p2):
    w1 = priority_weights.get(int(p1), 1)
    w2 = priority_weights.get(int(p2), 1)
    return (w1 + w2) / 2


def overlap_days(a_start, a_end, b_start, b_end):
    start = max(a_start, b_start)
    end = min(a_end, b_end)

    if end < start:
        return 0

    return (end - start).days + 1


def spatial_overlap(g1, g2):
    inter = g1.intersection(g2)

    if inter.is_empty:
        return 0

    smaller = min(g1.area, g2.area)

    if smaller == 0:
        return 0

    return inter.area / smaller


def time_overlap(days, dur1, dur2):
    shorter = min(dur1, dur2)

    if shorter <= 0:
        return 0

    return days / shorter


def analyse_pair(layer1, layer2):
    rows = []

    for _, a in layer1.iterrows():
        for _, b in layer2.iterrows():

            if not a.geometry.intersects(b.geometry):
                continue

            days = overlap_days(
                a.start_dt,
                a.end_dt,
                b.start_dt,
                b.end_dt
            )

            temporal = days > 0

            if not temporal:
                continue

            s_overlap = spatial_overlap(
                a.geometry,
                b.geometry
            )

            d1 = (a.end_dt - a.start_dt).days + 1
            d2 = (b.end_dt - b.start_dt).days + 1

            t_overlap = time_overlap(
                days,
                d1,
                d2
            )

            score = (
                s_overlap *
                t_overlap *
                priority_weight(
                    a.priority,
                    b.priority
                )
            )

            rows.append({
                "dataset_1": a.dataset_code,
                "object_1": a.source_object_id,
                "dataset_2": b.dataset_code,
                "object_2": b.source_object_id,
                "spatial_intersection": True,
                "temporal_intersection": temporal,
                "overlap_days": days,
                "conflict_score": round(score, 3)
            })

    return pd.DataFrame(rows)

# анализ
ab = analyse_pair(layer_A, layer_B)
ac = analyse_pair(layer_A, layer_C)
bc = analyse_pair(layer_B, layer_C)

collisions = pd.concat(
    [ab, ac, bc],
    ignore_index=True
)

# сохранение
collisions.to_csv(
    "results/collisions.csv",
    index=False
)

print(collisions)
