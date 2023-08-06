# MoreModels

A python library allowing you to use multiple models using the weight of each model based on their performance

install using 
```
pip install moremodels
```

Example code:

```
from moremodels import WeightedModels

model1 = catboost.CatBoostRegressor()
model2 = RandomForestRegressor()
model3 = xgboost.XGBRegressor()

my_data = pd.read('my_data.csv')
test = pd.read('test.csv)

my_models = [model1, model2, model3]
models = WeightedModels( models = my_models, trainSplit = 0.8, randomState = 696969 )

models.fit(my_data)

print(models.modelWeights)

myPredictedData = models.predict(test)

print(models.models[0])

```