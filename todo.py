
import sys
import json
import csv
import flask
from flask.ext.sqlalchemy import SQLAlchemy
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    done = db.Column(db.Boolean)

def main():
    cmd = sys.argv[1]
    if cmd == 'add':
        text = sys.argv[2]
        item = Item(text=text)
        db.session.add(item)
        db.session.commit()
        print 'adding', text
        
    elif cmd == 'list':
        for item in Item.query.all():
            status = '[x]' if item.done else '[ ]'
            print item.id, status, item.text

    elif cmd =='done':
        id = int(sys.argv[2])
        item = Item.query.get(id)
        item.done = True
        db.session.commit()
    elif cmd == 'csv':
        writer = csv.writer(sys.stdout)
        writer.writerow(['id', 'done', 'text', 'type'])
        for item in Item.query.all():
            writer.writerow([item.id, 'y' if item.done else 'n', item.text])
    elif cmd == 'remove':
        for item in Item.query.all():
            if item.text == sys.argv[2]:
                item.done = False
                db.session.commit()
    elif cmd == 'json':
        data = []
        for item in Item.query.all():
            data.append({
                'id' : item.id,
                'done': item.done,
                'text': item.text,
                'type': "Salut ",
               })
       # print data
        print json.dumps(data, indent=2)
    elif cmd == 'loadjson':
        data = json.load(sys.stdin)
        #print json.dumps(data, indent=2)
        for item in data:
            newitem = Item(text = item['text'], done=item['done'])
            db.session.add(newitem)
            db.session.commit()

    elif cmd == 'removeall':
        for item in Item.query.all():
            item.done = False
            db.session.commit()
    elif cmd == 'rmvelem':
        rmvelem = sys.argv[2]
        for item in Item.query.all():
            if rmvelem == item.text:
                db.session.delete(item)
                db.session.commit()
    elif cmd == 'cleanup':
        for item in Item.query.all():
            if item.done:
                db.session.delete(item)
                db.session.commit()
    else:
        print 'unknown comand', cmd

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    main()


