import streamlit as st
import pandas as pd
import psycopg2
# reference video :- https://youtu.be/M2NzvnfS-hI

# DB Management (connecting local DB for data storing & retrivting)
import psycopg2 # for connecting DB with Python

#connection with PostGres
connection = psycopg2.connect(
                       host = 'localhost', 
                       port = 5432 , 
                       dbname = 'Store_Student_details' , 
                       user = 'postgres',
                       password= 'abcdefhij' )

cur= connection.cursor()

# SQL queries for fetching & inserting values into our table
sql_create_new_table_query = '''create table if not exists login_details (
                                user_id varchar(15) not null,
                                password varchar(19) not null   ) '''

sql_all_data_fetch_query= "SELECT * from login_details"
sql_table_fetch_query = 'SELECT * FROM login_details'
sql_insert_script = '''INSERT INTO login_details 
                      ( user_id,password ) values ( %s,%s )''' 

# DB  Functions
def create_table() :
    cur.execute( sql_create_new_table_query )
    connection.commit()
    
    return 'Table created successfully!! '
def fetch_all_records( query ) : 
    return cur.fetchall()


def add_userdata( user_id,password ):
    try:
        cur.execute(sql_insert_script ,(user_id,password) ) 
        connection.commit()
        st.write( 'Added successfully! ')
    except:
        st.write( 'Facing error while adding new user. Please connect to administrator.')

def login_user( user_id ,password ):
    res=cur.execute('''SELECT * FROM login_details WHERE user_id =%s AND password = %s''', (user_id,password)) 
    data = cur.fetchall()
    return data
    #st.write( 'Inside login_user' )
	


def view_all_users():
	cur.execute('SELECT * FROM login_details')
	data = c.fetchall()
	return data



st.subheader("Login Section")
create_table()
#st.write( 'Table created successfully!!')
choose_one= st.selectbox( 'Choose an option ', options = ['SignUp(new user)', 'Login'])
if choose_one=='Login':
    #st.write( result )
    with st.form( 'login_first' ):
        username = st.text_input("User Name") 
        password = st.text_input("Password",type='password')
        submitted = st.form_submit_button("Login")  
        result = login_user( username,password )
        #st.write( result )
        if submitted:
            if result:
                st.success( 'You logged in successfully ' )
            elif result==None:
                pass
            else:
                st.warning('Incorrect Username/Password.\nFor reset password kindly connect with your college administrator.', icon="⚠️")


elif choose_one == "SignUp(new user)":
    with st.form( 'signup_first' ):
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')
        submitted_1 = st.form_submit_button("SingUp")
        if submitted_1:
            add_userdata( new_user,new_password )
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
