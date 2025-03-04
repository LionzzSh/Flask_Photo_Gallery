from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app import db, s3
from app.models import Folder, Photo, FolderShare, User
from app.utils import send_upload_notification
from werkzeug.utils import secure_filename
from datetime import datetime

gallery_bp = Blueprint('gallery', __name__)

@gallery_bp.route('/')
def index():
    return render_template('index.html')

@gallery_bp.route('/galleries')
@login_required
def galleries():
    if not current_user.is_authenticated:
        flash('Будь ласка, увійдіть, щоб отримати доступ до цієї сторінки.', 'error')
        return redirect(url_for('auth.login'))
    folders = Folder.query.filter_by(user_id=current_user.id, parent_id=None).all()
    photos = Photo.query.filter_by(user_id=current_user.id, folder_id=None).all()
    shared_folders = Folder.query.join(FolderShare).filter(FolderShare.user_id == current_user.id).all()
    return render_template('gallery.html', folders=folders, photos=photos, shared_folders=shared_folders)

@gallery_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files['file']
    folder_id = request.form.get('folder_id') or None
    
    if file:
        filename = secure_filename(file.filename)
        s3_key = f"{current_user.id}/{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
        
        s3.upload_fileobj(file, current_app.config['AWS_BUCKET_NAME'], s3_key)
        
        photo = Photo(filename=filename, s3_key=s3_key, folder_id=folder_id, user_id=current_user.id)
        db.session.add(photo)
        db.session.commit()
        
        if folder_id:
            folder = Folder.query.get(folder_id)
            if folder.user_id == current_user.id or FolderShare.query.filter_by(folder_id=folder_id, user_id=current_user.id, can_edit=True).first():
                shared_users = User.query.join(FolderShare).filter(FolderShare.folder_id == folder_id).all()
                send_upload_notification(shared_users, folder.name, filename)
            else:
                flash('Ви не маєте дозволу завантажувати сюди')
                db.session.delete(photo)
                db.session.commit()
                return redirect(url_for('folder.view_folder', folder_id=folder_id) if folder_id else url_for('gallery.galleries'))
        
        flash('Фото успішно завантажено')
        # Redirect to the folder if uploaded there, otherwise galleries
        return redirect(url_for('folder.view_folder', folder_id=folder_id) if folder_id else url_for('gallery.galleries'))
    flash('Не вибрано файл для завантаження')
    return redirect(url_for('gallery.galleries'))  # If no file, back to galleries

@gallery_bp.route('/create_folder', methods=['POST'])
@login_required
def create_folder():
    name = request.form['name']
    parent_id = request.form.get('parent_id') or None
    if parent_id:
        parent = Folder.query.get(parent_id)
        if parent.user_id != current_user.id and not FolderShare.query.filter_by(folder_id=parent_id, user_id=current_user.id, can_edit=True).first():
            flash('Ви не маєте дозволу створювати тут папку')
            return redirect(url_for('folder.view_folder', folder_id=parent_id) if parent_id else url_for('gallery.galleries'))
    folder = Folder(name=name, parent_id=parent_id, user_id=current_user.id)
    db.session.add(folder)
    db.session.commit()
    flash('Папку успішно створено')
    # Redirect to the parent folder if created there, otherwise galleries
    return redirect(url_for('folder.view_folder', folder_id=parent_id) if parent_id else url_for('gallery.galleries'))