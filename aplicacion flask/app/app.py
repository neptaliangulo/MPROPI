from flask import Flask, render_template, request, jsonify
from world import getCountryData, filterCountries, getAllCountries

app = Flask(__name__)

@app.route("/", methods=["GET"])
def welcomePage():
    return render_template("index.html")

@app.route("/countryData", methods=["POST"])
def countryData():
    country = request.form.get("country")
    countryData = getCountryData(country)
    if countryData is None:
        return jsonify({"error": "Country not found"}), 404
    return jsonify(countryData)

@app.route("/filterCountries", methods=["POST"])
def filterCountriesRoute():
    variable = request.form.get("variable")
    min_val = request.form.get("min_val")
    max_val = request.form.get("max_val")
    result = filterCountries(variable, min_val, max_val)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

@app.route("/getAllCountries", methods=["GET"])
def getAllCountriesRoute():
    return jsonify({"countries": getAllCountries()})

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
