from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# Инициализация веб-драйвера для браузера Chrome
driver = webdriver.Chrome()

# Установка времени ожидания в 10 секунд
wait = WebDriverWait(driver, 10)

# Переход на страницу логина
driver.get("http://127.0.0.1:5000/login")

# Логин
try:
    cursor = wait.until(EC.presence_of_element_located((By.NAME, 'username'))) # Ищем элемент по имени (name)
    cursor.click()
    cursor.send_keys("lisiy") # Вводим имя пользователя
    print("Username field found and value entered")

    cursor = wait.until(EC.presence_of_element_located((By.NAME, 'password'))) # Ищем элемент по имени (name)
    cursor.click()
    cursor.send_keys("cherep") # Вводим пароль
    print("Password field found and value entered")

    cursor = wait.until(EC.element_to_be_clickable((By.ID, 'submit'))) # Ищем кнопку для логина
    cursor.click()
    print("Login button found and clicked")

except Exception as e:
    print("An error occurred during login:", e)
    driver.quit()
    exit()

# Переход на страницу добавления книги
driver.get("http://127.0.0.1:5000/add_book")

# Добавление книги
try:
    cursor = wait.until(EC.presence_of_element_located((By.ID, 'title'))) # Ищем поле ввода названия книги
    cursor.click()
    cursor.send_keys("Test Book Title") # Вводим название книги
    print("Title field found and value entered")

    cursor = wait.until(EC.presence_of_element_located((By.ID, 'author'))) # Ищем поле ввода автора книги
    cursor.click()
    cursor.send_keys("Test Author") # Вводим автора книги
    print("Author field found and value entered")

    cursor = wait.until(EC.presence_of_element_located((By.ID, 'link'))) # Ищем поле ввода ссылки на книгу
    cursor.click()
    cursor.send_keys("http://example.com") # Вводим ссылку на книгу
    print("Link field found and value entered")

    cursor = wait.until(EC.presence_of_element_located((By.ID, 'description'))) # Ищем поле ввода описания книги
    cursor.click()
    cursor.send_keys("This is a test description for the book.") # Вводим описание книги
    print("Description field found and value entered")

    cursor = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit"]'))) # Ищем кнопку для добавления книги
    cursor.click()
    print("Add book button found and clicked")

except Exception as e:
    print("An error occurred during adding the book:", e)
    driver.quit()
    exit()

# Переход на страницу аккаунта для проверки добавленной книги
driver.get("http://127.0.0.1:5000/account")

# Проверка наличия добавленной книги
try:
    assert "Test Book Title" in driver.page_source # Проверяем наличие названия книги на странице
    assert "Test Author" in driver.page_source # Проверяем наличие автора книги на странице
    print("Book added successfully")

except Exception as e:
    print("An error occurred during book verification:", e)
    driver.quit()
    exit()

# Переход на страницу админ панели
driver.get("http://127.0.0.1:5000/admin")

# Удаление книги
try:


    cursor = Select(wait.until(EC.presence_of_element_located((By.ID, 'action')))) # Ищем селект по имени (name)
    cursor.select_by_value('delete') # Выбираем действие удаления
    print("Delete action selected")

    cursor = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))) # Ищем кнопку для подтверждения удаления
    cursor.click()
    print("Delete button found and clicked")

except Exception as e:
    print("An error occurred during book deletion:", e)
    driver.quit()
    exit()

# Проверка, что книга была удалена
driver.get("http://127.0.0.1:5000/account")
try:
    assert "Test Book Title" not in driver.page_source # Проверяем, что книга отсутствует на странице
    print("Book deleted successfully")

except Exception as e:
    print("An error occurred during book deletion verification:", e)
    driver.quit()
    exit()

# Разлогинивание
driver.get("http://127.0.0.1:5000/logout")

# Закрываем браузер
driver.quit()
