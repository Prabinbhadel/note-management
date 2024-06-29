from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for
from flask_login import login_required,current_user
from .models import User,Note
from . import db
import json


views=Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method=='POST':
        note=request.form.get('note')
        if len(note)<1:
            flash('note too short',category='error')
        else:
            new_note=Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()


            flash('note added successfully',category='success')
            


    return render_template("home.html",user=current_user)

@views.route('/delete-note',methods=['POST'])
def delete_note():
    note =json.loads(request.data)
    noteId=note['noteId']
    note=Note.query.get(noteId)
    if note:
        if note.user_id==current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('note deleted successfully',category='success')

    return jsonify({})     
@views.route('/edit/<int:id>',methods=["GET","POST"])
def edit(id):
    print(f"Editing note with ID: {id}")
    note=Note.query.get(id)
    if request.method == 'POST':
        note.data = request.form['data']
        db.session.commit()
        flash('note edited successfully',category='success')
        return redirect(url_for('views.home'))
    return render_template('edit.html', note=note)      