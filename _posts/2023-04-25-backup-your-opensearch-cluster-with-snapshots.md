---
title: Backup your OpenSearch indices with manual snapshots
tags: [How to, AWS, OpenSearch, DevOps, Article]
canonicalurl: https://www.dae.mn/insights/backup-your-opensearch-indices-with-manual-snapshots
layout: post
---

You're making a change to your OpenSearch managed service and it's all going great - right up until you make a mistake, destroying your cluster and causing you to lose all your indices. If only you had a snapshot you could restore your cluster from? Too bad you didn't create any. 

![Kermit the frog makes a rookie devops error]({{ site.baseurl }}/assets/images/kermit1.png)

Taking OpenSearch snapshots is relatively easy but may require making some configuration changes to your IAM roles. It's definitely worth doing because once you've successfully taken a snapshot you can use it to restore the indices in deleted, destroyed, or corrupted OpenSearch clusters or even create a duplicate cluster with the same data.

### Prerequisites

In order to manually take snapshots you'll need admin access to your OpenSearch service API either [via curl](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-snapshots.html#:~:text=every%20half%20hour.-,Take%20a%20snapshot,-You%20specify%20the) or OpenSearch devtools, in this guide I'll be using the latter method.

Before taking a snapshot you will need to create a role that will allow your OpenSearch service to write the snapshot to an S3 bucket and grant permission to the OpenSearch service to use that role. The Terraform for your IAM config should look something like the below, for more details see the [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html#add-policies-console).

_IAM role_
```
resource aws_iam_role" "es_snapshot" {
  name                 = "es-snapshot"
  managed_policy_arns  = [aws_iam_policy.es_snapshot.arn]
  assume_role_policy   = <<EOF
{
"Version" : "2012-10-17",
"Statement" : [{
    "Sid" : "",
    "Effect" : "Allow",
    "Principal" : {
    "Service" : "es.amazonaws.com"
    },
    "Condition" : {
    "StringEquals" : {
        "aws:SourceAccount" : "<your aws account id>"
    },
    "ArnLike" : {
        "aws:SourceArn" : "<the arn for your opensearch cluster>"
    }
    },
    "Action" : "sts:AssumeRole"
}]

}
  EOF
}
```

Note the condition in the above terraform statement: this limits access to this role to a specific OpenSearch service with your AWS account, without it any OpenSearch service could assume this role.

_IAM policy_
```
resource "aws_iam_policy" "es_snapshot" {
  name = "es-snapshot-policy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [{
      "Action" : [
        "s3:ListBucket"
      ],
      "Effect" : "Allow",
      "Resource" : [
        "<arn of the s3 bucket you want to store your snapshots in>"
      ]
      },
      {
        "Action" : [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ],
        "Effect" : "Allow",
        "Resource" : [
          "<arn of the s3 bucket you want to store your snapshots in>/*"
        ]
      }
    ]
  })
}
```

### Register a snapshot repository

In order to take a snapshot you first need to configure a snapshot repository to store your snapshots. In this guide I'll be covering how to do this using an S3 bucket

First, if there isn't one already you will need to register a snapshot repository, you can use the get request below to list any existing repositories (do not use _cs-automated-enc_, it is reserved by OpenSearch for automated snapshots).
```
GET _cat/repositories
```

If needed, register a new snapshot repository like so (note the use of the role we created in the previous section).
```
PUT _snapshot/opensearch-snapshots
{
  "type": "s3",
  "settings": {
    "bucket": "<your s3 bucket name>",
    "region": "eu-west-1",
    "role_arn": "<arn of your snapshot role>",
    "server_side_encryption": true
  }
}
```

### Manually taking a snapshot

Check for any ongoing snapshots, you cannot take a snapshot if one is already in progress and OpenSearch automatically takes snapshots periodically.
```
GET _snapshot/_status
```

Take a snapshot. Adding the data to the end of the snapshot name is optional, but I'd recommend adding the correct time here so you can easily find the snapshot if you need to restore from it later.
```
PUT _snapshot/opensearch-snapshots/snapshot-2023-03-13-1135
```

Check snapshot progress with the first get request below and then view it with the second once complete. Use of the “pretty” query is not required but helps to make the output more readable.
```
GET _snapshot/_status
GET _snapshot/opensearch-snapshots/_all?pretty
```

You should see your snapshot listed alongside any pre-existing snapshots. Congratulations, you’re now ready to restore from a snapshot should you ever need to. Don’t stop here though, I recommend that you continue with the next section to familiarise yourself with the process of restoring from a snapshot - you should also take snapshots regularly to help reduce the risk of data loss.

### Restoring from a snapshot


Check for snapshot repositories, if the cluster was destroyed you will need to re-add the snapshot repository that contains the snapshot you will be restoring from.
```
GET _cat/repositories
```

Re-register your snapshot repository if necessary (if the cluster is destroyed and recreated OpenSearch will not be aware of the pre-existing repositories even though they still exist in your S3 bucket) using the same command you used to register it initially.
```
PUT _snapshot/opensearch-snapshots
{
  "type": "s3",
  "settings": {
    "bucket": "<your s3 bucket name>",
    "region": "eu-west-1",
    "role_arn": "<arn of your snapshot role>",
    "server_side_encryption": true
  }
}
```

You can now view all the available snapshots in your repository.
```
GET _snapshot/opensearch-snapshots/_all?pretty
```

You should see your each of your snapshots output something like this.
```
1| snapshot-2023-03-13-1450 SUCCESS 1678978233 14:50:33 1678978966 15:02:46 12.2m 61 135 0 135
```

Check for any existing indexes and delete them if they exist in your snapshot, as restored indices may share the same name as those in the snapshot so in order to restore them it is recommended to delete all of the indices in your cluster prior to recovering from a snapshot (alternatively you can exclude these indices by adding them to the indices parameter and mark them to be ignored with “-” in the next step).
```
GET _cat/indices
DELETE _all
```

Restore data indexes from your chosen snapshot, note that we're excluding the Opendistro indices here. These are used for storing data about the cluster and are created automatically, we don't need to restore them from the snapshot and if we attempt to we will be unable to restore as they will clash with the snapshot version.
```
POST _snapshot/opensearch-snapshot/snapshot-2023-03-13-1135/_restore
{"indices": "-.opendistro*"}
```

Check the progress of index recovery with the get request below, this will return a list of all the indices that are being restored along with the progress of restoring each to the cluster. When this call returns null, the recovery process is complete.
```
GET _cat/recovery
```

You can now check the indices on your cluster using the below get request.
```
GET _cat/indices
```

Congratulations, you’ve successfully restored your cluster from a snapshot. If you’ve been following this guide through from the start you should now be equipped to use snapshots to protect your indices against data loss. If you’ve just used this guide to restore your OpenSearch cluster after a real issue I’m glad that we could help out, now relax in the knowledge that your data is safe.

 ![Kermit relaxes after resolving a devops issue]({{ site.baseurl }}/assets/images/kermit2.jpeg)

### Resources

[Manage OpenSearch domain snapshots](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-snapshots.html)  
[Adding IAM Identity Permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html#add-policies-console)  
[Modifying a role trust policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-console.html#roles-managingrole_edit-trust-policy)

[Backup your OpenSearch indices with manual snapshots](https://www.dae.mn/insights/backup-your-opensearch-indices-with-manual-snapshots) was originally published on the [Daemon Insights blog](https://www.dae.mn/insights)