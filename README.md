![Workshops](./assets/aws.png)

# Building a recommender system on AWS workshop

In this workshop you will learn how to implement a typical machine learning use case on the AWS platform end-to-end, in this case a recommender system.

You will start with implementing a prototype with [Amazon Personalize](https://aws.amazon.com/personalize/) and integrate it into our business application.

We will then train and serve our own recommendation machine learning model with [Amazon SageMaker](https://aws.amazon.com/sagemaker/)!

**AWS Experience:** Beginner

**Time to Complete:** 2-3 hours

## Prerequisites

- **An AWS Account and Administrator-level access to it**

Please be sure to terminate all of the resources created after this workshop to ensure that you are no longer charged.

## Begin this workshop

**[Proceed to Lab 0 - Setting up your Amazon SageMaker Jupyter notebook instance](/lab-0-setting-up-your-notebook)**

## Workshop structure

This workshop consists of following labs:

- [Lab 0 - Setting up your Amazon SageMaker Jupyter notebook instance](/lab-0-setting-up-your-notebook)
- [Lab 1 - Providing personalized movie recommendations using Amazon Personalize](/lab-1-recommendations-with-amazon-personalize)
- [Lab 2 - Training and deploying a custom recommender model using Amazon SageMaker](/lab-2-recommendations-with-sagemaker)

### Workshop Clean-Up (Once Complete)

Be sure to delete all of the resources created during the workshop in order to ensure that billing for the resources does not continue for longer than you intend. We recommend that you utilize the AWS Console to explore the resources you've created and delete them when you're ready.

For the two cases where you provisioned resources using AWS CloudFormation, you can remove those resources by simply running the following CLI command for each stack:

```bash
aws cloudformation delete-stack --stack-name STACK-NAME-HERE
```

To remove all of the created resources, you can visit the following AWS Consoles, which contain resources you've created during the workshop:

- [Amazon Sagemaker](https://console.aws.amazon.com/sagemaker/home)
- [Amazon Personalize](https://us-east-1.console.aws.amazon.com/personalize/home)

**[Proceed to Lab 0 - Setting up your Amazon SageMaker Jupyter notebook instance](/lab-0-setting-up-your-notebook)**
