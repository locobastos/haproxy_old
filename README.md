# HAProxy 2.4.16 for CentOS 7

This repository contains necessary build files of HAProxy 2.4.16 with no support and no expectation of stability. The recommended way of using the repository is to build and test your own packages.

This repository fills my needs. I am not expecting to handle all CentOS environments.

## Prerequisites

From a clean and minimal CentOS 7 server, you have to install some packages:

```bash
yum update -y && yum install -y git rpmdevtools epel-release
```

## Build HAProxy

Now your environment is ready, let's build HAProxy:

```bash
cd ~
git clone https://github.com/locobastos/haproxy
cd haproxy
spectool -g -C SOURCES SPECS/haproxy.spec
yum-builddep -y SPECS/haproxy.spec
rpmbuild -ba SPECS/haproxy.spec --define "_topdir $(pwd)"
cp RPMS/x86_64/haproxy-*.rpm ~/
cp SRPMS/haproxy-*.rpm ~/
```
