from flask import Flask, render_template, request, redirect, url_for
from blockchain import exchangerates, blockexplorer
import requests
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    prices = exchangerates.get_ticker()
    last_block = requests.get("https://blockchain.info/latestblock")
    last_block = json.loads(last_block.text)
	
    pre_blocks = []
    pre_block = requests.get("https://blockchain.info/rawblock/"+last_block["hash"])
    pre_block = json.loads(pre_block.text)
    pre_blocks.append(pre_block["prev_block"])
    for i in range(5):
        pre_block = requests.get("https://blockchain.info/rawblock/"+pre_block["prev_block"])
        pre_block = json.loads(pre_block.text)
        pre_blocks.append(pre_block["prev_block"])
    return render_template("index.html", prices=prices, last_block=last_block, pre_blocks=pre_blocks, datetime=datetime)
	
@app.route('/<string:block_hash>/blockinfo', methods=['GET', 'POST'])	
def block_info(block_hash):
	block = requests.get("https://blockchain.info/rawblock/"+block_hash)
	block = json.loads(block.text)
	return render_template("block_info.html", block=block, datetime=datetime)
	
@app.route('/<string:trans_hash>/transinfo', methods=['GET', 'POST'])	
def transaction_info(trans_hash):
	transaction = requests.get("https://blockchain.info/rawtx/"+trans_hash)
	transaction = json.loads(transaction.text)
	return render_template("trans_info.html", transaction=transaction, datetime=datetime)
	
if __name__ == '__main__':
    app.run()