from flask import Flask, send_file

app = Flask(__name__)

@app.route('/image', methods=['GET'])
def get_image():
    # Load the image from a file or from any other source
    image_path = 'maininput.jpg'
    return send_file(image_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=open,port=8800)
