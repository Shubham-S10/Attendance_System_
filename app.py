from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

with app.app_context():
    db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
 

    def __repr__(self):
        return '<attendances %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        attendance_content = request.form['content']
        new_attendee =Todo(content=attendance_content)

        try:
            db.session.add(new_attendee)
            db.session.commit()
            return redirect('/')

        except:
            return 'There was an issue adding you attendance !'


    else:
        attendances = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', attendances=attendances)



@app.route('/delete/<int:id>')
def delete(id):
    attendance_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(attendance_delete)
        db.session.commit()
        return redirect('/')
    except:
            return 'There was a problem deleting this attendance !'


                        



if __name__ =="__main__":
    app.run(debug=True)

