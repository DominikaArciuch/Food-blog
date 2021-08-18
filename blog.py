import sqlite3
import sys
import argparse

connection = sqlite3.connect("food_blog.db")
cursor = connection.cursor()


def add_elements():
    name = "i"
    data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
            "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
            "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

    cursor.execute("PRAGMA foreign_keys = ON")
    connection.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS meals("
                   "meal_id INTEGER PRIMARY KEY,"
                   "meal_name VARCHAR(30) UNIQUE NOT NULL"
                   ");")
    connection.commit()

    cursor.execute("CREATE TABLE IF NOT EXISTS ingredients("
                   "ingredient_id INTEGER PRIMARY KEY,"
                   "ingredient_name VARCHAR(30) UNIQUE NOT NULL"
                   ");")
    connection.commit()

    cursor.execute("CREATE TABLE IF NOT EXISTS measures("
                   "measure_id INTEGER PRIMARY KEY,"
                   "measure_name VARCHAR(30) UNIQUE"
                   ");")
    connection.commit()

    cursor.execute("CREATE TABLE IF NOT EXISTS recipes("
                   "recipe_id INTEGER PRIMARY KEY,"
                   "recipe_name VARCHAR(30) NOT NULL, "
                   "recipe_description VARCHAR(50)"
                   ");")
    connection.commit()

    cursor.execute("CREATE TABLE IF NOT EXISTS serve("
                   "serve_id INTEGER PRIMARY KEY,"
                   "recipe_id INTEGER NOT NULL,"
                   "meal_id INTEGER NOT NULL,"
                   "FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),"
                   "FOREIGN KEY(meal_id) REFERENCES meals(meal_id)"
                   ");")
    connection.commit()

    cursor.execute("CREATE TABLE IF NOT EXISTS quantity("
                   "quantity_id INTEGER PRIMARY KEY,"
                   "quantity INTEGER NOT NULL,"
                   "measure_id INTEGER NOT NULL,"
                   "ingredient_id INTEGER NOT NULL,"
                   "recipe_id INTEGER NOT NULL,"
                   "FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),"
                   "FOREIGN KEY(measure_id) REFERENCES measures(measure_id),"
                   "FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id)"
                   ");")
    connection.commit()

    for db in data:
        for item in data[db]:
            insert_query = f"INSERT OR IGNORE INTO {db} ({db[:-1] + '_name'}) VALUES (?)"
            cursor.execute(insert_query, (item,))
            connection.commit()

    meals_list = cursor.execute("SELECT * FROM meals").fetchall()
    ingredients_list = cursor.execute("SELECT * FROM ingredients").fetchall()
    measures_list = cursor.execute("SELECT * FROM measures").fetchall()
    ile = 0
    while len(name) > 0:
        print("Pass the empty recipe name to exit.")
        name = input("Recipe name: ")
        if len(name) > 0:
            description = input("Recipe description: ")
            [print(f"{i[0]}) {i[1]}", end="  ") for i in meals_list]
            serve = input("\nWhen the dish can be served: ")
            cursor.execute(f"INSERT INTO recipes (recipe_name, recipe_description) VALUES (?, ?)", (name, description,))
            recipe_id = cursor.lastrowid
            for s in serve.split():
                cursor.execute(f"INSERT INTO serve (recipe_id, meal_id) VALUES (?, ?)", (recipe_id, int(s),))
            connection.commit()
            ing = " "
            while len(ing) > 0:
                measure_id = 0
                ingredient_id = 0
                ing = input("Input quantity of ingredient <press enter to stop>: ").split()
                if len(ing) > 0:
                    if len(ing) > 2:
                        flaga = False
                        for measure in measures_list:
                            if ing[1] in measure[1]:
                                if flaga:
                                    measure_id = 0
                                else:
                                    flaga = True
                                    measure_id = measure[0]
                    else:
                        measure_id = 8
                        ing.insert(1, " ")
                    flaga = False
                    for i in ingredients_list:
                        if ing[2] in i[1]:
                            if flaga:
                                ingredient_id = 0
                            else:
                                flaga = True
                                ingredient_id = i[0]

                    if measure_id > 0 and ingredient_id > 0:
                        cursor.execute(
                            f"INSERT INTO quantity (quantity, measure_id, ingredient_id, recipe_id) VALUES (?, ?, ?, ?)",
                            (int(ing[0]), measure_id, ingredient_id, recipe_id))
                        print("Dodano")
                        ile += 1
                        connection.commit()


def search(ingredient, meals):
    cursor.execute(f"""SELECT recipe_name 
                        FROM recipes 
                        INNER JOIN quantity USING(recipe_id)
                        INNER JOIN ingredients USING(ingredient_id)
                        WHERE ingredient_name IN (?)
                        GROUP BY recipe_name;""", set(ingredient))
    recipes_ing = set([i[0] for i in cursor.fetchall()])
    cursor.execute(f"""SELECT recipe_name
                        FROM recipes
                        INNER JOIN serve USING(recipe_id)
                        INNER JOIN meals USING(meal_id)
                        WHERE meal_name IN (?)
                        GROUP BY recipe_name;""", set(meals))
    recipes_me = set([i[0] for i in cursor.fetchall()])
    print(recipes_ing & recipes_me)
    print(recipes_ing)


parser = argparse.ArgumentParser()
parser.add_argument("--ingredients", "--i")
parser.add_argument("--meals", "--m")
a = parser.parse_args()

add_elements()
# if len(a.ingredients) > 0 :
#     search(a.ingredients, a.meals)
# else:
#     add_elements()
# ingredient = ("milk", )
# cursor.execute(f"""SELECT recipe_name
#                         FROM recipes
#                         INNER JOIN quantity USING(recipe_id)
#                         INNER JOIN ingredients USING(ingredient_id)
#                         WHERE ingredient_name IN (?)
#                         GROUP BY recipe_name;""", (ingredient))
# recipes_ing = set([i[0] for i in cursor.fetchall()])
# print(recipes_ing)

connection.close()
