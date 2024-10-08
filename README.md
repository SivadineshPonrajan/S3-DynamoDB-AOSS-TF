# S3-DynamoDB-AOSS-TF

### Files and Folders
```
Project Folder
├── Readme-Images
├── search-script.py    // Standalone python script file to search in opensearch
├── terraform           // Terraform Infra files
└── lambda
    ├── package         // Contains the zipped layers and functions files
    ├── layer           // Contains the files for lambda layers
    │   └── python
    └── function        // Contains the files for lambda functions
```
- Terraform files (tf) defining the architecture can be found in `terraform` folder.
- `lambda/function` folder contains the python script defining the lambda function.
- Lambda layer files with requirements.txt and a shell file to compile and build to zip file can be found in `lambda/layer` folder.
- Built and zipped lambda layers zip file and the lambda functions zip file are present in the `lambda/package` folder.
- `search-script.py` is a python script file to run a full text search for specific keywords appearing in the customer comment field.
- Readme - Documentation of the assignment.

**Note:** Instead of creating a separate script file with the commands for the creation of the OpenSearch cluster with 1 node (t3.small.search), all these process were included in the terraform part and the data insertion part was added along with the lambda function to minimize the cost as mentioned.

---

### Budget
![Budget Overview](./Readme-Images/budget.png)

At the beginning of the assignment, I created a budget of 2$ or 730 HUF. The above screenshot was taken after the completion of the assignment and it has consumed literally zero.

---

### Workflow

Once the terraform is initialized, planned and applied, the pipeline will be successfully deployed and running. Once the csv file is uploaded to the mentioned S3 bucket, the trigger will call the lamdba function.

```
cd terraform
terraform init
terraform plan
terraform apply
```

---

### Lambda Function - Data Processing
- The rows with missing values will be dropped.
- The unnecessary whitespaces will be trimmed off.
- If the comments attribute contains a valid email address, that email address is obtained through regex match and will be overwritten to the email attribute.
- An unique user_id will be created and used as the primary key.

Once the data is processed, the data will be inserted into the DynamoDB and also the comments will be indexed in the Opensearch.

---

### Search Script


The `search-script.py` script is a CLI application which can be used to search for the particular keywords in the customer's comments that were populated in the OpenSearch.

- Search is done with wildcard pattern instead of query words so it can handle partial word search as well.
- Pagination retrieval is implemented to handle huge retrieval.

The opensearch service endpoint can be passed directly as an argument or the terraform output can be passed for the search script.

> python search_script.py [OpenSearch host URL]

or

> python search-script.py "$(terraform output -raw -state=terraform/terraform.tfstate opensearch_endpoint)"
---

### Development Timeline

Overall I took roughly around `3 hours and 45 minutes` for the development.
- Initially started with prebuilt Pandas ARN for the layers (like cdn) and manually created the S3 bucket, DynamoDB and the Opensearch cluster ~ `40 minutes`
- Developed the lambda function ~ `1 hour 15 minutes`
- Developed terraform scripts for the service creation and built (still with prebuilt ARN) ~ `45 minutes`
- Almost took an hour to debug, compile and make the custom lambda layer ~ `1 hour`
(Missed the binary argument while installing the dependencies)

---
