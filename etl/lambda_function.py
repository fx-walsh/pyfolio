import json
from utils import create_min_max_date
import datetime

def lambda_handler(event, context):
    # TODO implement
    
    current_date = datetime.datetime.today()
    
    print('the most recent invocation')
    
    date_range = create_min_max_date(current_date=current_date)
    
    print('something')
    print('---------------------------')
    print(event)
    print('---------------------------')
    print(context)
    print('---------------------------')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda2dfdf!'),
        'min_date': str(date_range[0]),
        'max_date': str(date_range[1])
    }
