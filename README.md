# to_do

In this application I have used celery to send the emails to the users on a particular time, if their tasks are due by 2days or any number of day depends upon query.

To start the Celery Worker run the Command:-
    
    celery -A todo worker --loglevel=info --pool=solo


To start the Celery Beat run the command:-
    
    celery -A todo beat --loglevel=info
