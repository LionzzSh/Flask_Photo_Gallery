from app import db, mail
from flask_login import current_user
from flask import current_app
from flask_mail import Message

def get_folder_path(folder):
    """Навігаційний шлях для папки"""
    path = []
    current = folder
    while current:
        path.insert(0, current)
        current = current.parent
    return path

def send_share_notification(user_email, folder_name, sender_name):
    msg = Message(
        "Нова спільна папка",
        sender=current_app.config['MAIL_USERNAME'], 
        recipients=[user_email]
    )
    msg.body = f"{sender_name} Cпільна папка '{folder_name}' доступна вам!"
    mail.send(msg)

def send_upload_notification(shared_users, folder_name, filename):
    for user in shared_users:
        if user.id != current_user.id: 
            msg = Message(
                "Нова фотографія в спільній папці",
                sender=current_app.config['MAIL_USERNAME'], 
                recipients=[user.email]
            )
            msg.body = f"Нове фото '{filename}' було завантажено до спільної папки '{folder_name}'"
            mail.send(msg)