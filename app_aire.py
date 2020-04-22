from flask import Flask, request, render_template, redirect, url_for
import make_map
import pickle
      
app = Flask(__name__)

maps_data, variables = make_map.get_data()
#variables = ['PM10', 'PST']

@app.route('/', methods=['GET', 'POST'])
def home():
  if request.method == 'POST':
    current_var = request.form['id']
    make_map.save_map(maps_data[current_var])
    return render_template('index.html', variables=variables, current=current_var)
  else:
    make_map.save_map(maps_data['PM10'])
    return render_template('index.html', variables=variables, current='PM10')

@app.route('/map/')
def map_display():
  return render_template('Map.html')

if __name__=="__main__":
    # carga los dos datos 2 veces. Creo que es por el 'lazy_loading' corre el script la primera vez y después cuando de verdad se carga el app.
    app.run(debug=True, port=8080)