from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Boolean, ForeignKey, func
from werkzeug.security import generate_password_hash, check_password_hash
# from openai import OpenAI

import random
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///serveys.db")

# Create the extension
db = SQLAlchemy(model_class=Base)
# initialise the app with the extension
db.init_app(app)

# Create table product
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[str] = mapped_column(String,unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=True)

class Product(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

# Create table Survey
class Survey(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_name: Mapped[str] = mapped_column(String,nullable=False)
    user_id: Mapped[str] = mapped_column(String(6), nullable=False)
    interested_lanched: Mapped[int] = mapped_column(Integer, nullable=False)
    path_to_market: Mapped[int] = mapped_column(Integer, nullable=False)
    pull_sales: Mapped[int] = mapped_column(Integer, nullable=False)
    comments: Mapped[str] = mapped_column(String, nullable=True)

#Create table user
class UserCompletedSurvey(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(6), nullable=False)
    product_id: Mapped[str] = mapped_column(String(250), nullable=False)
    product_Name: Mapped[str] = mapped_column(String(250), nullable=False)


# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()

# Main -----------------------------------------------------
@app.route('/')
def index():

    user_acount = db.session.execute(db.select(User))
    if len(user_acount.all()) == 0:
        new_user_admin = User(user_name='admin', password=os.environ.get('ADMIN_PASSWORD'))
        db.session.add(new_user_admin)
        db.session.commit()

    if not current_user.is_authenticated:
        return redirect(url_for('login_user_def'))

    user_completed_survey = db.session.execute(db.select(UserCompletedSurvey).where(UserCompletedSurvey.user_id == current_user.user_name)).scalars()

    user_completed_survey = [int(survey.product_id) for survey in user_completed_survey]
    surveyed_product = len(user_completed_survey)
    
    result = db.session.execute(db.select(Product))
    if len(result.all()) == 0:
        new_product_a = Product( name="Concept 1", description="Product Concept 1 name")
        new_product_b = Product( name="Concept 2", description="Product Concept 2 name")
        new_product_c = Product( name="Concept 3", description="Product Concept 3 name")
        new_product_d = Product( name="Concept 4", description="Product Concept 4 name")
        new_product_e = Product( name="Concept 5", description="Product Concept 5 name")
        new_product_f = Product( name="Concept 6", description="Product Concept 6 name")
        new_product_g = Product( name="Concept 7", description="Product Concept 7 name")
        new_product_h = Product( name="Concept 8", description="Product Concept 8 name")
        new_product_i = Product( name="Concept 9", description="Product Concept 9 name")
        new_product_j = Product( name="Concept 10", description="Product Concept 10 name")
        new_product_k = Product( name="Concept 11", description="Product Concept 11 name")
        new_product_l = Product( name="Concept 12", description="Product Concept 12 nameL")
        new_product_m = Product( name="Concept 13", description="Product Concept 13 name")
        new_product_o = Product( name="Concept 14", description="Product Concept 14 name")
        new_product_p = Product( name="Concept 15", description="Product Concept 15 name")
        new_product_q = Product( name="Concept 16", description="Product Concept 16 name")
        new_product_z = Product( name="Concept 17", description="Product Concept 17 name")

        db.session.add(new_product_a)
        db.session.add(new_product_b)
        db.session.add(new_product_c)
        db.session.add(new_product_d)
        db.session.add(new_product_e)
        db.session.add(new_product_f)
        db.session.add(new_product_g)
        db.session.add(new_product_h)
        db.session.add(new_product_i)
        db.session.add(new_product_j)
        db.session.add(new_product_k)
        db.session.add(new_product_l)
        db.session.add(new_product_m)
        db.session.add(new_product_o)
        db.session.add(new_product_p)
        db.session.add(new_product_q)
        db.session.add(new_product_z)
        db.session.commit()

    result = db.session.execute(db.select(Product))
    all_products = result.scalars()

    return render_template('index.html', products=all_products, user_id=current_user.user_name, completed_surveys=user_completed_survey, surveyed=surveyed_product, logged_in=current_user.is_authenticated)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if not current_user.is_authenticated:
        return redirect(url_for('login_user_def'))
    
    query = request.args.get('query').lower()
    filtered_products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()

    return render_template('search_results.html', products=filtered_products, query=query)

@app.route('/login-admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == "POST":
        input_user = request.form.get('inputUser')
        input_password = request.form.get('inputPassword')
        
        result = db.session.execute(db.select(User).where(func.lower(User.user_name) == input_user.lower()))
        user = result.scalar()
        # User name or password incorrect.
        if not user:
            flash("That user name incorrect, please try again.")
            return redirect(url_for('login_admin'))
        elif not check_password_hash(user.password, input_password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login_admin'))
        else:
            login_user(user)
            return redirect(url_for('admin'))

    return render_template("login_admin.html", logged_in=current_user.is_authenticated)

@app.route('/login-user', methods=["GET", "POST"])
def login_user_def():
    if request.method == "POST":
        l_user = request.form.get('inputUser')
        result = db.session.execute(db.select(User).where(func.lower(User.user_name) == l_user.lower()))

        user = result.scalar()
        # Email doesn't exist or password incorrect.
        if not user:
            new_user = User(
                user_name=l_user,
            )
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            # return redirect(url_for("index"))
        else:
            if user.user_name.lower() == 'admin':
                flash("That Username only for admin, please go to the admin page to log in if you are an admin.")
                return redirect(url_for('login_user_def'))
            
            login_user(user)

        return redirect(url_for('index'))

    return render_template("login_user.html")

@app.route('/register-user', methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        r_user = request.form.get('inputUser')
        result = db.session.execute(db.select(User).where(func.lower(User.user_name) == r_user.lower()))
        
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        if user:
            # User already exists
            flash("That Username already exist, Please register with another name!")
            return redirect(url_for('register_user'))

        if ' ' in r_user:
            flash("There must be no spaces in the username!")
            return redirect(url_for('register_user'))

        new_user = User(
            user_name=r_user,
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("index"))
    
    return render_template("register_user.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Survey ------------------------------------------------------
@app.route('/survey/<survey_id>', methods=['GET', 'POST'])
def survey(survey_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login_user_def'))

    # user_id = session.get('user_id')
    survey = db.session.execute(db.select(Product).where(Product.id == survey_id)).scalar()
    # survey = surveys.get(survey_id)
    if not survey:
        return redirect(url_for('index'))
    
    user_completed_survey = db.session.execute(db.select(UserCompletedSurvey).where(UserCompletedSurvey.user_id == current_user.user_name)).scalars()

    user_completed_survey = [survey.product_id for survey in user_completed_survey]
    surveyed_product = len(user_completed_survey)

    if request.method == 'POST':
        comment_ai = None
        new_completed_survey = UserCompletedSurvey(user_id=current_user.user_name, product_Name=survey.name, product_id=survey_id)
        db.session.add(new_completed_survey)
        db.session.commit()

        interested_lanch = int(request.form['launched'])
        path_to_mar = int(request.form['pathmarket'])
        pull_sale = int(request.form['pullsales'])
        comment = request.form['comment']
        new_survey = Survey(product_name=survey.name, user_id=current_user.user_name, interested_lanched=interested_lanch, path_to_market=path_to_mar, pull_sales=pull_sale, comments=comment)
        db.session.add(new_survey)
        db.session.commit()

        # if comment == '':
        #     prompt = f"Given the ratings: 'How interested are you in having this product launched?': {interested_lanch}, 'The path to market for this product concept established?': {path_to_mar}, 'Do you feel this product will “pull” sales of other products along?': {pull_sale}, generate a short comment."
        #     response = client.chat.completions.create(
        #         model="gpt-3.5-turbo",
        #         messages=[
        #             {"role": "user", "content": prompt},
        #         ]
        #     )
        #     comment_ai = response.choices[0].text.strip()

        return redirect(url_for('thank_you'))
    
    return render_template('survey.html', survey=survey, user_id=current_user.user_name, surveyed=surveyed_product)

# ------------------------------------------------------
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

def measure_survey():
    surveys = db.session.execute(db.select(Survey)).scalars()
    check_count = len(surveys.all())
    surveys = db.session.execute(db.select(Survey)).scalars()
    if check_count > 0:
        df = pd.DataFrame([{
            'product_name': survey.product_name,
            'interested_lanched': survey.interested_lanched,
            'path_to_market': survey.path_to_market,
            'pull_sales': survey.pull_sales
        } for survey in surveys])
        
        df_measure_survey = df.groupby('product_name').agg(
            Rating =('product_name', 'size'),
            Participation=('product_name', 'size'),
            Average_interested_lanched=('interested_lanched', 'mean'),
            Average_path_to_market=('path_to_market', 'mean'),
            Average_pull_sales=('pull_sales', 'mean'),
        ).reset_index()

        df_measure_survey['Rating'] = df_measure_survey[['Average_interested_lanched', 'Average_path_to_market', 'Average_pull_sales']].mean(axis=1)
        df_measure_survey['Rating'] = df_measure_survey['Rating'].round(2)
        df_measure_survey['Average_interested_lanched'] = df_measure_survey['Average_interested_lanched'].round(2)
        df_measure_survey['Average_path_to_market'] = df_measure_survey['Average_path_to_market'].round(2)
        df_measure_survey['Average_pull_sales'] = df_measure_survey['Average_pull_sales'].round(2)
        df_measure_survey = df_measure_survey.sort_values(by='Rating', ascending=False)
        return df_measure_survey.to_dict(orient='records')
    else:
        return pd.DataFrame()

# Admin web ------------------------------------------
@app.route('/admin')
def admin():
    
    if not current_user.is_authenticated:
        return redirect(url_for('login_admin'))

    df_measure_survey = measure_survey()
    total_surveys = len(df_measure_survey)
    total_user = 0
    user_surveys = db.session.execute(db.select(UserCompletedSurvey)).scalars()
    check_count = len(user_surveys.all())
    user_surveys = db.session.execute(db.select(UserCompletedSurvey)).scalars()
   
    if check_count > 0:
        df = pd.DataFrame([{
                'user_id': survey.user_id,
            } for survey in user_surveys])
        print(df)
        grouped_df = df.groupby('user_id').size().reset_index(name='num_surveys')
        total_user = grouped_df['user_id'].nunique()

    # print(df_measure_survey)
    return render_template('index_admin.html', measure_survey = df_measure_survey, total_surveys=total_surveys, total_user=total_user)


# Product Table ------------------------------------------
@app.route('/admin/product')
def product_table():
    if not current_user.is_authenticated:
        return redirect(url_for('login_admin'))

    product_all = db.session.execute(db.select(Product)).scalars()
    
    return render_template('product_admin.html', products = product_all)

# Add Product------------------------------------------
@app.route('/admin/add', methods=['GET', 'POST'])
def add_product():

    if not current_user.is_authenticated:
        return redirect(url_for('login_admin'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        new_product = Product(name=name, description=description)
        db.session.add(new_product)
        db.session.commit()

    return redirect(url_for('product_table'))

@app.route('/admin/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login_admin'))

    product = db.session.execute(db.select(Product).where(Product.id == product_id)).scalar()
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        db.session.commit()
        
    return redirect(url_for('product_table'))


# survey Table ------------------------------------------
@app.route('/admin/survey')
def survey_table():
    if not current_user.is_authenticated:
        return redirect(url_for('login_admin'))

    survey_all = db.session.execute(db.select(Survey)).scalars()
    
    return render_template('survey_admin.html', surveys = survey_all)

# survey Table ------------------------------------------
@app.route('/admin/user-completed-survey')
def user_completed_table():
    if not current_user.is_authenticated:
        return redirect(url_for('login_admin'))

    user_completed_all = db.session.execute(db.select(UserCompletedSurvey)).scalars()
    
    return render_template('user_completed_admin.html', user_completed = user_completed_all)

# Product Bizarre 2024 Rank Chart ------------------------------------------
@app.route('/admin/rank-chart')
def rank_chart_data():
    df_measure_survey = measure_survey()
    if len(df_measure_survey) > 0:
        # labels = df_measure_survey['product_name'].tolist()
        labels = [product['product_name'] for product in df_measure_survey]
        values = [product['Rating'] for product in df_measure_survey]

        data = {'labels': labels[:10], 'values': values[:10]}
    else:
        data = {'labels': [], 'values': []}
    
    return jsonify(data)

# Product Bizarre 2024 Participation Chart ------------------------------------------
@app.route('/admin/participation-chart')
def participation_chart_data():
    df_measure_survey = measure_survey()
    if len(df_measure_survey) > 0:
        df_measure_survey = sorted(df_measure_survey, key=lambda entry: entry['Participation'], reverse=True)
        labels = [product['product_name'] for product in df_measure_survey]
        values = [product['Participation'] for product in df_measure_survey]

        data = {'labels': labels[:10], 'values': values[:10]}
    else:
        data = {'labels': [], 'values': []}
    
    return jsonify(data)

# Product Bizarre 2024 interested lanched Chart ------------------------------------------
@app.route('/admin/interested-lanched-chart')
def interested_chart_data():
    df_measure_survey = measure_survey()
    if len(df_measure_survey) > 0:
        df_measure_survey = sorted(df_measure_survey, key=lambda entry: entry['Average_interested_lanched'], reverse=True)
        labels = [product['product_name'] for product in df_measure_survey]
        values = [product['Average_interested_lanched'] for product in df_measure_survey]

        data = {'labels': labels[:10], 'values': values[:10]}
    else:
        data = {'labels': [], 'values': []}
    
    return jsonify(data)

# Product Bizarre 2024 path to market Chart ------------------------------------------
@app.route('/admin/path-to-market-chart')
def market_chart_data():
    df_measure_survey = measure_survey()
    if len(df_measure_survey) > 0:
        df_measure_survey = sorted(df_measure_survey, key=lambda entry: entry['Average_path_to_market'], reverse=True)
        labels = [product['product_name'] for product in df_measure_survey]
        values = [product['Average_path_to_market'] for product in df_measure_survey]

        data = {'labels': labels[:10], 'values': values[:10]}
    else:
        data = {'labels': [], 'values': []}
    
    return jsonify(data)

# Product Bizarre 2024 pull sale Chart ------------------------------------------
@app.route('/admin/pull-sales-chart')
def pull_chart_data():
    df_measure_survey = measure_survey()
    if len(df_measure_survey) > 0:
        df_measure_survey = sorted(df_measure_survey, key=lambda entry: entry['Average_pull_sales'], reverse=True)
        labels = [product['product_name'] for product in df_measure_survey]
        values = [product['Average_pull_sales'] for product in df_measure_survey]

        data = {'labels': labels[:10], 'values': values[:10]}
    else:
        data = {'labels': [], 'values': []}
    
    return jsonify(data)

# Main python ------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=False, port=5001)
