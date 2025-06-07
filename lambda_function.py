import boto3
import pandas as pd
import io
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extract bucket name and file name from the event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Destination bucket (set via environment variable)
    destination_bucket = os.environ['DEST_BUCKET']
    output_file_key = f"cleaned/{object_key.split('/')[-1].replace('.csv', '_cleaned.csv')}"
    
    try:
        # Step 1: Read raw CSV from S3
        response = s3.get_object(Bucket=source_bucket, Key=object_key)
        raw_data = response['Body'].read()
        df = pd.read_csv(io.BytesIO(raw_data))

        # Step 2: Data Cleaning
        df = df.dropna(subset=['EmpID', 'Salary', 'PhoneNumber'])  # Remove incomplete records
        df = df[df['Salary'].apply(lambda x: str(x).isdigit())]
        df = df[df['PhoneNumber'].apply(lambda x: str(x).isdigit() and len(str(x)) >= 10)]

        df['Salary'] = df['Salary'].astype(float)

        # Step 3: Group by Dept
        grouped_df = df.groupby('Dept').agg(
            EmployeeCount=('EmpID', 'count'),
            AverageSalary=('Salary', 'mean')
        ).reset_index()

        # Step 4: Convert result to CSV
        csv_buffer = io.StringIO()
        grouped_df.to_csv(csv_buffer, index=False)

        # Step 5: Upload cleaned CSV to destination S3
        s3.put_object(
            Bucket=destination_bucket,
            Key=output_file_key,
            Body=csv_buffer.getvalue().encode('utf-8')
        )

        print(f"ETL succeeded. Cleaned file uploaded to: s3://{destination_bucket}/{output_file_key}")

    except Exception as e:
        print(f"ETL Failed: {str(e)}")
        raise
