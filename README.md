# Picsearch

### Assignment 3 submission for Cloud Computing Spring 2023 course at NYU Tandon  


Team Members:
1. Chirangivi Bhat - cdb9649
2. Preetham Rakshith - pp2959


Components:
1. Frontend Application which uses AWS to upload images and search for them.
2. Two S3 buckets to store the frontend code and images respectively.
3. Lambda functions - index-photos and search-photos.
4. OpenSearch domain to search for images stored in S3 bucket.
5. AWS Rekognition call to label images automatically.
6. API Gateway to handle the PUT and GET api calls from the frontend.
7. AWS Lex to determine the photo labels from user query.
8. Code Pipelines - P1 pushes lambda code to their respective functions, and P2 pushes frontend code to S3 bucket.
9. CloudFormation Template - Creates all the other modules using a single template.
 
  


![image](https://github.com/Chinnu1103/PicSearch/assets/32939338/19c3284a-168c-400a-8210-c61eae32e7f1)  


