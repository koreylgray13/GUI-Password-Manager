from tkinter import *
import sqlite3


root = Tk()
root.title('Password Manager')
root.geometry('320x500')
root.iconbitmap('lock.ico')

submit_frame = LabelFrame(root, text='Add Record', font=("Arial Bold", 9))
submit_frame.grid(row=0, column=0, pady=5, padx=5)

select_frame = LabelFrame(root, text='Edit/Delete Record', font=("Arial Bold", 9))
select_frame.grid(row=1, column=0, pady=5, padx=5)

query_frame = LabelFrame(root, text='Find Records', font=("Arial Bold", 9))
query_frame.grid(row=2, column=0, pady=5, padx=5)

query_frame2 = LabelFrame(root, text='Show Records', font=("Arial Bold", 9))
query_frame2.grid(row=3, column=0, pady=5, padx=5)

# Create / Connect Database
conn = sqlite3.connect('passwords.db')
# Create Cursor
c = conn.cursor()


# Create Submit Function
def submit():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()

    # Insert Into Table
    c.execute("INSERT INTO passwords VALUES (:website, :username, :password, :category)",
              {
                    'website': name.get(),
                    'username': username.get(),
                    'password': password.get(),
                    'category': category.get(),
              })


    conn.commit()
    conn.close()

    # Clear Text Boxes
    name.delete(0, END)
    username.delete(0, END)
    password.delete(0, END)
    category.delete(0, END)


# Create Update Record Function
def update():
    # Connect To Database & Create Cursor
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()

    record_id = delete_box.get()



    c.execute("""UPDATE passwords SET 
        name = :name,
        username = :username,
        password = :password,
        category = :category

        WHERE oid = :oid""",
        {
         'name': name_editor.get(),
         'username': username_editor.get(),
         'password': password_editor.get(),
         'category': category_editor.get(),
         'oid': record_id
        })

    # Commit Changes & Close Connection
    conn.commit()
    conn.close()


# Create Edit Record Function
def edit():
    editor = Tk()
    editor.title('Update A Record')
    editor.geometry('350x400')

    # Connect To Database & Create Cursor
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()

    # Query Database
    record_id = delete_box.get()
    c.execute("SELECT * FROM passwords WHERE oid = " + record_id)
    records = c.fetchall()

    # Create Global Variables
    global name_editor
    global username_editor
    global password_editor
    global category_editor

    # Text Boxes
    name_editor = Entry(editor, width=30)
    name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))

    username_editor = Entry(editor, width=30)
    username_editor.grid(row=1, column=1)

    password_editor = Entry(editor, width=30)
    password_editor.grid(row=2, column=1)

    category_editor = Entry(editor, width=30)
    category_editor.grid(row=3, column=1)

    # Text Box Labels
    name_editor_label = Label(editor, text="Tag")
    name_editor_label.grid(row=0, column=0, pady=(10, 0))

    username_editor_label = Label(editor, text="Username")
    username_editor_label.grid(row=1, column=0)

    password_editor_label = Label(editor, text="Password")
    password_editor_label.grid(row=2, column=0)

    category_editor_label = Label(editor, text="Category")
    category_editor_label.grid(row=3, column=0)

    # Create Save Button
    edit_btn = Button(editor, text="Save Record", command=update)
    edit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=130)

    # Loop Through Results
    for record in records:
        name_editor.insert(0, record[0])
        username_editor.insert(0, record[1])
        password_editor.insert(0, record[2])
        category_editor.insert(0, record[3])


# Create Delete Record Function
def delete():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()

    c.execute("DELETE from passwords WHERE oid= " + delete_box.get())


    conn.commit()
    conn.close()


# Create Query Function
def query():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()

    c.execute("SELECT *, oid FROM passwords")
    records = c.fetchall()

    # Create New Window
    password_window = Tk()
    password_window.title('Passwords')
    password_window.geometry('500x500')


    # Loop Through Results
    print_tag = ''
    print_user = ''
    print_pass = ''
    print_category = ''
    oid = ''
    for record in records:
        print_tag += str(record[0]) + "\n"
        print_user += str(record[1]) + "\n"
        print_pass += str(record[2]) + "\n"
        print_category += str(record[3]) + "\n"
        oid += str(record[4]) + "\n"

    # Place Results On Separate Window
    oid_label = Label(password_window, text=oid)
    oid_label.grid(row=1, column=0)

    web_label = Label(password_window, text=print_tag)
    web_label.grid(row=1, column=2)

    user_label = Label(password_window, text=print_user)
    user_label.grid(row=1, column=3)

    query_label = Label(password_window, text=print_pass)
    query_label.grid(row=1, column=4)

    query_label = Label(password_window, text=print_category)
    query_label.grid(row=1, column=1)

    # Column Names
    oid_column = Label(password_window, text='ID', font=("Arial Bold", 9))
    oid_column.grid(row=0, column=0, padx=5)

    web_column = Label(password_window, text='Tag', font=("Arial Bold", 9))
    web_column.grid(row=0, column=2, padx=25)

    user_column = Label(password_window, text='Username', font=("Arial Bold", 9))
    user_column.grid(row=0, column=3, padx=25)

    pass_column = Label(password_window, text='Password', font=("Arial Bold", 9))
    pass_column.grid(row=0, column=4, padx=25)

    pass_column = Label(password_window, text='Group', font=("Arial Bold", 9))
    pass_column.grid(row=0, column=1, padx=10)


    conn.commit()
    conn.close()
    # Run Separate Window
    password_window.mainloop()


# Create Query Function For Specific Tag
def query2():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()

    c.execute("SELECT *, oid FROM passwords WHERE name LIKE '" + tag_search_box.get() + "' OR category LIKE '" + group_search_box.get() + "'")
    records = c.fetchall()

    # Create New Window
    password_window = Tk()
    password_window.title('Passwords')
    password_window.geometry('500x500')


    # Loop Through Results
    print_tag = ''
    print_user = ''
    print_pass = ''
    print_category = ''
    oid = ''
    for record in records:
        print_tag += str(record[0]) + "\n"
        print_user += str(record[1]) + "\n"
        print_pass += str(record[2]) + "\n"
        print_category += str(record[3]) + "\n"
        oid += str(record[4]) + "\n"

    # Place Results On Separate Window
    oid_label = Label(password_window, text=oid)
    oid_label.grid(row=1, column=0)

    tag_label = Label(password_window, text=print_tag)
    tag_label.grid(row=1, column=2)

    user_label = Label(password_window, text=print_user)
    user_label.grid(row=1, column=3)

    query_label = Label(password_window, text=print_pass)
    query_label.grid(row=1, column=4)

    query_label = Label(password_window, text=print_category)
    query_label.grid(row=1, column=1)

    # Column Names
    oid_column = Label(password_window, text='ID', font=("Arial Bold", 9))
    oid_column.grid(row=0, column=0)

    web_column = Label(password_window, text='Tag', font=("Arial Bold", 9))
    web_column.grid(row=0, column=2)

    user_column = Label(password_window, text='Username', font=("Arial Bold", 9))
    user_column.grid(row=0, column=3)

    pass_column = Label(password_window, text='Password', font=("Arial Bold", 9))
    pass_column.grid(row=0, column=4)

    pass_column = Label(password_window, text='Group', font=("Arial Bold", 9))
    pass_column.grid(row=0, column=1)


    conn.commit()
    conn.close()
    # Run Separate Window
    password_window.mainloop()


# Text Boxes
name = Entry(submit_frame, width=30)
name.grid(row=0, column=1, padx=20, pady=(10, 0))

username = Entry(submit_frame, width=30)
username.grid(row=1, column=1)

password = Entry(submit_frame, width=30)
password.grid(row=2, column=1)

category = Entry(submit_frame, width=30)
category.grid(row=3, column=1)

delete_box = Entry(select_frame, width=30)
delete_box.grid(row=0, column=1)

tag_search_box = Entry(query_frame, width=30)
tag_search_box.grid(row=2, column=1)

group_search_box = Entry(query_frame, width=30)
group_search_box.grid(row=3, column=1)

# Text Box Labels
website_label = Label(submit_frame, text="Name")
website_label.grid(row=0, column=0, pady=(10, 0))

username_label = Label(submit_frame, text="Username")
username_label.grid(row=1, column=0)

password_label = Label(submit_frame, text="Password")
password_label.grid(row=2, column=0)

category_label = Label(submit_frame, text="Category")
category_label.grid(row=3, column=0)

delete_box_label = Label(select_frame, text="Select ID")
delete_box_label.grid(row=0, column=0, pady=10)

tag_search_box_label = Label(query_frame, text="Tag")
tag_search_box_label.grid(row=2, column=0)

group_search_box_label = Label(query_frame, text="Category")
group_search_box_label.grid(row=3, column=0, pady=5)

# Submit Button
submit_btn = Button(submit_frame, text="Add Record", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=5, padx=10, ipadx=100)

# Create Update Button
update_btn = Button(select_frame, text="Update Record", command=edit)
update_btn.grid(row=7, column=0, columnspan=2, pady=5, padx=10, ipadx=92)

# Create Delete Button
delete_btn = Button(select_frame, text="Delete Record", command=delete)
delete_btn.grid(row=8, column=0, columnspan=2, pady=5, padx=10, ipadx=94)

# Create Query Button For Search
query_btn = Button(query_frame, text="Search Records", command=query2)
query_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=91)

# Create Query Button For Show All
query_btn = Button(query_frame2, text="Show All Records", command=query)
query_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=10, ipadx=86)


root.mainloop()