import uuid
import datetime

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.jinja_env.trim_blocks = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:13d11m1976g@localhost:5432/exam'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'hsdkfjhsdjhadjkyuewyhfuehmndkhasjfhuiesdjvhasjdf'
UPLOAD_FOLDER = 'static/image/uploads'
UPLOAD_FOLDER_FOR_SOLUTIONS = 'static/files'
DEFAULT_PROFILE_IMAGE = 'defaultProfile1.png'
ALLOWED_PROFILE_IMAGE_EXTENSIONS = {'jpeg', 'jpg', 'gif', 'tiff', 'png', 'bmp', 'svg', 'WebP', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_FOR_SOLUTIONS'] = UPLOAD_FOLDER_FOR_SOLUTIONS
db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager(app)

app.config['MAIL_SERVER'] = 'smtp.ethereal.email'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'ida76@ethereal.email'
app.config['MAIL_PASSWORD'] = 'GqrDfJaefv4PGcRWaM'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

from model import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from routes.theme import themeTest, createTheme, themes

from routes.test import test, showTest, testType, createTest, tests

from routes.location import region, city

from routes.subject import subject, subjects

from routes.question import questionRequirements, questionSource, questionType, source, questionInfo, question, \
    criteria, solution

from routes.security import logout, login, resetPassword, registration


from routes.general import welcome, profile, adminPanel, fileUpload, termsOfUse, \
    students, teacherPanel, checkStudentWork, fileDownload, results,\
    fillTheme, markMaterialAsReaded, rating, error

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()

if False:
    with app.app_context():
        Teacher = Role(
            name='Teacher',
            value=1
        )
        db.session.add(Teacher)
        db.session.commit()
        Admin = Role(
            name='Admin',
            value=2
        )
        db.session.add(Admin)
        db.session.commit()
        Student = Role(
            name='Student',
            value=0
        )
        db.session.add(Student)
        db.session.commit()

        region = Region(
            name='Моего субъекта нет'
        )
        db.session.add(region)
        db.session.commit()

        city = City(
            name="Моего города нет",
            region_id=1
        )
        db.session.add(city)
        db.session.commit()

        admin = User(
            email='a@a',
            password=generate_password_hash('admin1243'),
            first_name='admin',
            last_name='admin',
            identifier=uuid.uuid4(),
            role_id=Role.query.filter(Role.name == 'Admin').first().id,
            activation_code=uuid.uuid4(),
            active=True,
            registration_date=datetime.datetime.now(),
            city_id=1
        )

        db.session.add(admin)
        db.session.commit()

        student1 = User(
            email='student1@s',
            password=generate_password_hash('student11243'),
            first_name='student',
            last_name='student',
            identifier=uuid.uuid4(),
            role_id=Role.query.filter(Role.name == 'Student').first().id,
            activation_code=uuid.uuid4(),
            active=True,
            registration_date=datetime.datetime.now(),
            city_id=1
        )

        db.session.add(student1)
        db.session.commit()

        student2 = User(
            email='student2@s',
            password=generate_password_hash('student21243'),
            first_name='student',
            last_name='student',
            identifier=uuid.uuid4(),
            role_id=Role.query.filter(Role.name == 'Student').first().id,
            activation_code=uuid.uuid4(),
            active=True,
            registration_date=datetime.datetime.now(),
            city_id=1
        )

        db.session.add(student2)
        db.session.commit()

        teacher = User(
            email='teacher@t',
            password=generate_password_hash('teacher1243'),
            first_name='teacher',
            last_name='teacher',
            identifier=uuid.uuid4(),
            role_id=Role.query.filter(Role.name == 'Teacher').first().id,
            activation_code=uuid.uuid4(),
            active=True,
            registration_date=datetime.datetime.now(),
            city_id=1
        )

        db.session.add(teacher)
        db.session.commit()

        qt = QuestionType(
            name='B'
        )
        db.session.add(qt)
        db.session.commit()
        qt = QuestionType(
            name='C'
        )
        db.session.add(qt)
        db.session.commit()

        src = Source(
            name='Решу егэ',
            link='https://ege.sdamgia.ru/'
        )
        db.session.add(src)
        db.session.commit()

        src = Source(
            name='Ларин',
            link='https://alexlarin.net/'
        )
        db.session.add(src)
        db.session.commit()


        test_type = TestType(
            name="Экзамен"
        )
        db.session.add(test_type)
        db.session.commit()

        db.session.add(src)
        db.session.commit()

        test_type = TestType(
            name="Тесты"
        )
        db.session.add(test_type)
        db.session.commit()

