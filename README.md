# Deployment Console 

The Deployment Console allow assists with deploying either a new AnyLog node or an existing node based on existing 
configs via a web interface. The console provides support for deploying a node of type:

* Empty -  clean node with nothing on it
* REST - node with a TCP/REST and authentication configuration, but no other processes running on it
* Master - notary node that manages and shares the content in blockchain 
* Operator - node containing data that comes in from device(s) 
* Publisher - node responsible for distributing the data 
* Query - node dedicated for querying data, though all nodes can query data
* Single-Node -  A node containing both _master_ and _operator_ process respectively
* Single-Node-Publisher -  A node containing both _master_ and _publisher_ process respectively

In addition, to the web-based interface, there's a [Manual Deployment](anylog_api/docker_deployment.py#L106) option, 
which allows for deploying an AnyLog instance, based on a configuration file, via command line.

### Requirements
* Python3
  * [docker](https://pypi.org/project/docker/) - used to deploy AnyLog
  * [django](https://pypi.org/project/Django/)
  * [requests](https://pypi.org/project/requests/)

### Deployment
```
cd $HOME/Django-API
python3 $HOME/Django-API/manage.py ${IP}:${PORT}
```




