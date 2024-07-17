# CML_AMP-Chromadb-rest-api
This AMP aims to show how to ingest data to chromadb using a NiFi flow.

The AMP deploys an application on CML that exposes a REST API server to interact with ChromaDB.

The companion CDF flow reads  some customer support tickets from a json file on the CDP storage, extracts some useful information (ticket_id and ticket_description) and pushes into chromadb using REST API.


# Deployment
## AMP Deploy
In a CML workspace, click "New Project", add a Project Name, select "AMPs" as the Initial Setup option, copy in the [repo URL](https://github.com/dvergari/CML_AMP-Chromadb-rest-api.git), click "Create Project".
In the "Configure Project" configure the following environment variables:
* COLLECTION -> The name of the collection to be created in chromadb
* DEBUG -> Set to 1 to enable debug (may impact performance)

**Important: once the deploy finishes, do not forget to allow unauthenticated access to the application**  [<link>](https://docs.cloudera.com/machine-learning/cloud/applications/topics/ml-securing-applications.html)


## CDF Flow deploy
1. Download the test data file from `/data/customer_support_tickets.json` and upload to a directory on the CDP environment storage (the S3 bucket associated with the environment). You will use the path of that directory later while configuring the CDF flow
2. Download the Json file from `/nifi/demo-chromadb-upsert.json` and import it into your catalog.
3. Setup in a manner similar to below screenshots:

Import the flow definition in the catalog

<img width="540" alt="image" src="https://github.com/user-attachments/assets/3ac2c9ce-7f2e-4ed3-8656-2e1c7ccd453a">
<img width="888" alt="image" src="https://github.com/user-attachments/assets/897ed8ad-da11-4288-97f5-bae48ece4b06">

Start a deployment in an existing environment

<img width="604" alt="image" src="https://github.com/user-attachments/assets/d4be6a78-090d-433b-88c0-704d9206666c">
<img width="790" alt="image" src="https://github.com/user-attachments/assets/7bbdc474-02d9-435a-95c9-be2693523845">

Select NiFi 1.x as runtime

<img width="790" alt="image" src="https://github.com/user-attachments/assets/1877308f-7b00-40bc-8e9a-ed0b574d5b79">

Configure the following properties:

<img width="759" alt="image" src="https://github.com/user-attachments/assets/e9b97e7d-1a16-45ba-a155-c14b03b52ae9">

1. CDP Username: your cdp workload username
2. CDP Password: your cdp workload password
3. Directory: the directory on your CDP Storage in which you saved the test data
4. chroma_endpoint_url: The URL of the deployed CML Application. **Important: Do not forget to append the path `/upsert` after the hostname**
   - for example, if the URL of the CML application is `https://cml-chroma-server-baf9yj.ml-6e045173-d3d.rags-ita.a465-9q4k.cloudera.site` the property value will be `https://cml-chroma-server-baf9yj.ml-6e045173-d3d.rags-ita.a465-9q4k.cloudera.site/upsert`


The "Extra small" tier should be enough

<img width="759" alt="image" src="https://github.com/user-attachments/assets/be5818aa-feaf-43ac-af34-a59e6514031a">
<img width="759" alt="image" src="https://github.com/user-attachments/assets/c484d366-56fc-4ff3-a7b6-62feef3b6f8e">


# Check results
After both the AMP and the flow are deployed, you can query the documents in chromadb using the jupyter notebook in `/notebooks/query_chromadb.ipynb`

## Technologies Used
#### Open-Source Models and Utilities
- [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/sentence-transformers/all-mpnet-base-v2/resolve/main/all-mpnet-base-v2.tar.gz)
   - Vector Embeddings Generation Model
#### Vector Database
- [Chroma](https://github.com/chroma-core/chroma)
#### Dataset
- [Customer support ticket dataset from Kaggle](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset)















