# simpleapp
Simple Flask app running on a Vagrant VM and demonstrating data processing.

# Clone
```shell
git clone https://github.com/mtecer/simpleapp.git
```

# Deployment
Part of the installation is Vagrant triggering ansible to deploy mongodb and simpleapp as a wsgi application on Apache.
For more information review resulting configuration in /etc/httpd/conf.d
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


