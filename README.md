[![Build Status](https://travis-ci.org/yokobot/snippet.svg?branch=master)](https://travis-ci.org/yokobot/snippet)

# snippet

## 構成

```
snippet/
├── README.md
├── ansible
└── aws
    ├── cloudformation
    └── lambda

```

### ansible
ansible/ec2.yml  
-> AWS 初期構築時に実行する ansible
  
### aws/cloudformation
aws/cloudformation/alb.template.yaml
-> ALB, ALB 用 Security Group, S3 logbucket, bucketpolicy を構築する CFn
  
aws/cloudformation/api_gateway.template.yaml
-> API, Resource, POST Method, S3 logbucket, ロールを構築する CFn
  
aws/cloudformation/bastion.template.yaml
-> 踏み台用 EC2 インスタンスこを構築する CFn
  
aws/cloudformation/ecs_web_cluster.template.yaml  
-> パブリック公開用の ECS クラスタを構築する CFn  
-> cluster, SG, ALB-listener, ALB-target-group, autoscale 設定, EC2 起動設定, EC2 ロール  
  
aws/cloudformation/ecs_worker_cluster.template.yaml  
-> 内部処理用の ECS クラスタを構築する CFn  
-> cluster, SG, autoscale 設定, EC2 起動設定, EC2 ロール  
  
aws/cloudformation/elasticache.template.yaml  
-> ElastiCache(Redis), ElastiCache 用 Security Group を構築する CFn 
  
aws/cloudformation/elasticsearch.template.yaml
-> ElasticSearchService, kibana proxy instance, lambda function を構築する CFn
  
aws/cloudformation/elb.template.yaml  
-> ELB, ELB 用 Security Group を構築する CFn  
  
aws/cloudformation/fargate_cluster.template.yaml
-> Fargeta 用のクラスタを構築する CFn
  
aws/cloudformation/fargate_service.template.yaml
-> Fargeta 用のサービス、タスクを構築する CFn
  
aws/cloudformation/kinesis.template.yaml
-> kinesis stream, firehose, S3 logbucket, ロールを構築する CFn
  
aws/cloudformation/pipeline.template.yaml
-> code-build, code-pipelinei, S3 logbucket, ロール を構築する CFn
  
aws/cloudformation/rds.template.yaml
-> postgreSQL RDS インスタンス, Internal DNS record を構築する CFn
  
aws/cloudformation/route53_internal.template.yaml
-> Internal 向け干すテッドゾーンを構築する CFn
  
aws/cloudformation/vpc.template.yaml  
-> VPC, route-table, internet-gateway, nat-gateway, subnet を構築する CFn
  
### aws/lambda
aws/lambda/console_login_check.py  
-> 24 時間以内に AWS アカウントに console login した(試みた)ユーザを slack に通知する lambda function
  
