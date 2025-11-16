import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

# Настройка стиля графиков
plt.style.use('seaborn-v0_8')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 12

# Точное значение площади
S_exact = 0.25 * math.pi + 1.25 * math.asin(0.8) - 1

# Загрузка данных
data = pd.read_csv('experiment_results.csv')

# График 1: Приближенная площадь в зависимости от количества точек
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(data['N'], data['wide_area'], 'b-', alpha=0.8, linewidth=2, label='Широкая область [0,3]×[0,3]')
plt.plot(data['N'], data['narrow_area'], 'r-', alpha=0.8, linewidth=2, label='Узкая область [1,2]×[1,2]')
plt.axhline(y=S_exact, color='k', linestyle='--', linewidth=2, label=f'Точное значение ({S_exact:.6f})')
plt.xlabel('Количество точек N')
plt.ylabel('Площадь пересечения')
plt.title('Зависимость оценки площади от количества точек', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim(S_exact * 0.8, S_exact * 1.2)

# График 2: Относительная ошибка в зависимости от количества точек
plt.subplot(2, 1, 2)
plt.semilogy(data['N'], data['wide_error'], 'b-', alpha=0.8, linewidth=2, label='Широкая область')
plt.semilogy(data['N'], data['narrow_error'], 'r-', alpha=0.8, linewidth=2, label='Узкая область')
plt.axhline(y=0.01, color='g', linestyle=':', linewidth=2, label='Порог 1%')
plt.xlabel('Количество точек N')
plt.ylabel('Относительная ошибка')
plt.title('Зависимость относительной ошибки от количества точек', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/combined_results.png', dpi=300, bbox_inches='tight')
plt.show()

# Отдельные графики для лучшей читаемости
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# График площади
ax1.plot(data['N'], data['wide_area'], 'b-', alpha=0.8, linewidth=2, label='Широкая область [0,3]×[0,3]')
ax1.plot(data['N'], data['narrow_area'], 'r-', alpha=0.8, linewidth=2, label='Узкая область [1,2]×[1,2]')
ax1.axhline(y=S_exact, color='k', linestyle='--', linewidth=2, label=f'Точное значение ({S_exact:.6f})')
ax1.set_xlabel('Количество точек N')
ax1.set_ylabel('Площадь пересечения')
ax1.set_title('Зависимость оценки площади от количества точек', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# График ошибки
ax2.semilogy(data['N'], data['wide_error'], 'b-', alpha=0.8, linewidth=2, label='Широкая область')
ax2.semilogy(data['N'], data['narrow_error'], 'r-', alpha=0.8, linewidth=2, label='Узкая область')
ax2.axhline(y=0.01, color='g', linestyle=':', linewidth=2, label='Порог 1%')
ax2.set_xlabel('Количество точек N')
ax2.set_ylabel('Относительная ошибка')
ax2.set_title('Зависимость относительной ошибки от количества точек', fontsize=14, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/area_vs_points.png', dpi=300, bbox_inches='tight')
plt.show()

# Анализ результатов
print("=" * 60)
print("АНАЛИЗ РЕЗУЛЬТАТОВ ЭКСПЕРИМЕНТА")
print("=" * 60)
print(f"Точная площадь пересечения: {S_exact:.6f}")
print("\nРезультаты при N = 100000:")
print(f"  Широкая область:  {data['wide_area'].iloc[-1]:.6f}")
print(f"    Относительная ошибка: {data['wide_error'].iloc[-1]*100:.2f}%")
print(f"  Узкая область:    {data['narrow_area'].iloc[-1]:.6f}")
print(f"    Относительная ошибка: {data['narrow_error'].iloc[-1]*100:.2f}%")

# Нахождение минимального N для достижения точности 1%
narrow_1percent = data[data['narrow_error'] <= 0.01]
wide_1percent = data[data['wide_error'] <= 0.01]

if not narrow_1percent.empty:
    print(f"\nТочность 1% достигнута:")
    print(f"  Узкая область: при N = {narrow_1percent['N'].iloc[0]}")
else:
    print(f"\nТочность 1% не достигнута для узкой области в диапазоне N")

if not wide_1percent.empty:
    print(f"  Широкая область: при N = {wide_1percent['N'].iloc[0]}")
else:
    print(f"  Широкая область: точность 1% не достигнута в диапазоне N")

# Статистика сходимости
print(f"\nСкорость сходимости:")
final_narrow_error = data['narrow_error'].iloc[-1]
final_wide_error = data['wide_error'].iloc[-1]
print(f"  Узкая область: конечная ошибка {final_narrow_error*100:.3f}%")
print(f"  Широкая область: конечная ошибка {final_wide_error*100:.3f}%")

print(f"\nЭффективность (отношение ошибок): {final_wide_error/final_narrow_error:.2f}x")
