# Flask Photo Gallery

![GitHub License](https://img.shields.io/github/license/LionzzSh/Flask_Photo_Gallery)  
![Python Version](https://img.shields.io/badge/Python-3.10-blue)  
![Deployed](https://img.shields.io/website?down_color=red&down_message=Down&up_color=green&up_message=Up&url=https%3A%2F%2Flionzz.pythonanywhere.com%2F)

Ласкаво просимо до **Flask Photo Gallery**, сучасної веб-програми, створеної за допомогою Flask для керування фотогалереями. Цей проект дозволяє користувачам автентифікуватися, завантажувати фотографії, упорядковувати їх у папки та ділитися з іншими, при цьому всі зображення надійно зберігаються на AWS S3. Додаток розгорнуто та працює на сайті-[https://lionzz.pythonanywhere.com/](https://lionzz.pythonanywhere.com/).

## Зміст 
- [Функції](#Функції)
- [Скріншоти](#скріншоти)
- [Tech Stack](#tech-stack)

## Функції
- **Автентифікація користувача**: зареєструйтеся та увійдіть із безпечним хешуванням пароля за допомогою Flask-Bcrypt.
- **Керування фотографіями**: завантажуйте, переглядайте, редагуйте та видаляйте фотографії.
- **Організація папок**: створюйте та керуйте папками для категоризації своїх фотографій.
- **Інтеграція з AWS S3**: надійно зберігайте фотографії в Amazon S3 за допомогою boto3.
- **Спільний доступ**: створюйте посилання для спільного використання для фотографій або папок.
- **Адаптивний дизайн**: базові шаблони HTML/CSS для зручного інтерфейсу.

## Скріншоти
![Сторінка входу](insert-screenshot-login.jpg)
*Сторінка входу: інтерфейс автентифікації користувача.*

![Перегляд галереї](insert-screenshot-gallery.jpg)
*Перегляд галереї: відображення фотографій у вигляді сітки.*

![Керування папками](insert-screenshot-folders.jpg)
*Керування папками: створення та впорядкування папок із фотографіями.*

![Завантажити фото](insert-screenshot-upload.jpg)
*Завантажити фото: інтерфейс для завантаження зображень в AWS S3.*

## Tech Stack
- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, boto3
- **Storage**: AWS S3
- **Database**: MySQL (or SQLite for local testing)
- **Hosting**: PythonAnywhere
- **Version Control**: Git, GitHub
- **Python Version**: 3.10

