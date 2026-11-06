# Лабораторна робота №7: `functools` та `operator`

## Варіант 11: Складські запаси (Inventory)

### Мета роботи
Освоєння функціональних інструментів Python:
- Часткового застосування функцій (`functools.partial`)
- Згортки та побудови функціональних конвеєрів (`functools.reduce`)
- Оптимізованих операторів доступу (`operator.itemgetter`, `methodcaller`)
- Поліморфного API за допомогою `functools.singledispatch`
- Організації повного порядку за допомогою `functools.total_ordering`

### Запуск програми та тестів
1. Встановлення залежностей:
   ```bash
   pip install -r requirements.txt