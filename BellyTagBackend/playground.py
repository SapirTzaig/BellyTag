
import boto3

def create_table(table_name, partition_key, sort_key=None, region='us-east-2'):
    dynamodb = boto3.resource('dynamodb', region_name=region)

    key_schema = [{'AttributeName': partition_key, 'KeyType': 'HASH'}]
    attribute_definitions = [{'AttributeName': partition_key, 'AttributeType': 'S'}]  # Default type as 'S'

    if sort_key:
        key_schema.append({'AttributeName': sort_key, 'KeyType': 'RANGE'})
        attribute_definitions.append({'AttributeName': sort_key, 'AttributeType': 'S'})  # Default type as 'S'

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    print(f"Creating table '{table_name}'...")
    table.wait_until_exists()
    print(f"Table '{table_name}' is now active!")

    return table


if __name__ == "__main__":
    create_table('Prenatal_Tests', 'u_id')