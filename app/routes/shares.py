from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Folder, FolderShare
from sqlalchemy.orm import joinedload

shares_bp = Blueprint('shares', __name__)

def get_owned_folders(user_id):
    return Folder.query.filter_by(user_id=user_id).all()

@shares_bp.route('/manage_shares')
@login_required
def manage_shares():
    owned_folders = get_owned_folders(current_user.id)
    folder_shares = {}
    for folder in owned_folders:
        shares = FolderShare.query.filter_by(folder_id=folder.id).options(joinedload(FolderShare.user)).all()
        if shares:
            folder_shares[folder] = shares
    return render_template('manage_shares.html', folder_shares=folder_shares)

@shares_bp.route('/update_share/<int:share_id>', methods=['POST'])
@login_required
def update_share(share_id):
    share = FolderShare.query.get_or_404(share_id)
    folder = share.folder
    if folder.user_id != current_user.id:
        flash('У доступі відмовлено')
        return redirect(url_for('shares.manage_shares'))
    
    # Отримання значень з форми, використовуючи get() для безпечного доступу
    can_edit = request.form.get('can_edit') == 'true'  # Перевіряємо, чи ключ 'can_edit' має значення 'true'
    can_delete = request.form.get('can_delete') == 'true'  # Перевіряємо, чи ключ 'can_delete' має значення 'true'
    
    # Додамо відладковий вивід для перевірки
    print(f"Updating share {share_id}: can_edit={can_edit}, can_delete={can_delete}")
    
    share.can_edit = can_edit
    share.can_delete = can_delete
    username = share.user.username
    db.session.commit()
    flash(f"Оновлені дозволи для {username} у папці {folder.name}")
    return redirect(url_for('shares.manage_shares')) 

@shares_bp.route('/revoke_share/<int:share_id>', methods=['POST'])
@login_required
def revoke_share(share_id):
    share = FolderShare.query.get_or_404(share_id)
    folder = share.folder
    if folder.user_id != current_user.id:
        flash('У доступі відмовлено')
        return redirect(url_for('shares.manage_shares'))
    
    username = share.user.username
    db.session.delete(share)
    db.session.commit()
    flash(f"Скасовано доступ для {username} у папці {folder.name}")
    return redirect(url_for('shares.manage_shares'))  