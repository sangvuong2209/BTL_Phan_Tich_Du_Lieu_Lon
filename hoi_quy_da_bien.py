from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import pickle
from sklearn.decomposition import PCA
from sklearn.preprocessing import PolynomialFeatures



#Đọc dữ liệu, giữ lại các cột của các thuộc tính định lượng
data=pd.read_csv('train4.csv', usecols=['Item_Weight', 'Item_Visibility', 'Item_MRP', 'Item_Outlet_Sales'])


#Chia dữ liệu ra làm phần dữ liệu phụ thuộc và phẩn dữ liệu độc lập
x=data[['Item_MRP', 'Item_Weight', 'Item_Visibility']]
y=data[['Item_Outlet_Sales']]


# Tạo các trường đa thức
poly = PolynomialFeatures(degree=2) #Bậc 2 
X_poly = poly.fit_transform(x) 



# Tạo PCA để trích chọn thuộc tính
pca = PCA(n_components=2)
x_pca = pca.fit_transform(x)


#Chia bộ dữ liệu ra, lấy 80% dữ liệu làm bộ train, 20% còn lại để làm bộ test
X_train, X_test, y_train, y_test = train_test_split(x_pca, y, test_size=0.2, random_state=42)



#Tạo mô hình hồi quy tuyến tính
model=LinearRegression()
#Fit dữ liệu cho mô hình tập huấn
model.fit(X_train, y_train)



#Lưu mô hình lại
with open('linear_regression_model.pkl', 'wb') as file:
    pickle.dump(model, file)


#Dự đoán trên bộ dữ liệu test
y_predict=model.predict(X_test)



#In ra chỉ số
print(pd.DataFrame([[mean_squared_error(y_test, y_predict), r2_score(y_test, y_predict)]], columns=['MSE', 'R2'], index=['Chỉ số']))





