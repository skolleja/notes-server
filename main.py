from flask import Flask, jsonify
import pymongo

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

mongo_client = pymongo.MongoClient(port=27017)
db = mongo_client['notes_db']
collection = db

@app.route("/", methods=['GET'])
def get_main():
    sortedDB = db['private_notes'].find()

    output_private = []
    output_archive = []
    output_work = []

    for item in sortedDB:
        output_private.append({'id': item['_id'], 'title': item['title'], 'text': item['text'], 'author': item['author:'], 'dateOfCreation': item['dateOfCreation']})

    sortedDB = db['archiv'].find()
    for item in sortedDB:
        output_archive.append({'id': item['_id'], 'title': item['title'], 'text': item['text'], 'author': item['author:'], 'dateOfCreation': item['dateOfCreation']})
    sortedDB = db['work_notes'].find()
    for item in sortedDB:
        output_work.append({'id': item['_id'], 'title': item['title'], 'text': item['text'], 'author': item['author:'], 'dateOfCreation': item['dateOfCreation']})

    return jsonify({'result_private': output_private, 'result_archive': output_archive, 'result_work': output_work})


@app.route('/work', methods=['GET'])
def work_notes():
    output_work = []
    sortedDB = db['work_notes'].find()
    for item in sortedDB:
        output_work.append({'id': item['_id'], 'title': item['title'], 'text': item['text'], 'author': item['author:'], 'dateOfCreation': item['dateOfCreation']})
    return jsonify({'result_work': output_work})


@app.route('/private', methods=['GET'])
def private_notes():
    output_private = []
    sortedDB = db['private_notes'].find()
    for item in sortedDB:
        output_private.append({'id': item['_id'], 'title': item['title'], 'text': item['text'], 'author': item['author:'], 'dateOfCreation': item['dateOfCreation']})
    return jsonify({'result_private': output_private})


@app.route('/archive', methods=['GET'])
def archive_notes():
    output_archive = []
    sortedDB = db['archiv'].find()
    for item in sortedDB:
        output_archive.append({'id': item['_id'], 'title': item['title'], 'text': item['text'], 'author': item['author:'], 'dateOfCreation': item['dateOfCreation']})
    return jsonify({'result_archive': output_archive})


if __name__ == '__main__':
    app.run()
