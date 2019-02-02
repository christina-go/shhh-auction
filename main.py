from flask import Flask, flash, redirect, request, render_template
import cgi
import os
from app import app, db
from models import Auction, Bid


@app.route('/')
def redirect_index():
    return redirect('/index')

@app.route('/index')
def index():
    return render_template('index.html')    

@app.route('/signup')
def signup():
    return render_template('signup.html')  

#TODO: username and password validation
# database 

@app.route('/new_item')    
def new_item():
    return render_template('new_item.html')


@app.route('/auctions')
def auction_list():
    all_auctions = Auction.query.all()
    return render_template('auctions.html', all_auctions=all_auctions)


@app.route('/auction', methods=['POST', 'GET'])
def single_auction():
    auction_id = request.args.get('id')
    owner = "christina_go"

    
    if request.method == 'POST':
        amount = request.form['bid_amount']
        auction_id = request.form['auction-id']

        new_bid = Bid(amount, auction_id, owner)
        db.session.add(new_bid)
        db.session.commit()

        auction = Auction.query.get(auction_id)

        flash("Success you placed a bid")
        return render_template('auction.html', auction=auction)

        #TODO - FLASH THE SUCCESS MESSAGE AND RELOAD THE AUCTION PAGE

    auction = Auction.query.get(auction_id)

    return render_template('auction.html', auction=auction)
 


if __name__ == '__main__':
    app.run()