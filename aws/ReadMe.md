This creates a CloudFormation template using AWS SAM.

It creates:
- Lambda Function
- API Gateway

The Lambda function is open right now. I'll implement an IP restriction soon.

Flow
1. Function parses query parameters and looks for `id`
2. Executes the `convert_user_data` function to generate user data with the result of `id`
3. Executes the `run_ec2`, requests Spot Instance
4. Spot Instance uses the user data
   - Installs software
   - Downloads video
   - Uploads to BackBlaze
