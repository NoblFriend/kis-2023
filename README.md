
# Gandalf's Tracking App

## Автор

Ребриков Алексей Витальевич

## Задача

Задача №6 "Клиентские приложения"

---

## Демо работы
https://www.loom.com/share/229825e4adcf450f8f528d9ede97bfc9?sid=b90080c5-0512-485b-9abe-81a4c72d4a20

## Установка и запуск

### Требования

- Python 3.x
- macOS

### Инструкции

1. Установите Python, если он ещё не установлен.
2. Установите необходимые библиотеки:

   ```bash
   pip install -r requirements.txt
   ```

3. Запустите `main.py`:

   ```bash
   python src/main.py
   ```

---

## Проектные решения

- Использован `tkinter` для создания пользовательского интерфейса.
- Для работы с базой данных создана собственная обёртка `CharacterAppDatabase`.
- Для выбора даты применена библиотека `tkcalendar`.
- Для отображения карт применена библиотека `TkinterMapView`.

---

## Дополнительные функции

- Фильтрация персонажей по времени.
- Валидация введённых данных.

---

## Примечания

- Протестировано на macOS.
- Для работы с картами используется offline база данных `offline_tiles.db`.
