# du-n2m

DU Notification to mail

학사공지를 메일로 받아 볼 수 있습니다.

## 요구사항

1. python 3.8 (3.8.5 에서 테스트됨)
2. `pip3 install beautifulsoup4 htmlmin requests`
3. starttls 를 지원하는 smtp 서버

## 세팅

1. config.sample.json 을 config.json 으로 이름을 바꾸십시오.
2. config.json 의 first_run 을 true 로 세팅한 뒤 스크립트를 1회 동작시키십시오.
3. config.json 의 first_run 을 false 로 세팅하고 메일 계정 정보를 입력하십시오.
4. 서버에 스크립트를 계속 켜 두면 됩니다. 60초마다 자동으로 데이터를 가져옵니다.

## config.json
```json
{
  "account": {
    "id": "메일 계정 ID (example@example.com)",
    "pw": "메일 계정 암호"
  },
  "sendto": "수신자 메일 주소",
  "sender": "송신자 메일 주소",
  "server": {
    "addr": "smtp 서버 주소",
    "port": 587
  },
  "store_cnt": 100,
  "no_get_page": 5,
  "first_run": false
}
```