# dec-project-01

# **Table of Content**

* Introduction
* Data Sources
* Analytical Questions
* Tools
* Architecture
* Challenges

# Introduction

Our goal in this project is to identify trends and answer questions regarding real estate in the United States and provide useful information to both house buyers and sellers wich will help them in the decison making process.

# Data Source

We are going to source data from the US real estate public API.

| Source name        | Source type | Source documentation                                                                                    |
| ------------------ | ----------- | ------------------------------------------------------------------------------------------------------- |
| US Real Estate API | API         | [https://rapidapi.com/datascraper/api/us-real-estate](https://rapidapi.com/datascraper/api/us-real-estate) |

# Analytical Questions

* what is the biggest home listing time
* wich house by size last longer on the market
* what are the 10 cheapest/most expensive homes across all zip codes
* When and where were the most expensive homes sold
* What are the location of the most expensive houses

# Tools

We are going to use the the below tool for this project


| Tool              | Usage                                        |
| ----------------- | -------------------------------------------- |
| Python            | Coding language of the "ELT" pipeline        |
| Postgres Database | To host our raw data collected from  the API |
| Docker            | To build, test and deploy the pipeline       |
| AWS               | The pipeline will be hosted on AWS           |

# Architecture

![1694036021835](image/README/1694036021835.png)

# Challenges

* Limitation of the number of API call
* Cost of calling an API.
