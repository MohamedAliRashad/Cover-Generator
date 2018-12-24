from flask import Flask, render_template, url_for, flash, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField
from wtforms_components import ColorField, SelectField
from wtforms.validators import DataRequired, Length
import racovimge
import cairosvg
import os

Templates = ["Blocks", "Column", "Cross", "Gradient", "Rings", "Simple Dark", "Simple", "Tiles", "Window"]

# Fonts = ["Alex Brush", "Gidole", "Crimson", "Horta", "Petit Formal Script",
#         "Bellota", "Liberation Serif", "Sofia", "Bradley Gratis", "Glacial Indifference",
#         "Libre Baskerville", "Unique", "Caladea", "Great Vibes", "Orkeny"]

class BookForm(FlaskForm):

    BookTitle = StringField('Book Title', validators=[DataRequired(), Length(min=2, max=20)])

    CoverTemplate = SelectField('Cover Template', choices=list((str(Templates[i]),)*2 for i in range(len(Templates))), validators=[DataRequired()])

    # Font = SelectField('Font', choices=list((str(Fonts[i]),)*2 for i in range(len(Templates))), validators=[DataRequired()])

    AuthorName = StringField('Author Name', validators=[DataRequired(), Length(min=2, max=20)])
    
    BackgroundColor = ColorField('Background Color', validators=[DataRequired()])

    Puplisher = StringField('Puplisher', validators=[DataRequired(), Length(min=2, max=20)])

    PuplishingYear = SelectField('Puplishing Year', choices=list((str(2018-i),)*2 for i in range(0,50)) , validators=[DataRequired()] )

    Generate = SubmitField('Generate')

# Initilaizing The App & DataBase
app = Flask(__name__)

app.config['SECRET_KEY'] = 'ccc6fd2dd37ee84209c87333365aea5b3e94b94e' 

@app.route("/")
# Home Directory
@app.route("/Home", methods=["GET", "POST"])
def Home():
    form = BookForm()
    
    if form.validate_on_submit():

        try:            
            with open('static/images/Cover.svg', 'w') as stream:
                # font sizes can be set explicitly even for random covers
                stream.write(racovimge.cover(
                    title=form.BookTitle.data,
                    author=[form.Puplisher.data, form.AuthorName.data],
                    template=form.CoverTemplate.data,
                    colors=[form.BackgroundColor.data, '#829fe4', '#6692c3', '#4878a4', '#00305a'],   # if you want random caolrs => ["#%06x" % random.randint(0, 0xFFFFFF)]
                    font="static/fonts/Gidole.ttf",
                    font_size=120,                          # Used for the title of the book.
                    font_size_author=70                     # Used for the authors.
                    )) 
    
            # Converting SVG To PNG           
            cairosvg.svg2png(url=os.path.join(os.getcwd(), "static/images/Cover.svg"), write_to=os.path.join(os.getcwd(), "static/images/Cover.png"))

            # Flash Message if everything finished successfully
            flash("Thank you, For using our service!", 'success')

            return render_template('Home.html', form=form, img_path = os.path.join(os.getcwd(), "static/images/Cover.png"))

        except:

            # Flash Message if anything happened wrong
            flash("Something went wrong!", 'danger')
            return redirect(url_for('Home'))
    
    return render_template('Home.html', form=form, img_path = "static/images/cat_with_horns.jpg")




if __name__ == '__main__':
    app.run(debug=True)
    # with open('static/images/cover.svg', 'w') as stream:
    #     # font sizes can be set explicitly even for random covers
    #     stream.write(racovimge.cover(
    #         title='Embedded',
    #         author='Rashad',
    #         template='Blocks',
    #         colors=['#000000']*5,   # if you want random caolrs => ["#%06x" % random.randint(0, 0xFFFFFF)]
    #         font='static/fonts/Gidole.ttf',
    #         font_size=120,                          # Used for the title of the book.
    #         font_size_author=70                     # Used for the authors.
    #         )) 

    # # Converting SVG To PNG           
    # cairosvg.svg2png(url="static/images/cover.svg", write_to="static/images/cover.png")