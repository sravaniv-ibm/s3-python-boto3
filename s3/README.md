########################################################################

############## S3 Operations #########################################

#######################################################################

Steps before Executing the Main Python Code:

1. Create .aws Folder in the Home Directory: mkdir ~/.aws

2. Create a credentials File in the ~/.aws/credential with the Following Content:
[default]
aws_access_key_id = <VALUE>
aws_secret_access_key = <VALUE>

3. Create a config File in the ~/.aws/config with the Following Content:
[default]
region = <REGION_NAME>
