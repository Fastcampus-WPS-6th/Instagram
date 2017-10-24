# Instagram

## 깜빡했다

## Requirements

- Python 3.6.2

## Secret config JSON files

`.config_secret/settings_common.json`

```json
{
  "django": {
    "secret_key": "<Django secret key value>"
  }
}
```

## 페이스북 로그인 과정

1. 사용자가 우리 사이트에서 '페이스북 로그인'버튼 클릭
2. 우리 사이트에서 '그럼 페이스북 가서 로그인하고 응답을 받아오세요'
3. 사용자는 페이스북으로 이동해서 로그인과 권한 인가를 완료함
4. 사용자가 로그인을 완료한 후 페이스북은 redirect_uri위치로 사용자가 로그인한 정보(code)를 브라우저에 리디렉션 요청
	4-1. 바로 액세스 토큰을 보내주지않음
	4-2. APP_ID는 공개정보이기 때문에, SECRET_CODE를 사용해 컨슈머를 인증해야함
5. 브라우저는 리디렉션 요청을 받아 우리 사이트에 GET요청
6. 브라우저는 GET요청에 포함된 code정보를 이용해 페이스북 서버에 access_token을 요청
7. 페이스북이 access_token을 돌려줌
8. (선택사항) access_token을 디버그함
9. access_token을 이용해 UserInfo를 graphAPI에 요청해 받아옴
10. 받아온 UserInfo에 해당하는 User가 우리의 DB에 있는지 검사
	10-1. 있으면 해당 user를 로그인
	10-2. 없으면 정보로 유저를 만들어 로그인
11. post_list로 리다이렉트