# Content of Project
* [General info](#general-info)
* [Technologies](#technologies)
* [Environment](#environment)
* [Setup](#setup)

## General Info
Investment Portfolio is an application for gathering and storage data concerning user strategic investment.
The application also serves an API, to communicate with the future main Home Finance application.

## Technologies
<ul>
<li>Python 3.10</li>
<li>Django 4.14</li>
<li>DjangoRestFramework</li>
<li>Docker</li>
<li>PostgreSQL</li>
<li>Pytest</li>
</ul>

## Setup
1. Clone GitHub repository 
``` 
git clone https://github.com/m-miler/investment_portfolios.git
```
2.  Install docker and docker-compose then run in project file.
```
  docker compose -f .\devOps\docker-compose-dev.yml up -d --build
```
