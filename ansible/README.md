[![Build Status](https://travis-ci.org/yokobot/snippet.svg?branch=master)](https://travis-ci.org/yokobot/snippet)

### 概要
AWSアカウントに新規でEC2を構築した時に設定する項目をansible化  
  
- JST対応
- ホスト名をNameタグの値にする  

### Dir構成

```
$ tree ansible/
ansible/
├── README.md
├── ansible.cfg
├── ec2.yml
├── group_vars
├── inventories
│   ├── ec2.py
│   └── tests
│       └── test_ec2.py
├── roles
│   └── common
│       └── tasks
│           └── main.yml
└── site.yml
```
  
### 設定情報
  
- README.md
    - これ
- ansible.cfg
    - default-userにec2-userを指定
- ec2.yml
    - hostsとroleを指定
- inventories 
    - AWSアカウント内のEC2(Public-IPを持っているかつステータスがrunnig)を取得
- roles
    - 今回はcommonのみ
        - JST
        - hostname
- site.yml
    -  ec2.ymlをインクルードしている

### Usage

```
$ ansible-playbook -i inventories/ec2.py site.yml --private-key=pemファイル 
```


