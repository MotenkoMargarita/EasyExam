from flask_login import UserMixin

from app import db, DEFAULT_PROFILE_IMAGE

test_question = db.Table('test_question',
                         db.Column('test_id', db.Integer, db.ForeignKey('test.id'), primary_key=True),
                         db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True)
                         )

user_read_material = db.Table('user_read_material',
                              db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                              db.Column('material_id', db.Integer, db.ForeignKey('material.id'), primary_key=True)
                              )


class Region(db.Model):
    __tablename__ = "region"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)

    cities = db.relationship('City', backref='region', lazy=True)


class City(db.Model):
    __tablename__ = "city"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)

    users = db.relationship('User', backref='city', lazy=True)

    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    value = db.Column(db.Integer, unique=False, nullable=False)

    users = db.relationship('User', backref='role', lazy=True)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(123), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    first_name = db.Column(db.String(255), unique=False, nullable=False)
    last_name = db.Column(db.String(255), unique=False, nullable=False)
    active = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    src = db.Column(db.String(1023), unique=False, nullable=False, default=DEFAULT_PROFILE_IMAGE)
    activation_code = db.Column(db.String(255), unique=False, nullable=True)
    reset_code = db.Column(db.String(255), unique=False, nullable=True, default=None)
    registration_date = db.Column(db.TIMESTAMP, unique=False, nullable=False)
    last_password_reset = db.Column(db.TIMESTAMP, unique=False, nullable=True)


    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    results = db.relationship('Result', backref='user', lazy=True)

    materials = db.relationship('Material', secondary=user_read_material, lazy=False,
                                backref=db.backref('materials', lazy=True))

    def is_active(self):
        return self.active


class TeachersStudents(db.Model):
    __tablename__ = "teachersStudents"
    student_id = db.Column(db.Integer, unique=False, nullable=False, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)


class Result(db.Model):
    __tablename__ = "result"
    id = db.Column(db.Integer, primary_key=True)
    first_part_first_mark = db.Column(db.Float, unique=False, nullable=False)
    result_first_mark = db.Column(db.Float, unique=False, nullable=False)
    first_part_test_mark = db.Column(db.Integer, unique=False, nullable=False)
    result_test_mark = db.Column(db.Integer, unique=False, nullable=False)
    time_spent = db.Column(db.String(127), unique=False, nullable=False)
    solution_file = db.Column(db.String(1023), unique=False, nullable=True)
    teacher_file = db.Column(db.String(1023), unique=False, nullable=True)
    teacher_id = db.Column(db.Integer, unique=False, nullable=True)
    is_checked = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    commentary = db.Column(db.String(511), unique=False, nullable=True)

    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    resultQuestions = db.relationship('ResultQuestion', backref='result', lazy=True)


class ResultQuestion(db.Model):
    __tablename__ = "resultQuestion"
    id = db.Column(db.Integer, primary_key=True)
    user_answer = db.Column(db.String(127), unique=False, nullable=True)
    commentary = db.Column(db.String(511), unique=False, nullable=True)
    mark = db.Column(db.Integer, unique=False, nullable=True)

    result_id = db.Column(db.Integer, db.ForeignKey('result.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)


class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254), unique=False, nullable=False)
    time_limit = db.Column(db.Float, unique=False, nullable=False)
    question_count = db.Column(db.Integer, unique=False, nullable=False)

    question_info = db.relationship('QuestionInfo', backref='subject', lazy=True)
    first_score_test_scores = db.relationship('FirstScoreTestScore', backref='subject', lazy=True)

    questions = db.relationship('Question', backref='subject', lazy=True)


class Theme(db.Model):
    __tablename__ = "theme"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254), unique=False, nullable=False)
    description = db.Column(db.String(1023), unique=False, nullable=True)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)


class Material(db.Model):
    __tablename__ = "material"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254), unique=False, nullable=False)
    text = db.Column(db.String(10000), unique=False, nullable=False)
    number_in_order = db.Column(db.Integer, unique=False, nullable=True)
    description = db.Column(db.String(1023), unique=False, nullable=False)
    file = db.Column(db.String(1023), unique=False, nullable=True)

    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'), nullable=False)
    images = db.relationship('Image', backref='material', lazy=True)

    users = db.relationship('User', secondary=user_read_material, lazy=False,
                            backref=db.backref('users', lazy=True))


class FirstScoreTestScore(db.Model):
    __tablename__ = "firstScoreTestScore"
    id = db.Column(db.Integer, primary_key=True)
    first_score = db.Column(db.Integer, unique=False, nullable=False)
    test_score = db.Column(db.Integer, unique=False, nullable=False)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)


class QuestionInfo(db.Model):
    __tablename__ = "questionInfo"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=False, nullable=False)
    max_mark = db.Column(db.Float, unique=False, nullable=False)

    questionType_id = db.Column(db.Integer, db.ForeignKey('questionType.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)


class TestType(db.Model):
    __tablename__ = "testType"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)

    tests = db.relationship('Test', backref='testType', lazy=True)


class Test(db.Model):
    __tablename__ = "test"
    id = db.Column(db.Integer, primary_key=True)
    is_for_theme = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    number_in_order = db.Column(db.Integer, unique=False, nullable=True)
    description = db.Column(db.String(1023), unique=False, nullable=True)
    max_first_score = db.Column(db.Integer, unique=False, nullable=True)

    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'), nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    testType_id = db.Column(db.Integer, db.ForeignKey('testType.id'), nullable=False)

    questions = db.relationship('Question', secondary=test_question, lazy=False,
                                backref=db.backref('questions', lazy=True))


class Source(db.Model):
    __tablename__ = "source"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1023), unique=False, nullable=False)
    link = db.Column(db.String(1023), unique=False, nullable=False)

    questions = db.relationship('Question', backref='source', lazy=True)




class QuestionType(db.Model):
    __tablename__ = "questionType"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)


class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2048), unique=False, nullable=False)
    number = db.Column(db.Integer, unique=False, nullable=False)
    answer = db.Column(db.String, unique=False, nullable=False)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'), nullable=True)

    images = db.relationship('Image', backref='question', lazy=True)

    resultQuestions = db.relationship('ResultQuestion', backref='question', lazy=True)

    tests = db.relationship('Test', secondary=test_question, lazy=False, backref=db.backref('tests', lazy=True))

    solutions = db.relationship('Solution', backref='question', lazy=True)


class Solution(db.Model):
    __tablename__ = "solution"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2047), unique=False, nullable=False)
    description = db.Column(db.String(1023), unique=False, nullable=False)

    file = db.Column(db.String(1023), unique=False, nullable=True)
    images = db.relationship('Image', backref='solution', lazy=True)

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)


class Requirement(db.Model):
    __tablename__ = "requirement"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=False, nullable=False)
    text = db.Column(db.String(1023), unique=False, nullable=False)

    criteria = db.relationship('Criteria', backref='criteria', lazy=True)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)


class Criteria(db.Model):
    __tablename__ = "criteria"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1023), unique=False, nullable=False)
    value = db.Column(db.Integer, unique=False, nullable=False)

    requirement_id = db.Column(db.Integer, db.ForeignKey('requirement.id'), nullable=False)


class Audio(db.Model):
    __tablename__ = "audio"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source = db.Column(db.String(1023), unique=False, nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=True)
    solution_id = db.Column(db.Integer, db.ForeignKey('solution.id'), nullable=True)


class Image(db.Model):
    __tablename__ = "image"
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(1023), unique=False, nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=True)
    solution_id = db.Column(db.Integer, db.ForeignKey('solution.id'), nullable=True)
