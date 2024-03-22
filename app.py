from backend import app
import flask
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    app.run(debug=True, host='0.0.0.0', port=port)