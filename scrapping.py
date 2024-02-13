import requests
from bs4 import BeautifulSoup
import csv
from dash import Dash , html,dcc
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(className='InputContainer', style={'height': '100vh'}, children=[
    html.H1('Outils de Scrapping'),

    
])






url = "https://books.toscrape.com/"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouver toutes les catégories
    categories = [category.text.strip() for category in soup.find_all('a') if category.get('href') and 'category' in category['href']]

    # Créer un fichier CSV
    with open('livres_par_categorie.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Categorie', 'Titre']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Écrire l'en-tête du fichier CSV
        writer.writeheader()

        # Parcourir chaque catégorie
        for category in categories:
            category_url = f"{url}catalogue/category/books/{category.lower().replace(' ', '-')}_1/index.html"
            category_response = requests.get(category_url)

            if category_response.status_code == 200:
                category_soup = BeautifulSoup(category_response.text, 'html.parser')

                # Obtenir tous les titres de livres de la catégorie
                books = category_soup.find_all('h3')
                for book in books:
                    book_title = book.find('a')['title'].strip()

                    # Écrire les données dans le fichier CSV
                    writer.writerow({'Categorie': category, 'Titre': book_title})

    print(f"Nombre total de catégories: {len(categories)}")
    print("Les données ont été enregistrées dans 'livres_par_categorie.csv'.")

else:
    print(f"Erreur: {response.status_code}")

if __name__ == '__main__':
    app.run(debug=True)