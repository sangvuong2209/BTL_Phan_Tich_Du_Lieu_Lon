# Import các thư viện cần thiết
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dữ liệu
file_path = 'train.csv'
df = pd.read_csv(file_path)

df.to_csv('new_file.csv', index=False)


print("Tóm lược dữ liệu:\n")
print(df.info())
print("\nGiá trị thiếu:\n", df.isnull().sum())  # Đếm số lượng giá trị thiếu ở mỗi cột
print("\nThống kê mô tả:\n", df.describe())  # Tóm tắt thống kê dữ liệu dạng số
# Xử lý dữ liệu thiếu cho từng cột
for column in df.columns:
    if df[column].isnull().sum() > 0:
        if df[column].dtype == 'object':  # Nếu cột là kiểu chuỗi
            # Điền giá trị phổ biến nhất (mode)
            df[column].fillna(df[column].mode()[0], inplace=True)
        else:  # Nếu cột là kiểu số (numerical)
            # Điền giá trị trung bình (mean)
            df[column].fillna(df[column].mean(), inplace=True)

if 'Outlet_Establishment_Year' in df.columns:
    df['Outlet_Age'] = 2024 - df['Outlet_Establishment_Year']

if 'Item_Outlet_Sales' in df.columns:
    df['Sales_Category'] = pd.cut(
        df['Item_Outlet_Sales'],
        bins=[-np.inf, 1000, 3000, np.inf],
        labels=['Low', 'Medium', 'High']
    )

 # Chuẩn hóa văn bản: viết thường và xóa khoảng trắng thừa
    for column in df.select_dtypes(include=['object']):
        df[column] = df[column].str.lower().str.strip()

    # Đồng bộ hóa giá trị trong cột Item_Fat_Content
    if 'Item_Fat_Content' in df.columns:
        df['Item_Fat_Content'] = df['Item_Fat_Content'].replace({
            'low fat': 'low fat',
            'lf': 'low fat',
            'reg': 'regular'
        })

## Chuẩn hóa dữ liệu
df['Item_Visibility_Normalized'] = (
    df['Item_Visibility'] - df['Item_Visibility'].min()
) / (df['Item_Visibility'].max() - df['Item_Visibility'].min())

df['Item_MRP_Normalized'] = (
    df['Item_MRP'] - df['Item_MRP'].min()
) / (df['Item_MRP'].max() - df['Item_MRP'].min())


# Loại bỏ hàng trùng lặp
df = df.drop_duplicates()

# Loại bỏ cột có trên 50% giá trị bị thiếu
df = df.dropna(axis=1, thresh=df.shape[0] * 0.5)

# Loại bỏ hàng có trên 50% giá trị bị thiếu
df = df.dropna(axis=0, thresh=df.shape[1] * 0.5)


# Biểu đồ 1: Histogram của Item_Outlet_Sales (Doanh thu theo thực phẩm)
plt.figure(figsize=(10, 6))
plt.hist(df['Item_Outlet_Sales'], bins=30, color='skyblue', edgecolor='black')
plt.title('Phân phối Doanh thu Bán lẻ', fontsize=16)
plt.xlabel('Doanh thu (Item_Outlet_Sales)', fontsize=12)
plt.ylabel('Tần suất', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Biểu đồ 2: Boxplot của Item_Outlet_Sales theo Outlet_Type
plt.figure(figsize=(10, 6))
sns.boxplot(x='Outlet_Type', y='Item_Outlet_Sales', data=df, palette='Set2')
plt.title('Doanh thu theo Loại Cửa hàng', fontsize=16)
plt.xlabel('Loại Cửa hàng', fontsize=12)
plt.ylabel('Doanh thu (Item_Outlet_Sales)', fontsize=12)
plt.xticks(rotation=45)
plt.show()

# Biểu đồ 3: Bar chart của Item_Type
plt.figure(figsize=(12, 8))
item_type_counts = df['Item_Type'].value_counts()
item_type_counts.plot(kind='bar', color='lightcoral', edgecolor='black')
plt.title('Số lượng Thực phẩm theo Loại', fontsize=16)
plt.xlabel('Loại Thực phẩm', fontsize=12)
plt.ylabel('Số lượng', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Biểu đồ 4: Scatter plot giữa Item_MRP và Item_Outlet_Sales
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Item_MRP', y='Item_Outlet_Sales', data=df, alpha=0.7, color='green')
plt.title('Mối quan hệ giữa Giá Thực phẩm và Doanh thu', fontsize=16)
plt.xlabel('Giá Thực phẩm (Item_MRP)', fontsize=12)
plt.ylabel('Doanh thu (Item_Outlet_Sales)', fontsize=12)
plt.grid(alpha=0.5)
plt.show()


# Biểu đồ 5: Pie chart của Outlet_Type
plt.figure(figsize=(8, 8))
outlet_type_counts = df['Outlet_Type'].value_counts()
outlet_type_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
plt.title('Tỷ lệ phần trăm Loại Cửa hàng', fontsize=16)
plt.ylabel('')
plt.show()





