from sqlalchemy import create_engine, text
from faker import Faker
import random
from datetime import datetime
from flask import Flask
 
 
db_string = "postgresql://root:root@localhost:5432/postgres"
 
engine = create_engine(db_string)
 
app = Flask(__name__)
 
@app.route("/user", methods=["GET"])
def get_users():
    users = run_sql_with_result("SELECT * FROM users")
    data = []
    for row in users:
        user = {
            "id":row[0],
            "firstname":row[1],
            "lastname":row[2],
            "age":row[3],
            "email":row[4],
            "job":row[5]
        }
        data.append(user)
    return data
 
fake = Faker()
create_user_table_sql = """
CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY ,
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    age  INT,
    email VARCHAR(200),
    job VARCHAR(100)
)
"""
 
create_application_table_sql="""
CREATE TABLE IF NOT EXISTS applications(
    id SERIAL PRIMARY KEY ,
    appname VARCHAR(100),
    username VARCHAR(100),
    lastconnection TIMESTAMP WITH TIME ZONE,
    user_id INTEGER REFERENCES users(id)
)
"""
 
def run_sql(query:str):
    with engine.connect() as connection:
        trans = connection.begin()  
        connection.execute(text(query))
        trans.commit()  
 
 
def run_sql_with_result(query:str):
    with engine.connect() as connection:
        trans = connection.begin()  
        result = connection.execute(text(query))
        trans.commit()  
        return result
 
def populate_tables():
    apps = ["Facebook", "Instagram", "Snapchat","TikTok","X"]
    for _ in range(100):
        firstname = fake.first_name()
        lastname = fake.last_name()
        age = random.randrange(18,50)
        email = fake.email()
        job = fake.job().replace("'","")
        insert_user_query = f"""   
        INSERT INTO users(firstname,lastname,age,email,job)
        VALUES ('{firstname}','{lastname}',{age},'{email}','{job}')
        RETURNING id
        """   
        user_id=run_sql_with_result(insert_user_query).scalar()
 
       # apps_name = [random.choice(apps) for _ in range(1,random.randrange(1,5))]
        num_apps = random.randint(1,5)
        for i in range(num_apps):
            username = fake.user_name()
            lastconnection = datetime.now()
            appname = random.choice(apps)
            insert_applications_query = f"""   
            INSERT INTO applications(appname,username,lastconnection,user_id)
            VALUES ('{appname}','{username}','{lastconnection}','{user_id}')
            """   
            run_sql(insert_applications_query)
 
if __name__ == '__main__':
    run_sql(create_user_table_sql)
    run_sql(create_application_table_sql) 
    populate_tables()
 
    app.run(host="0.0.0.0", port=8081, debug=True)