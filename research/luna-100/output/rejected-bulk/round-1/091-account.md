# This is the fourth article in a series based

I’m documenting one concrete piece of work here. The original material describes what was tried, what changed, and which parts remained useful. The important details are the decisions and the reasons behind them.

This is the fourth article in a series based on , the free course we run at DataTalks.Club.

In part 3, we deployed it to a cloud environment and configured CI/CD.

* Promote the exact version tested in development.

Deploy changes to development first, promote a tested release to production, and respond to observed failures

We will continue using AWS and CloudFormation, but the principles we show in this article are tool-agnostic and will work for any environment.

## Dev and prod environments

When we push the code, we automatically deploy the changes, and they go live immediately.

However, when we have real users, we want to be more careful and check that our changes didn’t introduce any regressions.

Typically we run the latest version of our project there, and every time we push, the changes are automatically deployed there.

We don’t want to deploy every single change there automatically and we want to have more control over the process.

Promoting from dev to prod happens only after a manual action.

We will most likely need to change a few things, like the size of the machine where the application is running, but the majority of the resources will stay the same.

We will only deploy to dev on every push.

Promotion to prod happens only after a manual approval

Now we have two environments.

I deploy to EC2 by executing the build script on the machine and then running the image in Docker.

The deploy stage is actually two things: build and deploy.

When we promote the dev version to production, we have to build again.

As a result, we split the deploy step into two separate steps:

* Build the image and upload it to a container registry
* Pull this image from the registry during the deploy

When promoting to prod, we just pull the same image to prod.

You can also push your images to Docker Hub or another container registry if you’re running outside of AWS and your cloud doesn’t have a special service for that.

The build step builds a docker image, tags it and uploads to the registry.

The production release step takes the tag currently deployed in dev and promotes it to prod.

We can test the dev application, and when we later promote it to production, we will be certain that it’s exactly the same image.

However, accidents will still happen, and the application needs to make sure we detect them and react as fast as possible.

“Observability” means collecting information about the application so it is possible to understand its behavior.

We achieve observability by adding monitoring to our applications.

If we see that CPU and memory utilization are growing and RPS is dropping, something may be off.

For that, the application needs to collect more.

Telemetry is all the information that the application produces:

* Metrics - requests per second, response latency, and number of errors
* Logs - timestamped records of individual events, like an error message or a failed database query
* Traces - all the steps (called “spans”) that a single request makes through the entire application


Metrics give us concrete numbers, logs give details, and traces show the path of a request with each step.

The result is specific to this project. Some parts worked, some became too complicated, and some ideas survived in a smaller form. That is enough to make the experiment useful without turning it into a universal recommendation.
