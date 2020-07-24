from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin

import requests
from bs4 import BeautifulSoup
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def hello():
  return render_template('main.html')


@app.route("/cotiza", methods = ['GET'])
def cotiza():
  if request.method == 'GET':
  
    url = request.args['txtLink']

    my_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "en-US,en;q=0.9", 
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}

    response = requests.get(url, headers= my_headers)
    
    res = BeautifulSoup(response.text,"lxml");

    # Data of interest
    img = res.find("img", {"id":"landingImage"})
    title = res.find("span", {"id":"productTitle"})


    # Getting image from the string
    image_txt = img['data-a-dynamic-image']
    print(image_txt)
    q1 = image_txt.find('"')
    q2 = image_txt[(q1+1):].find('"')
    txt_image = image_txt[(q1+1):(q1+q2+1)]
    
    # Excepciones debido al id del precio, ya que puede variar de producto a producto
    try:
      price = res.find("span", {"id":"priceblock_ourprice"}).text
    except:
      try:
        price = res.find("span", {"id":"priceblock_saleprice"}).text
      except:
        try:
          price = res.find("span", {"id":"priceblock_dealprice"}).text
        except:
          price = 'No se encontro el precio'

  # Return the json 
  return jsonify(title=title.text, price=price, imagen=txt_image)

  # Return the template html
  #return render_template('producto.html', titulo = title.text, precio = price, imagen=txt_image)
    
if __name__ == "__main__":
  app.run(host='0.0.0.0', port= 4000, debug=True)

