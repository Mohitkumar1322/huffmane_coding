from flask import Flask, render_template, request, send_from_directory

from huffman import HuffmanCode  # Your existing HuffmanCode class

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Render the home page

@app.route('/compress', methods=['POST'])
def compress_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            path = 'uploaded_file.txt'  #  is helps to save the file at location
            file.save(path)
            
            # here we call the huffman coding class from huffman.py
            huffman = HuffmanCode(path)
            output_file = huffman.compression()  # Process the file and return the compressed file path
            
            return f'File compressed successfully. Download it <a href="/download/{output_file}">here</a>'

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(directory='.', path=filename)

if __name__ == '__main__':
    app.run(debug=True)
