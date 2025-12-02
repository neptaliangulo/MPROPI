import os
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "countries.csv") 
try:
    df = pd.read_csv(DATA_PATH)
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]

    column_map = {
        "GDP": None,
        "Population": None,
        "Life_expectancy": None,
        "Area": None
    }

    for col in df.columns:
        if col == "GDP":
            column_map["GDP"] = col
        elif col == "Population":
            column_map["Population"] = col
        elif col in ["Life_expectancy", "Life_Expectancy"]:
            column_map["Life_expectancy"] = col
        elif "Area" in col:
            column_map["Area"] = col

    for key, col in column_map.items():
        if col is not None:
            df[col] = (
                df[col].astype(str)
                .str.replace(",", "")
                .str.replace("$", "")
                .str.replace("%", "")
                .str.strip()
                .astype(float)
            )

except FileNotFoundError:
    print(f"Error: No se encontro el fichero {DATA_PATH}")
    df = pd.DataFrame()  

def getCountryData(country_name):
    if df.empty:
        return None
    filtered = df[df["Country"] == country_name]
    if filtered.empty:
        return None
    return filtered.to_dict("records")[0]

def getTop10GDP():
    if df.empty or column_map["GDP"] is None:
        return []
    sorted_df = df.sort_values(by=column_map["GDP"], ascending=False).head(10)
    return sorted_df[["Country", column_map["GDP"]]].to_dict("records")

def filterCountries(variable, min_val, max_val):
    if df.empty:
        return {"error": "No hay datos disponibles"}
    try:
        min_val = float(min_val)
        max_val = float(max_val)
        if min_val > max_val:
            return {"error": "El valor mínimo no puede ser mayor que el maximo."}

        col_map = {
            "GDP": column_map["GDP"],
            "Population": column_map["Population"],
            "Life_Expectancy": column_map["Life_expectancy"],
            "Area": column_map["Area"]
        }

        col = col_map.get(variable)
        if col is None:
            return {"error": "Variable no vàlida"}

        filtered = df[(df[col] >= min_val) & (df[col] <= max_val)]
        return {"countries": filtered["Country"].tolist()}
    except:
        return {"error": "Valores numericos invalidos"}

def getAllCountries():
    if df.empty:
        return []
    return sorted(df["Country"].tolist())