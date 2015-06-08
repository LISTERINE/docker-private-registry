# Docker Registry (private)
This uses the `stackbrew/registry` as a base and adds basic auth via Nginx.

# Changes in this fork
* Removed non-ssl access
* Added run script

# Planned additions
* Add pages for GUI management of registry
* Add support for registry v2.0

# Usage
To run a private registry, launch a container from this image and bind a volume
with your SSL cert and key and then specify environment variables to define the
certificate and key in the container. This is contained in:

`sh docker-run.sh`

Don't forget to build the image from the included Dockerfile. While in the directory with the Dockerfile, run:

`docker build -t shipyard:private-registry .`

or customize docker-run.sh to your liking:

`docker run -i -t -p 5001:5001 -v /path/to/cert_and_key:/opt/ssl -e SSL_CERT_PATH=/opt/ssl/cert.crt -e SSL_CERT_KEY_PATH=/opt/ssl/cert.key shipyard/docker-private-registry`

# SSL
Until https://github.com/dotcloud/docker/pull/2687 is fixed, a valid (from a
recognized CA) SSL certificate is required. Unless --insecure-registry <registry_ip:port>
is specified.

# Management
There is a simple management application written in Flask that you can use
to manage registry users.  To access the management application, create a
container from this image and visit `/manage`.

The default username is `admin` with a password of `docker`.  You can change
the password at run via environment variables (see below).

# Environment
* `ADMIN_PASSWORD`: Use a custom admin password (default: docker)
* `REGISTRY_NAME`: Custom name for registry (used when prompted for auth)
* `SSL_CERT_PATH`: SSL Certificate path
* `SSL_CERT_KEY_PATH`: SSL Certificate key path
* `HTTPS_PORT`: Port on wich to access services (default: 5001)

# Ports
* 5000 registry
* 5001 (or specified) nginx

# Running on S3
To run with Amazon S3 as the backing store, you will need the following environment variables:

* `AWS_KEY`: Your AWS Access Key ID (make sure it has S3 access)
* `AWS_SECRET`: Your AWS Secret Key
* `AWS_BUCKET`: Your S3 bucket to store images
* `SETTINGS_FLAVOR`: This must be set to `prod`

# Generating your keys
* sudo openssl genrsa -des3 -out /opt/registry_ssl/shipyard-registry.key 2048
* sudo openssl req -new -key /opt/registry_ssl/shipyard-registry.key -out /opt/registry_ssl/shipyard-registry.csr
* sudo cp /opt/registry_ssl/shipyard-registry.key /opt/registry_ssl/shipyard-registry.key.org
* sudo openssl rsa -in /opt/registry_ssl/shipyard-registry.key.org -out /opt/registry_ssl/shipyard-registry.key
* sudo openssl x509 -req -days 365 -in /opt/registry_ssl/shipyard-registry.csr -signkey /opt/registry_ssl/shipyard-registry.key -out /opt/registry_ssl/shipyard-registry.crt
