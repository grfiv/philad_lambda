from flask import Blueprint, render_template, make_response

from philad_lambda.philad_lambda import get_db

import pandas as pd
import datetime, time, random

index_page_code = Blueprint('index_page_code', __name__,
                            template_folder='templates')


@index_page_code.route("/index")
@index_page_code.route("/index.htm")
@index_page_code.route("/index.html")
def index_page():
    """
    Philadelphia Reflections home page

    :return: Jinja2 rendered template
    """
    conn = get_db()

    random.seed(time.time())

    # 'template_variables' is an assoc array passed to Jinja2 template
    # ================================================================
    template_variables = {}

    copyright_end_year = datetime.datetime.now().year
    template_variables['copyright_end_year'] = copyright_end_year

    # variables for the left column ... topics
    # ========================================
    nTopics = conn.execute('SELECT COUNT(*) FROM topics').fetchone()[0]

    seed = random.randint(0, 1000)
    sql = "SELECT title, description, table_key \
           FROM topics \
           WHERE title LIKE '%%Phila%%' \
           ORDER BY RAND({}) limit 10".format(seed)

    df = pd.read_sql(sql, conn)
    topic_list = df.to_dict(orient='records')

    template_variables['nTopics'] = nTopics
    template_variables['topic_list'] = topic_list

    # variables for the middle column ... blogs
    # =========================================
    nBlogs = conn.execute('SELECT COUNT(*) FROM individual_reflections').fetchone()[0]

    seed = random.randint(0, 1000)
    sql = "SELECT title, description, TRIM(blog_contents) AS blog_contents, table_key \
           FROM individual_reflections \
           WHERE title LIKE '%%Frank%%' \
           ORDER BY RAND({}) limit 5".format(seed)

    df = pd.read_sql(sql, conn)
    blog_list = df.to_dict(orient='records')

    template_variables['nBlogs'] = nBlogs
    template_variables['blog_list'] = blog_list

    # variables for right column ... volumes
    # ======================================
    nVolumes = conn.execute('SELECT COUNT(*) FROM volumes').fetchone()[0]

    seed = random.randint(0, 1000)
    sql = "SELECT title, description, table_key \
           FROM volumes \
           WHERE title LIKE '%%Phila%%' \
           ORDER BY RAND({}) limit 10".format(seed)

    df = pd.read_sql(sql, conn)
    volume_list = df.to_dict(orient='records')

    template_variables['nVolumes'] = nVolumes
    template_variables['volume_list'] = volume_list

    # call the template
    # =================
    response = make_response(render_template('index.html', **template_variables), 404)
    return response
