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

The `c4.4xlarge` Spot Pricing seems to be cheaper overall versus DigitalOcean. Most likely because of the discount and per-minute billing. 

I'm only download/upload, so the `t3.nano` works for now. But this is sort of in preparation for #69 as well (even though AWS is not- self-hosted).

## AWS Performance for HLS Conversion via FFMPEG

I spent a few hours going through difference instance types and their FFMPEG performance. The test results are only for 5 minute video and I cancel FFMPEG after a few minutes or so.

I did switch to Docker Images as that was a lot quicker to install docker, then run these images:

- https://github.com/tnk4on/yt-dlp
- https://github.com/Sierra1011/backblaze-b2

If you have your CDN on AWS CloudFront this could be pretty cost effective. If you use a different CDN (CloudFlare, BunnyCDN, KeyCDN, etc.) then you'll get wrecked by $0.09/GB egress charges [AWS](https://aws.amazon.com/ec2/pricing/on-demand/) (after first 100 GB). The big 3 charge the same rate.

Because of the enormous egress charges, it's probably cheaper to use the provider's CDN or upload directly to the CDN. I may end up just having everything in DigitalOcean/Linode/Vultr or something...

`FFMPEG Rate` - The actual rate
`Price` - Spot Instance Pricing as of 7/30/2022
`Cost Server` - The Spot Instance's cost for the video


| CPU | Memory | Type        | FFMPEG Rate | Price  | Per Minute | Video Length | Minutes Taken | Cost Server |
| --- | ------ | ----------- | ----------- | ------ | ---------- | ------------ | ------------- | ----------- |
| 36  | 60     | c4.8xlarge  | 1.38        | 0.5449 | 0.0091     | 90.00        | 65.22         | 0.592283    |
| 36  | 72     | c5.9xlarge  | 3.10        | 0.6739 | 0.0112     | 90.00        | 29.03         | 0.326081    |
| 8   | 15     | c4.2xlarge  | 0.95        | 0.1825 | 0.0030     | 90.00        | 94.74         | 0.288158    |
| 4   | 7.5    | c4.xlarge   | 0.46        | 0.0694 | 0.0012     | 90.00        | 195.65        | 0.226304    |
| 2   | 8      | m5.large    | 0.25        | 0.0362 | 0.0006     | 90.00        | 360.00        | 0.217200    |
| 16  | 30     | c4.4xlarge  | 1.75        | 0.2486 | 0.0041     | 90.00        | 51.43         | 0.213086    |
| 8   | 32     | t3a.2xlarge | 0.66        | 0.0902 | 0.0015     | 90.00        | 136.36        | 0.205000    |
| 16  | 32     | c5.4xlarge  | 2.20        | 0.2641 | 0.0044     | 90.00        | 40.91         | 0.180068    |
| 2   | 3.75   | c4.large    | 0.26        | 0.0308 | 0.0005     | 90.00        | 346.00        | 0.177613    |
| 2   | 4      | c5.large    | 0.30        | 0.0354 | 0.0006     | 90.00        | 300.00        | 0.177000    |
| 8   | 32     | t3.2xlarge  | 0.85        | 0.0998 | 0.0017     | 90.00        | 105.88        | 0.176118    |
| 4   | 16     | t3.xlarge   | 0.45        | 0.0499 | 0.0008     | 90.00        | 200.00        | 0.166333    |
| 2   | 8      | t3.large    | 0.25        | 0.0265 | 0.0004     | 90.00        | 360.00        | 0.159000    |
| 2   | 4      | t3.medium   | 0.24        | 0.0125 | 0.0002     | 90.00        | 375.00        | 0.078125    |
