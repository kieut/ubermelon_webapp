from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2


app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site""" 
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""
    melons = []
    total = 0
    if "cart" in session.keys():
        for key in session["cart"].iterkeys():
            melon = model.get_melon_by_id(str(key))
            melons.append(melon)
            melon.quantity = session["cart"][str(key)]
            total += melon.quantity * melon.price

    return render_template("cart.html", cart_contents = melons, order_total = total)
    
@app.route("/add_to_cart/<int:melon_id>")
def add_to_cart(melon_id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.
    
    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """

    if "cart" in session.keys():
        if str(melon_id) in session["cart"].keys():
            session["cart"][str(melon_id)] += 1
        else:
            session["cart"][str(melon_id)] = 1
    else:
        session["cart"] = {}
        session["cart"][str(melon_id)] = 1

    flash("Your melon has been added to the cart.")

    return redirect("/melon/%d" % melon_id)
    
@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    cust_email =  str(request.form["email"])
    customer = model.get_customer_by_email(cust_email)
    if customer == None:
        return "You are not in the customer database"
    #return "You entered username: %s and password: %s" % (request.form["email"], request.form["password"])
    else:
        session["customer"] = [customer.email, customer.givenname, customer.surname]
        flash("You've Successfully logged in.")
        return redirect("/melons")

@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

@app.route("/logout")
def logout():
    session.clear()
    flash("You've successfully logged out.")
    return render_template("logout.html")

@app.route("/cart_items")
def show_cart():

    melons = [ (model.get_melon_by_id(int(id)), count) for id, count in session.setdefault("cart", {}).items() ]
    total = sum([melon[0].price * melon[1] for melon in melons])
    return render_template("_cart_items.html", melons = melons, total=total)

if __name__ == "__main__":
    app.run(debug=True)
