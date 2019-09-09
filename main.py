from flask import Flask, render_template, request,session
from util import *
from google.cloud import spanner
from pubsub_publisher import *
import json
import random

app=Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


# [START spanner_insert_data]
def insert_data(table_name, columns, values_rows):
    """Inserts sample data into the given database.

    The database and table must already exist and can be created using
    `create_database`.
    """

    # Your Cloud Spanner instance ID.
    instance_id = 'endtoenddemo-spanner'
    # Your Cloud Spanner database ID.
    database_id = 'demo_database'

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.batch() as batch:
        batch.insert(
            table=table_name,
            columns=columns,
            values=values_rows)

    print('Success Inserted data.')


# [END spanner_insert_data]



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        height=int(request.form["height_name"])
        weight=int(request.form["weight_name"])
        print(height, weight)

        bmi =  weight/height
        #email = get_random_email()

        #data = Data(email, height)
        #db.session.add(data)
        #db.session.commit()

        return render_template('index.html', text="This is calculated using Python : Your BMI is %s \n This is a simple logic calculated in Python, Python is a multipurpose programming language"%bmi)
    return render_template('index.html', text="Seems like we got something from that email once!")


@app.route("/generate_random_dimension", methods=['POST'])
def generate_random_dimension():
    if request.method=='POST':

        name = get_random_name()
        age = get_random_age()

        hash = random.randint(10000000,99999999)

        table_name = 'Customer'
        columns=('cust_id', 'age', 'name')
        values=[
            (hash, age, name)]

        insert_data(table_name,columns,values)

        # PubSub Publisher
        message = {'cust_id':hash,
        'age': age,
        'name': name}
        message_json = json.dumps(message)

        topic = "demo_customer"
        pubsub_publisher(topic,message_json)

        return render_template('index.html', text="This generate Dimension Data to Database, its an illustration for Customer Data. \n Random Customer Data Generated.")


@app.route("/generate_random_transaction", methods=['POST'])
def generate_random_transaction():
    if request.method=='POST':

        cust_id = get_random_cust_id()
        time = get_timestamp()
        amount = float(get_random_amount())

        import random
        hash = random.randint(1000000000,9999999999)

        table_name = 'transaction'
        columns=('trx_id', 'amount', 'cust_id','trx_time')
        values=[(hash, amount, cust_id,time)]

        insert_data(table_name,columns,values)

        # PubSub Publisher
        message = {'trx_id':hash,
        'amount': amount,
        'cust_id': cust_id,
        'trx_time': time}
        message_json = json.dumps(message)

        topic = 'demo_transaction'
        pubsub_publisher(topic,message_json)

        return render_template('index.html', text="This generate data to PostgreSQL Database, its an illustration for Transaction Apps. \n Random Transaction Data Generated.")

@app.route("/update_data_dimension", methods=['POST'])
def update_data_dimension():
    if request.method=='POST':

        name = get_random_name()

        row = DimensionData.query.filter_by(id=1).first()
        row.name = name
        row_2 = DimensionData.query.filter_by(id=2).first()
        row_2.age = get_random_age()
        db.session.commit()

        return render_template('index.html', text="This update Dimension Data to Database")

if __name__ == '__main__':
    HOST="127.0.0.1"
    PORT="8080"
    app.run(host=HOST,debug=True,port=PORT)
