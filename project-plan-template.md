# Project plan 

## Objective 
A short statement about the objective of your project.

Example: 

> The objective of our project is to provide analytical datasets from our Orders API and Customers database. 

## Consumers 
What users would find your data useful? How do they want to access the data? 

Example: 

> The users of our datasets are Data Analysts and the Production team in the business. 

## Questions 
What questions are you trying to answer with your data? How will your data support your users?

Example: 

> - How many orders are there for each customer? 
> - What countries and regions have the most orders? 
> - What customers have their orders delayed? 
> - How many delayed orders are there for each country and region? 
> - How many orders do we have for each day? 
> - How many delayed orders do we have for each day? 

## Source datasets 
What datasets are you sourcing from? How frequently are the source datasets updating?

Example: 

| Source name | Source type | Source documentation |
| - | - | - |
| Customers database | PostgreSQL database | - | 
| Orders API | REST API | - | 

## Solution architecture
How are we going to get data flowing from source to serving? What components and services will we combine to implement the solution? How do we automate the entire running of the solution? 

- What data extraction patterns are you going to be using? 
- What data loading patterns are you going to be using? 
- What data transformation patterns are you going to be performing? 

We recommend using a diagramming tool like [draw.io](https://draw.io/) to create your architecture diagram. 

Here is a sample solution architecture diagram: 

![images/sample-solution-architecture-diagram.png](images/sample-solution-architecture-diagram.png)

## Breakdown of tasks 
How is your project broken down? Who is doing what?

We recommend using a free Task board such as [Trello](https://trello.com/). This makes it easy to assign and track tasks to each individual. 

Example: 

![images/kanban-task-board.png](images/kanban-task-board.png)