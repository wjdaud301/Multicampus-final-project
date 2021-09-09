## ✔ Trouble shooting



### AWS EC2 Server reboot 이후 namenode 실행이 안될 때



##### 1. 문제

AWS EC2 인스턴스를 띄워 hdfs를 설치하고 $HADOOP_HOME/sbin/start-dfs.sh로 dfs와 yarn을 실행하였다.
하지만 저녁 6시이후 강제로 인스턴스를 종료하고 다음날 아침에 같은 방식으로 start-dfs.sh을 실행하면 namenode가 실행되지 않는 문제가 발생했다. 

그래서 계속 `$HADOOP_HOME/bin/hadoop namenode -format`을 통해 hadoop을 재시작 했다.







##### 2. 해결

hadoop을 설치하고 실행할 때, $HADOOP_HOME/etc/hadoop/hdfs-site.xml 파일 수정을 통해 hadoop에 여러세팅값을 주게 된다.

 이때, **dfs.name.dir** 값과 **dfs.data.dir** 값을 지정해주지 않으면 **default가 /tmp/ 디렉토리 어딘가**로 잡히게 되는데  <u>이 데이터들은 EC2 인스턴스가 reboot시 초기화 된다.</u>

 그렇기 때문에 reboot 후 $HADOOP_HOME/sbin/start-dfs.sh를 통해 namenode를 실행시켜도 이미 /tmp/폴더가 초기화되어 올바르게 실행되지 않는 것이다.



### core-site.xml

기존 :  

```xml
<configuration>     
      <property>         
            <name>fs.defaultFS</name>         
            <value>hdfs://localhost:9000</value>     
      </property> 
</configuration>
```



변경 후 : 

```xml
<configuration>     
      <property>         
            <name>fs.defaultFS</name>         
            <value>hdfs://localhost:9000</value>     
      </property> 
</configuration>

<configuration>     
      <property>         
            <name>dfs.name.dir</name>         
            <value>/home/ubuntu/pseude/dfs/name</value>     
      </property> 
</configuration>

<configuration>     
      <property>         
            <name>dfs.data.dir</name>         
            <value>/home/ubuntu/pseude/dfs/data</value>     
      </property> 
</configuration>
```





##### 3. 버전

Java : openjdk 11.0.11

hadoop : 3.2.2
