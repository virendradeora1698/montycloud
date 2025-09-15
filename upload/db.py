# services/db.py
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
)

# Ensure the 'images' table exists, create if not

table_name = 'images'

existing_tables = [t.name for t in dynamodb.tables.all()]
if table_name not in existing_tables:
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    # Wait for table to be created
    dynamodb.Table(table_name).wait_until_exists()

table = dynamodb.Table(table_name)

def save_image_metadata(id, user, name, image_url):
    table.put_item(Item={
        'id': id,
        'user': user,
        'name': name,
        'image_url': image_url
    })
def get_image_metadata(id):
    response = table.get_item(Key={'id': id})
    return response.get('Item')

def delete_image_metadata(id):
    table.delete_item(Key={'id': id})

def list_images_metadata(name=None, from_date=None, to_date=None):
    filter_expression = []
    expression_attribute_values = {}

    if name:
        filter_expression.append('contains(#name, :name)')
        expression_attribute_values[':name'] = name

    if from_date:
        filter_expression.append('#created_at >= :from_date')
        expression_attribute_values[':from_date'] = from_date

    if to_date:
        filter_expression.append('#created_at <= :to_date')
        expression_attribute_values[':to_date'] = to_date

    scan_kwargs = {}
    if filter_expression:
        scan_kwargs['FilterExpression'] = ' AND '.join(filter_expression)
        scan_kwargs['ExpressionAttributeValues'] = expression_attribute_values
        scan_kwargs['ExpressionAttributeNames'] = {
            '#name': 'name',
            '#created_at': 'created_at'
        }

    response = table.scan(**scan_kwargs)
    return response.get('Items', [])

def update_image_metadata(id, user=None, name=None, image_url=None):
    update_expression = []
    expression_attribute_values = {}

    if user:
        update_expression.append('#user = :user')
        expression_attribute_values[':user'] = user

    if name:
        update_expression.append('#name = :name')
        expression_attribute_values[':name'] = name

    if image_url:
        update_expression.append('#image_url = :image_url')
        expression_attribute_values[':image_url'] = image_url

    if not update_expression:
        return  # Nothing to update

    update_expr = 'SET ' + ', '.join(update_expression)

    table.update_item(
        Key={'id': id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames={
            '#user': 'user',
            '#name': 'name',
            '#image_url': 'image_url'
        }
    )

# Example usage:
# save_image_metadata('1', 'test_user', 'test_image', 'http://example.com/image.jpg')
# print(get_image_metadata('1'))
