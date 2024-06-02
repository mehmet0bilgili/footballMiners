import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc

data = pd.read_csv('model/dataset.csv')

#Feature Distinction According to categorical or numeric.
categorical_features = ['MatchStadium', 'Team1Formation', 'Team2Formation']
numerical_features = [col for col in data.columns if col not in categorical_features + ['Result']]

X = data.drop('Result', axis=1)
y = data['Result']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

#Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

#Random Forest Pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

#Training
model.fit(X_train, y_train)

#Prediction
y_pred = model.predict(X_test)

#Random Forest Accuracy Score
accuracy = accuracy_score(y_test, y_pred)
print("Random Forest Accuracy:", accuracy)

#Feauture Importance
rf = model.named_steps['classifier']
feature_importances = rf.feature_importances_
ohe = model.named_steps['preprocessor'].named_transformers_['cat']
ohe_feature_names = ohe.get_feature_names_out(categorical_features)

#Combining all features
all_feature_names = numerical_features + list(ohe_feature_names)

feature_importance_df = pd.DataFrame({
    'feature': all_feature_names,
    'importance': feature_importances
}).sort_values(by='importance', ascending=False)

#Feature Importance Plot
plt.figure(figsize=(30, 22))
plt.barh(feature_importance_df['feature'], feature_importance_df['importance'], color='skyblue')
plt.xlabel('Feature Importance')
plt.title('Random Forest Feature Importance')
plt.gca().invert_yaxis()
plt.show()

#Creating Confusion Matrix and Plot
conf_matrix = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix)
disp.plot()
plt.title("Random Forest Confusion Matrix")
plt.show()

#Creating Correlation Matrix and Plot
correlation_matrix = data[numerical_features].corr()
plt.figure(figsize=(18, 15))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Random Forest Correlation Matrix")
plt.show()
