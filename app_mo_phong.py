import tkinter as tk
from tkinter import ttk, messagebox



class layout:
    def __init__(self):
        self.root=tk.Tk()
        tk.Label(self.root, text='Dự báo doanh thu thực phẩm', font=(14)).grid(column=0, row=0, columnspan=4, padx=20, pady=20)

        tk.Label(self.root, text='Khối lượng').grid(column=0, row=1, padx=20, pady=20)
        tk.Label(self.root, text='Chất béo').grid(column=0, row=2, padx=20, pady=20)
        tk.Label(self.root, text='Độ nổi bật').grid(column=0, row=3, padx=20, pady=20)
        tk.Label(self.root, text='Loại thực phẩm').grid(column=0, row=4, padx=20, pady=20)
        tk.Label(self.root, text='Giá cao nhất có thể bán ra').grid(column=0, row=5, padx=20, pady=20)
        tk.Label(self.root, text='Năm thành lập điểm bán').grid(column=2, row=1, padx=20, pady=20)
        tk.Label(self.root, text='Kích thước điểm bán').grid(column=2, row=2, padx=20, pady=20)
        tk.Label(self.root, text='Cấp độ điểm bán').grid(column=2, row=3, padx=20, pady=20)
        tk.Label(self.root, text='Loại điểm bán').grid(column=2, row=4, padx=20, pady=20)
        # tk.Label(self.root, text='').grid(column=2, row=5, padx=20, pady=20)

        self.weight=tk.Entry(self.root, width=20)
        self.weight.grid(row=1, column=1)

        self.visibility=tk.Entry(self.root, width=20)
        self.visibility.grid(row=3, column=1)

        self.fat=ttk.Combobox(self.root, state="readonly", value=['Regular', 'Low Fat'])
        self.fat.set('Regular')
        self.fat.grid(row=2, column=1)

        self.type=ttk.Combobox(self.root, state="readonly", value=['Soft Drinks', 'Snack Foods', 'SeaFood', ' Others', 'Meat', 'Household', 'Health and Hygiene', 'Hard Drinks', 'Fruits and Vegetables', 'Froxen Food', 'Dairy', 'Canned', 'Breakfast', 'Breads', 'Baking Goods', 'Starchy Foods'])
        self.type.set('Soft Drinks')
        self.type.grid(row=4, column=1)

        self.mrp=tk.Entry(self.root, width=20)
        self.mrp.grid(row=5, column=1)

        self.year=tk.Entry(self.root, width=20)
        self.year.grid(row=1, column=3)

        self.size=ttk.Combobox(self.root, state="readonly", value=['Small', 'High', 'Medium'])
        self.size.set('Small')
        self.size.grid(row=2, column=3, padx=20)

        self.location=ttk.Combobox(self.root, state="readonly", value=['Tier 1', 'Tier 2', 'Tier 3'])
        self.location.set('Tier 1')
        self.location.grid(row=3, column=3)

        self.type=ttk.Combobox(self.root, state="readonly", value=['Supermarket Type 1', 'Supermarket Type 2', 'Supermarket Type 3', 'Grocery Store'])
        self.type.set('Supermarket Type 1')
        self.type.grid(row=4, column=3)

        tk.Label(self.root, text='Doanh thu dự báo', font=('9')).grid(row=6, column=0, columnspan=2, pady=30, sticky='e', padx=10)

        self.sale=tk.Text(self.root, width=20, height=1.3, font=(10))
        self.sale.grid(row=6, column=2, columnspan=2, sticky='w', padx=10)

        self.predictt=tk.Button(self.root, text='Nhập', width=15, height=3, font='9', bd=5, command=self.predict)
        self.predictt.grid(row=7, column=0, columnspan=4, padx=20, pady=10)

        
    def check(self):
        if self.weight.get().strip()=='' or self.year.get().strip()=='' or self.visibility.get().strip()=='' or self.mrp.get().strip()=='':
            messagebox.showerror('Thông báo', 'Cần điền đủ thông tin!')
            return False
        return True



    def predict(self):
        import pickle
        import pandas as pd
        with open('linear_regression_model.pkl', 'rb') as file:
            if not self.check():
                return
            loaded_model = pickle.load(file)
            predictions = loaded_model.predict(pd.DataFrame([int(self.mrp.get())]))
            self.sale.delete('1.0', tk.END)
            self.sale.insert('1.0', "{:.2f} $".format(predictions[0][0]))



if __name__=="__main__":
    gui=layout()
    gui.root.mainloop()
    