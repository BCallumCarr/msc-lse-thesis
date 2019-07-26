DOCKER EXAMPLE FOR APPLICATION

This example uses [docker](docker.com) to package an application and provide predictions.
A more robust tutorial can be found [here](https://mlinproduction.com/docker-for-ml-part-4/)

## To run:
You need to have docker installed.

Build the docker image:
`docker build . -t real_state`
Get a prediction:
`docker run real_state $(cat example_observation.json)`
