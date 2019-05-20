#import pandas as pd
from api import app
from requests import get, post
import flask

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
