# [Heroku](http://heroku.com)

We are deploying our API on [Heroku](http://heroku.com) and here’s what you should know about it.

## What’s [Heroku](http://heroku.com)

[Heroku](http://heroku.com) is a PaaS (Platform as a Service) which you don’t have to worry about configuring the production environment. I strongly recommend you go on [Heroku](heroku.com) try them out for free. They have a 5 minutes tutorial that will guide you through.

## Deployment

According to the Heroku tutorial, after setting everything up you run

>git push heroku master

and you'd be good to go, but our process is a little bit different.

We decided to deploy directly from Github, which means that all the code on the branch master should be good for production. If you have any code that is not ready yet to go on production you should keep it out of the master branch.
