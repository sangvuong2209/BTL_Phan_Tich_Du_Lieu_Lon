import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# Đọc dữ liệu từ tệp CSV
data = pd.read_csv('train.csv')

# Loại bỏ các hàng có giá trị bị thiếu trong cột Item_Weight
data_cleaned = data.dropna(subset=['Item_Weight'])

# Chia dữ liệu thành tập train và test
data_train, data_test = train_test_split(data_cleaned, test_size=0.2, random_state=42)

# Danh sách các biến độc lập và biến phụ thuộc
independent_vars = ['Item_Weight', 'Item_Visibility', 'Item_MRP', 'Outlet_Establishment_Year']
dependent_var = 'Item_Outlet_Sales'

# Hàm vẽ biểu đồ phân tán và tính toán chỉ số
def plot_scatter_with_regression(data_train, data_test, independent_var, dependent_var):
    # Chuẩn bị dữ liệu train và test
    X_train = data_train[[independent_var]]
    y_train = data_train[dependent_var]
    X_test = data_test[[independent_var]]
    y_test = data_test[dependent_var]

    # Khởi tạo mô hình hồi quy và huấn luyện
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Tính toán các chỉ số đánh giá trên tập test
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    # Vẽ biểu đồ phân tán trên tập train
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=independent_var, y=dependent_var, data=data_train, alpha=0.5, edgecolor='w')
    plt.plot(X_test, model.predict(X_test), color='red', linewidth=2, label=f'R²={r2:.2f}')
    plt.title(f'{independent_var} vs {dependent_var}')
    plt.xlabel(independent_var)
    plt.ylabel(dependent_var)
    plt.legend()
    plt.show()

    # Trả về các chỉ số đánh giá
    return {'R²': r2, 'MAE': mae, 'RMSE': rmse}

# Tính toán và hiển thị chỉ số cho từng biến
metrics = {}
for var in independent_vars:
    print(f"Plotting {var} vs {dependent_var}...")
    metrics[var] = plot_scatter_with_regression(data_train, data_test, var, dependent_var)

# Chuyển các chỉ số thành bảng và hiển thị
metrics_df = pd.DataFrame(metrics).T
metrics_df.reset_index(inplace=True)
metrics_df.columns = ['Variable', 'R²', 'MAE', 'RMSE']
print(metrics_df)
