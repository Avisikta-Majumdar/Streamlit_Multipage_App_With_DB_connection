# done
import streamlit as st
import os
import psycopg2 # for connecting DB with Python

#connection with PostGres
connection = psycopg2.connect(
                       host = 'localhost', 
                       port = 5432 , 
                       dbname = 'Store_Student_details' , 
                       user = 'postgres',
                       password= 'abcdefghijkl' )

cur= connection.cursor()

# sql queires
sql_create_new_table_query = '''create table if not exists students_data (
                                s_name varchar(50) not null,
                                s_dept varchar(3) not null , 
                                s_roll_no varchar(3) not null,
                                assignment_location varchar(200) not null) '''

sql_all_data_fetch_query= "SELECT * from students_data"
insert_script = "INSERT INTO students_data ( s_name,s_dept,s_roll_no, assignment_location ) values (%s, %s, %s, %s)"  
#insert_values = ( your_name, department, roll_no )

def create_table() :
    cur.execute( sql_create_new_table_query )
    connection.commit()
    
    return 'Table created successfully!! '
def fetch_all_records( query ) : 
    return cur.fetchall()
    
def insert_form_values( name, dept, roll, location ):
    insert_values = ( name, dept, roll, location )
    cur.execute( insert_script, insert_values )
    # saving the new record by using commit command
    connection.commit( )
    cur.execute( sql_all_data_fetch_query )
    return cur.fetchall()

temp = create_table()
st.header("Upload Your Assignment")

#st.write("You have entered", st.session_state["my_input"])
col1, col2, col3 = st.columns( 3 ) 
with st.form( 'my_assignment_upload_form' ):
    your_name = st.text_input( label='Enter your name here', max_chars= 50)
    department =st.selectbox('Choose your department',options=['CSE','IT','ECE','CE','ME','EE'])
    roll_no = st.number_input( 'Your roll number', min_value=1, max_value=120 )
    
    # st.write( 'Current working directory ' , os.getcwd() ) 
    
    # the assignment will be ither in docx or pdf format
    uploaded_files= st.file_uploader( "Upload your assignment", type=[ 'docx','pdf'], accept_multiple_files=True)
    for uploaded_file in uploaded_files[:1]:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        with open( os.path.join( 'Files_will_be_stored_here', uploaded_file.name) ,'wb') as f:
            # next line will save the directory in the mention directory
            f.write( uploaded_file.getbuffer() ) 
        
            # st.success( 'Sucessfully saved the file' ) 
        assignment_location = os.path.join( os.getcwd(),'Files_will_be_stored_here', uploaded_file.name )
        
     
    #Every form must have a submit button.
    submitted = st.form_submit_button("Submit")   
    if submitted: 
        insert_form_values( your_name, department, roll_no, assignment_location )
        st.success( 'Your have submitted your assignment successfully ' )
    insert_values = ( your_name, department, roll_no )
