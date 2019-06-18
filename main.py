import pymongo
from flask import Flask, jsonify, request
from datetime import datetime, date, time

app =  Flask(__name__)
app.config['JSON_AS_ASCII'] = False

class Note:

    def __init__(self, database = None, note_id = None, title = None, text = None, author = None, dateOfCreation = None):
        if note_id is None:
            #свободный _id
            sortedDB = notes_db[database].find({}).sort("_id", -1).limit(1)

            if sortedDB.count() == 0:
                note_id = 0
            else:
                for item in sortedDB:
                    note_id = (item["_id"]) + 1

        if title is None:
            title = "Empty"
        if text is None:
            text = "Empty"
        if author is None:
            author = "me"
        if dateOfCreation is None:
            dateOfCreation = datetime.now().strftime("%d.%m.%Y %H:%M:%S")


        self.note_id = int(note_id)
        self.title = title
        self.text = text
        self.author = author
        self.dateOfCreation = dateOfCreation

    def get_info(self):
        return {
            "_id": self.note_id,
            "title": self.title,
            "text": self.text,
            "author:": self.author,
            "dateOfCreation": self.dateOfCreation
        }


mongo_client = pymongo.MongoClient(port=27017)
notes_db = mongo_client['notes_db']


@app.route('/save/<database>/<note_id>/<title>/<text>/')
@app.route('/save/<database>/<note_id>/<title>/<text>/<author>/')
@app.route('/save/<database>/<note_id>/<title>/<text>/<author>/<dateOfCreation>')
def add_one_route(database = None, note_id = None, title = None, text = None, author = None, dateOfCreation = None):
    tempObj = Note(
        database,
        note_id,
        title,
        text,
        author,
        dateOfCreation
    )

    try:
        notes_db[database].insert_one(tempObj.get_info())
        return jsonify(tempObj.get_info())
    except Exception as error:
        return('Error: ' + repr(error))


@app.route('/update/<database>/<note_id>/<title>/<text>/')
@app.route('/update/<database>/<note_id>/<title>/<text>/<author>/')
@app.route('/update/<database>/<note_id>/<title>/<text>/<author>/<dateOfCreation>')
def update_one_route(database = None, note_id = None, title = None, text = None, author = None, dateOfCreation = None):
    tempObj = Note(
        database,
        note_id,
        title,
        text,
        author,
        dateOfCreation
    )

    try:
        notes_db[database].replace_one({"_id": note_id}, tempObj.get_info())
        return jsonify(tempObj.get_info())
    except Exception as error:
        return('Error: ' + repr(error))


if __name__ == '__main__':
    app.run()
