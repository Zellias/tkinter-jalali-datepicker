import tkinter as tk
from tkinter import ttk
from jdatetime import date as JalaliDate
from tkcalendar import DateEntry
from jdatetime import date as JalaliDate, GregorianToJalali
import jdatetime


class JalaliDatepicker(tk.Toplevel):
    def __init__(self, master, target_entry):
        super().__init__(master)
        self.target_entry = target_entry
        self.title("Jalali Datepicker")
        self.geometry("600x320")

        self.selected_date = JalaliDate.today()

        self.min_year = 1300
        self.max_year = 1500

        self.create_widgets()

    def create_widgets(self):
        self.date_label = ttk.Label(self, text="")
        self.date_label.pack(pady=10)

        self.month_year_frame = ttk.Frame(self)
        self.month_year_frame.pack()

        self.month_var = tk.StringVar(self)
        self.month_dropdown = ttk.Combobox(
            self.month_year_frame, textvariable=self.month_var)
        self.month_dropdown['values'] = ('فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
                                         'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند')
        self.month_dropdown.set(self.selected_date.strftime("%B"))
        self.month_dropdown.bind("<<ComboboxSelected>>", self.update_month)
        self.month_dropdown.grid(row=0, column=0, padx=5, pady=5)

        self.year_var = tk.StringVar(self)
        self.year_dropdown = ttk.Combobox(
            self.month_year_frame, textvariable=self.year_var)
        self.year_dropdown['values'] = list(
            range(self.min_year, self.max_year + 1))
        self.year_dropdown.set(self.selected_date.year)
        self.year_dropdown.bind("<<ComboboxSelected>>", self.update_year)
        self.year_dropdown.grid(row=0, column=1, padx=5, pady=5)

        self.calendar_frame = ttk.Frame(self)
        self.calendar_frame.pack()

        self.create_calendar()

        self.update_display()

    def create_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        day_names = ["ش", "ی", "د", "س", "چ", "پ", "ج"]
        for i, day_name in enumerate(day_names):
            label = ttk.Label(self.calendar_frame, text=day_name)
            label.grid(row=0, column=i, padx=5, pady=5)

        year = self.selected_date.year
        month = self.selected_date.month

        if month == 12:
            num_days = 30 if self.is_leap_year(year+1) else 29
        else:
            num_days = (JalaliDate(year, month + 1, 1) -
                        JalaliDate(year, month, 1)).days

        self.date_label.config(text=self.selected_date.strftime("%d %B %Y"))

        first_day = JalaliDate(year, month, 1).weekday()

        for day in range(1, num_days + 1):
            row = (first_day + day - 1) // 7 + 1
            col = (first_day + day - 1) % 7
            button = ttk.Button(self.calendar_frame, text=str(
                day), command=lambda d=day: self.select_date(d))
            button.grid(row=row, column=col, padx=5, pady=5)

    def update_display(self):
        self.date_label.config(text=self.selected_date.strftime("%d %B %Y"))
        self.month_dropdown.set(self.selected_date.strftime("%B"))
        self.year_dropdown.set(self.selected_date.year)
        self.create_calendar()

    def update_month(self, event):
        selected_month = self.month_var.get()
        month_index = self.month_dropdown['values'].index(selected_month) + 1
        self.selected_date = JalaliDate(
            self.selected_date.year, month_index, 1)
        if month_index == 12:
            self.create_calendar()
        self.update_display()

    def update_year(self, event):
        selected_year = int(self.year_var.get())
        self.selected_date = JalaliDate(
            selected_year, self.selected_date.month, self.selected_date.day)
        self.update_display()

    def select_date(self, day):
        self.selected_date = JalaliDate(
            self.selected_date.year, self.selected_date.month, day)
        self.target_entry.delete(0, tk.END)
        self.target_entry.insert(0, self.selected_date.strftime("%Y-%m-%d"))

        self.destroy()

    def is_leap_year(self, year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('300x300')
    entry = ttk.Entry(root)
    entry.pack(pady=10)

    def open_datepicker():
        datepicker = JalaliDatepicker(root, entry)
        datepicker.grab_set()

    def convert_to_gregorian():
        jalali_date = entry.get()
        try:
            jalali_parts = jalali_date.split('-')
            jalali_year = int(jalali_parts[0])
            jalali_month = int(jalali_parts[1])
            jalali_day = int(jalali_parts[2])

            gregorian_date = JalaliDate(
                jalali_year, jalali_month, jalali_day).togregorian()

            result_label.config(
                text=f"میلادی: {gregorian_date.strftime('%Y-%m-%d')}")
        except Exception as e:
            result_label.config(text="خطا در تبدیل به میلادی")






    button = ttk.Button(root, text="بازکردن تقویم", command=open_datepicker)
    result_label_gregorian = ttk.Label(root, text="")
    result_label_gregorian.pack()
    button.pack()
    root.mainloop()
