# External Modules
from flask import Flask, render_template, request, jsonify, send_file, Response, abort
import json
import pandas as pd
import numpy as np
from io import StringIO, BytesIO
from base64 import b64encode
import matplotlib
import os
import pickle
# Modules
from DataMining.tools.data_table_parser import CSV_reader
from DataMining.tools.apyori_parser import rules_to_html
from DataMining.tools.reader import Reader
from DataMining.tools.data_obj import Data
from DataMining.tools.table_html import TableHTML
from DataMining.algorithms.distance import Distance
from DataMining.algorithms.clustering import Clustering
from DataMining.algorithms.linear_reg import LinearReg
from DataMining.algorithms.logistic_reg import LogisticReg
from DataMining.tools.html_tools import HTML_tools
# Configurations
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask("Data Mining")
app.config["DATA_UPLOAD"] = "/uploads"
data_config = {}


def df_to_csv(df, decimal_round=3):
    file = StringIO()
    df.round(decimal_round).to_csv(file)
    return file.getvalue()

def set_export_data(file,filename):
    global data_config
    # Export Data #########################################
    data_config["EXPORT_FILE"] = file
    data_config["EXPORT_FILENAME"] = filename
    #######################################################

def get_image_b64(b64encoded):
    image = """
        <img src="data:image/png;base64,{b64}"/>
    """
    return image.format(b64=b64encoded.decode("utf-8"))

def get_html_by_figure(figure):
    pic_IObytes = BytesIO()
    figure.savefig(pic_IObytes,format='png')
    pic_IObytes.seek(0)
    pic_hash = b64encode(pic_IObytes.read())
    image_hash = get_image_b64(pic_hash)
    plt.close()
    return image_hash


def get_correlation_heatmap(matrix_correlation):
    from matplotlib import rcParams
    rcParams.update({'figure.autolayout': True})
    import seaborn as sb 
    pic_IObytes = BytesIO()
    heatmap = sb.heatmap(matrix_correlation, annot = True)
    # fix for mpl bug that cuts off top/bottom of seaborn viz
    b, t = plt.ylim() # discover the values for bottom and top
    b += 0.5 # Add 0.5 to the bottom
    t -= 0.5 # Subtract 0.5 from the top
    plt.ylim(b, t) # update the ylim(bottom, top) values
    ###########################################################
    figure = heatmap.get_figure()
    figure.savefig(pic_IObytes,format='png')
    pic_IObytes.seek(0)
    return b64encode(pic_IObytes.read())

def load_clustering(method):
    data = data_config["DATA"]
    return Clustering(data.df,data.filename,method)

@app.route("/pearson_correlation_heatmap", methods=["GET"])
def pearson_correlation_heatmap():
    response = {}
    if "DATA" in data_config:
        matrix_correlation = data_config["DATA"].df.corr(method='pearson')
        pic_hash = get_correlation_heatmap(matrix_correlation)
        response["heatmap_html"] = get_image_b64(pic_hash)
        plt.close()
    return jsonify(response)

@app.route("/get_current_columns", methods=["GET"])
def get_current_columns():
    response = {}
    if "DATA" in data_config:
        response["sel_columns_html"] = data_config["DATA"].get_current_columns_html()
        response["columns"] = data_config["DATA"].get_current_columns()
    return jsonify(response)

@app.route("/get_visualization_method", methods=["POST"])
def get_visualization_method():
    response = {}
    if "DATA" in data_config:
        cluster = load_clustering(request.form["method"])
        figure = cluster.get_visualization_method()
        response["visualization_html"] = get_html_by_figure(figure)
    else:
        raise Warning("No hay un archivo cargado.")
    return jsonify(response)

@app.route("/get_heuristic_method", methods=["POST"])
def get_heuristic_method():
    response = {}
    if "DATA" in data_config:
        cluster = load_clustering(request.form["method"])
        value = cluster.get_heuristic_method()
        response["elbow"] = int(value)
    else:
        raise Warning("No hay un archivo cargado.")
    return jsonify(response)

@app.route("/set_current_columns", methods=["POST"])
def set_current_columns():
    global data_config
    response = {}
    if "DATA" in data_config and request.form:
        form = dict(request.form) 
        data_config["DATA"].set_columns([k for k,v in form.items() if v == "false"])
        response["summary_columns"] = data_config["DATA"].get_selected_columns_html()
    return jsonify(response)

@app.route("/apriori_process", methods=["POST"])
def apriori_process():
    response = {}
    if request.form and "DATA" in data_config:
        min_sup = float(request.form["support"])/100
        min_conf = float(request.form["confidence"])/100
        min_lif = float(request.form["lift"])
        from apyori import apriori
        rules = apriori(data_config["DATA"].get_apyori_list(), min_support=min_sup, min_confidence=min_conf, min_lift=min_lif, min_length=2)
        rules = list(rules)
        response["html"] = TableHTML(table_class="table table-hover",table_id="apriori_table").apriori_table(rules)
        if not "<h5>" in response["html"]:
            df = pd.read_html(response["html"])[0]
            set_export_data(df_to_csv(df),"apriori_rules.csv")
    return jsonify(response)

@app.route("/correlation_process", methods=["POST"])
def correlation_process():
    response = {}
    if "DATA" in data_config:
        matrix_correlation = data_config["DATA"].df.corr(method='pearson')
        response["correlation_matrix_html"] = matrix_correlation.to_html(table_id='correlation_table').replace("dataframe","table")
        pic_hash = get_correlation_heatmap(matrix_correlation)
        response["heatmap_html"] = get_image_b64(pic_hash)
        plt.close()
        response["options"] = data_config["DATA"].get_options_html()
        set_export_data(df_to_csv(matrix_correlation),"correlation.csv")
    return jsonify(response)

@app.route("/clustering_process", methods=["POST"])
def clustering_process():
    response = {}
    if "DATA" in data_config:
        cluster = load_clustering(request.form["method"])
        clusters_df = cluster.get_clusters(int(request.form["n_clusters"]))
        response["clustering_summary"] = clusters_df.to_html(index=False,table_id='clustering_table').replace("dataframe","table table-bordered")
        set_export_data(cluster.get_export_file(),"clusters.csv")
    return jsonify(response)

@app.route("/calc_distance", methods=["POST"])
def calc_distance():
    global data_config
    response = {}
    if request.form and "DATA" in data_config:
        method = request.form["metric"]
        distance = Distance(data_config["DATA"].df , dict(request.form))
        distance_table = distance.get_matrix_table()
        title = "<h5>Matriz de Distancias</h5>"
        response["distance_table"] = title + distance_table
        set_export_data(distance.get_export_file(),"distance_matrix.csv")
    return jsonify(response)


@app.route("/get_regression_vars", methods=["GET"])
def get_regression_vars():
    global data_config
    response = {}
    if "DATA" in data_config:
        response["colum-sel"] = data_config["DATA"].get_current_columns_html(table_id="table-input-reg")
        response["options"] = data_config["DATA"].get_options_html()
    else:
        raise Warning("No existe un archivo a analizar")
    return jsonify(response)


def parse_form_regression(form):
    data = {}
    columns = data_config["DATA"].get_current_columns().copy()
    data["train_percent"] = int(form.get("train-percent",0))
    if form.get("input",False):
        output = columns[0]
        data["output_column"] = [output]
        data["input_columns"] = columns[1:]
    else:
        data["output_column"] = [form.get("output")]
        new_columns = [column for column in columns if column in form.keys()]
        if form.get("output") in new_columns:
            new_columns.remove(form.get("output"))
        data["input_columns"] = new_columns
    return data


@app.route("/logistic_regression", methods=["POST"])
def logistic_regression():
    global data_config
    response = {}
    if request.form and "DATA" in data_config:
        data = parse_form_regression(request.form)
        regression = LogisticReg(data_config["DATA"].df, data["input_columns"],data["output_column"], data["train_percent"])
        response.update(regression.fit_model(html=True))
        data_config["MODEL"] = regression
    else:
        raise Warning("No existe un archivo a analizar")
    return jsonify(response)

@app.route("/linear_regression", methods=["POST"])
def linear_regression():
    global data_config
    response = {}
    if request.form and "DATA" in data_config:
        data = parse_form_regression(request.form)
        regression = LinearReg(data_config["DATA"].df, data["input_columns"],data["output_column"])
        response.update(regression.fit_model(html=True))
        response["colum-sel"] = regression.get_columns_html(table_id="table-x-reg")
        response["options"] = regression.get_options_html()
        data_config["MODEL"] = regression
    else:
        raise Warning("No existe un archivo a analizar")
    return jsonify(response)

@app.route("/plot_regression", methods=["POST"])
def plot_regression():
    global data_config
    response = {}
    if request.form and "DATA" in data_config:
        form = dict(request.form)
        y = form["output"]
        del form["output"]
        x_s = [column for column in form.keys()]
        if y in x_s:
            x_s.remove(y)
        b64enc = data_config["MODEL"].plot([y], x_s)
        response["image"] = get_image_b64(b64enc)
    else:
        raise Warning("No existe un archivo a analizar")
    return jsonify(response)


@app.route("/analize_data", methods=["POST"])
def analize_data():
    global data_config
    response = {}
    file_content = request.files["file"].read().decode("utf-8")
    if len(file_content) > 0:
        file = file_content
        filename = request.files["file"].filename
        header = True if "header" in request.form else False
        table = True if "is_table" in request.form else False
        data_config = {"DATA" : Data(file,filename,header,table)}
        response = data_config["DATA"].get_dict_data_analize()
        response["columns"] = data_config["DATA"].get_columns()
    else:
        raise Warning("No existe un archivo a analizar")
    return jsonify(response)

@app.route("/save_conf", methods=["POST"])
def save_conf():
    global data_config
    form = dict(request.form) 
    nrows = int(form.get("len",0))
    form.pop("len")
    shuffle = False
    if form.get("random",False):
        shuffle = True if form.get("random") == "true" else False
        form.pop("random")
    data_config["DATA"].set_rows(nrows,n_shuffle=shuffle)
    data_config["DATA"].set_columns([k for k,v in form.items() if v == "false"])
    return jsonify(data_config["DATA"].get_summary())

@app.route("/plot_graph", methods=["POST"])
def plot_graph():
    global data_config
    response = {}
    abcisa = request.form["abcisa"]
    ordenada = request.form["ordenada"]
    df = data_config["DATA"].df
    pic_IObytes = BytesIO()
    figure = plt.figure()
    plt.plot(df[abcisa],df[ordenada], 'bo')
    plt.ylabel(abcisa)
    plt.xlabel(ordenada)
    figure.savefig(pic_IObytes,format='png')
    pic_IObytes.seek(0)
    pic_hash = b64encode(pic_IObytes.read())
    response["plot"] = get_image_b64(pic_hash)
    plt.close()
    return jsonify(response)



@app.route("/save_model" , methods=["POST"])
def save_model():
    global data_config
    if request.form and "MODEL" in data_config:
        data = data_config["MODEL"].get_model_data()
        model_name = request.form["model_name"]
        model_dir = os.path.join("models",model_name)
        #Crea el directorio
        try:
            os.mkdir(model_dir)
        except FileExistsError:
            raise Warning("Ya existe un modelo llamado "+ model_name)
        #Save config file
        config_path = os.path.join(model_dir,"config.json")
        with open(config_path, "w") as fp:
            json.dump(data["config"] , fp) 
        model_path = os.path.join(model_dir,"model.bin")
        pickle.dump(data["model"], open(model_path, 'wb'))
    else:
        raise Warning("No existe un modelo a guardar")   
    return jsonify({"title": "Guardado con Éxito", "content": "Se ha guardado correctamente el modelo " + model_name +" en el sistema."})



@app.route("/export_table")
def export_table():
    csv = data_config["EXPORT_FILE"]
    export_name = "attachment; filename=" + data_config["EXPORT_FILENAME"]
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 export_name})


"""
Error Handler
"""

@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    try:
        response = {
            "name": e.__class__.__name__,
            "description": e.args[0],
        }
        return jsonify(response), 408
    except:
        return e

"""
Error Handler
"""
@app.route("/delete_model" , methods=["POST"])
def delete_model():
    import shutil
    response = {}
    model_path = "models"
    model_name = request.form["model_name"]
    shutil.rmtree(os.path.join(model_path,model_name), ignore_errors=True)
    return jsonify(response)

@app.route("/inference_model" , methods=["POST"])
def inference_model():
    response = {}
    model = data_config["MODEL"]
    config = data_config["MODEL_CONFIG"]
    values = {k: [float(v)] for k,v in request.form.items()}
    data = pd.DataFrame.from_dict(values)
    result = model.predict(data)
    response["result"] = get_value_from_array(result)
    response["output_id"] = config["output"]
    return jsonify(response)

@app.route("/file_inference_model" , methods=["POST"])
def file_inference_model():
    response = {}
    file_content = request.files["file"].read().decode("utf-8")
    model = data_config["MODEL"]
    config = data_config["MODEL_CONFIG"]
    if len(file_content) > 0:
        file = file_content
        filename = request.files["file"].filename
        data = Data(file,filename,True,True)
        result = model.predict(data.df[config["inputs"]])
        output_name = config["output"][0]
        try:
            output_df = pd.DataFrame.from_records(result,columns=["PREDICTED_"+output_name])
        except TypeError:
             result = result.reshape(-1,1)
             output_df = pd.DataFrame.from_records(result,columns=["PREDICTED_"+output_name]) 
        new_df = pd.concat([data.df, output_df], axis=1)
        response["result"] = new_df.to_html(table_id="predict_rable_result", classes="table table-bordered").replace("dataframe","")
        response["table_id"] = "predict_rable_result"
    else:
        raise Warning("No existe un archivo a analizar")
    return jsonify(response)


def get_value_from_array(result):
    if isinstance(result, np.integer):
        return int(result)
    if not isinstance(result, np.ndarray):
        return result
    for element in result:
        return get_value_from_array(element)
    return 

def get_model_data(path):
    json_path = os.path.join(path,"config.json")
    model_path = os.path.join(path,"model.bin")
    with open(json_path, 'r') as config_file:
        config = json.load(config_file)
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file) 
    return config, model


@app.route("/change_model_inference" , methods=["POST"])
def change_model():
    response = {}
    models_path = "models"
    config, model = get_model_data(os.path.join(models_path, request.form["model_name"]))
    inputs = config["inputs"]
    vargroup1 = inputs[:len(inputs)//2]
    vargroup2 = inputs[len(inputs)//2:]
    output = config["output"]
    to_html = HTML_tools().input_from_list
    response["vargroup1"] = to_html(vargroup1, required=True)
    response["vargroup2"] = to_html(vargroup2, required=True)
    response["output"] = to_html(output, disbled=True)
    data_config["MODEL"] = model
    data_config["MODEL_CONFIG"] = config
    return jsonify(response)


@app.route("/inference")
def inference():
    global data_config
    models_path = "models"
    models = [value for value in os.listdir(models_path) if os.path.isdir(os.path.join(models_path,value))]
    if len(models)==0:
        return render_template("inference_not_found.html")
    #Carga los datos del primer modelo
    config, model = get_model_data(os.path.join(models_path, models[0]))
    inputs = config["inputs"]
    vargroup1 = inputs[len(inputs)//2:]
    vargroup2 = inputs[:len(inputs)//2]
    output = config["output"]
    data_config["MODEL"] = model
    data_config["MODEL_CONFIG"] = config
    return render_template("inference.html", models=models, vargroup1=vargroup1, vargroup2=vargroup2 ,output=output)

@app.route("/regression")
def regression():
    return render_template("regression.html")

@app.route("/apriori")
def apriori():
    return render_template("apriori.html")

@app.route("/correlaciones")
def correlaciones():
    return render_template("correlation.html")

@app.route("/metricas")
def metricas():
    return render_template("metricas.html")

@app.route("/clustering")
def clustering():
    return render_template("clustering.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/")
def index():
    return render_template("index.html")


app.run(debug=True,port=8000)


#data = CSV_reader('apriori.csv',bool)
#print(data.df)

