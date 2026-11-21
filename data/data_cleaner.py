import numpy as np
import pandas as pd

survey_data = pd.read_csv("raw_data/Survey_results.csv")
survey_data.columns = ["id", "time", "status", "age", "road_min", "house_min", "food_min",
                       "sleep_h", "task_min", "walk_min", "hobby_min", "passive_min",
                       "scroll_min", "overdue_tasks", "productivity_score",
                       "satisfaction", "own_tasks"]

age_is_impossible = survey_data["age"] > 100
survey_data["age"] = np.where(age_is_impossible, np.nan, survey_data["age"])

sleep_is_minutes = survey_data["sleep_h"] > 24
survey_data["sleep_h"] = np.where(sleep_is_minutes, survey_data["sleep_h"] / 60, survey_data["sleep_h"])

sleep_is_impossible = survey_data["sleep_h"] < 3
survey_data["sleep_h"] = np.where(sleep_is_impossible, np.nan, survey_data["sleep_h"])

hobby_is_impossible = survey_data["hobby_min"] > 480
survey_data["hobby_min"] = np.where(hobby_is_impossible, np.nan, survey_data["hobby_min"])

passive_is_impossible = survey_data["passive_min"] > 480
survey_data["passive_min"] = np.where(passive_is_impossible, np.nan, survey_data["passive_min"])

survey_data["satisfaction"] = survey_data["satisfaction"].str.replace("  ", " ")
survey_data["status"] = survey_data["status"].str.strip()

short_satisfaction_labels = {
    "Не устраивает, но не знаю, как изменить/не хватает инструментов для изменений": "Не устраивает, нет инструментов",
    "Частично устраивает, хочу оптимизировать расписание": "Частично, хочу оптимизировать",
    "Частично устраивает, не хочу ничего менять": "Частично, не хочу менять",
    "Полностью устраивает, ничего менять не нужно": "Полностью устраивает",
    "Не устраивает, но не хочу ничего менять": "Не устраивает, не хочу менять",
}
survey_data["satisfaction"] = survey_data["satisfaction"].map(short_satisfaction_labels)

survey_data.to_csv("processed_data/survey_clean.csv", index=False)