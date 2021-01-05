from flask import Flask, render_template, request, send_file
from pipeline_methods import construct_prot_dict, pipeline
import tarfile
import os

app = Flask(__name__)

@app.route('/')
def default():
    return "hello world"

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/dataset_form")
def dataset_construction():
    return render_template("dataset_form.html")

@app.route("/file_download")
def file_construction():
    return send_file("../data/swissprot_goa.gaf.gz")

@app.route('/server', methods=['GET', 'POST'])
def process_sequence():
    print("recieved post request")
    if request.method == 'POST':
        req_dict = request.form.to_dict()
        print(req_dict)
        print("parsing request\n\n\n\n")
        input_dict = construct_prot_dict(req_dict)
        print(input_dict)
        pipeline(input_dict)
        source_dir = "../data/generated_datasets/"
        with tarfile.open("../data/gene_ontology_data.tar.gz", "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
        #config_dict = parse_server_multidict(request.form)
        #return str(config_dict)
        return send_file("../data/gene_ontology_data.tar.gz")

if __name__ == '__main__':
    app.run()