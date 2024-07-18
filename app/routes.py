from flask import render_template, flash, redirect, url_for, request, session
from app import app, bcrypt, db
from app.forms import RegisterForm, LoginForm, AddBookForm, UpdateForm, DeleteForm
from app.models import User, Book


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    checkbox = request.form.get("terms")
    message = None
    if form.validate_on_submit():
        if checkbox == "agree":
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        password=hashed_password
                        )
            db.session.add(user)
            db.session.commit()
            flash("Successfully registered!", "success")
            return redirect(url_for('login'))
        else:
            message = "You have to agree to the terms."
    return render_template('register.html', form=form, message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash("Logged in successfully!", "success")
            return redirect(url_for('home_menu'))
    return render_template('login.html', form=form)


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/home_menu')
def home_menu():
    if not session.get('user_id'):
        return redirect(url_for('login'))

    return render_template('home_menu.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if not session.get('user_id'):
        return redirect(url_for('login'))

    form = AddBookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data,
                    author=form.author.data,
                    page_count=form.page_count.data,
                    owner_id=session['user_id'])
        db.session.add(book)
        db.session.commit()
        flash("Successfully added!", "success")
        return redirect(url_for('home_menu'))
    return render_template('add_book.html', form=form)


@app.route('/my_book')
def my_book():
    books = Book.query.filter_by(owner_id=session['user_id']).all()
    return render_template('my_book.html', books=books)


@app.route('/update_book', methods=['GET', 'POST'])
def update_book():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    form = UpdateForm()
    book = Book.query.filter_by(id=form.id.data).first()
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.page_count = form.page_count.data
        db.session.commit()
        flash("Post successfully updated", "success")
        return redirect(url_for("my_book"))
    return render_template('update.html', form=form)


@app.route('/top_book')
def top_book():
    books = Book.query.all()
    return render_template('/top_book.html', books=books)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    form = DeleteForm()
    if form.validate_on_submit():
        book = Book.query.filter_by(id=form.id.data).first()
        db.session.delete(book)
        db.session.commit()
        flash("Successfully deleted!", "success")
        return redirect(url_for('my_book'))
    return render_template('delete.html', form=form)


@app.route('/log_out')
def log_out():
    session.pop("user_id")
    flash(f"Successfully logged out", "info")
    return redirect(url_for("home"))
