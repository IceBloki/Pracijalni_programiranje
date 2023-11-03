import tkinter as tk
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from db.dbManager import User, Admin, db_engine


Session = sessionmaker(bind=db_engine)
session = Session()


root = tk.Tk()
root.geometry("1000x500+300+100")
root.title("Smart Key")
root.grid_columnconfigure(0, weight=1)



class Window:
    def __init__(self):
        self.initial_frame = tk.Frame(root)
        self.btn_admin_panel = tk.Button(self.initial_frame, text="Admin panel", command=self.open_admin_panel)
        self.btn_ring = tk.Button(self.initial_frame, text="Ring", width=20, height=10, borderwidth=20, command=self.ring).grid(row=2, column=0)
        self.btn_open = tk.Button(self.initial_frame, text="Open", width=20, height=10, borderwidth=20, command=self.open_unlock_panel).grid(row=2, column=1)
        self.message_text = tk.Label(self.initial_frame, text="The bell has been activated. Someone will come soon and open the door")

        self.initial_frame.grid(row=0, column=0)
       
        self.btn_admin_panel.grid(row=1, column=0)

    def ring(self):
        self.message_text.grid(row=25, column=0, columnspan=25, rowspan=25)


    def open_admin_panel(self):
        self.initial_frame.grid_forget()
        admin_window.admin_panel.grid()

    def open_unlock_panel(self):
        self.initial_frame.grid_forget()
        unlock_window.unlock_panel.grid()
        
class AdminWindow:
    def __init__(self):

        self.checkbox_var_activ = tk.BooleanVar()
        self.checkbox_var_admin = tk.BooleanVar()
        self.admin_panel = tk.Frame(root)
        self.admin_label = tk.Label(self.admin_panel, text="This is the admin panel view")
        self.btn_back = tk.Button(self.admin_panel, text="Back", command=self.back)
        self.db_list = tk.Listbox(self.admin_panel, width=30, height=23)
        for item in Admin.get_users():
            self.db_list.insert(tk.END, f"{item.id}: {item.name} {item.surname} ")
        self.e_name_label = tk.Label(self.admin_panel, text="Name")
        self.e_surname_label = tk.Label(self.admin_panel, text="Surname")
        self.e_pin_label = tk.Label(self.admin_panel, text="PIN(4 digits)")
        self.e_activity_label = tk.Label(self.admin_panel, text="Active")
        self.e_admin_label = tk.Label(self.admin_panel, text="Admin")
        self.e_name = tk.Entry(self.admin_panel)
        self.e_surname = tk.Entry(self.admin_panel)
        self.e_pin = tk.Entry(self.admin_panel)
        self.e_activity = tk.Checkbutton(self.admin_panel, variable=self.checkbox_var_activ)
        self.e_admin = tk.Checkbutton(self.admin_panel, variable=self.checkbox_var_admin)
        self.btn_save = tk.Button(self.admin_panel, text="Save", command=self.save)
        self.btn_delete = tk.Button(self.admin_panel, text="Delete", command=self.delete)
        self.btn_update = tk.Button(self.admin_panel, text="Update", command=self.update)


        self.admin_label.grid(row=0, column=0)
        self.db_list.grid(row=1, column=0, columnspan=10, rowspan=10, sticky='w')
        self.e_name_label.grid(row=1, column=11, columnspan=2)
        self.e_surname_label.grid(row=2, column=11, columnspan=2)
        self.e_pin_label.grid(row=3, column=11, columnspan=2)
        self.e_activity_label.grid(row=4, column=11, columnspan=2)
        self.e_admin_label.grid(row=5, column=11, columnspan=2)
        self.e_name.grid(row=1, column=13, columnspan=3)
        self.e_surname.grid(row=2, column=13, columnspan=3)
        self.e_pin.grid(row=3, column=13, columnspan=3)
        self.e_activity.grid(row=4, column=13, columnspan=3)
        self.e_admin.grid(row=5, column=13, columnspan=3)
        self.btn_save.grid(row=6, column=11, columnspan=2)
        self.btn_delete.grid(row=6, column=13, columnspan=2)
        self.btn_back.grid(row=6, column=15, columnspan=2)
        self.btn_update.grid(row=6, column=18, columnspan=2)

    def back(self):
        self.admin_panel.grid_forget()
        window.initial_frame.grid()


    def save(self):
        self.db_list.delete(0, tk.END)
        Admin.add_user()
        for item in Admin.get_users():
            self.db_list.insert(tk.END, f"{item.id}: {item.name} {item.surname} ")

    def delete(self):
        selected_index = self.db_list.curselection()
        if selected_index:
            selected_value = self.db_list.get(selected_index)
            self.db_list.delete(selected_index)
            user_id = int(selected_value.split(':')[0])
            Admin.delete_user(user_id)

    def update(self):
        selected_index = self.db_list.curselection()
        if selected_index:
            selected_value = self.db_list.get(selected_index)
            user_id = int(selected_value.split(':')[0])
            self.db_list.delete(0, tk.END)
            Admin.update_user(user_id)
            for item in Admin.get_users():
                self.db_list.insert(tk.END, f"{item.id}: {item.name} {item.surname} ")

        

class UnlockWindow:
    
    def __init__(self):
      

        self.unlock_panel = tk.Frame(root)
        self.label = tk.Label(self.unlock_panel, text="PIN panel")
        self.input_box_1 = tk.Entry(self.unlock_panel, width=5, borderwidth=5)
        self.input_box_2 = tk.Entry(self.unlock_panel, width=5, borderwidth=5)
        self.input_box_3 = tk.Entry(self.unlock_panel, width=5, borderwidth=5)
        self.input_box_4 = tk.Entry(self.unlock_panel, width=5, borderwidth=5)
        self.btn_back = tk.Button(self.unlock_panel, text="Back", width=10, height=5, command=self.back)
        self.btn_0 = tk.Button(self.unlock_panel, text=str(0), width=10, height=5, command=lambda: self.btn_click(str(0)))
        self.btn_1 = tk.Button(self.unlock_panel, text=str(1), width=10, height=5, command=lambda: self.btn_click(str(1)))
        self.btn_2 = tk.Button(self.unlock_panel, text=str(2), width=10, height=5, command=lambda: self.btn_click(str(2)))
        self.btn_3 = tk.Button(self.unlock_panel, text=str(3), width=10, height=5, command=lambda: self.btn_click(str(3)))
        self.btn_4 = tk.Button(self.unlock_panel, text=str(4), width=10, height=5, command=lambda: self.btn_click(str(4)))
        self.btn_5 = tk.Button(self.unlock_panel, text=str(5), width=10, height=5, command=lambda: self.btn_click(str(5)))
        self.btn_6 = tk.Button(self.unlock_panel, text=str(6), width=10, height=5, command=lambda: self.btn_click(str(6)))
        self.btn_7 = tk.Button(self.unlock_panel, text=str(7), width=10, height=5, command=lambda: self.btn_click(str(7)))
        self.btn_8 = tk.Button(self.unlock_panel, text=str(8), width=10, height=5, command=lambda: self.btn_click(str(8)))
        self.btn_9 = tk.Button(self.unlock_panel, text=str(9), width=10, height=5, command=lambda: self.btn_click(str(9)))
        self.btn_clear = tk.Button(self.unlock_panel, text="C", width=10, height=5, command=self.clear)
        self.btn_enter = tk.Button(self.unlock_panel, text="Enter", width=10, height=10, command=self.enter)
        self.message_box = tk.Text(self.unlock_panel, width=30, height=23)
    	

        self.label.grid(row=0, column=0)
        self.input_box_1.grid(row=1, column=0, sticky='w', columnspan=1)
        self.input_box_2.grid(row=1, column=0, sticky='e', columnspan=1)
        self.input_box_3.grid(row=1, column=1, sticky='w', columnspan=1)
        self.input_box_4.grid(row=1, column=1, sticky='e', columnspan=1)
        self.btn_back.grid(row=5, column=0)
        self.btn_0.grid(row=5, column=1)
        self.btn_1.grid(row=2, column=0)
        self.btn_2.grid(row=2, column=1)
        self.btn_3.grid(row=2, column=2)
        self.btn_4.grid(row=3, column=0)
        self.btn_5.grid(row=3, column=1)
        self.btn_6.grid(row=3, column=2)
        self.btn_7.grid(row=4, column=0)
        self.btn_8.grid(row=4, column=1)
        self.btn_9.grid(row=4, column=2)
        self.btn_clear.grid(row=5, column=2)
        self.btn_enter.grid(row=4, column=4, rowspan=2, sticky="s")
        self.message_box.grid(row=1, column=5, columnspan=10, rowspan=10, sticky="e")
        

    def back(self):
        unlock_window.unlock_panel.grid_forget()
        window.initial_frame.grid() 


    def btn_click(self,number):
        for entry in [self.input_box_1, self.input_box_2, self.input_box_3, self.input_box_4]:
            if not entry.get():
                entry.insert(0, str(number))
                break

    def clear(self):
        for entry in [self.input_box_4, self.input_box_3, self.input_box_2, self.input_box_1]:
            if entry.get():
                entry.delete(0)
                break
    
    def open_admin_panel(self):
        self.unlock_panel.grid_forget()
        admin_window.admin_panel.grid()


    def enter(self):
        pin_to_check = ""
        for entry in [self.input_box_1, self.input_box_2, self.input_box_3, self.input_box_4]:
            pin_to_check += str(entry.get())
        if Admin.compare_pin(pin_to_check) and User.is_admin == False and User.is_activ:
            self.message_box.insert("1.0","Doors are open. Thank you")
        elif Admin.compare_pin(pin_to_check) and User.is_admin and User.is_activ:
            self.open_admin_panel()
        else:
            self.message_box.insert("1.0","You shall not pass")
            

window = Window()
admin_window = AdminWindow()
unlock_window = UnlockWindow()

def play():
    window.initial_frame.grid()
    root.mainloop()
