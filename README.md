# simpleapp
Simple Flask app running on a Vagrant VM and demonstrating data processing.

# Clone
```shell
git clone https://github.com/mtecer/simpleapp.git
```

# Deployment
Vagrant triggers an ansible run to configure this server.
Ansible deploys mongodb service, and also deploys simpleapp as a wsgi application on Apache.
Python library requirements are installed as part of ansible run.
For more information review resulting configuration in /etc/httpd.
```shell
cd simpleapp
vagrant up
vagrant ssh
```

# Testing
```
vagrant ssh
vagrant $ cd /usr/local/python/simpleapp
vagrant $ python python tests/simpleapp-test.py
```


