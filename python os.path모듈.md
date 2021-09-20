## Python os.path 모듈



- 코드 내에서 직접 파일을 다루는 경우 `os.path`모듈을 사용하게 된다.



1. abspath(path)

   path의 절대 경로를 반환, 입력받은 path에는 파일 혹은 폴더 이름이 들어온다.

   ```python
   import os.path
   os.path.abspath('Django')
   ```

   ```
   C:\\Users\\jm\\Django'
   ```

   

2. basename(path)

   path의 기본이름을 반환한다. 입력받은 path에는 절대경로가 들어온다. (abspath의 반대)

   ```python
   import os
   os.path.basename('Django')
   ```

   ```
   'Django'
   ```



3. dirname(path)

   path의 파일/디렉토리 경로를 반환한다.

   ```python
   import os.path
   os.path.dirname('C:\\Users\\jm\\Django')
   ```

   ```
   'C:\\Users\\jm\\'
   ```



4. exists(path)

   입력받은 path가 존재하면 True, 존재하지 않으면 False를 반환

   ```python
   import os.path
   os.path.exists('C:\\Users\\jm\\Django')
   ```

   ```
   True
   ```

   

5. isdir(path)

   path가 디렉토리이면 True, 아니면 False를 반환

   ```python
   import os.path
   os.path.isdir('C:\\Users\\jm\\Django')
   ```

   ```
   True
   ```



6. join(path1, path2, ...)

   OS의 형식에 맞게 각각의 경로들을 하나의 경로로 이어준다.

   ```python
   import os.path
   os.path.join('C:\\Users','jm','Django')
   ```

   ```
   'C:\\Users\\jm\\Django'
   ```



7. normpath(path)

   path에서 `.`/`..` 과 같은 구분자를 제거해 path를 정규화시킨다.

   원래 path의 패턴으로 만들어준다.

   ```python
   import os.path
   os.path.normpath('C:\\Users\\..\\jm\\.\\Django')
   ```

   ```
   'C:\\jm\\Django'
   ```

   

8. split(path)

   path를 <b>`디렉토리`</b>와 <b>`파일`</b>로 분리한다.

   ```python
   import os.path
   os.path.split('C:\\Users\\jm\\Django\\temp.txt')
   ```

   ```
   'C:\\Users\\jm\\Django','temp.txt'
   ```



### glob

glob는 파일들의 리스트를 뽑을 때 사용한다.

```python
from glob import glob

glob('*.exe')
출력 : ['python.exe', 'pythonw.exe']

glob(r'C:\U*')  #  C:\에서 이름이 U로 시작하는 디렉터리나 파일을 찾기
출력 : ['C:\\Users', 'C:\\usr']
```

