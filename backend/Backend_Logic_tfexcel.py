from flask import Flask, request, redirect, url_for, send_from_directory, flash, render_template
import pandas as pd
import os

TEMPLATES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))

app = Flask(__name__, template_folder=TEMPLATES_DIR)
app.secret_key = "supersecretkey"
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def add_column_to_excel(excel_file_path, column_name, references):
    # Charger le fichier Excel et obtenir le DataFrame
    df = pd.read_excel(excel_file_path, engine='openpyxl')
    # Extraire les références existantes dans la colonne 1 du DataFrame 
    existing_references = df.iloc[:, 0]

    # Parcourir chaque référence à ajouter 
    for reference in references:
        # Vérifier si la référence existe déjà dans les références existantes
        if reference in existing_references.values:
            # Mettre à jour la valeur de la colonne spécifiée à "X" pour la référence existante
            df.loc[df.iloc[:, 0] == reference, column_name] = "X"
        else:
            # Ajouter une nouvelle ligne avec la référence et la valeur "X" pour la colonne spécifiée
            new_row = pd.DataFrame([[reference] + [""] * (len(df.columns) - 1)], columns=df.columns)
            new_row[column_name] = "X"
            df = pd.concat([df, new_row], ignore_index=True)

    # Écrire le DataFrame dans le fichier Excel sans inclure l'index  
    df.to_excel(excel_file_path, index=False, engine='openpyxl')

def read_references_from_file(file_path):
    with open(file_path, 'r') as file:
        references = [line.strip() for line in file.readlines() if line.strip()]
    return references

@app.route('/tfexcel', methods=['GET', 'POST'])
def tfexcel():
    if request.method == 'POST':
        excel_file = request.files['excel_file']
        text_file = request.files['text_file']
        column_name = request.form['column_name']

        # Vérification du type de fichier Excel
        if not excel_file or not text_file or not column_name:
            flash("All fields are required.")
            return redirect(request.url)

        # Vérifie l'extension du fichier Excel
        allowed_excel_extensions = ['.xlsx', '.xls']
        filename = excel_file.filename
        if not any(filename.lower().endswith(ext) for ext in allowed_excel_extensions):
            flash("Veuillez sélectionner un fichier Excel valide (.xlsx ou .xls).")
            return redirect(request.url)
        
        excel_path = os.path.join(UPLOAD_FOLDER, "Bibliographie accès classe 5 SM.xlsx")
        text_path = os.path.join(UPLOAD_FOLDER, "Ref.txt")

        try:
            excel_file.save(excel_path)
            text_file.save(text_path)
        except Exception as e:
            print(f"Error saving files: {e}")
            flash("There was an error saving the files.")
            return redirect(request.url)

        try:
            references = read_references_from_file(text_path)
            add_column_to_excel(excel_path, column_name, references)
        except Exception as e:
            print(f"Error processing files: {e}")
            flash("There was an error processing the files.")
            return redirect(request.url)

        return redirect(url_for('download_file', filename="Bibliographie accès classe 5 SM.xlsx"))

    return render_template('tfexcel.html')


@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
