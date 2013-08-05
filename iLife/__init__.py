from flask import Flask


app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "ilife"}
app.secret_key = 'fspilifefspilifefspilife'
app.debug = True

from iLife.views.hello import hello
from iLife.views.iblog import iblog
from iLife.views.ilife import ilife
from iLife.views.inews import inews
from iLife.views.imovie import imovie

app.register_module(hello, url_prefix='/hello')
app.register_module(iblog)
app.register_module(ilife)
app.register_module(inews)
app.register_module(imovie)
