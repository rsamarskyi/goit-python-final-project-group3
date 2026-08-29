# Personal Assistant Bot

Короткий опис: це консольний помічник для збереження контактів і нотаток. Бот дозволяє керувати адресною книгою, відстежувати дні народження, зберігати замітки, шукати інформацію за різними критеріями та працювати в інтерактивному режимі через термінал.

## Основні функції

- Додавання, пошук, редагування та видалення контактів
- Зберігання кількох телефонів для одного контакту
- Додавання електронної пошти, адреси та дня народження
- Показ всіх контактів та список майбутніх днів народження
- Створення, редагування, видалення та пошук нотаток
- Пошук нотаток за заголовком, вмістом або тегами
- Автоматичне збереження даних між запусками

## Встановлення

Проєкт написаний на Python. Для коректної роботи потрібні залежності з файлу requirements.txt.

1. Створіть віртуальне середовище:

   Windows PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   macOS / Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Оновіть pip:

   ```bash
   python -m pip install --upgrade pip
   ```

4. Встановіть залежності:

   ```bash
   pip install -r requirements.txt
   ```

## Запуск застосунку

У активованому віртуальному середовищі виконайте:

```bash
python Bot/main.py
```

Після запуску бот виводить привітання і очікує команду.

## Порядок використання

1. Введіть `help`, щоб переглянути список доступних команд.
2. Додайте контакти, наприклад `add Alice 1234567890`.
3. За потреби редагуйте контакт через `edit <name>`.
4. Перевіряйте список всіх контактів через `all`.
5. Додавайте нотатки через `add-note <title> <text>`.
6. Шукайте нотатки або контакти за ключовими словами.
7. Коли закінчите роботу, введіть `close` або `exit`.

> Бот зберігає дані у файлах `addressbook.pkl` та `notebook.pkl` у корені проєкту. Якщо файли ще не існують, бот створить їх автоматично.

## Список команд бота

| Команда | Використання | Опис |
| --- | --- | --- |
| `help` | `help` | Показати список усіх команд |
| `hello` | `hello` | Вивести привітання |
| `add` | `add <name> <phone>` | Додати новий контакт |
| `find` | `find <name>` | Знайти контакт за ім'ям |
| `edit` | `edit <name>` | Додати або змінити телефон, email, адресу, день народження |
| `birthdays` | `birthdays [days]` | Показати наближені дні народження |
| `delete` | `delete <name>` | Видалити контакт |
| `all` | `all` | Показати всі контакти |
| `add-note` | `add-note <title> <text>` | Додати нотатку |
| `edit-note` | `edit-note <title> <new_text>` | Редагувати нотатку за заголовком |
| `delete-note` | `delete-note <title>` | Видалити нотатку |
| `search-title` | `search-title <title>` | Пошук нотатки за заголовком |
| `search-notes` | `search-notes <word>` | Пошук нотаток за текстом |
| `search-tag` | `search-tag <tag>` | Пошук нотаток за тегом |
| `all-notes` | `all-notes` | Показати всі нотатки |
| `close` (or `exit` ) | `close` | Завершити роботу бота |

## Приклади використання

### Контакти

```bash
add Alice 1234567890
add Bob 0987654321
find Alice
all
birthdays 7
edit Alice
delete Bob
```

Приклад роботи команди `edit`:

```bash
edit Alice
```

Бот задасть питання:

```text
Change phone? (y/n): y
Current phones: 1234567890
Enter the phone to change, or press Enter to add a new phone:
Enter new phone: 1112223333
Add e-mail? (y/n): y
Enter e-mail: alice@example.com
Add address? (y/n): y
Enter address: Kyiv, Main Street 15
Add birthday? (y/n): y
Enter birthday (DD.MM.YYYY): 15.06.1995
```

### Нотатки

```bash
add-note meeting Project review and planning
search-title meeting
search-notes planning
search-tag #work
edit-note meeting Project review and final planning
all-notes
delete-note meeting
```

### Пошук днів народження

```bash
birthdays
birthdays 3
```

- `birthdays` показує дні народження на найближчі 7 днів.
- `birthdays 3` показує контакти, у яких день народження саме через 3 дні.

## Формат вводу

- Команди вводяться без урахування регістру, наприклад: `ADD Alice 1234567890` також працює.
- Телефон повинен містити рівно 10 цифр.
- Для дня народження використовуйте формат `DD.MM.YYYY`.
- В нотатках теги пишуться через `#`, наприклад: `#work`, `#family`.

## Приклад повного сценарію роботи

```bash
help
hello
add Alice 1234567890
add Alice 9876543210
find Alice
all
birthdays 7
add-note project Launch plan for Q4 #work
search-tag work
all-notes
close
```
