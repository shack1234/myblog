
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField, RadioField
from wtforms.validators import Required

# A form to enable users to add their bio 
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit') 
  
# A form to enable users to add their blog    
class Blogs(FlaskForm):
    title = StringField('Enter Blog Title',validators=[Required()])
    blogc = TextAreaField('Write your blog here',validators=[Required()])
    submit = SubmitField('Add Blog')