import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["axes.axisbelow"] = True #глобально кладёт сетку под все элементы

cleaned_survey = pd.read_csv("processed_data/survey_clean.csv")
satisfaction_order = ["Не устраивает, нет инструментов", "Частично, хочу оптимизировать",
                      "Частично, не хочу менять", "Полностью устраивает", "Не устраивает, не хочу менять"]
status_order = ["Учусь", "Совмещаю учёбу с работой", "Временно не работаю и не учусь"]

satisfaction_counts = cleaned_survey["satisfaction"].value_counts().loc[satisfaction_order]
plot_order = satisfaction_order[::-1]
plot_counts = satisfaction_counts.loc[plot_order]
plt.figure(figsize=(9, 4))
plt.barh(plot_order, list(plot_counts), color="steelblue")
plt.xlim(0, satisfaction_counts.max() * 1.3)
for position, value in enumerate(plot_counts):
    plt.text(value + 0.3, position, f"{value} · {value / len(cleaned_survey) * 100:.1f}%".replace(".", ","), va="center")
plt.title(f"Удовлетворённость распределением времени (n={len(cleaned_survey)})")
plt.xlabel("Число ответов")
plt.grid()
plt.tight_layout()
plt.savefig("graphics/Satisfaction_with_time_management.png", dpi=200)
plt.close()

status_counts_table = pd.crosstab(cleaned_survey["status"], cleaned_survey["satisfaction"]).loc[status_order, satisfaction_order]
status_shares = pd.crosstab(cleaned_survey["status"], cleaned_survey["satisfaction"], normalize="index").loc[status_order, satisfaction_order] * 100
status_sizes = cleaned_survey["status"].value_counts()
wrapped_status_names = {
    "Учусь": "Учусь",
    "Совмещаю учёбу с работой": "Совмещаю учёбу\nс работой",
    "Временно не работаю и не учусь": "Временно не работаю\nи не учусь",
}
status_labels = [f"{wrapped_status_names[status]}\nn={status_sizes[status]}" for status in status_order]
plt.figure(figsize=(10, 5))
accumulated_bottom = np.zeros(len(status_order))
for category in satisfaction_order:
    category_values = np.array(status_shares[category])
    plt.bar(status_labels, category_values, bottom=accumulated_bottom, label=category)
    for position, value in enumerate(category_values):
        if value > 0:
            plt.text(position, accumulated_bottom[position] + value / 2, f"{value:.1f}%".replace(".", ","), ha="center", va="center", fontsize=8, color="white")
    accumulated_bottom = accumulated_bottom + category_values
plt.ylim(0, 100)
plt.ylabel("Доля ответов, %")
plt.title("Удовлетворённость по статусу")
plt.grid()
plt.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=8)
plt.tight_layout()
plt.savefig("graphics/Satisfaction_by_status.png", dpi=200)
plt.close()

activities = {"Дорога": "road_min", "Быт": "house_min", "Готовка и еда": "food_min",
              "Прогулки": "walk_min", "Хобби": "hobby_min",
              "Пассивный отдых": "passive_min", "Скроллинг": "scroll_min"}
time_medians = cleaned_survey[list(activities.values())].median()
plot_activity_names = list(activities.keys())[::-1]
plot_median_values = list(time_medians)[::-1]
plt.figure(figsize=(9, 4))
plt.barh(plot_activity_names, plot_median_values, color="seagreen")
plt.xlim(0, time_medians.max() * 1.2)
for position, value in enumerate(plot_median_values):
    plt.text(value + 1, position, f"{value:g} мин".replace(".", ","), va="center")
sleep_median = cleaned_survey["sleep_h"].median()
plt.title(f"Медианные затраты времени в день (сон: {sleep_median:g} ч)".replace(".", ","))
plt.xlabel("Минуты в день")
plt.grid()
plt.tight_layout()
plt.savefig("graphics/Median_time_per_day.png", dpi=200)
plt.close()

figure, axes = plt.subplots(1, 2, figsize=(12, 5))
target_group = cleaned_survey[cleaned_survey["satisfaction"].isin(satisfaction_order[:2])].copy()
target_group["has_problem"] = (target_group["overdue_tasks"] > 0) | (target_group["sleep_h"] < 7) | (target_group["scroll_min"] > 120)
with_problems = np.count_nonzero(target_group["has_problem"])
axes[0].pie([with_problems, len(target_group) - with_problems], labels=["Есть проблема", "Нет проблем"], autopct="%1.1f%%", colors=["tomato", "mediumseagreen"])
plt.title(f"Хотя бы один проблемный признак (n={len(target_group)})")
np.random.seed(42)
scroll_points = np.array(target_group["scroll_min"]) + np.random.uniform(-4, 4, len(target_group))
debt_points = np.array(target_group["overdue_tasks"]) + np.random.uniform(-0.15, 0.15, len(target_group))
sleep_colors = np.where(target_group["sleep_h"] < 7, "crimson", "steelblue")
axes[1].scatter(scroll_points, debt_points, c=sleep_colors)
axes[1].scatter([], [], c="crimson", label="сон < 7 ч")
axes[1].scatter([], [], c="steelblue", label="сон ≥ 7 ч")
plt.xlabel("Спонтанный скроллинг, мин/день")
plt.ylabel("Долги / просроченные задачи, шт")
plt.title("Комбинации проблем")
plt.grid()
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig("graphics/Problem_profile_of_target_group.png", dpi=200)
plt.close()
