from view import app
from auth import app


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)


#pip freeze > requirements.txt or pipreqs>requirements.txt