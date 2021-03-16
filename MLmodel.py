import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix

from imblearn.over_sampling import RandomOverSampler

df_top100_category1_pivoted=pd.read_csv('ByCategory1top100_pivoted.csv')
df_top100_category1_pivoted

a=df_top100_category1_pivoted.columns[1:]
df=df_top100_category1_pivoted.groupby('h3_loc')[a].sum()

X=df.drop(['Bubble Tea'],axis=1).iloc[:,1:]
y=df['Bubble Tea']

#Creating categories st if more than 4, then categorized as 4
def ymap(y):
    if y==0:
        m=0
    elif y==1:
        m=1
    elif y==2:
        m=2
    elif y==3:
        m=3
    else:
        m=4
    return m

y1=y.apply(ymap)

plt.scatter(y,y1)
print(y1.value_counts())
print(X.shape,y.shape)

X_train, X_test, y_train, y_test = train_test_split(X,y1,test_size=.2,random_state=15)

y_train.sort_index()
y_test.sort_index()

#model for oversampling data
OS = RandomOverSampler(sampling_strategy='auto', random_state=0)
Xos, yos = OS.fit_sample(X, y1)
print(yos.value_counts())

X_train, X_test, y_train, y_test = train_test_split(Xos,yos,test_size=.2,random_state=21)

#Fitting Random Forest Classifier model
classifier_OS = RandomForestClassifier(n_estimators=50,criterion='entropy',max_depth=10,random_state=10)
pipe_SC_RFCOS=Pipeline([('RFM',classifier_OS)])
pipe_SC_RFCOS.fit(X_train,y_train)

#Training data estimation
y_pred_train=pipe_SC_RFCOS.predict(X_train)
cm1=confusion_matrix(y_train,y_pred_train)
sns.heatmap(cm1,annot=True)
print(classification_report(y_train,y_pred_train))
print(cm1)

#Test data prediction
y_predict=pipe_SC_RFCOS.predict(X_test)
cm=confusion_matrix(y_test,y_predict)
sns.heatmap(cm,annot=True)
print(classification_report(y_test,y_predict))

compare_train=pd.concat([pd.Series(y_predict),y_test.reset_index(drop=True)],axis=1)
compare_train.index=y_test.index
compare_train.columns=['y_predict','y_test']
false_pos=compare_train[(compare_train['y_test']==0)&((compare_train['y_predict']!=0))]
false_pos

#finding h3 location of false positives
h3_falsepos=[]
for i in false_pos.index:
    h3_falsepos.append(df.reset_index().loc[i]['h3_loc'])
h3_falsepos

#Finding lat long of false positives
falsepos_latlong=[]
for i in map(int,h3_falsepos):
    falsepos_latlong.append([df_hexcenters.loc[i][1],df_hexcenters.loc[i][2]])
falsepos_latlong

categ_rel_to=[]
for i in h3_falsepos:
    for j in df.loc[i][df.loc[882.0]>0].index.values:
        categ_rel_to.append(j)

categ_rel_to=[]
for i in h3_falsepos:
    for j in df.loc[i][df.loc[882.0]>0].index.values:
        categ_rel_to.append(j)

print(set(categ_rel_to))
