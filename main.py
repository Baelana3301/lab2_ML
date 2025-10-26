import numpy as np
import matplotlib.pyplot as plt


# Функция для определения трапециевидной функции принадлежности
def trapezoidal_mf(x, a, b, c, d):
    """
    Трапециевидная функция принадлежности.
    :param x: Точки, для которых вычисляется функция принадлежности.
    :param a: Левая граница начала возрастания функции.
    :param b: Левая верхняя граница (где функция равна 1).
    :param c: Правая верхняя граница (где функция равна 1).
    :param d: Правая граница окончания убывания функции.
    :return: Значение функции принадлежности в точках x.
    """
    left_slope = np.clip((x - a) / (b - a + 1e-6), 0, 1)
    right_slope = np.clip((d - x) / (d - c + 1e-6), 0, 1)
    return np.maximum(0, np.minimum(left_slope, right_slope))


# Операция пересечения нечетких множеств (минимум)
def fuzzy_intersection(set1, set2):
    return np.minimum(set1, set2)


# Основная программа
def main():
    print("=== Пересечение нечетких множеств для финансового риска ===\n")

    # Универсум для кредитного рейтинга (0-1000)
    x_credit = np.linspace(0, 1000, 1000)

    # Универсум для уровня риска (0-100%)
    x_risk = np.linspace(0, 100, 1000)

    # Параметры для кредитного рейтинга
    print("Параметры трапециевидных функций для кредитного рейтинга:")
    print("Низкий: a=0, b=0, c=300, d=400")
    print("Средний: a=350, b=450, c=550, d=650")
    print("Высокий: a=600, b=700, c=800, d=900")
    print("Премиальный: a=850, b=900, c=1000, d=1000")

    # Определение функций принадлежности для кредитного рейтинга
    credit_low = trapezoidal_mf(x_credit, 0, 0, 300, 400)
    credit_medium = trapezoidal_mf(x_credit, 350, 450, 550, 650)
    credit_high = trapezoidal_mf(x_credit, 600, 700, 800, 900)
    credit_premium = trapezoidal_mf(x_credit, 850, 900, 1000, 1000)

    # Параметры для уровня риска
    print("\nПараметры трапециевидных функций для уровня риска:")
    print("Безопасный: a=0, b=0, c=10, d=25")
    print("Приемлемый: a=15, b=25, c=35, d=45")
    print("Рискованный: a=35, b=45, c=55, d=65")
    print("Опасный: a=55, b=65, c=100, d=100")

    # Определение функций принадлежности для уровня риска
    risk_safe = trapezoidal_mf(x_risk, 0, 0, 10, 25)
    risk_acceptable = trapezoidal_mf(x_risk, 15, 25, 35, 45)
    risk_risky = trapezoidal_mf(x_risk, 35, 45, 55, 65)
    risk_dangerous = trapezoidal_mf(x_risk, 55, 65, 100, 100)

    # Ввод значений от пользователя
    try:
        credit_score = float(input("\nВведите значение кредитного рейтинга (0-1000): "))
        risk_level = float(input("Введите значение уровня риска (0-100%): "))

        # Проверка корректности ввода
        if credit_score < 0 or credit_score > 1000:
            print("Ошибка: кредитный рейтинг должен быть в диапазоне 0-1000")
            return
        if risk_level < 0 or risk_level > 100:
            print("Ошибка: уровень риска должен быть в диапазоне 0-100")
            return

    except ValueError:
        print("Ошибка: введите числовые значения")
        return

    # Вычисление степеней принадлежности для кредитного рейтинга
    credit_memberships = {
        'Низкий': np.interp(credit_score, x_credit, credit_low),
        'Средний': np.interp(credit_score, x_credit, credit_medium),
        'Высокий': np.interp(credit_score, x_credit, credit_high),
        'Премиальный': np.interp(credit_score, x_credit, credit_premium)
    }

    # Вычисление степеней принадлежности для уровня риска
    risk_memberships = {
        'Безопасный': np.interp(risk_level, x_risk, risk_safe),
        'Приемлемый': np.interp(risk_level, x_risk, risk_acceptable),
        'Рискованный': np.interp(risk_level, x_risk, risk_risky),
        'Опасный': np.interp(risk_level, x_risk, risk_dangerous)
    }

    # Вывод степеней принадлежности
    print("\n=== Степени принадлежности ===")
    print("Кредитный рейтинг:")
    for category, membership in credit_memberships.items():
        print(f"  {category}: {membership:.3f}")

    print("\nУровень риска:")
    for category, membership in risk_memberships.items():
        print(f"  {category}: {membership:.3f}")

    # Выполнение пересечения для всех комбинаций
    print("\n=== Пересечение нечетких множеств ===")
    intersection_results = {}

    for credit_cat, credit_mem in credit_memberships.items():
        for risk_cat, risk_mem in risk_memberships.items():
            intersection = min(credit_mem, risk_mem)
            intersection_results[f"{credit_cat} рейтинг ∩ {risk_cat} риск"] = intersection
            print(f"{credit_cat} рейтинг ∩ {risk_cat} риск: {intersection:.3f}")

    # Визуализация
    visualize_results(x_credit, x_risk, credit_low, credit_medium, credit_high, credit_premium,
                      risk_safe, risk_acceptable, risk_risky, risk_dangerous,
                      credit_score, risk_level, credit_memberships, risk_memberships)


def visualize_results(x_credit, x_risk, credit_low, credit_medium, credit_high, credit_premium,
                      risk_safe, risk_acceptable, risk_risky, risk_dangerous,
                      credit_score, risk_level, credit_memberships, risk_memberships):
    # Создание графиков
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

    # График 1: Кредитный рейтинг
    ax1.plot(x_credit, credit_low, 'b-', label='Низкий', linewidth=2)
    ax1.plot(x_credit, credit_medium, 'g-', label='Средний', linewidth=2)
    ax1.plot(x_credit, credit_high, 'y-', label='Высокий', linewidth=2)
    ax1.plot(x_credit, credit_premium, 'r-', label='Премиальный', linewidth=2)
    ax1.axvline(x=credit_score, color='k', linestyle='--', label=f'Введенное значение: {credit_score}')
    ax1.set_title('Нечеткие множества: Кредитный рейтинг')
    ax1.set_xlabel('Кредитный рейтинг')
    ax1.set_ylabel('Степень принадлежности')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # График 2: Уровень риска
    ax2.plot(x_risk, risk_safe, 'b-', label='Безопасный', linewidth=2)
    ax2.plot(x_risk, risk_acceptable, 'g-', label='Приемлемый', linewidth=2)
    ax2.plot(x_risk, risk_risky, 'y-', label='Рискованный', linewidth=2)
    ax2.plot(x_risk, risk_dangerous, 'r-', label='Опасный', linewidth=2)
    ax2.axvline(x=risk_level, color='k', linestyle='--', label=f'Введенное значение: {risk_level}%')
    ax2.set_title('Нечеткие множества: Уровень риска')
    ax2.set_xlabel('Уровень риска (%)')
    ax2.set_ylabel('Степень принадлежности')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # График 3: Степени принадлежности для кредитного рейтинга
    credit_categories = list(credit_memberships.keys())
    credit_values = list(credit_memberships.values())
    bars1 = ax3.bar(credit_categories, credit_values, color=['blue', 'green', 'yellow', 'red'], alpha=0.7)
    ax3.set_title('Степени принадлежности: Кредитный рейтинг')
    ax3.set_ylabel('Степень принадлежности')
    ax3.grid(True, alpha=0.3)

    # Добавление значений на столбцы
    for bar, value in zip(bars1, credit_values):
        ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                 f'{value:.3f}', ha='center', va='bottom')

    # График 4: Степени принадлежности для уровня риска
    risk_categories = list(risk_memberships.keys())
    risk_values = list(risk_memberships.values())
    bars2 = ax4.bar(risk_categories, risk_values, color=['blue', 'green', 'yellow', 'red'], alpha=0.7)
    ax4.set_title('Степени принадлежности: Уровень риска')
    ax4.set_ylabel('Степень принадлежности')
    ax4.grid(True, alpha=0.3)

    # Добавление значений на столбцы
    for bar, value in zip(bars2, risk_values):
        ax4.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                 f'{value:.3f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()