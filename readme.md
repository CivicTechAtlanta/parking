# Marta Parking API

## Installation
```
pip install -r requirements.txt
```

## Configuration
There is no need to modify the config.py file unless you wish to push the json object to S3. 

If you want to push to S3, set the `push_to_s3` value to True and also set the rest of the values. (NOTE: I have not
tested this recently and may have a bug or two in it)

## Running
```
python parking.py
```

#### Tested on Python 2.7 - I imagine it will run on Python 3 as well (no promises :) )
