from flask import Flask

app =  Flask(__name__)
app.config['JSON_AS_ASCII'] = False

if __name__ == '__main__':
    app.run()
