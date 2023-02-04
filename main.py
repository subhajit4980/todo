from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    description=db.Column(db.String(200),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}-{self.description}"
@app.route("/",methods=["GET", "POST"])
def hello():
    if request.method =='POST':
        title=request.form['title']
        description=request.form['desc']
        if title=='' or description=='':
            todos=Todo.query.all()
            return render_template('index.html',alltodo=todos)
        todo=Todo(title=title,description=description)
        db.session.add(todo)
        db.session.commit()
    todos=Todo.query.all()
    return render_template("index.html",alltodo=todos)

@app.route("/delete/<int:sno>")
def delete(sno):
    todos=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todos)
    db.session.commit()
    return redirect("/")
    # todo=Todo(title="first",description="start reading carefully to got this")
    # db.session.add(todo)
    # db.session.commit()
    # todos=Todo.query.all()
# pass the all queries through the alltodo variable in the html file
    # return render_template("index.html",alltodo=todos)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        description=request.form['desc']
        todos=Todo.query.filter_by(sno=sno).first()
        todos.title=title
        todos.description=description
        # if title=='' or description=='':
        #     return redirect("/update")
        db.session.add(todos)
        db.session.commit()
        return redirect("/")
    todos=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todos)
if __name__=="__main__":
    app.run(debug=True,port='5000')