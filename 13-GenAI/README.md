# 13-GenAI

## Architecture

Blog generation system using AWS Bedrock (Llama 3), Lambda, S3, and API Gateway.

## Setup Steps

1. **Create S3 Bucket** for archiving blog responses
2. **Create AWS Lambda function** using Python 3.12 runtime with `app.lambda_handler` as the handler, and choose Llama 3 (`meta.llama3-8b-instruct-v1:0`) as the Bedrock model
3. **Attach IAM permissions** to the Lambda execution role — Bedrock full access (`AmazonBedrockFullAccess`) and S3 full access (`AmazonS3FullAccess`)
4. **Create API Gateway** (HTTP API) pointing to the Lambda function, expose a POST endpoint at `/generate-blog`

## Usage

Upon making an API call to this URL with this payload-

https://n4x1j6bf6j.execute-api.us-east-1.amazonaws.com/generate-blog

With this payload
{
    "blog_topic":"super bowl 2026"
}

One can expect to receive a response back liek this-

{"message": "Blog Generation is completed", "blog_content": "\n\nAs we look ahead to the 2026 Super Bowl, excitement is building for what promises to be an unforgettable event. The big game is set to take place on February 7th, 2026, at the newly renovated SoFi Stadium in Inglewood, California.\n\nThis year's championship matchup is shaping up to be a thrilling one, with the top teams in the league battling it out for the Vince Lombardi Trophy. The Kansas City Chiefs, led by quarterback Patrick Mahomes, are looking to repeat their 2020 success, while the Buffalo Bills, with their high-powered offense, are looking to make a deep playoff run.\n\nOff the field, the Super Bowl is expected to be a celebration of music, fashion, and entertainment. The halftime show is rumored to feature a star-studded lineup of performers, including pop sensation Ariana Grande and rock legend Bruce Springsteen. Meanwhile, the Super Bowl commercials are sure to be a highlight, with major brands vying for attention and ad dollars.\n\nAs the big day approaches, fans are gearing up for a weekend of football, friends, and festivities. Whether you're a die-hard football fan or just looking for a fun excuse to get together with friends, the 2026 Super Bowl is an event you won't want to miss. Mark your calendars and get ready to join the party!"}