#This project is made by YousefHUT (Yusuf Eren HUT) and if you want to use this project, you dont need to give credit to me. You can use it freely. 
import pathlib
import tkinter as tk
import pygubu
import time
import json

__version__ = '1.0.0'

PROJECT_PATH = pathlib.Path(__file__).resolve().parent
PROJECT_UI = PROJECT_PATH / 'app.ui'
CLASSES_PATH = PROJECT_PATH / 'Classes'
ICON_PATH = PROJECT_PATH / 'icons'

class ClassroomApp:
    def __init__(self, master=None):
        self.selectedclass = None
        self.selecteddate = None
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
        self.numberlist.bind("<<ListboxSelect>>", self.select_student)
        self.namelist.bind("<<ListboxSelect>>", self.select_student)
        self.pointlist.bind("<<ListboxSelect>>", self.select_student)
        self.checklist.bind("<<ListboxSelect>>", self.update_attendance)
        
        # Scrollbar'ı listbox'lara bağla
        self.scrollbar = builder.get_object('scrollbarlist')
        for lb in [self.numberlist, self.namelist, self.pointlist, self.checklist]:
            lb.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.on_scroll)

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
        self.edit_student_save_button = builder.get_object('editstudentsavebutton')
        self.edit_student_save_button.config(command=self.edit_student)

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

        # Arama çubuğunu tanımla
        self.search_entry = builder.get_object('searchentry')

        # Arama butonunu ayarla
        self.search_button = builder.get_object('searchbutton')
        self.search_button.config(command=self.search_student)

        # Öğrenci ekleme butonunu ayarla
        self.add_student_button = builder.get_object('addstudentbutton')
        self.add_student_button.config(command=self.open_add_student_dialog)

        # Öğrenci düzenleme butonunu ayarla
        self.edit_student_button = builder.get_object('editstudentbutton')
        self.edit_student_button.config(command=self.open_edit_student_dialog)

        # Öğrenci silme butonunu ayarla
        self.remove_student_button = builder.get_object('removestudentbutton')
        self.remove_student_button.config(command=self.remove_student_confirm_dialog)

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


        #Butonlara icon ekle
        self.add_image = tk.PhotoImage(file=str(ICON_PATH / 'add.png'))
        self.remove_image = tk.PhotoImage(file=str(ICON_PATH / 'remove.png'))
        self.search_image = tk.PhotoImage(file=str(ICON_PATH / 'search.png'))
        self.remove_student_image = tk.PhotoImage(file=str(ICON_PATH / 'deletestudent.png'))
        self.add_student_image = tk.PhotoImage(file=str(ICON_PATH / 'addstudent.png'))
        self.edit_student_image = tk.PhotoImage(file=str(ICON_PATH / 'editstudent.png'))
        self.select_today_image = tk.PhotoImage(file=str(ICON_PATH / 'today.png'))
        self.yes_image = tk.PhotoImage(file=str(ICON_PATH / 'yes.png'))
        self.no_image = tk.PhotoImage(file=str(ICON_PATH / 'no.png'))
        self.save_icon = tk.PhotoImage(file=str(ICON_PATH / 'save.png'))
        self.quick_check_icon = tk.PhotoImage(file=str(ICON_PATH / 'quickcheck.png'))
        self.all_here_icon = tk.PhotoImage(file=str(ICON_PATH / 'allhere.png'))
        self.none_here_icon = tk.PhotoImage(file=str(ICON_PATH / 'nonehere.png'))
        self.here_icon = tk.PhotoImage(file=str(ICON_PATH / 'here.png'))
        self.not_here_icon = tk.PhotoImage(file=str(ICON_PATH / 'unhere.png'))
        self.quick_here_icon = tk.PhotoImage(file=str(ICON_PATH / 'quickhere.png'))
        self.quick_not_here_icon = tk.PhotoImage(file=str(ICON_PATH / 'quickunhere.png'))
        self.quick_next_icon = tk.PhotoImage(file=str(ICON_PATH / 'quicknext.png'))
        self.quick_previous_icon = tk.PhotoImage(file=str(ICON_PATH / 'quickback.png'))

        self.add_date_button.config(image=self.add_image)
        self.remove_date_button.config(image=self.remove_image)
        self.add_student_button.config(image=self.add_student_image)
        self.remove_student_button.config(image=self.remove_student_image)
        self.add_class_button.config(image=self.add_image)
        self.remove_class_button.config(image=self.remove_image)
        self.edit_student_button.config(image=self.edit_student_image)
        self.add_points_button.config(image=self.add_image)
        self.remove_points_button.config(image=self.remove_image)
        self.select_today_button.config(image=self.select_today_image)
        self.select_date_button.config(image=self.add_image)
        self.remove_class_confirm.config(image=self.yes_image)
        self.remove_class_unconfirm.config(image=self.no_image)
        self.remove_date_confirm.config(image=self.yes_image)
        self.remove_date_unconfirm.config(image=self.no_image)
        self.remove_student_confirm.config(image=self.yes_image)
        self.remove_student_unconfirm.config(image=self.no_image)
        self.search_button.config(image=self.search_image)
        self.edit_student_save_button.config(image=self.save_icon)
        self.quick_check_button.config(image=self.quick_check_icon)
        self.all_here_button.config(image=self.all_here_icon)
        self.none_here_button.config(image=self.none_here_icon)
        self.here_button.config(image=self.here_icon)
        self.not_here_button.config(image=self.not_here_icon)
        self.quick_here_button.config(image=self.quick_here_icon)
        self.quick_not_here_button.config(image=self.quick_not_here_icon)
        self.quick_next_button.config(image=self.quick_next_icon)
        self.quick_previous_button.config(image=self.quick_previous_icon)


    def load_data(self):
        # JSON dosyalarını yükle
        try:
            with open(CLASSES_PATH / self.selectedclass / 'namelist.json', 'r') as f:
                self.namelist_data = json.load(f)
            with open(CLASSES_PATH / self.selectedclass / 'pointlist.json', 'r') as f:
                self.pointlist_data = json.load(f)
        except FileNotFoundError:
            self.namelist_data = {}
            self.pointlist_data = {}
        try:
            with open(CLASSES_PATH / self.selectedclass / 'dates' / f'{self.selecteddate}.json', 'r') as f:
                self.checklist_data = json.load(f)    
        except:
                self.checklist_data = {}

    def save_data(self):
        # JSON dosyalarını kaydet
        if (CLASSES_PATH / self.selectedclass) != CLASSES_PATH:
            try:
                with open(CLASSES_PATH / self.selectedclass / 'namelist.json', 'w') as f:
                    json.dump(self.namelist_data, f)
                with open(CLASSES_PATH / self.selectedclass / 'pointlist.json', 'w') as f:
                    json.dump(self.pointlist_data, f)
                if self.selecteddate != None:
                    with open(CLASSES_PATH / self.selectedclass / 'dates' / f'{self.selecteddate}.json', 'w') as f:
                        json.dump(self.checklist_data, f)
            except FileNotFoundError:
                self.add_class()
                with open(CLASSES_PATH / self.selectedclass / 'namelist.json', 'w') as f:
                    json.dump(self.namelist_data, f)
                with open(CLASSES_PATH / self.selectedclass / 'pointlist.json', 'w') as f:
                    json.dump(self.pointlist_data, f)

    def on_scroll(self, *args):
        #Scrollbar'ı listbox'lara bağla
        for lb in [self.numberlist, self.namelist, self.pointlist, self.checklist]:
            lb.yview(*args)
    
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
        except FileNotFoundError:
            pass
        self.select_date_list['values'] = datelist

    def select_date(self, event=None):
        # Tarihi seç
        try:
            self.selecteddate = self.select_date_list.get()
        except:
            self.selecteddate = None
        self.load_data()
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
            for student_id in self.namelist_data.keys():
                newchecklist[student_id] = '-'
            with open(CLASSES_PATH / self.selectedclass / 'dates' / f'{self.selecteddate}.json', 'w') as f:
                json.dump(newchecklist, f)
            self.update_date_list()
            self.select_date_list.set(self.selecteddate)
            self.load_data()
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
        self.populate_listboxes()
        self.remove_date_dialog.close()

    def remove_date_cancel(self):
        # Tarih silme işlemini iptal et
        self.remove_date_dialog.close()

    def populate_listboxes(self):
        # Listbox'ları yenile
        self.numberlist.delete(0, tk.END)
        self.namelist.delete(0, tk.END)
        self.pointlist.delete(0, tk.END)
        self.checklist.delete(0, tk.END)
        for student_id in self.namelist_data.keys():
            try:
                self.numberlist.insert(tk.END, student_id)
                self.namelist.insert(tk.END, self.namelist_data[student_id])
                self.pointlist.insert(tk.END, self.pointlist_data[student_id])
            except:
                break
            try:
                self.checklist.insert(tk.END, self.checklist_data[student_id])
            except:
                self.checklist.insert(tk.END, ' ')

    def select_student(self, event=None):
        if self.selectedclass != None or self.namelist_data != {}:
            selected_index = self.namelist.curselection()
            if selected_index:
                self.selected_id = self.numberlist.get(selected_index)
                self.selected_name = self.namelist.get(selected_index)
                self.number_label.config(text=f'Öğrenci No: {self.selected_id}')
                self.name_label.config(text=f'Öğrenci Adı: {self.selected_name}')
            self.namelist.selection_clear(0, tk.END)
            self.pointlist.selection_clear(0, tk.END)

    def search_student(self):
        # Öğrenci ara
        if self.search_entry.get() != '' or self.search_entry.get() != None:
            search_text = self.search_entry.get()
            for student_id, student_name in self.namelist_data.items():
                if search_text.lower() in student_name.lower():
                    index = list(self.namelist_data.values()).index(student_name)
                    self.namelist.selection_set(index)
                    self.numberlist.selection_set(index)
                    self.pointlist.selection_set(index)
                    self.selected_id = student_id
                    self.selected_name = student_name
                    self.number_label.config(text=f'Öğrenci No: {self.selected_id}')
                    self.name_label.config(text=f'Öğrenci Adı: {self.selected_name}')
                    break

    def update_class_list(self):
        # Sınıf Listesini Güncelle
        self.classlist.delete(0, tk.END)
        classlist = []
        for class_name in CLASSES_PATH.iterdir():
            if class_name.is_dir():
                classlist.append(class_name.name)
        self.classlist['values'] = classlist

    def select_class(self, event=None):
        # Sınıf seç
        if self.classlist.get() not in self.classlist['values']:
            self.selectedclass = self.classlist['values'][0]
        else:
            self.selectedclass = self.classlist.get()
        self.update_date_list()
        self.load_data()
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
        self.update_class_list()
        self.select_class()
        self.remove_class_dialog.close()
    
    def remove_class_confirm_dialog(self):
        # Sınıf silme onay penceresini aç
        if self.selectedclass != None:
            self.remove_class_dialog.run()
    
    def remove_class_cancel(self):
        # Sınıf silme işlemini iptal et
        self.remove_class_dialog.close()
    
    def open_add_student_dialog(self, event=None):
        # Öğrenci düzenleme penceresini aç
        if self.selectedclass != None or self.selected_class != '':
            self.edit_number_entry.delete(0, tk.END)
            self.edit_name_entry.delete(0, tk.END)
            self.edit_points_entry.delete(0, tk.END)
            self.edit_points_entry.insert(tk.END, '0')
            self.edit_student_dialog.run()
    
    def open_edit_student_dialog(self, event=None):
        self.open_add_student_dialog()
        self.edit_points_entry.delete(0, tk.END)
        self.edit_number_entry.insert(tk.END, self.selected_id)
        self.edit_name_entry.insert(tk.END, self.namelist_data[self.selected_id])
        self.edit_points_entry.insert(tk.END, self.pointlist_data[self.selected_id])
        self.numberlist.selection_clear(0, tk.END)

    def edit_student(self, event=None):
        # Yeni öğrenci ekle veya öğrenci bilgilerini güncelle
        student_id = self.edit_number_entry.get()
        student_name = self.edit_name_entry.get()
        student_points = self.edit_points_entry.get()
        if student_id != '' and student_name != '':
            if student_id not in self.namelist_data:
                self.namelist_data[student_id] = student_name
                self.pointlist_data[student_id] = student_points
                self.checklist_data[student_id] = '-'
                for date in (CLASSES_PATH / self.selectedclass / 'dates').iterdir():
                    with open(CLASSES_PATH / self.selectedclass / 'dates' / date, 'r') as f:
                        newchecklist = json.load(f)
                    with open(CLASSES_PATH / self.selectedclass / 'dates' / date, 'w') as f:
                        newchecklist[student_id] = '-'
                        json.dump(newchecklist, f)
            else:
                self.namelist_data[student_id] = student_name
                self.pointlist_data[student_id] = student_points
            self.edit_student_dialog.close()
            self.save_data()
            self.load_data()
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

    def update_attendance(self, event=None):
        # Yoklama durumunu güncelle
        student_index = self.checklist.curselection()
        if student_index:
            student_id = self.numberlist.get(student_index)
            status = self.checklist_data[student_id]
            if status == '-':
                status = '+'
            else:
                status = '-'
            self.checklist_data[student_id] = status
            self.save_data()
            self.populate_listboxes()
        self.checklist.selection_clear(0, tk.END)

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
        if self.selecteddate != None or self.selecteddate != '':
            for student_id in self.namelist_data.keys():
                self.checklist_data[student_id] = '+'
            self.save_data()
            self.populate_listboxes()
    
    def none_here(self):
        # Tüm öğrencileri yoklama alınmadı yap
        if self.selecteddate != None or self.selecteddate != '':
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
    # Uygulamayı başlat
    root = tk.Tk()
    app = ClassroomApp(root)
    root.withdraw()  # Root penceresini gizle
    root.mainloop()