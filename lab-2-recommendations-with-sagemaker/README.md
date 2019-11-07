![Workshops](../assets/aws.png)

# Lab 2 - Training and deploying a custom recommender model using Amazon SageMaker

## Overview

In the previous lab we have trained custom recommendation models using Amazon Personalize and integrated this into our movie recommendation application.

Following figure shows a simplified architecture of this application:

![Sagemaker console](images/architecture-lab1.png)

Now your startup has become very successful, you where able to hire a team of data scientists. This team consists of experts on recommender systems and wants to have more control over the machine learning workflow.

To accommodate this we will use [Amazon SageMaker](https://aws.amazon.com/sagemaker/) in this lab.
Amazon SageMaker is a fully-managed service that covers the entire machine learning workflow to label and prepare your data, choose an algorithm, train the model, tune and optimize it for deployment, make predictions, and take action.

Throughout this lab we will:

- Train a custom machine learning model based on Amazon SageMaker Built-in algorithms
- Deploy this model via a SageMaker Endpoint
- Integrate this endpoint into the Movie Recommender App using Api Gateway and a Lambda function

The final architecture will look like this:

![architecture-final](images/architecture-lab2.png).

## Training and deploying a custom recommendation model

1. Navigate to Amazon SageMaker service in the AWS Console --> Select `Notebook instances`
1. Select `Open JupyterLab` for your notebook instance to navigate back to the JupyterLab web interface.
1. In the file browser select `lab-2-recommendations-with-sagemaker` and open the notebook --> `1-Training-and-deploying-your-recommendation-model.ipynb`

Now slowly work through the notebook to train and deploy your first machine learning model.

## Integrating the model into the movie recommender application

If you followed the notebook closely, you might have noticed that we have deployed an endpoint which takes a user embedding (simple vector) as input. The user embedding identifies the user and the endpoint returns a list of recommended movie ids in following format

```json
{'distances': [2.964694738388061,
  2.967271327972412,
  2.976406097412109,
  2.978152751922607,
  ....,
  5.529520988464356,
  6.034342765808105],
 'labels': [527.0,
  732.0,
  484.0,
  56.0,
  ...,
  50.0,
  64.0],
 'predicted_label': 1.0}

```

This is not ideal for our recommendation app. The movie recommendation application requires a simple REST endpoint which takes a userId as request parameter like this:

`https://endpointurl/recommendEndpoint?user_id=3`

and returns a JSON based list of user id, similar to this:

```json
{"movies": [814, 1125, 653, 428, 1525, 60, 652, 185, 654, 86, 223, 12, ...]}
```

To solve this we will create a Lambda function to integrate both. The Lambda function transforms a given user id into a user embedding required by the SageMaker endpoint. It will then call the endpoint using the AWS SDK and return a list of recommended movies in the required format. The Lambda function will be fronted by a API Gateway.

This is a typical architecture in a microservice based environment. This approach has following advantages:

- A stable contract between the parts of the application owned by the application development team and the data science team
- The data science team can easily experiment with new models and change the backend architecture without impacting the business application by simply changing the endpoint of the API Gateway.

1. To create the required Lambda Function and API Gateway open the notebook `2-Integrating-your-endpoint-with-lambda.ipynb` and work through each of the steps