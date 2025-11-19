---
title: Clustered Keycloak SSO Deployment in AWS
tags: [How to, Keycloak, AWS, SSO, Article]
canonicalurl: https://www.dae.mn/insights/clustered-keycloak-sso-deployment-in-aws
status: published
---

 [Keycloak](http://www.keycloak.org/) is an open source Identity and Access Management tool with features such as Single-Sign-On (SSO), Identity Brokering and Social Login, User Federation, Client Adapters, an Admin Console, and an Account Management Console.

### Why use Keycloak?

There are several factors to deciding whether or not to use Keycloak or a SaaS IAM Service like AWS SSO. SaaS IAM services are typically easier to implement, better supported, and do not require manual deployment but Keycloak is free to use, feature rich, and flexible.

### Pre-requisites

This guide assumes you already have at least one Keycloak instance with a Postgres database configured, if this is the case your _keycloak.conf_ should include a section that looks something like the example below.

```
db=postgres
db-password=<your db password>
db-userame=keycloak
db-pool-initial-size=1
db-pool-max-size=10
db-schema=public
db-url-database=keycloak
db-url-host=<url of your db>
db-url-port=5432
```
    

If you do not yet have your database configured please refer to [the documentation on configuring relational databases for Keycloak](https://www.keycloak.org/server/db).

### Configuring JDBC Ping

In order for Keycloak instances to cluster they must discover each other and this can be achieved by using JDBC Ping which allows nodes to discover each other via your existing database. JDBC Ping is a convenient discovery method because it does not require the creation of additional AWS resources and is compatible with AWS unlike the default discovery method (multicast) which is not permitted by AWS.

In order to use JDBC Ping we first need to define a transport stack, this can be achieved by adding the below element to the _infinispan_ tag in your _cache-ispn.xml_ file and replacing the default values (these should match the _db-password_ and _db-url-host_ from your _keycloak.conf_ file).

```
<jgroups>
    <stack name="jdbc-ping-tcp" extends="tcp">
        <JDBC_PING connection_driver="org.postgresql.Driver"
                    connection_username="keycloak"
                    connection_password="<your database password>"
                    connection_url="jdbc:postgresql://<url of your database>:5432/keycloak"
                    initialize_sql="CREATE TABLE IF NOT EXISTS JGROUPSPING (own_addr varchar(200) NOT NULL, cluster_name varchar(200) NOT NULL, ping_data BYTEA, constraint PK_JGROUPSPING PRIMARY KEY (own_addr, cluster_name));"
                    info_writer_sleep_time="500"
                    remove_all_data_on_view_change="true"
                    stack.combine="REPLACE"
                    stack.position="MPING" />
    </stack>
</jgroups>
```
    

We have now defined a new JGroups stack which will create a table in your database if one doesn’t already exist which Keycloak instances can use to discover each other, when you start a new Keycloak instance it will write its name as a new record into this table. To use this stack simply amend the _transport_ element as shown below to reference the newly defined stack.

```
<transport lock-timeout="60000" stack="jdbc-ping-tcp"/>
```

### Configuring Security Groups

Keycloak uses Infinispan to cache data both locally to the Keycloak instance and for remote caches. Infinispan by default uses port 7800 so we need to configure the Security Group our Keycloak instances are deployed to in order to permit both ingress and egress via port 7800. This can be done in a number of ways such as via the AWS Console, below is an example of configuring ports for Keycloak using Terraform.

```
## keycloak cluster egress
resource "aws_security_group_rule" "keycloak_cluster_egress_to_keycloak" {
    description              = "keycloak cluster"
    from_port                = 7800
    protocol                 = "tcp"
    security_group_id        = aws_security_group.keycloak.id
    source_security_group_id = aws_security_group.keycloak.id
    to_port                  = 7800
    type                     = "egress"
}

## keycloak cluster ingress
resource "aws_security_group_rule" "keycloak_cluster_ingress_to_keycloak" {
    description              = "keycloak cluster"
    from_port                = 7800
    protocol                 = "tcp"
    security_group_id        = aws_security_group.keycloak.id
    source_security_group_id = aws_security_group.keycloak.id
    to_port                  = 7800
    type                     = "ingress"
}
```   

### Restarting Keycloak

Keycloak does not automatically apply changes made to its configuration so you will need to restart your Keycloak instance/instances for clustering to work. First run the following from the terminal to rebuild your Keycloak instance to register the changes we made to your configuration.

```
➜/bin/kc.sh build
```

Once you have rebuilt Keycloak restart your Keycloak service by running the following (alternatively you can restart your Keycloak instance).

```
systemctl restart keycloak
```

Your Keycloak instances should now be running in a clustered state.

### Testing your Keycloak cluster

To check that your Keycloak cluster is functioning correctly check your database and see if the _JGROUPSPING_ table both exists and includes the name of all instances currently in the cluster, your table should look something like the below.

    
|own_addr|cluster_name|ping_data|
|--------|------------|---------|
|*****   |ISPN        | *****   |
|*****   |ISPN        | *****   |

If you terminate a Keycloak instance or start a new instance you should see the records in this table change.

### Troubleshooting

**Changes made to config files aren’t applied after building Keycloak**

Ensure that the config files you have changed match those configured in _keycloak.conf_, this guide for example assumes that you have your Infinispan config file set as cache-ispn.xml in your _keycloak.conf_ file.
```
cache-config-file: cache-ispn.xml
```

**Keycloak services don’t start after changing config files**

Check the Keycloak logs and ensure your database access details (password and host url) are set correctly: if these values are incorrect the Keycloak service will fail to start.

### Resources

[
Use of JDBC_PING with Keycloak 17 (Quarkus distro)](https://keycloak.discourse.group/t/use-of-jdbc-ping-with-keycloak-17-quarkus-distro/13571/29)

[Embedding Infinispan caches in Java applications](https://infinispan.org/docs/dev/titles/embedding/embedding.html#jgroups-cloud-discovery-protocols_cluster-transport)

[Keycloak Server caching](https://www.keycloak.org/server/caching)

[Clustered Keycloak SSO Deployment in AWS](https://www.dae.mn/insights/clustered-keycloak-sso-deployment-in-aws) was originally published on the [Daemon Insights blog](https://www.dae.mn/insights)
