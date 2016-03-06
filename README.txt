Written and tested on:
    Python 2.7.6
    PyTest 2.9.0


To run this application:
    1. Open schedule.py and follow example included
    2. Change data if needed
    3. Run 'python schedule.py' from current directory


To run unit tests:
    1. run 'pip install -r requirements.txt'
       or 'pip install pytest==2.9.0'
    2. run 'py.test tests.py'


Assumptions:
    * There is no preference for event order
    * No need for optimization of 'waiting time' between events and breaks
    * The networking event will start immideately after last event has ended, if the last event ended within its time-span to minimize waiting time
    * No preference on filling Tracks