from crypt import methods
from flask import Flask, render_template, request, redirect, url_for
#getting the views blue print from the views file
#from views import views
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#creating a flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

#db.Model: Makes (class name) Todo a table
#creating a model with a class
     #inheriting db.Model class
class Todo(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     content = db.Column(db.String(200), nullable = False)
     date_created = db.Column(db.DateTime, default = datetime.utcnow)


     def __repr__(self):
          return '<Task %r' %self.id



#registering blueprint and url
##app.register_blueprint(views, url_prefix = "/views", method)

#adding 2 methods this route can accept
    #instead of only 'GET'(get data from website) by DEFAULT now we can 'POST' TOO
        #'POST' = SEND DATA TO DATABASE
          #POST =  ANY ACTIONS USER DOES WITH WEBSITE(press button) and where it takes them
@app.route("/", methods = ['POST', 'GET'])
def home():
     #we imported request(User REQUEST something to front end AND BACK END RESPONDS)
     if request.method == "POST":
          """if user POST something (press add tasks button) then send them to ANOTHER PAGE that only says hello
          return "Hello"""
          #creating task_content variable
               #where we're storing content of user's input
               #request(request object).form(form = created something when posting something)
               #[content] = pass in the ID of the input that we want
                    #the ID(name) is "content" in HTML
#storing users content(name & ID) in task_content
          task_content = request.form['content']

          #CREATING todo MODEL by
               #creating todo object(putting in task_content here)
               #Todo class has (id, content and date created) we're only passing in content
#HOW TO ADD TO Todo TABLE
          new_task = Todo(content = task_content)

          #PUSHING THIS (new task) MODEL TO DATABASE by:
          try:
               #adding new_task model(object) into database
               db.session.add(new_task)

               #commiting new_task back to database
               db.session.commit()

               #redirect back to index.html (home page) page
               return redirect("/")
          #if ^ fails 
          except:
               return "There was an issue adding your task"

#HOW WE'RE GOING TO DISPLAY CURRENT TASKS IN TABLE(Todo)
     #if nothing is CURRENTLY being posted into website
          #then DISPLAY Todo TABLE (BY QUERY)
     else:

#Todo is a TABLE(bc of db.Model baseclass)
     #query is getting ALL columns and ORDERING THEM by date created
          #STORING THEM IN TASKS
          tasks = Todo.query.order_by(Todo.date_created).all()

          #rendering html template and giving it variable name = "javi"
               #passing tasks into templates(just like we passed our name earlier)
                    #then html will run through all the tasks (columns) and PRINT THEM
          return render_template("index.html", tasks = tasks,)


#CREATING THE DELETE FUNCTION

#creating new route and giving it ID (bc easier to identify and UNIQUE BC its a primary key)
@app.route('/delete/<int:id>')
def delete(id):

     #Quering from database the ID we passed in, if no id in QUERY then 404
     task_to_delete = Todo.query.get_or_404(id)

     #going to database
     try:
          #deleting the task_to_delete we queried
          db.session.delete(task_to_delete)

          #comming it back to database
          db.session.commit()

          #return us back to home page
          return redirect("/")
     #if no work
     except:
          return "There was an error delelting your task"

#FOR UPDATING TASK
#creating new route and giving it unique id
     #Giving it post bc we're going to be POSTING TO website
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
     #quering the task we want to update
     task = Todo.query.get_or_404(id)
     
     #if user is POSTING SOMETHIMG 
     if request.method == 'POST':
          #we're setting the current task(we queried) content = the content in the input box(what the user is requesting in the update box)
          task.content = request.form['content']
          
          try:
               #NOT ADD BC we already changed the task's content ^
               db.session.commit()
               #then redirect back to home page
               return redirect('/')
          except:
               return "update was unsusecful "

     else:
          #rendering the new update file and passing in the task we queried
          return render_template('update.html', task = task)


 

if __name__ == '__main__':
    #what port do we want out website in (og is 5000)
    #debug: when chaining any files in app it will AUTO REFRESH app instead of always running this script
         #auto debugs when we save
    app.run(debug = True, port = 8000)