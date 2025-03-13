# This project is made by YousefHUT (Yusuf Eren HUT) and if you want to use this project, you don't need to give credit to me. You can use it freely.
import pathlib
import tkinter as tk
import pygubu
import time
import json
import random
import pandas
import auth
from tkinter import filedialog

__version__ = '1.1.0'
__author__ = 'YousefHUT'


PROJECT_PATH = pathlib.Path(__file__).resolve().parent
PROJECT_UI = PROJECT_PATH / 'app.ui'
CLASSES_PATH = PROJECT_PATH / 'Classes'
ICON_PATH = PROJECT_PATH / 'icons'

class ClassroomApp:
    def __init__(self, master=None):
        self.selectedclass = None
        self.selecteddate = None
        self.selected_id = None
        self.selected_name = None
        self.selected_students = []
        self.builder = builder = pygubu.Builder()
        self.builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainscreen = builder.get_object('mainscreen', master)
        self.mainscreen.protocol("WM_DELETE_WINDOW", self.on_closing)
        builder.connect_callbacks(self)
        
        # Listbox'ları al
        self.numberlist = builder.get_object('numberlist')
        self.namelist = builder.get_object('namelist')
        self.pointlist = builder.get_object('pointlist')
        self.checklist = builder.get_object('checklist')
        self.obligatelist = builder.get_object('obligatelist')
        for lb in [self.numberlist, self.namelist, self.pointlist, self.checklist,self.obligatelist]:
            lb.bind("<<ListboxSelect>>", self.select_student)

        # Scrollbar'ı listbox'lara bağla
        self.scrollbar = builder.get_object('scrollbarlist')
        self.scrollbar.config(command=self.on_scroll)
        for lb in [self.numberlist, self.namelist, self.pointlist, self.checklist,self.obligatelist]:
            lb.config(yscrollcommand=self.scrollbar.set)
            lb.bind("<MouseWheel>", self.on_mouse_wheel)
            lb.bind("<Button-4>", self.on_mouse_wheel)
            lb.bind("<Button-5>", self.on_mouse_wheel)

        # Tarih menüsünü düzenle
        self.add_date_button = builder.get_object('adddatebutton')
        self.add_date_button.config(command=self.add_date_dialog)
        self.remove_date_button = builder.get_object('removedatebutton')
        self.remove_date_button.config(command=self.remove_date_confirm_dialog)
        self.select_date_list = builder.get_object('selecteddate')
        self.select_date_list.bind("<<ComboboxSelected>>", self.select_date)

        #Dialog pencerelerini al
        self.remove_date_dialog = builder.get_object('removedatedialog', self.mainscreen) #Tarih silme onay penceresi

        self.select_date_dialog = builder.get_object('selectdatedialog', self.mainscreen)#Tarih seçme penceresi
        self.year_spinbox = builder.get_object('yearspinbox')
        self.month_spinbox = builder.get_object('monthspinbox')
        self.day_spinbox = builder.get_object('dayspinbox')
        self.year_spinbox_variable = tk.IntVar()
        self.month_spinbox_variable = tk.IntVar()
        self.day_spinbox_variable = tk.IntVar()
        self.year_spinbox.config(from_=2020,to=3000,textvariable=self.year_spinbox_variable)
        self.month_spinbox.config(from_=1,to=12,textvariable=self.month_spinbox_variable)
        self.day_spinbox.config(from_=1,to=31,textvariable=self.day_spinbox_variable)
        self.select_date_button = builder.get_object('selectdatebutton')
        self.select_today_button = builder.get_object('selecttodaybutton')
        self.select_date_button.config(command=self.add_date)
        self.select_today_button.config(command=self.select_today)

        self.remove_student_dialog = builder.get_object('removestudentdialog', self.mainscreen)#Öğrenci silme onay penceresi
        self.remove_student_confirm = builder.get_object('removestudentconfirm')
        self.remove_student_unconfirm = builder.get_object('removestudentunconfirm')
        self.remove_student_confirm.config(command=self.remove_student)
        self.remove_student_unconfirm.config(command=self.remove_student_cancel)

        self.remove_class_dialog = builder.get_object('removeclassdialog', self.mainscreen)#Sınıf silme onay penceresi
        self.remove_class_confirm = builder.get_object('removeclassconfirm')
        self.remove_class_unconfirm = builder.get_object('removeclassunconfirm')
        self.remove_class_confirm.config(command=self.remove_class)
        self.remove_class_unconfirm.config(command=self.remove_class_cancel)

        self.remove_date_dialog = builder.get_object('removedatedialog',self.mainscreen)#Tarih silme onay penceresi
        self.remove_date_confirm = builder.get_object('removedateconfirm')
        self.remove_date_unconfirm = builder.get_object('removedateunconfirm')
        self.remove_date_confirm.config(command=self.remove_date)
        self.remove_date_unconfirm.config(command=self.remove_date_cancel)

        self.edit_student_dialog = builder.get_object('editstudentdialog', self.mainscreen)#Öğrenci düzenleme penceresi
        self.edit_number_entry = builder.get_object('editnumberentry')
        self.edit_name_entry = builder.get_object('editnameentry')
        self.edit_points_entry = builder.get_object('editpointentry')
        self.edit_status_entry = builder.get_object('editstatusentry')
        self.edit_status_entry['values'] = ["Zorunlu","Alttan","Alttan Devamlı"]
        self.edit_student_save_button = builder.get_object('editstudentsavebutton')
        self.edit_student_save_button.config(command=self.edit_student)

        self.about_student_dialog = builder.get_object('aboutstudentdialog',self.mainscreen)#Öğrenci Bilgileri penceresi
        self.about_number = builder.get_object('aboutnumber')
        self.about_name = builder.get_object('aboutname')
        self.about_number = builder.get_object('aboutnumber')
        self.about_point = builder.get_object('aboutpoints')
        self.about_attendance = builder.get_object('abouthere')
        self.about_absence = builder.get_object('aboutunhere')
        self.about_attendance_list = builder.get_object('aboutherelist')
        self.about_absence_list = builder.get_object('aboutunherelist')

        self.quick_check_dialog = builder.get_object('quickcheckdialog', self.mainscreen)#Hızlı yoklama penceresi
        self.quick_check_button = builder.get_object('quickcheckbutton')
        self.quick_check_button.config(command=self.open_quick_check_dialog)
        self.quick_number_label = builder.get_object('quicknumber')
        self.quick_name_label = builder.get_object('quickname')
        self.quick_here_button = builder.get_object('herebutton')
        self.quick_not_here_button = builder.get_object('notherebutton')
        self.quick_next_button = builder.get_object('nextbutton')
        self.quick_next_button.config(command=self.quick_next)
        self.quick_previous_button = builder.get_object('gobackbutton')
        self.quick_previous_button.config(command=self.quick_previous)
        self.quick_here_button.config(command=self.quick_here)
        self.quick_not_here_button.config(command=self.quick_not_here)


        # Tablo verilerini tanımla
        self.namelist_data = {}
        self.pointlist_data = {}
        self.checklist_data = {}

        # Sınıfları yükle
        self.classlist = builder.get_object('classnamebox')
        self.classlist.bind("<<ComboboxSelected>>", self.select_class)
        self.update_class_list()

        # Sınıf ekleme butonunu ayarla
        self.add_class_button = builder.get_object('addclassbutton')
        self.add_class_button.config(command=self.add_class)

        # Sınıf silme butonunu ayarla
        self.remove_class_button = builder.get_object('removeclassbutton')
        self.remove_class_button.config(command=self.remove_class_confirm_dialog)

        # Arama menüsünü tanımla ve filtreleme seçeneklerini göster
        self.search_entry = builder.get_object('searchentry')
        self.search_entry.bind("<<ComboboxSelected>>", self.filterlist)
        self.search_entry.bind('<Return>', self.filterlist)
        self.search_button = builder.get_object('searchbutton')
        self.search_button.config(command=self.filterlist)
        self.search_entry['values'] = ["Hepsi"]

        # Öğrenci ekleme butonunu ayarla
        self.add_student_button = builder.get_object('addstudentbutton')
        self.add_student_button.config(command=self.open_add_student_dialog)

        # Öğrenci düzenleme butonunu ayarla
        self.edit_student_button = builder.get_object('editstudentbutton')
        self.edit_student_button.config(command=self.open_edit_student_dialog)

        # Öğrenci silme butonunu ayarla
        self.remove_student_button = builder.get_object('removestudentbutton')
        self.remove_student_button.config(command=self.remove_student_confirm_dialog)

        # Öğrenci bilgileri butonunu ayarla
        self.about_student_button = builder.get_object('aboutstudentbutton')
        self.about_student_button.config(command=self.open_student_info_dialog)

        # Seçili öğrenci bilgilerini tanımla
        self.number_label = builder.get_object('numberlabel')
        self.name_label = builder.get_object('namelabel')

        #Puan butonlatını ayarla
        self.add_points_button = builder.get_object('addpointsbutton')
        self.add_points_button.config(command=self.add_points)
        self.remove_points_button = builder.get_object('removepointsbutton')
        self.remove_points_button.config(command=self.remove_points)

        #Yoklama butonlarını tanımla
        self.here_button = builder.get_object('here')
        self.here_button.config(command=self.here_selected)
        self.not_here_button = builder.get_object('unhere')
        self.not_here_button.config(command=self.not_here_selected)
        self.all_here_button = builder.get_object('allherebutton')
        self.all_here_button.config(command=self.all_here)
        self.none_here_button = builder.get_object('noneherebutton')
        self.none_here_button.config(command=self.none_here)

        #Rastgele öğrenci seçme butonunu tanımla
        self.random_button = builder.get_object('randomstudentbutton')
        self.random_button.config(command=self.random_select)

        #Sayaçları tanımla
        self.student_counter = builder.get_object('studentcounter')
        self.student_here_counter = builder.get_object('studentherecounter')
        self.student_unhere_counter = builder.get_object('studentunherecounter')
        self.list_counter = builder.get_object('listcounter')
        self.list_here_counter = builder.get_object('listherecounter')
        self.list_unhere_counter = builder.get_object('listunherecounter')
        self.date_counter = builder.get_object('datecounter')
        self.attendance_counter = builder.get_object('classattendanceratecounter')
        self.populate_listboxes()


        #Butonlara icon ekle
        self.add_icon = self.load_icon('add.png')
        self.remove_icon = self.load_icon('remove.png')
        self.search_icon = self.load_icon('search.png')
        self.remove_student_icon = self.load_icon('deletestudent.png')
        self.add_student_icon = self.load_icon('addstudent.png')
        self.edit_student_icon = self.load_icon('editstudent.png')
        self.select_today_icon = self.load_icon('today.png')
        self.yes_image = self.load_icon('yes.png')
        self.no_image = self.load_icon('no.png')
        self.save_icon = self.load_icon('save.png')
        self.quick_check_icon = self.load_icon('quickcheck.png')
        self.all_here_icon = self.load_icon('allhere.png')
        self.none_here_icon = self.load_icon('nonehere.png')
        self.here_icon = self.load_icon('here.png')
        self.not_here_icon = self.load_icon('unhere.png')
        self.quick_here_icon = self.load_icon('quickhere.png')
        self.quick_not_here_icon = self.load_icon('quickunhere.png')
        self.quick_next_icon = self.load_icon('quicknext.png')
        self.quick_previous_icon = self.load_icon('quickback.png')
        self.random_icon = self.load_icon('random.png')
        self.menu_icon = self.load_icon('menu.png')
        self.import_icon = self.load_icon('import.png')
        self.export_icon = self.load_icon('export.png')
        self.student_info_icon = self.load_icon('studentinfo.png')

        if self.add_icon:
            self.add_date_button.config(image=self.add_icon)
            self.add_class_button.config(image=self.add_icon)
            self.add_points_button.config(image=self.add_icon)
        if self.remove_icon:
            self.remove_date_button.config(image=self.remove_icon)
            self.remove_student_button.config(image=self.remove_student_icon)
            self.remove_class_button.config(image=self.remove_icon)
            self.remove_points_button.config(image=self.remove_icon)
        if self.add_student_icon:
            self.add_student_button.config(image=self.add_student_icon)
        if self.edit_student_icon:
            self.edit_student_button.config(image=self.edit_student_icon)
        if self.student_info_icon:
            self.about_student_button.config(image=self.student_info_icon)
        if self.select_today_icon:
            self.select_today_button.config(image=self.select_today_icon)
        if self.save_icon:
            self.select_date_button.config(image=self.save_icon)
            self.edit_student_save_button.config(image=self.save_icon)
        if self.yes_image:
            self.remove_class_confirm.config(image=self.yes_image)
            self.remove_date_confirm.config(image=self.yes_image)
            self.remove_student_confirm.config(image=self.yes_image)
        if self.no_image:
            self.remove_class_unconfirm.config(image=self.no_image)
            self.remove_date_unconfirm.config(image=self.no_image)
            self.remove_student_unconfirm.config(image=self.no_image)
        if self.search_icon:
            self.search_button.config(image=self.search_icon)
        if self.quick_check_icon:
            self.quick_check_button.config(image=self.quick_check_icon)
        if self.all_here_icon:
            self.all_here_button.config(image=self.all_here_icon)
        if self.none_here_icon:
            self.none_here_button.config(image=self.none_here_icon)
        if self.here_icon:
            self.here_button.config(image=self.here_icon)
        if self.not_here_icon:
            self.not_here_button.config(image=self.not_here_icon)
        if self.quick_here_icon:
            self.quick_here_button.config(image=self.quick_here_icon)
        if self.quick_not_here_icon:
            self.quick_not_here_button.config(image=self.quick_not_here_icon)
        if self.quick_next_icon:
            self.quick_next_button.config(image=self.quick_next_icon)
        if self.quick_previous_icon:
            self.quick_previous_button.config(image=self.quick_previous_icon)
        if self.random_icon:
            self.random_button.config(image=self.random_icon)

        #Menü butonunu tanımla
        self.menu_button = builder.get_object('menubuton')
        if self.menu_icon:
            self.menu_button.config(image=self.menu_icon)
        self.menu_button.menu = tk.Menu(self.menu_button, tearoff=0)
        self.menu_button["menu"] = self.menu_button.menu
        self.menu_button.menu.add_command(label="Sınıf içe aktar",command=self.import_class, image=self.import_icon)
        self.menu_button.menu.add_command(label="Sınıf dışa aktar",command=self.export_class, image=self.export_icon)

    def load_icon(self, icon_name):
        icon_path = ICON_PATH / icon_name
        if icon_path.exists():
            return tk.PhotoImage(file=str(icon_path))
        else:
            print(f"Icon {icon_name} not found.")
            return None

    def load_data(self):
        # JSON dosyalarını yükle
        if self.selectedclass != None:
            try:
                with open(CLASSES_PATH / f"{self.selectedclass}" / 'namelist.json', 'r') as f:
                    self.namelist_data = json.load(f)
                with open(CLASSES_PATH / f"{self.selectedclass}" / 'pointlist.json', 'r') as f:
                    self.pointlist_data = json.load(f)
                with open(CLASSES_PATH / f"{self.selectedclass}" / 'obligatelist.json', 'r') as f:
                    self.obligatelist_data = json.load(f)
            except:
                self.namelist_data = {}
                self.pointlist_data = {}
                self.obligatelist_data ={}
            if self.selecteddate != None:
                try:
                    with open(CLASSES_PATH / self.selectedclass / 'dates' / f'{self.selecteddate}.json', 'r') as f:
                        self.checklist_data = json.load(f)    
                except:
                        self.checklist_data = {}

    def save_data(self):
        # JSON dosyalarını kaydet
        if (CLASSES_PATH / self.selectedclass) != CLASSES_PATH and self.selectedclass != None:
            with open(CLASSES_PATH / self.selectedclass / 'namelist.json', 'w') as f:
                json.dump(self.namelist_data, f)
            with open(CLASSES_PATH / self.selectedclass / 'pointlist.json', 'w') as f:
                json.dump(self.pointlist_data, f)
            with open(CLASSES_PATH / self.selectedclass / 'obligatelist.json', 'w') as f:
                json.dump(self.obligatelist_data, f)
            if self.selecteddate != None:
                with open(CLASSES_PATH / self.selectedclass / 'dates' / f'{self.selecteddate}.json', 'w') as f:
                    json.dump(self.checklist_data, f)

    def on_scroll(self, *args):
        # Scrollbar'ı listbox'lara bağla
        for lb in [self.numberlist, self.namelist, self.obligatelist, self.pointlist, self.checklist]:
            lb.yview(*args)
    
    def on_mouse_wheel(self, event):
        if event.num == 5 or event.delta == -120:
            for lb in [self.numberlist, self.namelist, self.obligatelist, self.pointlist, self.checklist]:
                lb.yview_scroll(1, "units")
        if event.num == 4 or event.delta == 120:
            for lb in [self.numberlist, self.namelist, self.obligatelist, self.pointlist, self.checklist]:
                lb.yview_scroll(-1, "units")
        return "break"
    
    def on_closing(self):
        # Program kapatılırken verileri kaydet
        self.mainscreen.destroy()
        exit()

    def update_date_list(self):
        # Tarih listesini güncelle
        self.select_date_list.delete(0, tk.END)
        datelist = []
        try:
            for date in (CLASSES_PATH / self.selectedclass / 'dates').iterdir():
                datelist.append(date.stem)
        except:
            pass
        self.select_date_list['values'] = datelist

    def select_date(self, event=None):
        # Tarihi seç
        try:
            self.selecteddate = self.select_date_list.get()
        except:
            self.selecteddate = None
        self.load_data()
        self.filterlist()
        self.populate_listboxes()

    def add_date_dialog(self, event=None):
        # Tarih seçme penceresini aç
        if self.selectedclass != None:
            self.select_date_dialog.run()

    def add_date(self):
        # Tarih ekle
        if self.selectedclass != None:
            year = self.year_spinbox.get()
            month = self.month_spinbox.get()
            day = self.day_spinbox.get()
            self.selecteddate = f'{year}-{month}-{day}'
            newchecklist = self.checklist_data
            if newchecklist != {}:
                for student_id in self.namelist_data.keys():
                    newchecklist[student_id] = '-'
            with open(CLASSES_PATH / self.selectedclass / 'dates' / f'{self.selecteddate}.json', 'w') as f:
                json.dump(newchecklist, f)
            self.update_date_list()
            self.select_date_list.set(self.selecteddate)
            self.none_here()
            self.load_data()
            self.filterlist()
            self.populate_listboxes()
            self.select_date_dialog.close()

    def select_today(self):
        # Bugünün tarihini seç
        today = time.localtime()
        year = int(today.tm_year)
        month = int(today.tm_mon)
        day = int(today.tm_mday)
        self.year_spinbox_variable.set(year)
        self.month_spinbox_variable.set(month)
        self.day_spinbox_variable.set(day)
    
    def remove_date_confirm_dialog(self):
        # Tarih silme onay penceresini aç
        if self.selectedclass != None and self.selecteddate != None:
            self.remove_date_dialog.run()
    
    def remove_date(self):
        # Tarihi sil
        try:
            (CLASSES_PATH / self.selectedclass / 'dates' / f'{self.selecteddate}.json').unlink()
        except FileNotFoundError:
            pass
        self.update_date_list()
        self.select_date_list.set('')
        self.selecteddate = ''
        self.load_data()
        self.selected_students = []
        self.filterlist()
        self.populate_listboxes()
        self.remove_date_dialog.close()

    def remove_date_cancel(self):
        # Tarih silme işlemini iptal et
        self.remove_date_dialog.close()

    def populate_listboxes(self):
        # Listbox'ları yenile
        self.update_search_list()
        self.numberlist.delete(0, tk.END)
        self.namelist.delete(0, tk.END)
        self.obligatelist.delete(0, tk.END)
        self.pointlist.delete(0, tk.END)
        self.checklist.delete(0, tk.END)
        if self.selectedclass != None:
            self.classlist.delete(0, tk.END)
            self.classlist.insert(tk.END, self.selectedclass)
            for student_id in self.selected_students:
                try:
                    self.numberlist.insert(tk.END, student_id)
                    self.namelist.insert(tk.END, self.namelist_data[student_id])
                    self.obligatelist.insert(tk.END, self.obligatelist_data[student_id])
                    self.pointlist.insert(tk.END, self.pointlist_data[student_id])
                except:
                    self.numberlist.insert(tk.END, student_id)
                    self.namelist.insert(tk.END, '?')
                    self.obligatelist.insert(tk.END, '?')
                    self.pointlist.insert(tk.END, '?')

            self.student_counter.config(text=f"Toplam Öğrenci Sayısı: {len(self.namelist_data)}")
            self.date_counter.config(text=f"İşlenmiş Ders Sayısı: {len(self.select_date_list['values'])}")
            if self.search_entry.get() != "" and self.search_entry.get() !="Hepsi":
                self.list_counter.config(text=f"Listedeki Öğrenci Sayısı: {len(self.selected_students)}")
            else:
                self.list_counter.config(text="")
                self.list_here_counter.config(text="")
                self.list_unhere_counter.config(text="")
            check = 0
            uncheck = 0
            for date in self.select_date_list['values']:
                with open(CLASSES_PATH / f"{self.selectedclass}" / 'dates' / f'{date}.json', 'r') as f:
                    checklist = json.load(f)
                for student in checklist:
                    if checklist[student] == '+':
                        check += 1
                    elif checklist[student] == '-':
                        uncheck += 1
                if (check + uncheck != 0):
                    percent = round((check / (check + uncheck) * 100))
                else:
                    percent = "0"
                self.attendance_counter.config(text=f"Derslere Katılım Oranı: %{percent}")
            if self.selecteddate != None:
                for student_id in self.selected_students:
                    try:
                        self.checklist.insert(tk.END, self.checklist_data.get(student_id, ' '))
                    except:
                        self.checklist.insert(tk.END, '?')

                check = 0
                uncheck = 0
                for student in self.checklist_data:
                    if self.checklist_data[student] == '+':
                        check += 1
                    elif self.checklist_data[student] == '-':
                        uncheck += 1
                self.student_here_counter.config(text=f"Toplam Gelen Sayısı: {check}")
                self.student_unhere_counter.config(text=f"Toplam Gelmeyen Sayısı: {uncheck}")
                if self.search_entry.get() != "" and self.search_entry.get() !="Hepsi":
                    check = 0
                    uncheck = 0
                    for student in self.selected_students:
                        if self.checklist_data[student] == '+':
                            check += 1
                        elif self.checklist_data[student] == '-':
                            uncheck += 1
                    self.list_here_counter.config(text=f"Listedeki Gelen Sayısı: {check}")
                    self.list_unhere_counter.config(text=f"Listedeki Gelmeyen Sayısı: {uncheck}")
            else:
                self.student_here_counter.config(text="")
                self.student_unhere_counter.config(text="")
                self.list_here_counter.config(text="")
                self.list_unhere_counter.config(text="")
                self.date_counter.config(text="")
                self.attendance_counter.config(text="")
        else:
            self.student_counter.config(text="")
            self.student_here_counter.config(text="")
            self.student_unhere_counter.config(text="")
            self.list_counter.config(text="")
            self.list_here_counter.config(text="")
            self.list_unhere_counter.config(text="")
            self.date_counter.config(text="")
            self.attendance_counter.config(text="")

    def filterlist(self, event=None):
        self.selected_students = []
        search = self.search_entry.get()
        if self.selectedclass !=None:
            if search == "Hepsi" or search == "":
                for student_number in self.namelist_data.keys():
                    self.selected_students.append(student_number)
                self.search_entry.delete(0, tk.END)
            elif search == "Gelen":
                if self.selecteddate != None:
                    for student_number, student_check in self.checklist_data.items():
                        if student_check == '+':
                            self.selected_students.append(student_number)
                else:
                    pass
            elif search == "Gelmeyen":
                if self.selecteddate != None:
                    for student_number, student_check in self.checklist_data.items():
                        if student_check == '-':
                            self.selected_students.append(student_number)
                else:
                    pass
            elif search == "Zorunlu":
                for student_number, status in self.obligatelist_data.items():
                    if status == "Zorunlu":
                        self.selected_students.append(student_number)
            elif search == "Alttan":
                for student_number, status in self.obligatelist_data.items():
                    if status == "Alttan":
                        self.selected_students.append(student_number)
            elif search == "Alttan Devamlı":
                for student_number, status in self.obligatelist_data.items():
                    if status == "Alttan Devamlı":
                        self.selected_students.append(student_number)
            else:
                self.search_student()
        self.populate_listboxes()

    def random_select(self,event=None):
        #Listeden rastgele öğrenci seçme
        if self.selectedclass and self.selected_students != []:
            selected_id = random.choice(self.selected_students)
            self.selected_id = selected_id
            self.selected_name = self.namelist_data[selected_id]
            self.number_label.config(text=f'Öğrenci No: {self.selected_id}')
            self.name_label.config(text=f'Öğrenci Adı: {self.selected_name}')

    def select_student(self, event=None):
        #Listede tıklanan öğrenciyi seçme
        if self.selectedclass != None or self.namelist_data != {}:
            selected_index = self.namelist.curselection()
            if selected_index:
                self.selected_id = self.numberlist.get(selected_index)
                self.selected_name = self.namelist.get(selected_index)
                self.number_label.config(text=f'Öğrenci No: {self.selected_id}')
                self.name_label.config(text=f'Öğrenci Adı: {self.selected_name}')
            self.namelist.selection_clear(0, tk.END)
            self.pointlist.selection_clear(0, tk.END)
            self.obligatelist.selection_clear(0, tk.END)

    def update_search_list(self):
        #Öğrenci filtreleme seçeneklerini güncelle
        values = []
        if self.selectedclass != None:
            values.append("Hepsi")
            for status in set(self.obligatelist_data.values()):
                values.append(status)
            if self.selecteddate != None:
                values.append("Gelen")
                values.append("Gelmeyen")
            self.search_entry['values'] = values

    def search_student(self):
        # Öğrenci ara
        if self.search_entry.get() != '' or self.search_entry.get() != None:
            search_text = self.search_entry.get()
            for student_id, student_name in self.namelist_data.items():
                if search_text.lower() in student_name.lower() or search_text in student_id:
                    self.selected_students.append(student_id)

    def update_class_list(self):
        # Sınıf Listesini Güncelle
        classlist = []
        for class_name in CLASSES_PATH.iterdir():
            if class_name.is_dir():
                classlist.append(class_name.name)
        self.classlist['values'] = classlist

    def select_class(self, event=None):
        # Sınıf seç
        if self.classlist.get() in self.classlist['values']:
            self.selectedclass = self.classlist.get()
        elif self.classlist['values']:
            self.selectedclass = self.classlist['values'][0]
        else:
            self.selectedclass = None
        self.load_data()
        self.update_date_list()
        self.selected_students = []
        self.update_search_list()
        self.filterlist()
        self.populate_listboxes()

    def add_class(self):
        # Yeni sınıf ekle
        if self.classlist.get() != '' or self.classlist.get() != None:
            class_path = CLASSES_PATH / self.classlist.get()
            if not class_path.exists():
                class_path.mkdir(parents=True, exist_ok=True)
                (class_path / 'dates').mkdir(exist_ok=True)
                with open(class_path / 'namelist.json', 'w') as f:
                    json.dump({}, f)
                with open(class_path / 'pointlist.json', 'w') as f:
                    json.dump({}, f)
                with open(class_path / 'obligatelist.json', 'w') as f:
                    json.dump({}, f)
                self.update_class_list()
                self.select_class()
                self.load_data()
                self.populate_listboxes()
    
    def remove_class(self):
        # Sınıfı sil
        class_path = PROJECT_PATH / 'Classes' / self.selectedclass
        date_path = class_path / 'dates'
        if date_path.exists():
            for item in date_path.glob('*'):
                try:
                    item.unlink()
                except:
                    pass
            date_path.rmdir()
        if class_path.exists():
            for item in class_path.glob('*'):
                try:
                    item.unlink()
                except:
                    pass
            class_path.rmdir()
        self.selectedclass = None
        self.selecteddate = None
        self.selected_students = []
        self.classlist.delete(0, tk.END)
        self.filterlist()
        self.update_class_list()
        self.update_date_list()
        self.remove_class_dialog.close()
    
    def remove_class_confirm_dialog(self):
        # Sınıf silme onay penceresini aç
        if self.selectedclass != None:
            self.remove_class_dialog.run()
    
    def remove_class_cancel(self):
        # Sınıf silme işlemini iptal et
        self.remove_class_dialog.close()

    def export_class(self):
        if self.selectedclass:
            output_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Exel Tablosu","*.xlsx"),
                                                        ("Yazı dosyası", "*.txt"),
                                                        ("Tüm dosyalar", "*.*")])
            if output_path != ():
                directory = CLASSES_PATH / self.selectedclass

                with open(directory / 'namelist.json', 'r', encoding='utf-8') as f:
                    namelist = json.load(f)

                with open(directory / 'obligatelist.json', 'r', encoding='utf-8') as f:
                    obligatelist = json.load(f)

                with open(directory / 'pointlist.json', 'r', encoding='utf-8') as f:
                    pointlist = json.load(f)

                date_files = list((directory/"dates").glob('*.json'))
                if output_path.endswith(".xlsx"):
                    data = []
                    for key in namelist:
                        student_data = {
                            "Numara": key,
                            "Ad/Soyad": namelist[key],
                            "Öğrenci durumu": obligatelist[key],
                            "Puan": pointlist[key]
                        }
                        for date_file in date_files:
                            with open(date_file, 'r', encoding='utf-8') as f:
                                date_data = json.load(f)
                                date_str = date_file.stem
                                student_data[date_str] = date_data.get(key, "")
                        data.append(student_data)
                    df = pandas.DataFrame(data)
                    df.to_excel(output_path, index=False)
                else:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        for student_id, student_name in namelist.items():
                            f.write(f"{student_id},{student_name},{obligatelist[student_id]},{pointlist[student_id]}\n")

    def import_class(self,event=None):
        # Exel dosyasından yada text dosyasından sınıf import etme
        file_path = filedialog.askopenfilename(defaultextension="*.*",
                                             filetypes=[("Exel Tablosu","*.xlsx"),
                                                        ("Yazı dosyası", "*.txt"),
                                                        ("Tüm dosyalar", "*.*")])
        if file_path != ():
            namelist = {}
            obligatelist = {}
            pointlist = {}
            class_path = CLASSES_PATH / pathlib.Path(file_path).stem
            class_path.mkdir(parents=True, exist_ok=True)
            dates_path = class_path / "dates"
            dates_path.mkdir()
            if file_path.endswith(".xlsx"):
                table = pandas.read_excel(file_path)
                namelist = table.set_index('Numara')['Ad/Soyad'].to_dict()
                obligatelist = table.set_index('Numara')['Öğrenci durumu'].to_dict()
                pointlist = table.set_index('Numara')['Puan'].to_dict()
                date_columns = [col for col in table.columns if col not in ['Numara', 'Ad/Soyad', 'Öğrenci durumu', 'Puan']]
                date_data = {date: table.set_index('Numara')[date].to_dict() for date in date_columns}
                for date, data in date_data.items():
                    with open(dates_path / f'{date}.json', 'w') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
            else:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        student_data = line.strip().split(',')
                        if len(student_data) >= 3:
                            student_id, student_name = student_data[:2]
                            student_points = '0'
                            student_status = student_data[2].split('/')[0]
                            if len(student_data) == 4:
                                student_points = student_data[3]
                            namelist[student_id] = student_name
                            obligatelist[student_id] = student_status
                            pointlist[student_id] = student_points
            with open(class_path / 'namelist.json', 'w') as f:
                json.dump(namelist, f, ensure_ascii=False, indent=4)

            with open(class_path / 'obligatelist.json', 'w') as f:
                json.dump(obligatelist, f, ensure_ascii=False, indent=4)

            with open(class_path / 'pointlist.json', 'w') as f:
                json.dump(pointlist, f, ensure_ascii=False, indent=4)
            self.update_class_list()

    def open_add_student_dialog(self, event=None):
        # Öğrenci düzenleme penceresini aç
        if self.selectedclass != None:
            self.edit_number_entry.delete(0, tk.END)
            self.edit_name_entry.delete(0, tk.END)
            self.edit_status_entry.delete(0, tk.END)
            self.edit_points_entry.delete(0, tk.END)
            self.edit_points_entry.insert(tk.END, '0')
            self.edit_student_dialog.run()
    
    def open_edit_student_dialog(self, event=None):
        if self.selected_id != None:
            self.open_add_student_dialog()
            self.edit_points_entry.delete(0, tk.END)
            self.edit_number_entry.insert(tk.END, self.selected_id)
            self.edit_name_entry.insert(tk.END, self.namelist_data[self.selected_id])
            self.edit_status_entry.insert(tk.END, self.obligatelist_data[self.selected_id])
            self.edit_points_entry.insert(tk.END, self.pointlist_data[self.selected_id])
            self.numberlist.selection_clear(0, tk.END)

    def edit_student(self, event=None):
        # Yeni öğrenci ekle veya öğrenci bilgilerini güncelle
        student_id = self.edit_number_entry.get()
        student_name = self.edit_name_entry.get()
        student_statue = self.edit_status_entry.get()
        student_points = self.edit_points_entry.get()
        if student_id != '' and student_name != '':
            self.namelist_data[student_id] = student_name
            self.obligatelist_data[student_id] = student_statue
            self.pointlist_data[student_id] = student_points
            self.checklist_data[student_id] = '-'
            if student_id not in self.namelist_data.keys():
                for date in (CLASSES_PATH / self.selectedclass / 'dates').iterdir():
                    with open(CLASSES_PATH / self.selectedclass / 'dates' / date, 'r') as f:            
                        newchecklist = json.load(f)
                    newchecklist[student_id] = '-'
                    with open(CLASSES_PATH / self.selectedclass / 'dates' / date, 'w') as f:
                        json.dump(newchecklist, f)
            self.edit_student_dialog.close()
            self.save_data()
            self.load_data()
            self.filterlist()
            self.populate_listboxes()

    def remove_student_confirm_dialog(self, event=None):
        # Öğrenci silme onay penceresini aç
        if self.selectedclass != None or self.selected_id != None:
            self.remove_student_dialog.run()

    def remove_student(self, event=None):
        # Öğrenciyi sil
        if self.selectedclass != None:
            student_id = self.selected_id
            if student_id in self.namelist_data:
                del self.namelist_data[student_id]
                del self.obligatelist_data[student_id]
                del self.pointlist_data[student_id]
                for date in (CLASSES_PATH / self.selectedclass / 'dates').iterdir():
                    try:
                        with open(CLASSES_PATH / self.selectedclass / 'dates' / date, 'r') as f:
                            newchecklist = json.load(f)
                            del newchecklist[student_id]
                        with open(CLASSES_PATH / self.selectedclass / 'dates' / date, 'w') as f:
                            json.dump(newchecklist, f)
                    except:
                        pass
                self.filterlist()
                self.save_data()
                self.populate_listboxes()
                self.edit_student_dialog.close()
                self.selected_id = None
                self.number_label.config(text='Öğrenci No:')
                self.name_label.config(text='Öğrenci Adı:')
                self.remove_student_dialog.close()
    
    def remove_student_cancel(self):
        # Öğrenci silme işlemini iptal et
        self.remove_student_dialog.close()
    
    def open_student_info_dialog(self, event=None):
        if self.selected_id:
            self.about_number.config(text=f"Öğrenci Numarası: {self.selected_id}")
            self.about_name.config(text=f"Öğrenci Adı: {self.selected_name}")
            self.about_point.config(text=f"Puan: {self.pointlist_data.get(self.selected_id, '0')}")
            self.about_attendance_list.delete(0, tk.END)
            self.about_absence_list.delete(0, tk.END)
            check = 0
            uncheck = 0
            for date in self.select_date_list['values']:
                with open(CLASSES_PATH / f"{self.selectedclass}" / 'dates' / f'{date}.json', 'r') as f:
                    checklist = json.load(f)
                if checklist[self.selected_id] == '+':
                    self.about_attendance_list.insert(tk.END, date)
                    check += 1
                elif checklist[self.selected_id] == '-':
                    self.about_absence_list.insert(tk.END, date)
                    uncheck += 1
            self.about_attendance.config(text=f"Derse Katılım Sayısı: {check}")
            self.about_absence.config(text=f"Devamsızlık: {uncheck}")   
            self.about_student_dialog.run()

    def open_quick_check_dialog(self):
        # Hızlı yoklama alma penceresini aç
        if self.selecteddate == None or self.selecteddate == '':
            pass
        else:
            self.selected_id = self.numberlist.get(0)
            self.selected_name = self.namelist.get(0)
            self.quick_number_label.config(text=f'Öğrenci No: {self.selected_id}')
            self.quick_name_label.config(text=f'Öğrenci Adı: {self.selected_name}')
            self.quick_check_dialog.run()

    def quick_next(self):
        # Sonraki öğrenciye geç
        try:
            index = list(self.namelist_data.keys()).index(self.selected_id)
            self.selected_id = list(self.namelist_data.keys())[index + 1]
            self.selected_name = self.namelist_data[self.selected_id]
            self.quick_number_label.config(text=f'Öğrenci No: {self.selected_id}')
            self.quick_name_label.config(text=f'Öğrenci Adı: {self.selected_name}')
        except:
            self.quick_check_dialog.close()

    def quick_previous(self):
        # Önceki öğrenciye geç
        try:
            index = list(self.namelist_data.keys()).index(self.selected_id)
            self.selected_id = list(self.namelist_data.keys())[index - 1]
            self.selected_name = self.namelist_data[self.selected_id]
        except:
            self.selected_id = self.numberlist.get(0)
            self.selected_name = self.namelist.get(0)
        self.quick_number_label.config(text=f'Öğrenci No: {self.selected_id}')
        self.quick_name_label.config(text=f'Öğrenci Adı: {self.selected_name}')
    
    def quick_here(self):
        # Öğrenciyi yoklama alındı yap
        self.checklist_data[self.selected_id] = '+'
        self.save_data()
        self.populate_listboxes()
        self.quick_next()

    def quick_not_here(self):
        # Öğrenciyi yoklama alınmadı yap
        self.checklist_data[self.selected_id] = '-'
        self.save_data()
        self.populate_listboxes()
        self.quick_next()

    def all_here(self):
        # Tüm öğrencileri yoklama alındı yap
        if self.selectedclass and self.selecteddate:
            for student_id in self.namelist_data.keys():
                self.checklist_data[student_id] = '+'
            self.save_data()
            self.populate_listboxes()
    
    def none_here(self):
        # Tüm öğrencileri yoklama alınmadı yap
        if self.selectedclass and self.selecteddate:
            for student_id in self.namelist_data.keys():
                self.checklist_data[student_id] = '-'
            self.save_data()
            self.populate_listboxes()

    def here_selected(self):
        # Seçili öğrenciyi yoklama alındı yap
        if self.selected_id != None:
            try:
                self.checklist_data[self.selected_id] = '+'
                self.save_data()
                self.populate_listboxes()
            except:
                self.checklist_data[self.selected_id] = '-'
    
    def not_here_selected(self):
        # Seçili öğrenciyi yoklama alınmadı yap
        if self.selected_id != None:
            try:
                self.checklist_data[self.selected_id] = '-'
                self.save_data()
                self.populate_listboxes()
            except:
                self.checklist_data[self.selected_id] = '-'

    def add_points(self):
        # Öğrenciye artı ver
        if self.selected_id != None:
            try:
                self.pointlist_data[self.selected_id] = str(int(self.pointlist_data[self.selected_id]) + 1)
                self.save_data()
                self.populate_listboxes()
            except:
                self.pointlist_data[self.selected_id] = '0'
    
    def remove_points(self):
        # Öğrenciden puan sil
        if self.selected_id != None:
            try:
                self.pointlist_data[self.selected_id] = str(int(self.pointlist_data[self.selected_id]) - 1)
                self.save_data()
                self.populate_listboxes()
            except:
                self.pointlist_data[self.selected_id] = '0'

if __name__ == '__main__':
    if auth.open_login_window():
        # Uygulamayı başlat
        root = tk.Tk()
        root.withdraw()
        app = ClassroomApp(root)
        root.mainloop()