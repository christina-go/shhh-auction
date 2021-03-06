from flask import Flask, flash, redirect, request, render_template, session
import cgi
import os
from app import app, db
from models import Item, Bid, User
from helper_functions import input_validation, password_match, allowed_file
from werkzeug.utils import secure_filename


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        flash("You must be logged in to continue")
        return redirect('/login')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
def redirect_index():
    return redirect('/index')


@app.route('/home')
def home():
    username = session['username']
    user = User.query.filter_by(username=username).first()
    bids = Bid.query.filter_by(owner_id=user.id).all()
    items = Item.query.filter_by(owner_id=user.id).all()

    all_auctions = Item.query.all()

    return render_template('home.html', username=username, user=user, bids=bids, items=items, all_auctions=all_auctions)    


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if input_validation(password) and password_match(password, verify) == True:
            existing_user = User.query.filter_by(username=username).first()

            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/home')

            else:
                flash("User already exists")
                return render_template('signup.html', title="Register to Shhh")    

        else:
            if not input_validation(password):
                flash("Password must be more than 3 characters in length and contain no spaces")
            if not password_match(password, verify):
                flash("Password and password confirmation do not match")

                return render_template('signup.html', title="Register to Shhh")

    return render_template('signup.html', title="Register to Shhh") 


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if not user:
            flash("User does not exist")
            return render_template('login.html', title="Log In to Shhh")

        if not password == user.password:
            flash("User password incorrect")
            return render_template('login.html', title="Log In to Shhh")

        if user and user.password == password:
            session['username'] = username
            return redirect('/home')

    return render_template('login.html', title="Log In to Shhh")     


@app.route('/new_item', methods=['POST', 'GET'])    
def new_item():
    username = session['username']
    user = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        title = request.form['title']
        start = request.form['auction_start']
        stop = request.form['auction_end']
        description = request.form['description']
        owner_id = user.id
        image = request.files['item_image']

        #check if user folder already exists
   
        folders_list = os.listdir('./static/users/')
        
        if username in folders_list:
            user_folder = str('./static/users/' + username)

        #if not make folder    
        
        else:
            user_folder = str(os.mkdir('./static/users/' + username))
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            app.config.update (
                UPLOAD_FOLDER = user_folder
            )
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_item = Item(title, start, stop, description, owner_id, filename)
        db.session.add(new_item)
        db.session.commit()

        return redirect('/auction?id=' + str(new_item.id))

    else:    
        return render_template('new_item.html')


@app.route('/auctions')
def auction_list():
    all_auctions = Item.query.all()
    return render_template('auctions.html', all_auctions=all_auctions)


@app.route('/auction', methods=['POST', 'GET'])
def single_auction():
    username = session['username']
    user = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        amount = request.form['bid_amount']
        item_id = request.form['item_id']
        owner_id = user.id

        new_bid = Bid(amount, item_id, owner_id)
        db.session.add(new_bid)
        db.session.commit()

        item = Item.query.get(item_id)

        flash("Success you placed a bid")
        return render_template('auction.html', item=item)


    item_id = request.args.get('id')
    item = Item.query.get(item_id)

    return render_template('auction.html', item=item)



@app.route('/bids_list', methods=['POST', 'GET'])
def bid_list():
    username = session['username']
    item_id = request.args.get('id')

    #TODO - query Bid db using item id. pass item id to the function
    bids = Bid.query.filter_by(item_id=item_id).all()
    item = Item.query.filter_by(id=item_id).first()
    
    return render_template('bids_list.html', bids=bids, item=item)

@app.route('/winner')
def winner():
    winning_bid = request.args.get('bid_owner_id')
    auction_winner = User.query.filter_by(id=winning_bid).first()

    return render_template('winner.html', auction_winner=auction_winner)

@app.route('/my_items')
def my_items():
    username = session['username']
    user = User.query.filter_by(username=username).first()
    
    items = Item.query.filter_by(owner_id=user.id).all()

    return render_template('my_items.html', items=items)


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')
 

if __name__ == '__main__':
    app.run()