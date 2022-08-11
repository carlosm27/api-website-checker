# api_website_checker
An API written in Python using FastApi, Piccolo-ORM, and Rocketry to check the connectivity of websites.

The goal of this API is that the user add the url of website, to check if the website is online. The server will check website's connectivity doing requets periodically.

One of the goal is that the user may select the period of time the server will the website or websites, that is the reason this project using Rocketry as task scheduler.
