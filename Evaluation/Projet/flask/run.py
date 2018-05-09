from app import app

if __name__ == '__main__':
    # threaded equals true lets the application make use of the available cores of the host machine
    # in order to provide better performances.
    app.run(debug=True, port=8000, host='localhost', threaded=True)
