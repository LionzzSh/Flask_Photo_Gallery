from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app import db, s3
from app.models import Photo, Folder, FolderShare

photo_bp = Blueprint('photo', __name__)

@photo_bp.route('/photo/<int:photo_id>')
@login_required
def view_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    folder = Folder.query.get(photo.folder_id) if photo.folder_id else None
    share = FolderShare.query.filter_by(folder_id=photo.folder_id, user_id=current_user.id).first() if folder else None
    
    is_folder_owner = folder and folder.user_id == current_user.id
    if not (photo.user_id == current_user.id or is_folder_owner or share):
        flash('Відмовлено в доступі')
        return redirect(url_for('gallery.galleries'))
    
    url = f"https://{current_app.config['AWS_BUCKET_NAME']}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{photo.s3_key}"
    return render_template('view_photo.html', photo=photo, url=url)

@photo_bp.route('/delete_photo/<int:photo_id>', methods=['POST'])
@login_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    folder = Folder.query.get(photo.folder_id) if photo.folder_id else None
    share = FolderShare.query.filter_by(folder_id=photo.folder_id, user_id=current_user.id).first() if folder else None
    
    is_folder_owner = folder and folder.user_id == current_user.id
    if is_folder_owner or photo.user_id == current_user.id or (share and share.can_delete):
        s3.delete_object(Bucket=current_app.config['AWS_BUCKET_NAME'], Key=photo.s3_key)
        db.session.delete(photo)
        db.session.commit()
        flash('Фото успішно видалено')
    else:
        flash('Ви не маєте дозволу на видалення цієї фотографії')
    return redirect(url_for('folder.view_folder', folder_id=photo.folder_id) if photo.folder_id else url_for('gallery.galleries'))