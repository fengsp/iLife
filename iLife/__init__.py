from flask import Flask
from iLife.views.hello import hello


app = Flask(__name__)
app.register_module(hello)
app.secret_key = 'fspilifefspilifefspilife'
