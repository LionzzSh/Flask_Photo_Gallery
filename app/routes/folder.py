from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app import db, s3
from app.models import Folder, Photo, FolderShare, User
from app.utils import get_folder_path, send_share_notification

folder_bp = Blueprint('folder', __name__)

@folder_bp.route('/folder/<int:folder_id>')
@login_required
def view_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    share = FolderShare.query.filter_by(folder_id=folder_id, user_id=current_user.id).first()
    
    if folder.user_id != current_user.id and not share:
        flash('Відмовлено в доступі')
        return redirect(url_for('gallery.galleries'))
    
    photos = Photo.query.filter_by(folder_id=folder_id).all()
    subfolders = Folder.query.filter_by(parent_id=folder_id).all()
    shares = FolderShare.query.filter_by(folder_id=folder_id).all()
    path = get_folder_path(folder)
    return render_template('view_folder.html', folder=folder, photos=photos, subfolders=subfolders, shares=shares, path=path, share=share)

@folder_bp.route('/share_folder/<int:folder_id>', methods=['POST'])
@login_required
def share_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    if folder.user_id != current_user.id:
        flash('Відмовлено в доступі')
        return redirect(url_for('folder.view_folder', folder_id=folder_id))
    
    username = request.form['username']
    can_edit = request.form.get('can_edit') == 'true'  # Перевіряємо, чи ключ 'can_edit' має значення 'true'
    can_delete = request.form.get('can_delete') == 'true'  # Перевіряємо, чи ключ 'can_delete' має значення 'true'
    
    # Додамо відладковий вивід для перевірки
    print(f"Sharing folder {folder_id} with {username}: can_edit={can_edit}, can_delete={can_delete}")
    
    user = User.query.filter_by(username=username).first()
    if user and user.id != current_user.id:
        share = FolderShare.query.filter_by(folder_id=folder_id, user_id=user.id).first()
        if share:
            # Якщо доступ уже надано, оновлюємо права
            share.can_edit = can_edit
            share.can_delete = can_delete
        else:
            # Якщо доступу ще немає, створюємо новий запис
            share = FolderShare(folder_id=folder_id, user_id=user.id, can_edit=can_edit, can_delete=can_delete)
            db.session.add(share)
        db.session.commit()
        send_share_notification(user.email, folder.name, current_user.username)
        flash('До папки надано доступ')
    else:
        flash('Користувач не знайдений або не можна ділитися з собою')
    return redirect(url_for('folder.view_folder', folder_id=folder_id))  # Stay on current folder

@folder_bp.route('/delete_folder/<int:folder_id>', methods=['POST'])
@login_required
def delete_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    if folder.user_id != current_user.id:
        flash('Лише власник може видалити цю папку')
        return redirect(url_for('folder.view_folder', folder_id=folder_id))
    
    def delete_recursive(fldr):
        for photo in Photo.query.filter_by(folder_id=fldr.id).all():
            s3.delete_object(Bucket=current_app.config['AWS_BUCKET_NAME'], Key=photo.s3_key)
            db.session.delete(photo)
        for subfolder in fldr.subfolders:
            delete_recursive(subfolder)
        db.session.delete(fldr)
    
    delete_recursive(folder)
    db.session.commit()
    flash('Папку та її вміст успішно видалено')
    # Redirect to parent folder if it exists, otherwise galleries
    parent_id = folder.parent_id
    return redirect(url_for('folder.view_folder', folder_id=parent_id) if parent_id else url_for('gallery.galleries'))