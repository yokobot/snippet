[![Build Status](https://travis-ci.org/yokobot/snippet.svg?branch=master)](https://travis-ci.org/yokobot/snippet)

## 概要
AWS アカウントに 24 時間以内に console login をした(試みた)ユーザを slack に通知する lambda function  
一日一回 cloud watch logs event でキックする  
  
## 構成

```
$ tree aws/lambda/
aws/lambda/
├── README.md
├── console_login_check.py
└── tests
    └── test_console_login_check
```
  
## 処理

- cloud trail から過去 24 時間以内の console login event を抽出する
- slack 通知用の配列を作成する
- slack web API を使用して slack に通知する

## 設定

- lambda function には cloud trail の READ 権限のある role が必要
- 環境変数 SLACK_URL に  slack incoming webhook URL を定義する
  
