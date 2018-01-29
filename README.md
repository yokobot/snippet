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
aws/cloudformation/vpc.template.yaml  
-> VPC, route-table, internet-gateway, nat-gateway, subnet を構築する CFn
  
aws/cloudformation/elb.template.yaml  
-> ELB, ELB 用 Security Group を構築する CFn  
  
aws/cloudformation/alb.template.yaml  
-> ALB, ALB 用 Security Group, S3 logbucket, bucketpolicy を構築する CFn
  
aws/cloudformation/ecs_web_cluster.template.yaml  
-> パブリック公開用の ECS クラスタを構築する CFn  
-> cluster, SG, ALB-listener, ALB-target-group, autoscale 設定, EC2 起動設定, EC2 ロール  
  
aws/cloudformation/ecs_worker_cluster.template.yaml  
-> 内部処理用の ECS クラスタを構築する CFn  
-> cluster, SG, autoscale 設定, EC2 起動設定, EC2 ロール  
  
### aws/lambda
aws/lambda/console_login_check.py  
-> 24 時間以内に AWS アカウントに console login した(試みた)ユーザを slack に通知する lambda function
