[![Build Status](https://travis-ci.org/yokobot/snippet.svg?branch=master)](https://travis-ci.org/yokobot/snippet)

# snippet

## 構成

```
snippet/
├── README.md
├── ansible
└── aws
    └── lambda
```

### ansible
ansible/ec2.yml  
-> AWS 初期構築時に実行する ansible

### aws/lambda
aws/lambda/console_login_check.py  
-> 24 時間以内に AWS アカウントに console login した(試みた)ユーザを slack に通知する lambda function

### aws/cloudformation
TBD  
