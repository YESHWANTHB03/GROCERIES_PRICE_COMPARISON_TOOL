from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import csv

app = Flask(__name__)

def get_items_from_csv(csv_file):
    items = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append(row['Product_name'])
    return items

def get_lowest_price(file1, file2, item_to_compare):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    price1 = df1[df1['Product_name'].str.contains(item_to_compare, case=False)]['Product_Prices'].min()
    price2 = df2[df2['Product_name'].str.contains(item_to_compare, case=False)]['Product_Prices'].min()

    website1 = "FLIPKART"  # Name of the first website
    website2 = "JIOMART"   # Name of the second website

    if pd.notnull(price1) and pd.notnull(price2):
        lowest_price = min(price1, price2)
        lowest_website = website1 if lowest_price == price1 else website2
        return lowest_price, lowest_website
    elif pd.notnull(price1):
        return price1, website1
    elif pd.notnull(price2):
        return price2, website2
    else:
        return None, None

@app.route('/')
def upload_file():
    flip_items = get_items_from_csv("FLIP.csv")
    jio_items = get_items_from_csv("JIO.csv")
    items = flip_items + jio_items
    return render_template('upload.html', items=items)

@app.route('/compare', methods=['POST'])
def compare_files():
    file1 = "FLIP.csv"
    file2 = "JIO.csv"
    item_to_compare = request.form['item_to_compare']

    if file1 and file2:
        lowest_price, lowest_website = get_lowest_price(file1, file2, item_to_compare)
        if lowest_price is not None:
            result = f"Lowest Price: {lowest_price} (from {lowest_website})"
        else:
            result = "No price found for the specified item."
        return render_template('result.html', result=result)
    else:
        return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run(debug=True)
