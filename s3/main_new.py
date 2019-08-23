import s3operations

print(s3operations.get_bucket_acl("sravani-poc-project-bucket-new"))
s3operations.putBucketACL("sravani-poc-project-bucket-new")
print(s3operations.get_bucket_acl("sravani-poc-project-bucket-new"))
s3operations.list_files("sravani-poc-project-bucket-new")

s3operations.setBucketPolicy("sravani-poc-project-bucket-new")