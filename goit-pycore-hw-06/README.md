# Homework 6 / Домашнє завдання №6

<p align="left">
  <a href="#english">English Description</a> • 
  <a href="#українська">Опис українською</a>
</p>

---

<a name="english"></a>
## 📋 Project Overview (EN)

In this homework, I implemented an object-oriented system for managing a contact book. The project is focused on **Encapsulation**, **Validation**, and **Modular Architecture**.

### 🏗 Architecture
The code is split into two logical modules:
1.  **`models.py`**: Contains the data structure (Entities).
    *   `AddressBook`: A container for managing records (inherited from `UserDict`).
    *   `Record`: Manages a single contact's data (name and multiple phones).
    *   `Phone`: Includes validation logic (exactly 10 digits).
2.  **`main.py`**: Demonstrates the functionality and interaction between classes.


### 🛠 Key Features & Optimization
* **Validation**: Phone numbers are strictly validated via the `Phone` class initializer.
* **Pythonic Search**: Implemented generator expressions and the `next()` function for concise and efficient lookup within object lists.
* **Safe Deletion**: Used the `pop()` method in `AddressBook` for robust and error-resistant record removal.
* **Code Refinement**: Refactored `Record` methods to minimize logic duplication and enhance readability (Clean Code principles).

---

<a name="українська"></a>
## 📋 Огляд проєкту (UA)

У цьому домашньому завданні я реалізувала об'єктно-орієнтовану систему для керування адресною книгою. Основний акцент зроблено на **Інкапсуляції**, **Валідації** та **Модульній архітектурі**.


### 🏗 Архітектура
Код розділений на два логічні модулі:
1.  **`models.py`**: Містить структуру даних (Сутності).
    *   `AddressBook`: Контейнер для керування записами (успадковано від `UserDict`).
    *   `Record`: Керує даними одного контакту (ім'я та список телефонів).
    *   `Phone`: Включає логіку валідації (рівно 10 цифр).
2.  **`main.py`**: Демонструє функціонал та взаємодію між класами.


### 🛠 Ключові особливості та Оптимізація
* **Валідація**: Номери телефонів суворо перевіряються через ініціалізатор класу `Phone`.
* **Елегантний пошук**: Використано генераторні вирази та функцію `next()` для швидкого та лаконічного пошуку об'єктів у списках.
* **Безпечне видалення**: Застосовано метод `pop()` для `AddressBook`, що робить видалення записів стабільним та стійким до помилок.
* **Чистота коду**: Проведено рефакторинг методів `Record` для мінімізації дублювання логіки та покращення читабельності.

---
