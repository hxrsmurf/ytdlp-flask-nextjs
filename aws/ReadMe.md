## About
This creates a CloudFormation template using [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html).

Using Lambda with yt-dlp and ffmpeg was not a great time. While I did add `ffmpeg` layer, I think yt-dlp expects actual `ffmpeg` to exist and it spits out an error. Too much of a hassle to custom build something, for now.

SAM creates:
- Lambda Function
- API Gateway

The Lambda function is open right now. I'll implement an IP restriction soon.

## Flow
1. Function parses query parameters and looks for `id`
2. Executes the `convert_user_data` function to generate user data with the result of `id`
3. Executes the `run_ec2`, requests Spot Instance
4. Spot Instance uses the user data
   - Installs software
   - Downloads video
   - Uploads to BackBlaze


## Why AWS?

While I wanted to go with DigitalOcean, they charge by the hour. I'm more familiar with AWS and AWS has `Spot Instances` which offer a deep discount. 

The `c4.4xlarge` Spot Pricing seems to be cheapr overall versus DigitalOcean. Most likely because of the discount and per-minute billing. 

I'm only download/upload, so the `t3.nano` works for now. But this is sort of in preparation for #69 as well (even though AWS is not- self-hosted).
