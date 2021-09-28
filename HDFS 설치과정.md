## ## AWS EC2 :: Hadoop HDFS 설치과정 정리



#### 1. Java Install 

```shell
# openjdk가 있으면 생략 가능!

# java install
$ sudo apt-get install openjdk-8-jdk

# java 설치 확인
$ java -version
```



---



#### 2. 하둡을 다운 받고 셋팅

```shell
# ubuntu에서 file download
$ wget http://apache.claz.org/hadoop/common/hadoop-3.2.2/hadoop-3.2.2.tar.gz

# tar.gz 압축 해제
$ tar -xzvf hadoop-3.2.2.tar.gz

# /usr/local/hadoop directory로 파일 옮기기
$ sudo mv hadoop-3.2.2 /usr/local/
```



---



#### 3. SSH 설정

```shell
$ sudo apt-get install ssh
$ sudo service ssh restart
$ ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
$ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
$ chmod 0600 ~/.ssh/authorized_keys
$ ssh localhost
```



---



#### 4. 환경변수 추가

```bash
$ nano ~/.bashrc  # => nano 대신 vim, vi 써도 상관없음

### .bashrc에 추가할 내용
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 # 설치한 java 버전으로 입력
export HADOOP_HOME=/usr/local/hadoop-3.2.2 # 설치한 hadoop 버전으로 입력
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop

# bashrc 추가한 내용실행
$ source ~/.bashrc
```



---



#### 5. 하둡 환경변수 추가

```shell
# hadoop-env.sh 내용 변경
$ nano /usr/local/hadoop-3.2.2/etc/hadoop/hadoop-env.sh

# export JAVA_HOME 있는 부분 찾아서 아래 내용으로 변경
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 # .bashrc에 입력한 JAVA_HOME과 동일
```



---



#### 6. Web UI Setting

```html
# HADOOP_HOME 에서 모두 진행
$ vi etc/hadoop/core-site.xml


<configuration>     
      <property>         
            <name>fs.defaultFS</name>         
            <value>hdfs://localhost:9000</value>     
      </property> 
</configuration>
```

```html
$ cp etc/hadoop/mapred-site.xml.template etc/hadoop/mapred-site.xml
$ vi etc/hadoop/mapred-site.xml


<configuration>     
      <property>         
            <name>mapreduce.framework.name</name>         
            <value>yarn</value>     
      </property>
      <property>
            <name>mapreduce.application.classpath</name>
            <value>$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/mapreduce/lib/*</value>
      </property>
</configuration>
```

```html
$ vi etc/hadoop/yarn-site.xml


<configuration>     
      <property>         
            <name>yarn.nodemanager.aux-services</name>         
            <value>mapreduce_shuffle</value>     
      </property> 
      <property>
            <name>yarn.resourcemanager.hostname</name>
            <value>localhost</value>
      </property>
</configuration>
```



---



#### 7. NameNode format (최초 1번)

```shell
# format namenode
$ bin/hadoop namenode -foramt


# run DFS daemons
$ sbin/start-dfs.sh
$ jps
Jps
NameNode
DataNode
SecondaryNameNode 


# run YARN daemons
$ sbin/start-yarn.sh
$ jps
SecondaryNameNode
DataNode
Jps
ResourceManager
NameNode
NodeManager


# DFS와 YARN daemons 모두 한번에 키고 끄기
$ sbin/start-all.sh #(추천)
$ sbin/stop-all.sh
```





---



#### 8. Web UI 접속

namenode web ui => hadoop-3.0.0 부터는 **localhost:9870 **

resource manager web ui => **localhost:8088 **





---



#### 9. HDFS 명령어 (많이 쓰이는 것들 위주로 정리)

**1) appendToFile**

- Local 파일들을 hdfs에 append 저장하기 위한 목적

```sh
hdfs dfs -appendToFile {localsrc} ... {dst}
```



**2) cat**

- 해당 파일을 stdout으로 찍어서 보여준다. (linux 명령어 cat과 동일)

```sh
 hdfs dfs -cat URI [URI ...]
```



**3) chmod**

- 해당 파일의 오너이거나 슈퍼오너라면, 특정 파일의 permission 수정. -R 옵션과 함께라면 예하 파일들에 대해서 동일하게 permission 적용 가능

```sh
hdfs dfs -chmod [-R] {MODE[,MODE]... | OCTALMODE} URI [URI ...]
```



**4) chown**

- 슈퍼오너일 경우 해당 파일의 owner를 변경

```sh
hdfs dfs -chown [-R] [OWNER][:[GROUP]] URI [URI ]
```



**5) copyFromLocal**

- Local 파일을 hdfs에 업로드. put명령어와 유사 (중요)

```sh
hdfs dfs -copyFromLocal {localsrc} URI
```



**6)  copyToLocal**

- Hdfs에 있는 파일을 local directory에 다운로드, get 명령어와 유사 (중요)

```sh
hdfs dfs -copyToLocal [-ignorecrc] [-crc] URI {localdst}
```



**7) cp**

- <u>Hdfs내부에서 파일을 복붙함.</u> 만약 복사하고자 하는 대상이 여러개라면 붙여넣는 곳은 반드시 Directory여야 한다.

```sh
 hdfs dfs -cp [-f] [-p | -p[topax]] URI [URI ...] {dest}
```



**8) du**

- Hdfs내부의 특정 file이나 directory의 size를 보여줌

```sh
hdfs dfs -du [-s] [-h] URI [URI ...]
```



**9) get**

- Hdfs의 파일을 local directory로 다운로드 (중요)

```sh
hdfs dfs -get [-ignorecrc] [-crc] {src} {localdst}
```



**10) getfattr**

- Hdfs의 특정 파일 혹은 디렉토리의 속성 정보들을 나열, 보여줌

```sh
hdfs dfs -getfattr [-R] -n name | -d [-e en] {path}
```



**11) ls**

- 특정 디렉토리의 파일 혹은 디렉토리를 보여줌

```sh
hdfs dfs -ls [-R] {args}
```



**12) mkdir**

- 특정 path에 directory 생성

```sh
hdfs dfs -mkdir [-p] {paths}
```



**13) movefromLocal** ***

- Local의 파일을 hdfs에 저장. put과 비슷하지만 저장 이후 local file은 삭제

````sh
hdfs dfs -moveFromLocal {localsrc} {dst}
````



**14) moveToLocal** ***

- Hdfs의 파일을 local에 저장. get과 비슷하지만 저장 이후 hdfs file은 삭제

```sh
hdfs dfs -moveToLocal [-crc] {src} {dst}
```



**15) mv**

- Hdfs내부에서 파일을 옮김

```
 hdfs dfs -mv URI [URI ...] {dest}
```



**16) put**

- Local의 파일들을 hdfs에 저장

```sh
hdfs dfs -put {localsrc} ... {dst}
```



**17) rm**

- Hdfs의 특정 폴더 혹은 파일을 삭제

```sh
hdfs dfs -rm [-f] [-r|-R] [-skipTrash] URI [URI ...]
```



**18) rmr**

- rm -r과 동일한 명령어

```sh
hdfs dfs -rmr [-skipTrash] URI [URI ...]
```



**19) setrep**

- Hdfs의 특정 파일에 대해 replication factor을 수정

```sh
hdfs dfs -setrep [-R] [-w] {numReplicas} {path}
```



 **20 )tail**

- 특정 file에 대해 마지막 kilobyte을 stdout으로 보여줌

```sh
hdfs dfs -tail [-f] URI
```



**21) text**

- Hdfs의 특정 파일을 text format으로 확인

```sh
hdfs dfs -text {src}
```



**22) touchz**

- Zero length인 file을 생성

```sh
hdfs dfs -touchz URI [URI ...]
```



---



### * 중요 :: AWS EC2에서 외부 노드접속시 tunneling 필요

- putty -> SSH -> Auth -> Tunnels
- Source port =>  9870 / Destination => 127.0.0.0:9870    ->   add  -> save
- Source port =>  8088 / Destination => 127.0.0.0:8088    ->   add  -> save



