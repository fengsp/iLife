from flask import Flask


app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "ilife"}
app.secret_key = 'fspilifefspilifefspilife'
app.debug = True

from iLife.views.hello import hello
from iLife.views.tumblelog import tumblelog
app.register_module(hello)
app.register_module(tumblelog)
