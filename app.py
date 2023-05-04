from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.app_context().push()

app.config[ 'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/")
def index():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template("index.html", tasks=tasks)

@app.route("/add_todo", methods=['POST'])
def todo():
    to_do_item = request.form['content']
    if not to_do_item:
        return 'no content'
    else:
        new_todo = Todo(content=to_do_item)
        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')
        except:
            return 'uh oh'
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        "still there"
