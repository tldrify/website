tldrify.com
============

![Build Status](https://github.com/tldrify/website/workflows/build/badge.svg)

Source code for [tldrify.com](https://tldrify.com).


### CI ###

See `./github/workflows/build.yml` script.


### Deployment ###

The easiest way of depoying the service with all the dependencies is using Docker.

Prerequisites:

 * Have Docker and `docker-compose` installed.
 * Update `deploy/prd.env` file.
 
When everything is ready, run:

    ENV=prd ./deploy/run.sh

