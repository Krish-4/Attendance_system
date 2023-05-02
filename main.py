from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
attendanceframe = None

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="attendance_system"
)
mycursor = mydb.cursor()

def sub_select(event):
    selected_sem = semchoose.get()
    mycursor.execute(f"SELECT * FROM `courses_info` WHERE sem={selected_sem}")
    myresult = mycursor.fetchall()
    subjects=[]
    for x in myresult:
        subjects.append((x[1]))
    subchoose['values'] = subjects
    subchoose.current(0)

def division_show(event):
    selected_sem = semchoose.get()
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM `stu_div_info` WHERE `stu_sem`={selected_sem} GROUP BY `stu_div`")
    myresult = mycursor.fetchall()
    divisions=[]
    for x in myresult:
        divisions.append((x[1]))
    divchoose['values'] = divisions
    divchoose.current(0)

def saveattendance(attendance):
    selected_sem = semchoose.get()
    selected_div = divchoose.get()
    selected_subject = subchoose.get()

    # convert the list of attendance into a string of comma-separated values
    attendance_str = ','.join(map(str, attendance))

    # execute the SQL query to insert the attendance data into the database
    mycursor.execute("INSERT INTO attandance (course_id, present_no, sem, division) VALUES (%s, %s, %s, %s)", (selected_subject, attendance_str, selected_sem, selected_div))

    # commit the changes to the database
    mydb.commit()

    # show a message box to confirm that attendance has been saved
    messagebox.showinfo("Success", "Attendance has been saved.")


def show_student(event):
    selected_sem = semchoose.get()
    selected_div = divchoose.get()
    print(selected_sem)
    print(selected_div)
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT `stu_div_info`.`enroll_no`, `stu_div_info`.`stu_roll_no`, `stu_info`.`name` FROM `stu_div_info`, `stu_info` WHERE `stu_div_info`.`enroll_no` = `stu_info`.`enroll_no` AND `stu_div_info`.`stu_div`='{selected_div}' AND `stu_div_info`.`stu_sem`={selected_sem}")
    myresult = mycursor.fetchall()
    srno=1
    attendance=[]
    global attendanceframe
    
   
    if attendanceframe is not None and attendanceframe.winfo_exists():
        for widget in attendanceframe.winfo_children():
            widget.destroy()
        attendanceframe.destroy()

    attendanceframe = Frame(mainframe, borderwidth=10, bg='AliceBlue')
    attendanceframe.pack(side='top', fill='none')

    attendanceframe.pack(side='top', fill='none')
    Label(attendanceframe, text="Sr. No.", background='AliceBlue', font=("Times New Roman",15)).grid(row=0, column=0, padx=5, pady=10)
    Label(attendanceframe, text="Name", background='AliceBlue', font=("Times New Roman",15)).grid(row=0, column=1, padx=5, pady=10)
    Label(attendanceframe, text="Enroll No.", background='AliceBlue', font=("Times New Roman",15)).grid(row=0, column=2, padx=5, pady=10)
    Label(attendanceframe, text="Roll No.", background='AliceBlue', font=("Times New Roman",15)).grid(row=0, column=3, padx=5, pady=10)
    Label(attendanceframe, text="Present", background='AliceBlue', font=("Times New Roman",15)).grid(row=0, column=4, padx=5, pady=10)

    for x in myresult:
        print(x)
        Label(attendanceframe, text=f"{srno}", background='AliceBlue', font=("Times New Roman",15)).grid(row=srno, column=0, padx=5, pady=5)
        Label(attendanceframe, text=f"{x[2]}", background='AliceBlue', font=("Times New Roman",15)).grid(row=srno, column=1, padx=5, pady=5)
        Label(attendanceframe, text=f"{x[0]}", background='AliceBlue', font=("Times New Roman",15)).grid(row=srno, column=2, padx=5, pady=5)
        Label(attendanceframe, text=f"{x[1]}", background='AliceBlue', font=("Times New Roman",15)).grid(row=srno, column=3, padx=5, pady=5)
        attendace_var = BooleanVar()
        def update_attendance(roll_no, state):
            if state == 1 and roll_no not in attendance:
                attendance.append(roll_no)
            elif state == 0 and roll_no in attendance:
                attendance.remove(roll_no)
        Checkbutton(attendanceframe, variable=attendace_var, background='AliceBlue', font=("Times New Roman",15), command=lambda state=attendace_var, roll_no=x[1]: update_attendance(roll_no, state.get())).grid(row=srno, column=4, padx=0, pady=0)
        srno+=1
    Button(attendanceframe,text="Submit",command=lambda: saveattendance(attendance),width=50).grid(row=srno, column=2, padx=0, pady=0,columnspan=4)


    
root = Tk()
root.geometry('800x800')
root.title('Attendance System')

mainframe = Frame(root, borderwidth=10, bg='AliceBlue', relief='groove')
mainframe.pack(side='top', fill='both', expand=True)

topframe = Frame(mainframe, borderwidth=10, bg='AliceBlue')
topframe.pack(side='top', fill='both')
# topframe.pack_forget()
Label(topframe, text="Attendance System", font='arial 25 bold', bg='AliceBlue', pady=1).pack()

middleframe = Frame(mainframe, borderwidth=10, bg='AliceBlue')
middleframe.pack(side='top', fill='none')

# style = ttk.Style()
# style.theme_use('clam')
# style.configure('TCombobox', fieldbackground='white', background='AliceBlue', focuscolor='AliceBlue')
# style.configure('TLabel', background='AliceBlue', focuscolor='AliceBlue')


    


ttk.Label(middleframe, text="Select Semester:", background='AliceBlue', font=("Times New Roman",15)).grid(row=0, column=0, padx=5, pady=10)
semchoose = ttk.Combobox(middleframe, width=27,state='readonly')
mycursor = mydb.cursor()
mycursor.execute(f"SELECT * FROM `stu_div_info` GROUP BY `stu_sem`")
myresult = mycursor.fetchall()
sem=[]
for x in myresult:
    print(x)
    sem.append(x[3])
semchoose['values'] =sem
semchoose.grid(row=1, column=0, padx=5, pady=10)
semchoose.current(0)
semchoose.bind("<<ComboboxSelected>>",sub_select)

selected_subject = StringVar()
ttk.Label(middleframe, text="Select Subject:", background='AliceBlue', font=("Times New Roman",15)).grid(row=0, column=1, padx=5, pady=10)
subchoose = ttk.Combobox(middleframe, width=27, textvariable=selected_subject,state='readonly')
subchoose.grid(row=1, column=1, padx=5, pady=10)
subchoose.bind("<<ComboboxSelected>>",division_show)

selected_division = StringVar()
ttk.Label(middleframe, text="Select Division:", background='AliceBlue', font=("Times New Roman",15)).grid(row=0, column=2, padx=5, pady=10)
divchoose = ttk.Combobox(middleframe, width=27, textvariable=selected_division,state='readonly')
divchoose.grid(row=1, column=2, padx=5, pady=10)
divchoose.bind("<<ComboboxSelected>>",show_student)

root.mainloop()
