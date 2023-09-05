# Project plan

## Objective

The objective of the product is to provide property pricing trends in different areas of the United States.

## Consumers

Home buyers.

## Questions

1. Longest days on the market by home size.
2. Average home price of top 10 most expensive homes sold.
3. 10 cheapest/most expensive homes/across all zip codes.
4. How long it took to sell the biggest homes per zip code.
5. When the most expensive homes were sold and where.
6. Location of most expensive homes sold.

## Source datasets

What datasets are you sourcing from? How frequently are the source datasets updating?

Example:

| Source name        | Source type | Source documentation                                |
| ------------------ | ----------- | --------------------------------------------------- |
| US Real Estate API | API         | https://rapidapi.com/datascraper/api/us-real-estate |

## Solution architecture

Retrieve values from API in JSON format.

1. (Extract & Load) Ingest the dataset to Postgres with Python to raw table.
2. (Transform) Raw input table perform transformations to create tables containing the query data that is useful for consumers.
3. Transformation patterns include data organized by city, by state, by region.

We recommend using a diagramming tool like [draw.io](https://draw.io/) to create your architecture diagram.

Here is the solution architecture diagram:

![images/dec.png](images/dec.png)

## Breakdown of tasks

1. Python to ingest data to Postgres
2. SQL queries for the transformations
3. Python to run SQL queries
4. Python to run pipeline
5. Python to log pipeline
6. Docker image of the Python code
7. Run container in ECS

Trello board created and will add members pending receiving everyone's e-mail addresses: https://trello.com/b/UaWnmHYO/dec-project-1
