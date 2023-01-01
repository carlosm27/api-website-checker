# api-website-checker
An API written in Python using FastApi, Piccolo-ORM, and Rocketry to check the connectivity of websites.

The goal of this API is that the user add the url of website, to check if the website is online. The server will check website's connectivity doing requets periodically.

One of the goal is that the user may select the period of time the server will the website or websites, that is the reason this project using Rocketry as task scheduler.

### This is WIP is not ready to use

## To Do List

- [X] Add FastAPI.
- [X] Add CRUD endpoints.
- [ ] Add a Scheduler
- [ ] Task schedule to request websites.
- [ ] Add a function that returns the log of a request, and the website requested in JSON format.
- [ ] Add an endpoint to return log information detail.
- [ ] Add email notifications using
- [ ] Create frontend with Vuejs
- [ ] Add authentication and authorization
