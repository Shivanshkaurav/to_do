# to_do

To start the Celery Worker run the Command:-
    
    celery -A todo worker --loglevel=info --pool=solo


To start the Celery Beat run the command:-
    
    celery -A todo beat --loglevel=info
