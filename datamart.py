import pandas as pd
df = pd.read_csv("collisions.csv")

# тип пары
df["pair_type"] = (df["dataset_1"] + "*" + df["dataset_2"])

# тип коллизии
df["conflict_type"] = "Combined"

# критичность
df["critical"] = df["conflict_score"] >= 2

# приоритет пары
df["priority_group"] = (
    df["priority_1"].fillna(4)
    .astype(int)
    .astype(str)
    +
    "-"
    +
    df["priority_2"].fillna(4)
    .astype(int)
    .astype(str)
)

metrics = []

# количество по типам
for pair, group in df.groupby("pair_type"):

    metrics.append({
        "metric": f"collisions_{pair}",
        "value": len(group)
    })

# количество критичных
metrics.append({
    "metric":"critical_collisions",
    "value":df["critical"].sum()
})

# среднее перекрытие
metrics.append({
    "metric":"avg_overlap_days",
    "value":round(df["overlap_days"].mean(),2)
})

# максимум
metrics.append({
    "metric":"max_overlap_days",
    "value":df["overlap_days"].max()
})

# распределение по статусам
status = pd.concat([
    df["status_1"],
    df["status_2"]
])

for s,c in status.value_counts().items():
    metrics.append({
        "metric":f"status_{s}",
        "value":c
    })

# распределение по приоритетам
priority = pd.concat([
    df["priority_1"],
    df["priority_2"]
])

for p,c in priority.fillna(4).value_counts().sort_index().items():
    metrics.append({
        "metric":f"priority_{int(p)}",
        "value":c
    })

datamart = pd.DataFrame(metrics)

datamart.to_csv(
    "datamart.csv",
    index=False
)
files.download("datamart.csv")
print(datamart)
