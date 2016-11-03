splunkforwarder-deployment-config
=================================

This package creates and deploys a custom deploymentclient.conf file. The resulting RPM can be used in RHN Satellite, Spacewalk or other RPM-based repo to install the splunk or splunkforwarder RPM along with a custom deploymentclient.conf file--typically without actually touching the client system. Since the splunk or splunkforwarder RPM is a requirement, it will be installed automatically when splunkforwarder-deployment-config is installed on the client--at least with a properly configured RHN Satellite, Spacewalk or yum repos.

The deploymentclient.conf file will be placed in its own app directory on the client. The directory is /opt/splunkforwarder/etc/apps/zzRPM-splunkforwarder-deployment-config, by default.


Build-time Variables:
-------------------
In order to create the custom splunkforwarder-deployment-config RPM, you must define the following variables at RPM build-time:

* `CLIENTNAME` - This is the deployment client name used by the Splunk deployment server.
 * Note: This is not the hostname of the client that will receive the RPM.

* `DEPLOYMENTSERVER` - This is the deployment server that your clients should contact in order to receive their configurations.

The following variables can be defined to further customize your deployment configuration:

* `SPLUNKPKG` - This is the RPM package (splunk or splunkforwarder) that must be installed before the splunkforwarder-deployment-config package is installed.
 * Default: `splunkforwarder`

* `SPLUNKUSER` - This is the user that will run splunkd and own the files under $SPLUNK_HOME.
 * Default: `splunk`

* `SPLUNKVERSION` - This is the version of splunk or splunkforwarder that will be required (as a minimum) in order to install the splunkforwarder-deployment-config rpm.
 * Default: `6.1.0`

* `DEPLOYMENTPORT` - This is the TCP port on which your DEPLOYMENTSERVER listens. By default, this is port 8089. If you changed this from the default, then you need to define it here.
 * Default: `8089`

RPM CREATION:
------------
General rpmbuild command:

    rpmbuild -ba --define 'CLIENTNAME [deployment client name]' --define 'DEPLOYMENTSERVER [deployment server]' splunkforwarder-deployment-config.spec
Note: You can/should add `--sign` to your `rpmbuild` command in order to embed a GPG signature into your RPM. This will allow you to verify the integrity of the RPM. In order for this to work, you will need to generate a GPG key for RPM signing. For more information, see the `rpmbuild(8)` man page and [Red Hat's RPM Building](https://access.redhat.com/documentation/en-US/Red_Hat_Network_Satellite/5.3/html/Deployment_Guide/satops-rpm-building.html) page.

Example rpmbuild command:

    rpmbuild -ba --define 'CLIENTNAME Splunk-UF' --define 'DEPLOYMENTSERVER deploy.example.com' --sign splunkforwarder-deployment-config.spec

RPM USAGE:
----------
Once you have built your RPM, you can add it to RHN Satellite, Spacewalk or your private yum repo. You can then run the following command to install `splunkforwarder-deployment-config` *and* `splunkforwarder`:

    yum install splunkforwarder-deployment-config

After the command completes, `splunkforwarder` will be installed, configured and it will contact your defined deployment server for further configuration.

If you don't have a repository to hold the `splunkforwarder-deployment-config` and `splunkforwarder` RPMs, you can also install both of the packages directly with the `rpm` command. First copy the files to the target system, then run the following to install and configure `splunkforwarder`:

    rpm --install splunkforwarder-deployment-config*rpm splunkforwarder*rpm
