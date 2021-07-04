import numpy as np
from sklearn import metrics
import LegitimateTest
import pandas as pd
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

df = pd.read_csv("dataset.csv")
df = df.dropna()

#dependent variable
Y = df['LegitimateOrNot'].values
Y = Y.astype('int')

#independent variables
X = df.drop(labels=['LegitimateOrNot'], axis =1)

#Split data into train and test datasets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.05, random_state=20)

model = RFC(n_estimators= 10, random_state=30)
model.fit(X_train, Y_train)
prediction_test = model.predict(X_test)


def randomForestChecker(url):
    Take_X  = LegitimateTest.generate_data_set(url)
    for index, number in enumerate(Take_X):
        #print(number)
        if number == 9:
            Take_X[index] = -1

    for index,item in enumerate(Take_X):
        if item == "":
            Take_X[index] = -1

    Take_X = np.array(Take_X).reshape(1,-1)

    try:
        prediction = model.predict(Take_X)
        #print("prediction : " +str(prediction))
        #Url failed the test
        if prediction == -1:
            return url + " Kriter Testinden Geçemedi!!!"
        #Url passed the test
        if prediction == 1:
            return url + " Kriter Testinde Temiz Çıktı!!!"

    except Exception as ex:
        print("Hata: " +str(ex))


"""feature_list = list(X.columns)
feature_imp = pd.Series(model.feature_importances_,index=feature_list).sort_values(ascending=False)
feature_imp.plot(kind="bar")
plt.show()"""





