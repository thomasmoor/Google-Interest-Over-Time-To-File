from flask import Flask, json, jsonify, redirect, render_template, request, session, make_response, url_for
from flask_cors import CORS, cross_origin
from flask_session import Session
import json
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from pytrends.request import TrendReq

# pip install flask flask_cors Flask_Session matplotlib pytrends

ma_long=252
ma_medium=52
ma_short=6
max_keywords=5
timeframes = ['today 5-y','today 12-m','today 3-m','today 1-m']
cat = '0'
geo = 'US'
gprop = ''

# Create the Flask instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing for API use from another IP and/or port
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Use Flask server session to avoid a "Confirm Form Resubmission" pop-up:
# Redirect and pass form values from post to get method
app.config['SECRET_KEY'] = "your_secret_key" 
app.config['SESSION_TYPE'] = 'filesystem' 
app.config['SESSION_PERMANENT']= False
app.config.from_object(__name__)
Session(app)

# Results dict
def google_data(keyword,s):
  # Moving Averages
  mal = s.ewm(span=ma_long, adjust=False).mean()
  mam = s.ewm(span=ma_medium, adjust=False).mean()
  mas = s.ewm(span=ma_short, adjust=False).mean()
  r={
    'keyword':keyword,
    'last':int(s[-1]),
    'max': int(s.loc[s.idxmax()]),
    'min': int(s.loc[s.idxmin()]),
    'mal' : round(mal[-1],1),
    'mam' : round(mam[-1],1),
    'mas' : round(mas[-1],1),
  }
  print(f"kw:{r['keyword']} last:{r['last']} min:{r['min']} max:{r['max']} mal:{r['mal']} mam:{r['mam']} mas:{r['mas']}")
  return r
# google_data

# Extract the Google Trends data for the given keywords
def extract(str):
  # Get the list of keywords
  keywords=str.split(',')
  # Restrict to max_keywords
  keywords=keywords[:max_keywords]  
  # Build the pytrends payload
  pytrends.build_payload(keywords,
    cat,
    timeframes[0],
    geo,
    gprop
  )
  # Retrieve the Google Trends Interest Over Time
  df=pytrends.interest_over_time()
  # print(df.describe)
  # Prepare the results
  results=[]
  for keyword in keywords:
    results.append(google_data(keyword,df[keyword]))
  print(f"results 1 length: {len(results)}")
  for result in results:
    print(f"results 1 - k:{result['keyword']} {result['last']}")
  return results
# extract

# API Endpoint
@app.route('/getgoogleiot', methods=['POST'])
@cross_origin()
def api():
  if request.data:
    data = json.loads(request.data)
  else:
    data=request.form
  print("data:")
  print(data)
  keywords=data['keywords']
  print(f"GoogleTrends - branch: api - keywords: {keywords}")
  results=extract(keywords)
  return jsonify(results)
# api

# HTML home page
@app.route('/', methods=['GET','POST'])
def slash():

  # The 'extract' button was pressed
  if 'extract' in request.form:
    # keywords="SEO,yfinance"
    keywords = request.form["keywords"]
    print(f"GoogleTrends - branch: extract - keywords: {keywords}")
    results=extract(keywords)
  
  # Download Option
  elif 'download' in request.form and 'results' in session:
    text="Keyword,Last,Max,Min,Avg 5Y,Avg 1Y,Avg 6W\n"
    results=json.loads(session['results'])
    for r in results:
      text+=f"{r['keyword']},{r['last']},{r['max']},{r['min']},{r['mal']},{r['mam']},{r['mas']}\n"
    print(f"Branch: Download - text len={len(text)}")
    output = make_response(text)
    output.headers["Content-Disposition"] = "attachment; filename=thomasmoor-googleIOT.csv"
    output.headers["Content-type"] = "text/csv"
    return output
  
  # Redirect
  if request.method=='POST':
    print("GoogleTrends - branch: redirect")
    print(f"results 3 length: {len(results)}")
    for result in results:
      print(f"results 3 - k:{result['keyword']} {result['last']}")
    session['results'] = json.dumps(results)
    return redirect(url_for('slash'))

  # Render
  else:
    # print(f"data 4 length: {len(data)}")
    # for d in data:
    #   print(f"data 4 - k:{d.keyword} {d.last}")
    print("GoogleTrends - branch: render index.html")
    if 'results' in session:
      j=session['results']
      print("j:")
      print(j)
      if j:
        results=json.loads(session['results'])
      else:
        results=[]
      # print(f"results length:{len(results)}")
      # for result in results:
      #   print(result)
      # https://stackoverflow.com/questions/51932277/print-values-of-array-of-arrays-in-flask
    else:
      results=[]
    return render_template("index.html",results=results)
  
# slash

# Set the pytrends API language
pytrends = TrendReq(hl='en-US')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5004, debug=True)
