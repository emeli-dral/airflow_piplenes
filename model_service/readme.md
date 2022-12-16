# Running FastAPI application example

1. Make sure you have python dependencies installed: fastapi, uvicorn, requests, pandas, skikit-learn
fastapi installation: https://fastapi.tiangolo.com/#installation

2. Before running the example, make sure that you have an access to the binary file with the trained ml model. The model can be generated using either airflow example_ml_model_training_dag.py or separately via python/jupyter script. We used green taxi trip records data from the https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page 

3. To run the example call the following command from the model_service folder in your terminal: ```uvicorn fastapi_app:app --reload```

4. To see the auto generated docs and test exposed endpoints go to the ```http://127.0.0.1:8000/docs``` in your browser

