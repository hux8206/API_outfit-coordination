from sklearn import tree
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OrdinalEncoder
from sklearn.multioutput import MultiOutputClassifier
import joblib


df = pd.read_csv('dataset.csv', encoding='latin-1')

inputs = ['mau_da','mua','gioi_tinh','hoan_canh','phong_cach']
outputs = ['ao_trong','ao_khoac','quan']

content = df[inputs]
label = df[outputs]

encoder_cont = OrdinalEncoder()
encoder_label = OrdinalEncoder()

content_enc = encoder_cont.fit_transform(content) #fit : la doc toan bo data va hoc nhung data da duoc chuyen sang so, transform : dich chu sang so cua input tu fit de dich
label_enc = encoder_label.fit_transform(label)

content_train, content_test, label_train, label_test = train_test_split(content_enc, label_enc, test_size = 0.2, random_state = 42)

model = MultiOutputClassifier(tree.DecisionTreeClassifier(class_weight='balanced',ccp_alpha=0.01))
model.fit(content_train, label_train)

label_pre = model.predict(content_test)
for i, col in enumerate(outputs):
    acc = accuracy_score(label_test[:,i], label_pre[:,i])
    print(round(acc*100,2))

#luu model
joblib.dump(model,'model.pkl')
joblib.dump(encoder_cont,'encoder_cont.pkl')
joblib.dump(encoder_label,'encoder_label.pkl')
print('da luu model !') 