from flask_wtf import FlaskForm,Form
from wtforms import StringField,TextAreaField,SubmitField,PasswordField,BooleanField,RadioField,ValidationError
from wtforms.validators import Required,Email,EqualTo



class BlogForm(FlaskForm):
	title = StringField('Title', validators=[Required()])
	description = TextAreaField("Type your desired quote?",validators=[Required()])
	submit = SubmitField('Submit')

class CommentForm(FlaskForm):
	description = TextAreaField('Add comment',validators=[Required()])
	submit = SubmitField()