import boto3
import botocore.config
import json
from datetime import datetime

def generate_blog_using_bedrock(blogtopic:str):
    print('Generating blog')
    prompt = f'''<|begin_of_text|><|start_header_id|>user<|end_header_id|>
            Write a 200 word blog post about {blogtopic}. 
            Write only the blog post text. No code, no explanations, no markdown, just plain prose.
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>'''

    body = {
            'prompt':prompt,
            'max_gen_len':512,
            'temperature':0.5,
            'top_p':0.9
        }


    try:
        bedrock_client = boto3.client('bedrock-runtime',
                                      region_name='us-east-1',
                                      config=botocore.config.Config(read_timeout=300,retries={'max_attempts':3})
        )
        response = bedrock_client.invoke_model(body=json.dumps(body), modelId='meta.llama3-8b-instruct-v1:0')
        response_content = response.get('body').read()
        response_data = json.loads(response_content)
        print(f'Response from bedrock = {response_data}')
        blog_details = response_data['generation']
        return blog_details
    except Exception as e:
        print(f'Error generating the blog: {e}')
        raise e
    
def save_blog_details_s3(s3_key,s3_bucket,generated_blog):
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=generated_blog)
        print('Code saved to s3')
    except Exception as e:
        print('Error in saveing blog')
        raise e

def lambda_handler(event,context):
    event = json.loads(event['body'])
    if 'blog_topic' not in event:
        return {
            'statusCode':400,
            'body':json.dumps('ERROR: Malforned json payload, please make sure it contains blog_topic as a key.')
        }
    blog_topic = event['blog_topic']
    if not blog_topic:
        return {
            'statusCode':400,
            'body':json.dumps('ERROR: Please enter a blog topic in the request body')
        }
    print(f'Rececived request to generate blog for topic={blog_topic}')
    generated_blog = generate_blog_using_bedrock(blog_topic)
    if generated_blog:
        print('Blog has been generetad')
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f'blog-output/{blog_topic}-{current_time}.txt'
        s3_bucket = 'hardysawsbedrockdemo'
        save_blog_details_s3(s3_key,s3_bucket,generated_blog)
        print('Saving glob was successful. Exit')
    else:
        print('No blog content was generated')
        return {
            'statusCode':500,
            'body':json.dumps('Blog post was not generated.')
        }

    return {
            'statusCode':200,
            'body':json.dumps({
                                'message':'Blog Generation is completed',
                                'blog_content':generated_blog
                               })
            }
