##  👍 AWS EC2 인스턴스 VSCode로 연결하기



EC2 인스턴스에 접속하여 VScode로 코드를 수정하는 이유는 불편하기 때문이다. 

Ubuntu환경에서 python 파일을 작업하는 것보다 local환경 VScode를 이용하여 편리하게 작성하자!



### 1. ftp-simple 설치

VScode에서 `ctrl+shift+x`를 눌러 extensions를 띄운다

ftp-simple 파일을 찾아서 설치한다.



### 2. FTP connection setting

`ctrl+shitt+p`를 눌러 Command Pallette를 열고  ">ftp-simple"을 입력한 뒤 ftp-simple: Config - FTP connection setting을 클릭한다.

그리고 파일을 아래와 같은 형식으로 입력한다.

```web-idl
[
	{
		"name": "aws-env",  # ftp 연결된 이름 (임의로 지정 가능)
		"host": "AWS EC2 public IP주소",  
		"port": 22,     # SSH 연결이면 port 22
		"type": "sftp",
		"username": "ubuntu",  # putty 설정 때 host name
		"password": "",
		"path": "/home/ubuntu/",
		"autosave": true,
		"confirm": false,
		"privateKey": "D:/aws-key/backend.pem" # aws pem key
	}
]
```



- SSH는 22번 포트를 사용
- username은 SSH에 접속할 때 IP 주소 앞에 붙는 이름 (ubuntu)
- path는 아마존 EC2의 경로
- privateKeyPath가 아닌 **PrivateKey**를 키 값으로 주어야 한다.



### 3. 다운로드

`ctrl+shitt+p`를 눌러 Command Palette를 열고 ">ftp-simple"을 입력한 뒤 

ftp-simple: Remote directory open to workspace을 클릭한 후 

위에서 지정했던 ftp 연결 name을 클릭하면 상세 directory를 지정하여 열 수 있다.



[참고 링크]

https://share4share.tistory.com/32