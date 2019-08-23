import s3operations

s3operations.create_bucket("sravani-poc-project-bucket-new", "ap-south-1")
s3operations.list_bucket()

s3operations.upload_file("C:\Users\VenkataSatyaSravaniM\Desktop\StateFarm-Account\StateFarm.txt", "sravani-poc-project-bucket-new", "Sample.txt")
s3operations.download_file("sravani-poc-project-bucket-new", "Sample.txt", "C:/Users/VenkataSatyaSravaniM/Desktop/StateFarm-Account/StateFarmNew.txt")
s3operations.upload_file_multipart_transfer("C:\Users\VenkataSatyaSravaniM\Desktop\StateFarm-Account\StateFarm.txt", "sravani-poc-project-bucket-new", "SampleNew.txt")
s3operations.list_files("sravani-poc-project-bucket-new")