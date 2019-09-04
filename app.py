from flask import request, jsonify, Flask
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return '''<h1>API-Cryptocurrencies Prices</h1>
<p>Made by João Cesar</p>'''

@app.route('/currency/all', methods=['GET'])
def currencies_list():
	return jsonify(cg.get_coins_list())

@app.route('/currency', methods=['GET'])
def currency_conv():
	if 'f_id' in request.args:
		f_id = str(request.args['f_id'])
	else:
		return "Error: No id field provided. Please specify the first id (f_id)."
	if 's_id' in request.args:
		s_id = str(request.args['s_id'])
	else:
		return "Error: No id field provided. Please specify the second id (s_id)."
	if 'f_value' in request.args:
		f_value = float(request.args['f_value'])
	else:
		return "Error: No id field provided. Please specify the first value (f_value)."

	all_currencies = cg.get_coins_list()
	for currency in all_currencies:
		if currency['id'] == f_id:
			f_name = currency['name']
		if currency['id'] == s_id:
			s_name = currency['name']

	try:
		f_price = float(cg.get_price(ids = f_id, vs_currencies='usd')[f_id]['usd'])
		s_price = float(cg.get_price(ids = s_id, vs_currencies='usd')[s_id]['usd'])
		div1 = f_price/s_price
		s_value = div1 * f_value

		result = [{
			'id' : f_id,
			'price' : f_price,
			'value' : f_value,
			'name' : f_name
		},
		{
			'id' : s_id,
			'price' : s_price,
			'value' : s_value,
			'name' : s_name
		}]
		return jsonify(result)
	except:
		return jsonify([{}])



if __name__ == '__main__':
    app.run(debug=True)




