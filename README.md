# delivery fee-API

Requirements to run: Docker & Docker Compose.

To start API: ```docker-compose up --build```  

To run tests:
First ```docker exec -it wolt_task_app_container sh``` 
and then run ```python -m pytest ./app/tests/test_main.py```
in container. 
