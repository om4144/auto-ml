from typing import List, Annotated, Literal

from pydantic import BaseModel, Field


class ModelResult(BaseModel):
  algo: Annotated[str, Field(
    ..., 
    title= "Alogrithm name",
    description= "Name of the alogorithem",
    examples= ["Random Forest", "Linear Regression", "Logistic Regression"]
  )]

  train_time_sec: Annotated[float, Field(
    ..., 
    title= "Training Time",
    description= "Time taken by algo in training",
    examples= [5.6455, 34.547567, 1000.56]
  )]

  metric: Annotated[str, Field(
    ...,
    title= "Metric",
    description= "Metric used to check model performence",
    examples=["mse", "r2_score", "accuracy", "f1"]
  )]

class AnalyzeResponse(BaseModel):
  task_type: Annotated[Literal["regression", "classifaction"], Field(
    ...,
    title= "Task Type",
    description= "Type of the task like regression or classifaction",
    examples=["regression", "classifaction"]
  )]

  best_model: Annotated[str, Field(
    ...,
    title= "Best model",
    description= "Best performed model on dataset",
    examples= ["Linear Regression", "Logistic Regression", "Random Forest"],
  )]
  
  results: Annotated[List[ModelResult], Field(
    ..., 
    title= "Result",
    description= "Result of all algorithmes on the dataset",
    examples= [
      {
        "algo": "Linear Regression",
        "train_time_sec": 1000.348,
        "metric": "r2_score"
      },
      {
        "algo": "Random Forest",
        "train_time_sec": 987.56,
        "metric": "accuracy"
      },
    ]
  )]