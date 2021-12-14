# 第一章 Sqoop简介

Sqoop是一个在关系型数据库与Hadoop平台之间进行数据互导的工具。

# 第二章 Mysql与Hadoop平台互导

## 1.1 MySQL导入HDFS

MySQL中提前准备好数据，测试导入到HDFS

- **不指定导出目录、字段分隔符**

  ```shell
  # import 导入
  # --connect 指定mysql连接地址，数据库为sqooptest
  # --username mysql用户名
  # --password mysql密码
  # --table 指定要导出的表Person
  # --m 指定map task数，默认是4个
  [hadoop@node01 ~]$ sqoop import --connect jdbc:mysql://node01:3306/sqooptest --username root --password 123456 --table Person --m 1
  ```

     导出到HDFS后，默认保存位置为/user/hadoop/数据库表名

- **指定导出目录、字段分隔符**

  ```shell
  [hadoop@node01 ~]$ sqoop import \
  > --connect jdbc:mysql://node01:3306/sqooptest \   
  > --username root \
  > --password 123456 \
  > --table Person \
  > --target-dir /sqoop/person \  # 指定导出目录
  > --delete-target-dir \ # 如果导出目录存在，就先删除
  > --fields-terminated-by '\t' \  # 指定字段数据分隔符
  > --m 1
  ```

- **导入表的数据子集**

  ```shell
  [hadoop@node01 ~]$ sqoop import \
  > --connect jdbc:mysql://node01:3306/sqooptest \
  > --username root --password 123456 \
  > --table Person \
  > --target-dir /sqoop/person_where \
  > --delete-target-dir \
  > --where "name = 'messi'" \ # where指定条件  按照name条件过滤messi
  > --m 1 
  ```

- **指定sql查询条件过滤数据**

  ```shell
  [hadoop@node01 ~]$ sqoop import \
  > --connect jdbc:mysql://node01:3306/sqooptest \
  > --username root \
  > --password 123456 \
  > --target-dir /sqoop/person_sql \
  > --delete-target-dir \
  > --query 'select * from Person where age>20 and $CONDITIONS' \ 
  > --split-by 'id' \
  > --m 2
  ```

  ==只要有--query+sql，就需要加$CONDITIONS，哪怕只有一个maptask==。

  ==如果只有一个maptask，可以不加--split-by来区分数据，因为处理的是整份数据，无需切分==。

  **原理**：

  当sqoop使用--query+sql执行多个maptask并行运行导入数据时，每个maptask将执行一部分数据的导入，原始数据需要使用'--split-by 某个字段'来切分数据，不同的数据交给不同的maptask去处理。maptask执行sql副本时，需要在where条件中添加$CONDITIONS条件，这个是linux系统的变量，可以根据sqoop对边界条件的判断，来替换成不同的值，这就是说若split-by id，则sqoop会判断id的最小值和最大值判断id的整体区间，然后根据maptask的个数来进行区间拆分，每个maptask执行一定id区间范围的数值导入任务，如下为示意图。

  ![](Sqoop基础.assets\1.png)

## 1.2MySQL导入到Hive

导出数据到hive前，需要将hive中的一个包(hive-exec-1.1.0-cdh5.14.2.jar)拷贝到sqoop的lib目录。

- 手动创建hive表后导入

​	先手动在hive中建一个接收数据的表，这里指定的分隔符和sqoop导出时的分隔符要一致。

​	1. 创建数据库

```sql
hive (default)> create database sqooptohive;
OK
Time taken: 0.185 seconds
hive (default)> use sqooptohive;
OK
Time taken: 0.044 seconds
```

2. 创建表

```sql
hive (sqooptohive)> create external table person(id int,name string,age int,score int,position string)row format delimited fields terminated by '\t';
OK
Time taken: 0.263 seconds
hive (sqooptohive)> show tables;
OK
tab_name
person
```

3. sqoop导出数据到hive表中。

```sql
[hadoop@node01 ~]$ sqoop import \
> --connect jdbc:mysql://node01:3306/sqooptest \
> --username root \
> --password 123456 \
> --table Person \
> --fields-terminated-by '\t' \  # 这里需要和hive中分隔指定的一样
> --delete-target-dir \
> --hive-import \  # 导入hive
> --hive-table sqooptohive.person \  #hive表
> --hive-overwrite \ # 覆盖hive表中已有数据
> --m 1
```

- 导入时自动创建hive表

​	也可以不需要提前创建hive表，会自动创建。

```sql
[hadoop@node01 ~]$ sqoop import \
> --connect jdbc:mysql://node01:3306/sqooptest \
> --username root \
> --password 123456 \
> --table Person \
> --hive-import \
> --hive-database sqooptohive \
> --hive-table person1 \
> --m 1
```


​	导入后，发现数据库下多了一个表person1。



## 1.3 MySQL导入数据到HBase

也可以将数据导入到hbase，依然使用sqooptest.Person表，导入前集群需启动zookeeper和hbase。

```sql
[hadoop@node01 ~]$ sqoop import \
> --connect jdbc:mysql://node01:3306/sqooptest \
> --username root \
> --password 123456 \
> --table Person \
> --hbase-table mysqltohbase \ # 指定hbase表名
> --hbase-create-table \ # hbase没有表就创建表
> --column-family f1 \ # 指定列族
> --hbase-row-key id \ # 执行rowkey
> --m 1
```

执行完成后，hbase中查看发现新建了一张表，并且成功导入数据。

导出数据 

## 1.4 从HDFS导出到MySQL

hdfs中先准备数据

```sql
[hadoop@node01 ~]$ hadoop fs -cat /hdfstomysql.txt
20/02/06 14:31:17 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
1 messi 32 50
2 ronald 35 55
3 herry 40 51
```


mysql中需要先建表，否则会报错。


```sql
CREATE TABLE sqooptest.hdfstomysql (
    id INT NOT NULL,
    name varchar(100) NOT NULL,
    age INT NOT NULL,
    score INT NOT NULL
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COLLATE=utf8_general_ci;
```


sqoop命令执行导出。


```sql
[hadoop@node01 ~]$ sqoop export \
> --connect jdbc:mysql://node01:3306/sqooptest \
> --username root \
> --password 123456 \
> --table hdfstomysql \  # 提前建立好的表
> --export-dir /hdfstomysql.txt \ # hdfs中目录文件
> --input-fields-terminated-by " " # 指定文件数据的分隔符
```

## 1.5 从Hive导出到MySQL

```sh
[hadoop@node01 ~]$ sqoop export \
> --connect jdbc:mysql://node01:3306/sqooptest \
> --username root \
> --password 123456 \
> --table hdfstomysql \  # 提前建立好的表
> --export-dir /user/hive/warehouse/uv/dt=2011-08-03 \ # hdfs中存储的hive表
> --input-fields-terminated-by " " # 指定文件数据的分隔符
```

## 1.6 从HBase导出到MySQL

默认的没有命令直接将hbase中的数据导入到MySQL，因为在hbase中的表数据量通常比较大，如果一次性导入到MySQL，可能导致MySQL直接崩溃。

如果要将hbase数据导出到mysql，工具方面，可以用两种方法。

第一种，将hbase导出成hdfs平面文件，然后用sqoop导出到mysql。

第二种，将hbase数据导出到hive，再用sqoop导出到mysql。

如果想提高效率和进行更多控制，可以直接Java API的方式，从hbase中读出数据，导出到mysql。

# 参考文献

> 《sqoop使用入门》https://www.cnblogs.com/youngchaolin/p/12253859.html#_label2_0
