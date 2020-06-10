from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('닉네임', 
        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('이메일',
        validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', 
        validators=[DataRequired()])
    confirm_password = PasswordField('비밀번호 확인', 
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('회원가입')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('이메일',
        validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', 
        validators=[DataRequired()])
    remember = BooleanField('이 아이디와 암호를 기억')
    submit = SubmitField('로그인')

class UpdateAccountForm(FlaskForm):
    username = StringField('닉네임', 
        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('이메일',
        validators=[DataRequired(), Email()])
    picture = FileField('프로필 사진 변경', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('수정완료')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('이 닉네임은 이미 존재하는 닉네임입니다. 다른 닉네임을 사용하세요.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('이 이메일은 이미 존재하는 이메일입니다. 다른 이메일을 사용하세요.')

class PostForm(FlaskForm):
    title = StringField('제목', validators=[DataRequired()])
    content = TextAreaField('내용', validators=[DataRequired()])
    submit = SubmitField('작성')