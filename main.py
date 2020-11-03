from DataMining.tools.data_table_parser import CSV_reader
from flask import Flask, render_template, request, jsonify
import pandas as pd
from io import StringIO
from DataMining.tools.data_table_parser import CSV_reader

app = Flask("Data Mining")

app.config["DATA_UPLOAD"] = "/uploads"

@app.route("/apriori_process", methods=["POST"])
def apriori_process():
    response = {}
    if request.files and request.form:
        file = request.files["file"].read().decode("utf-8")
        df = CSV_reader(StringIO(file),remove_first_column=True)
        min_sup = int(request.form["support"])/100
        min_conf = int(request.form["confidence"])/100
        min_lif = int(request.form["lift"])
        from apyori import apriori
        rules = apriori(df.apyori, min_support=min_sup, min_confidence=min_conf, min_lift=min_lif, min_length=2)
        print(list(rules))
    return jsonify(response)

@app.route("/apriori")
def apriori():
    return render_template("apriori.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/")
def index():
    return render_template("index.html")
app.run(debug=True,port=8000)


#data = CSV_reader('apriori.csv',bool)
#print(data.df)

