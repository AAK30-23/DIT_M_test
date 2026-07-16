# Street Collision Analysis

Тестовое задание, направленное на поиск пространственно-временных коллизий между городскими работами, анализ качества исходных данных и формированию аналитической витрины для последующего использования в BI-системах. Работа выполнена в среде Google Colab.

## Структура проекта

```
.
|-- data
│   |-- street_cases.csv
│
|-- out
│   |-- collisions.csv
│   |-- datamart.csv
│
├-- src
│   |-- spatial_analysis.py
│   |-- datamart.py
│   |-- quality_analysis.sql
│
|-- report.md
|-- README.md
```

## Стек технологий

- Python 3.11+
- pandas
- GeoPandas
- Shapely

## Необходимые библиотеки

```bash
pip install pandas geopandas shapely
```

### Проверка качества данных

```
src/quality_analysis.sql
```

для поиска:

- дубликатов;
- пропусков;
- некорректных дат;
- отсутствующей геометрии.

## Запуск в Google Colab

### 1. Откройте Colab

Перейдите по ссылке: [colab.research.google.com](https://colab.research.google.com)

Создайте новый ноутбук: **File → New Notebook**

### 2. Установите зависимости

```python
!pip install geopandas shapely
```

### 3. Загрузите данные

```python
from google.colab import files
uploaded = files.upload()
# Выберите файл street_cases.csv
```


### 4. Загрузите и выполните скрипты

**Скопируйте содержимое `src/spatial_analysis.py` в ячейку и выполните.**

**Скопируйте содержимое `src/datamart.py` в следующую ячейку и выполните.**

## Логика решения

В качестве коллизии рассматривается ситуация, когда две работы одновременно:

- пересекаются в пространстве;
- выполняются в один и тот же период времени.

Для оценки силы конфликта используется показатель

```
Conflict Score = SpatialOverlap * TimeOverlap * PriorityWeight
```

где:

- SpatialOverlap - доля площади пересечения;
- TimeOverlap - доля временного перекрытия;
- PriorityWeight - средний вес приоритетов двух работ.

## Результаты

| Файл | Описание |
|------|----------|
| collisions.csv | Таблица всех выявленных коллизий |
| datamart.csv | Агрегированные показатели для BI |

## Визуализация результатов
Dashboard.bpix
<img width="1117" height="627" alt="image" src="https://github.com/user-attachments/assets/0864579d-548c-4bd9-bdcf-32c37ec0b91a" />

