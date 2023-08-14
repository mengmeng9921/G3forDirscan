# G3forDirscan
多线程目录扫描工具


0.使用帮助

python3 G3forDirscan.py -h

1.简单使用

python3 G3forDirscan.py -u URL

2.指定字典

python3 G3forDirscan.py -u URL -df "dicc.txt"

3.指定路径爆破

python3 G3forDirscan.py -u URL -d "\index.php"

4.指定URL字典扫描单一路径

python3 G3forDirscan.py -uf "url.txt" -d "\index.php"

5.指定URL字典路径字典交叉扫描

python3 G3forDirscan.py -uf "url.txt" -df "dicc.txt"

6.只获取单一状态码的路径

python3 G3forDirscan.py -u URL -sf 200

7.指定线程

python3 G3forDirscan.py -u URL -t 20
