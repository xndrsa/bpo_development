# from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
# import pandas as pd
# import os

# app = Flask(__name__)
# app.secret_key = "secret_key"
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Variables globales para los datos
# df_modificado = None

# def calcular_cuartiles(df, columna):
#     Q1 = df[columna].quantile(0.25)
#     Q2 = df[columna].median()
#     Q3 = df[columna].quantile(0.75)
#     Q4 = df[columna].max()
    
#     nombre_nueva_columna = f"{columna}_cuartil"
#     df[nombre_nueva_columna] = pd.cut(df[columna], bins=[-float('inf'), Q1, Q2, Q3, Q4], labels=["1", "2", "3", "4"])
#     return {"Q1": Q1, "Q2": Q2, "Q3": Q3, "Q4": Q4}, df

# def agrupacion_personalizada(df, columna, metodo_agrupacion):
#     if metodo_agrupacion == "Suma":
#         return df.groupby(columna).sum()
#     elif metodo_agrupacion == "Media":
#         return df.groupby(columna).mean()
#     elif metodo_agrupacion == "Conteo":
#         return df.groupby(columna).count()
#     else:
#         return None

# @app.route("/", methods=["GET", "POST"])
# def index():
#     global df_modificado

#     if request.method == "POST" and "file" in request.files:
#         file = request.files["file"]
#         if file.filename.endswith((".csv", ".tsv")):
#             sep = "," if file.filename.endswith(".csv") else "\t"
#             df_modificado = pd.read_csv(file, sep=sep)
#             session["archivo_cargado"] = True
#             flash("Archivo cargado exitosamente.", "success")
#         else:
#             flash("Por favor, carga un archivo CSV o TSV.", "error")

#     columnas = df_modificado.columns if df_modificado is not None else []
#     return render_template("index.html", df=df_modificado, columnas=columnas)

# @app.route("/analisis", methods=["GET", "POST"])
# def analisis():
#     global df_modificado

#     if request.method == "POST":
#         if "cuartil_columna" in request.form:
#             columna = request.form["cuartil_columna"]
#             if df_modificado is not None and columna in df_modificado.columns:
#                 cuartiles, df_modificado = calcular_cuartiles(df_modificado, columna)
#                 flash(f"Cuartiles calculados para la columna {columna}.", "success")
#         elif "agrupacion_columna" in request.form and "metodo_agrupacion" in request.form:
#             columna = request.form["agrupacion_columna"]
#             metodo = request.form["metodo_agrupacion"]
#             if df_modificado is not None and columna in df_modificado.columns:
#                 df_modificado = agrupacion_personalizada(df_modificado, columna, metodo)
#                 flash(f"Agrupación realizada en la columna {columna} usando el método {metodo}.", "success")
    
#     columnas = df_modificado.columns if df_modificado is not None else []
#     return render_template("analisis.html", df=df_modificado, columnas=columnas)

# @app.route("/descargar")
# def descargar():
#     if df_modificado is not None:
#         df_modificado.to_csv(os.path.join(app.config["UPLOAD_FOLDER"], "data_modificada.csv"), index=False)
#         return send_file(os.path.join(app.config["UPLOAD_FOLDER"], "data_modificada.csv"), as_attachment=True)
#     else:
#         flash("No hay datos para descargar.", "error")
#         return redirect(url_for("index"))

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = "secret_key"
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Variable global para el DataFrame
df_modificado = None

def calcular_cuartiles(df, columna):
    Q1 = df[columna].quantile(0.25)
    Q2 = df[columna].median()
    Q3 = df[columna].quantile(0.75)
    Q4 = df[columna].max()
    
    nombre_nueva_columna = f"{columna}_cuartil"
    df[nombre_nueva_columna] = pd.cut(df[columna], bins=[-float('inf'), Q1, Q2, Q3, Q4], labels=["1", "2", "3", "4"])
    return {"Q1": Q1, "Q2": Q2, "Q3": Q3, "Q4": Q4}, df

def estadisticas_descriptivas(df):
    # Filtra solo las columnas numéricas antes de aplicar describe()
    df_numerico = df.select_dtypes(include=['number'])
    return df_numerico.describe().T

@app.route("/", methods=["GET", "POST"])
def index():
    global df_modificado

    if request.method == "POST" and "file" in request.files:
        file = request.files["file"]
        if file.filename.endswith((".csv", ".tsv")):
            sep = "," if file.filename.endswith(".csv") else "\t"
            df_modificado = pd.read_csv(file, sep=sep)
            session["archivo_cargado"] = True
            flash("Archivo cargado exitosamente.", "success")
        else:
            flash("Por favor, carga un archivo CSV o TSV.", "error")

    columnas = df_modificado.columns if df_modificado is not None else []
    return render_template("index.html", df=df_modificado, columnas=columnas)

@app.route("/analisis", methods=["GET", "POST"])
def analisis():
    global df_modificado

    if request.method == "POST":
        if "cuartil_columna" in request.form:
            columna = request.form["cuartil_columna"]
            if df_modificado is not None and columna in df_modificado.columns:
                cuartiles, df_modificado = calcular_cuartiles(df_modificado, columna)
                flash(f"Cuartiles calculados para la columna {columna}.", "success")
        elif "agrupacion_columna" in request.form and "metodo_agrupacion" in request.form:
            columna = request.form["agrupacion_columna"]
            metodo = request.form["metodo_agrupacion"]
            if df_modificado is not None and columna in df_modificado.columns:
                df_modificado = df_modificado.groupby(columna).agg(metodo.lower())
                flash(f"Agrupación realizada en la columna {columna} usando el método {metodo}.", "success")
    
    columnas = df_modificado.columns if df_modificado is not None else []
    return render_template("analisis.html", df=df_modificado, columnas=columnas)

@app.route("/estadisticas")
def estadisticas():
    global df_modificado
    if df_modificado is None:
        flash("Por favor, carga un archivo primero.", "error")
        return redirect(url_for("index"))
    estadisticas = estadisticas_descriptivas(df_modificado)
    return render_template("estadisticas.html", estadisticas=estadisticas)


@app.route("/filtrar", methods=["GET", "POST"])
def filtrar():
    global df_modificado
    if df_modificado is None:
        flash("Por favor, carga un archivo primero.", "error")
        return redirect(url_for("index"))

    # Crear una copia temporal del DataFrame original para filtrar
    df_filtrado = df_modificado.copy()

    if request.method == "POST":
        columna = request.form["columna"]
        condicion = request.form["condicion"]
        valor = request.form["valor"]

        # Aplicar filtro en la copia temporal
        try:
            if condicion == ">":
                df_filtrado = df_filtrado[df_filtrado[columna] > float(valor)]
            elif condicion == "<":
                df_filtrado = df_filtrado[df_filtrado[columna] < float(valor)]
            elif condicion == "=":
                df_filtrado = df_filtrado[df_filtrado[columna] == float(valor)]
            elif condicion == "!=":
                df_filtrado = df_filtrado[df_filtrado[columna] != float(valor)]
            flash("Filtro aplicado correctamente.", "success")
        except ValueError:
            flash("Por favor, ingresa un valor numérico válido.", "error")

    columnas = df_modificado.columns
    return render_template("filtro.html", columnas=columnas, df=df_filtrado)

@app.route("/graficos", methods=["GET", "POST"])
def graficos():
    global df_modificado
    if df_modificado is None:
        flash("Por favor, carga un archivo primero.", "error")
        return redirect(url_for("index"))

    grafico = None
    if request.method == "POST":
        columna = request.form["columna"]
        tipo_grafico = request.form["tipo_grafico"]

        plt.figure(figsize=(10, 6))
        if tipo_grafico == "Histograma":
            sns.histplot(df_modificado[columna], kde=True)
        elif tipo_grafico == "Barras":
            sns.countplot(x=columna, data=df_modificado)
        elif tipo_grafico == "Dispersión":
            otra_columna = request.form.get("otra_columna", None)
            if otra_columna:
                sns.scatterplot(x=df_modificado[columna], y=df_modificado[otra_columna])
        
        img = BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        grafico = base64.b64encode(img.getvalue()).decode()
        plt.close()

    columnas = df_modificado.columns
    return render_template("graficos.html", columnas=columnas, grafico=grafico)

if __name__ == "__main__":
    app.run(debug=True)
