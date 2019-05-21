# Project 2019
This is the repository for submitting your final assignment.
**Deadline: 30th April 2019, 5pm London time.**

**Comments**:
* **MV 5 April 2019**: project topic approved

Please add the following information:

## Name: 
`Bradley Carruthers`
## LSE ID:
`201770480`
## e-mail:
`b.c.carruthers@lse.ac.uk`
## Project title:
`Exploring Community Engagement with Questions on the 20 Largest StackExchange datasets`

## New Summary:
This project explores data on over 1.2 million answers and questions from 5 of the largest StackExchange communities. Different infrastructures of GCP Dataproc clusters are explored to minimise read-in and analysis time for the five StackExchange fora, finally scaling vertically by using 1 high-memory master node with 96 CPUs and no worker nodes.

Various aspects of the data are explored via EDA and t-SNE graphs, and lastly an LDA model is implemented on post content to investigate latent topics and underlying semantic structure across each forum. While this only serves as an inital analysis of a planned classification project over a greater collection of larger datasets, it lays the groundwork for analysing data of this size and nature in a distributed computing framework.

---

### Old Summary:
The aim of the project is to explore how the top 20 largest StackExchange communities interact with questions. Firstly, I will perform EDA on all questions, answers and comments of the 20 large datasets. The second goal is to build a classification model on various different communities to identify questions with high potential of positive community engagement. 

The classification model will use only the question text and title as input, deriving features using sentiment analysis and LDA. Positive community engagement will be summarised by PCA using the score of the question, the number of answers and the sentiment of the answers.

I will then test the individual models across all 20 communities to compare results. In this way I should gain insight into the degree to which StackExchange communities engage with questions homogenously.

---

## You may add comments and references to the included files here:

## Final file:
The final file is `Community_Engagement_StackExchange_Fora.ipynb`
