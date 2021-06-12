# Guestbook on Red Hat OpenShift

The guestbook shows how to build a simple multi-tier web application using Kubernetes and Docker. The application consists of a web front end, Redis master for storage, and replicated set of Redis slaves, all for which we will create Kubernetes deployments, pods, and services.

There are two versions of this application. Version 1 (in the `v1` directory) is the the basic guestbook application in go with a Dockerfile. Version 2 (in the `v2` directory) extends the guestbook example with additional functionality to call the IBM Watson Tone Analyzer service.

## Get Started
This application is used in the Introduction to Containers, Kubernetes, and OpenShift, available on [Cognitive Class](https://cognitiveclass.ai/courses/kubernetes-course), [Coursera](https://www.coursera.org/learn/getting-started-with-kubernetes-openshift), and [edX](https://courses.edx.org/courses/course-v1:IBM+CC0201EN+3T2020/course/).
