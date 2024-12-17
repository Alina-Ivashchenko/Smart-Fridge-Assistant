from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import openai
from datetime import date, timedelta  

openai.api_key = "paste-you-openAI-key-here" #Paste your Open AI Key here

app = Flask(__name__)

app.config['DEBUG'] = True


@app.route('/')
def index():
    items = display_items()  
    return render_template('main.html', items=items)


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",         
        password="Login123",
        database="dbproject"
    )

def add_item(item_name, quantity, expiration_date):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO items (item_name, quantity, expiration_date) VALUES (%s, %s, %s)"
    cursor.execute(query, (item_name, quantity, expiration_date))
    conn.commit()
    cursor.close()
    conn.close()

def display_items():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def delete_item(item_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = "DELETE FROM items WHERE id = %s"
    cursor.execute(query, (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
def get_expiring_soon_items():
    conn = connect_db()
    cursor = conn.cursor()
    today = date.today()
    warning_date = today + timedelta(days=3)  # Items expiring within 3 days
    query = "SELECT * FROM items WHERE expiration_date BETWEEN %s AND %s"
    cursor.execute(query, (today, warning_date))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def save_recipe_to_db(name, ingredients, instructions):
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        INSERT INTO recipes (name, ingredients, instructions)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (name, ingredients, instructions))
    conn.commit()
    cursor.close()
    conn.close()
    
def fetch_saved_recipes():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, ingredients, instructions FROM recipes")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"name": row[0], "ingredients": row[1], "instructions": row[2]} for row in rows]

def save_nutrition_info(item_id, calories, protein, carbs, fat, sugars, fiber):
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        INSERT INTO nutrition_items (item_id, calories, protein, carbs, fat, sugars, fiber)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (item_id, calories, protein, carbs, fat, sugars, fiber))
    conn.commit()
    cursor.close()
    conn.close()

    

@app.route('/add', methods=['POST'])
def add():
    item_name = request.form['item_name']
    quantity = request.form['quantity']
    expiration_date = request.form['expiration_date']  
    add_item(item_name, int(quantity), expiration_date)
    
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    if request.form.get('_method') == 'DELETE':
        delete_item(item_id)
    return redirect(url_for('index'))


@app.route('/expiration_dates')
def expiration_dates():
    expiring_items = get_expiring_soon_items()  
    return render_template('expiration_dates.html', expiring_items=expiring_items)


@app.route('/generate_recipes')
def generate_recipes():
    items = display_items() 
    return render_template('generate_recipes.html', items=items, recipes=[])

@app.route('/get_recipes', methods=['POST'])
def get_recipes():
    items = display_items()  
    ingredient_list = ", ".join([item[1] for item in items])  

    if not items:
        return render_template(
            'generate_recipes.html',
            items=items,
            recipes=[],
            error="No ingredients available to generate recipes!"
        )

    prompt = f"Generate 3 recipes using the following ingredients: {ingredient_list}. Format each recipe as:\nDish Name:\nIngredients:\n- Ingredient 1\n- Ingredient 2\n...\nInstructions:\n1. Step 1\n2. Step 2\n..."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful chef."},
                {"role": "user", "content": prompt}
            ]
        )
        ai_output = response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return render_template(
            'generate_recipes.html',
            items=items,
            recipes=[],
            error="Failed to connect to OpenAI API. Please try again later."
        )

    recipes = []
    current_recipe = {"name": "", "ingredients": [], "instructions": ""}
    section = None  

    for line in ai_output.split("\n"):
        line = line.strip()

        if line.startswith("Dish Name:"):
            if current_recipe["name"]:
                recipes.append(current_recipe)
                save_recipe_to_db(
                    current_recipe["name"],
                    ", ".join(current_recipe["ingredients"]),
                    current_recipe["instructions"]
                )
                current_recipe = {"name": "", "ingredients": [], "instructions": ""}
            current_recipe["name"] = line.replace("Dish Name:", "").strip()
            section = None
        elif line.startswith("Ingredients:"):
            section = "ingredients"
        elif line.startswith("Instructions:"):
            section = "instructions"
        elif line.startswith("-") and section == "ingredients":
            current_recipe["ingredients"].append(line[1:].strip())  
        elif section == "instructions":
            current_recipe["instructions"] += line + " "  

    if current_recipe["name"]:
        recipes.append(current_recipe)
        save_recipe_to_db(
            current_recipe["name"],
            ", ".join(current_recipe["ingredients"]),
            current_recipe["instructions"]
        )

    return render_template('generate_recipes.html', items=items, recipes=recipes)



@app.route('/get_nutrition_info', methods=['POST'])
def get_nutrition_info():
    items = display_items()
    ingredient_list = ", ".join([item[1] for item in items])

    if not items:
        return render_template(
            'nutrition_info.html',
            items=items,
            nutrition_info=[],
            error="No ingredients available to fetch nutrition information!"
        )

    prompt = f"Provide the nutritional information for the following ingredients: {ingredient_list} Include calories, protein, carbs, fat, sugars, and fiber in your response. Provide the data in the format: Ingredient: <name> Calories: <calories> Protein: <protein> Carbs: <carbs> Fat: <fat> Sugars: <sugars> Fiber: <fiber>"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful nutrition expert."},
                      {"role": "user", "content": prompt}]
        )
        ai_output = response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return render_template(
            'nutrition_info.html',
            items=items,
            nutrition_info=[],
            error="Failed to connect to OpenAI API. Please try again later."
        )

    nutrition_info = []
    current_item = {"name": "", "calories": "", "protein": "", "carbs": "", "fat": "", "sugars": "", "fiber": ""}

    for line in ai_output.split("\n"):
        line = line.strip()

        if line.startswith("Ingredient:"):
            if current_item["name"]:
                item_id = next((item[0] for item in items if item[1].lower() == current_item["name"].lower()), None)
                if item_id:
                    save_nutrition_info(
                        item_id,
                        current_item["calories"],
                        current_item["protein"],
                        current_item["carbs"],
                        current_item["fat"],
                        current_item["sugars"],
                        current_item["fiber"]
                    )
                nutrition_info.append(current_item)
                current_item = {"name": "", "calories": "", "protein": "", "carbs": "", "fat": "", "sugars": "", "fiber": ""}
            
            current_item["name"] = line.replace("Ingredient:", "").strip()

        elif "Calories:" in line:
            current_item["calories"] = line.replace("Calories:", "").strip()

        elif "Protein:" in line:
            current_item["protein"] = line.replace("Protein:", "").strip()

        elif "Carbs:" in line:
            current_item["carbs"] = line.replace("Carbs:", "").strip()

        elif "Fat:" in line:
            current_item["fat"] = line.replace("Fat:", "").strip()

        elif "Sugars:" in line:
            current_item["sugars"] = line.replace("Sugars:", "").strip()

        elif "Fiber:" in line:
            current_item["fiber"] = line.replace("Fiber:", "").strip()

    if current_item["name"]:
        item_id = next((item[0] for item in items if item[1].lower() == current_item["name"].lower()), None)
        if item_id:
            save_nutrition_info(
                item_id,
                current_item["calories"],
                current_item["protein"],
                current_item["carbs"],
                current_item["fat"],
                current_item["sugars"],
                current_item["fiber"]
            )
        nutrition_info.append(current_item)

    return render_template(
        'nutrition_info.html',
        items=items,
        nutrition_info=nutrition_info
    )


@app.route('/bulk_insert')
def bulk_insert():
    return render_template('bulk_insert.html')

@app.route('/bulk_add', methods=['POST'])
def bulk_add():
    bulk_data = request.form['bulk_data']

    if not bulk_data.strip():
        return redirect(url_for('bulk_insert'))  

    lines = bulk_data.strip().split("\n")

    for line in lines:
        try:
            item_name, quantity, expiration_date = map(str.strip, line.split(","))
            add_item(item_name, int(quantity), expiration_date)
        except Exception as e:
            print(f"Error processing line: {line}. Error: {e}")
            continue

    return redirect(url_for('index'))


@app.route('/nutrition_info')
def nutrition_info():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT items.item_name, 
               items_nutrition.calories, 
               items_nutrition.protein, 
               items_nutrition.carbs, 
               items_nutrition.fat, 
               items_nutrition.sugars, 
               items_nutrition.fiber
        FROM items
        JOIN items_nutrition ON items.id = items_nutrition.item_id
    """)
    nutrition_data = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('nutrition_info.html', nutrition_data=nutrition_data)



if __name__ == "__main__":
    app.run(debug=True)