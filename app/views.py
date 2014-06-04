from flask import render_template, request
from app import app, con
from app.helpers.database import world_index, get_all
import jinja2
import decimal


# ROUTING/VIEW FUNCTIONS
@app.route('/')
@app.route('/index')
def index():
    # Renders index.html.
    return render_template('index.html')

@app.route('/world', methods=['GET'])
def world():
    print request.args
    # Renders page with world data
    country = request.args.get("country")
    edu_index = request.args.get("edu_index", '0')
    median_age = request.args.get("median_age", '0')
    gdp = request.args.get("gdp", '0')
    order_by = request.args.get("order_by", "edu_index")
    sort = request.args.get("sort", "DESC")

    def format_currency(value):
        return "${:,}M".format(value)

    jinja2.filters.FILTERS['format_currency'] = format_currency

    # if not country:
    #     data = get_all(con)
    # else:
    data = world_index(con, country, edu_index, median_age, gdp, order_by, sort)
    return render_template('world.html',
        data=data,
        edu_index=edu_index,
        median_age=median_age,
        gdp=gdp,
        order_by=order_by,
        sort=sort)

@app.route('/home')
def home():
    # Renders home.html.
    return render_template('home.html')

@app.route('/slides')
def about():
    # Renders slides.html.
    return render_template('slides.html')

@app.route('/author')
def contact():
    # Renders author.html.
    return render_template('author.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
