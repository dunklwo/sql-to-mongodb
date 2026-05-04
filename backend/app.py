from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from parser import parse_sql
from converter import convert_to_mongo

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    data = request.json
    sql_query = data.get("query", "")

    parsed = parse_sql(sql_query)
    mongo_query = convert_to_mongo(parsed)

    return jsonify({
        "mongo_query": mongo_query
    })
if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000)
        
