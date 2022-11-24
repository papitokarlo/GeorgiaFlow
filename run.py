from api import create_app
import logging



# logging.basicConfig(filename='logger.log', level=logging.INFO, format='%(asctime)s:%(levelno)s:%(pathname)s:%(processName)s:%(levelname)s:%(name)s:%(message)s')

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# formatter = logging.Formatter('%(asctime)s:%(levelno)s:%(pathname)s:%(processName)s:%(levelname)s:%(name)s:%(message)s')

# file_handler = logging.FileHandler('logger.log')
# file_handler.setLevel(logging.ERROR)
# file_handler.setFormatter(formatter)

# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)

# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)

if __name__ == '__main__':
    
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
    # logging.info('api accsess : ', app)
    # # logger.info(app)
    # # logger.error(app)