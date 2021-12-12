# Hive

Hive是一个基于Hadoop的数据仓库工具，可以用于对Hadoop文件中的数据集进行整理、查询、分析。Hive提供了类似于SQL的HiveQL，HiveQL可以转化为MapReduce任务进行运行，而不必开发专门的MapReduce应用。

## 安装Hive

1. 嵌入模式的安装特点：不需要MySQL数据库的支持，使用Hive自带的数据块Derby。但只支持一个数据库连接。
2. 本地模式的安装特点：采用MySQL数据库存储数据。
3. 远程模式的安装特点：如果有其他主机已经启动了Metastore服务（hive --service metastore），参考本地模式的安装步骤并修改配置文件hive-site.xml即可。

## Hive的数据类型和存储格式

Hive 的基本数据类型有：TINYINT，SAMLLINT，INT，BIGINT，BOOLEAN，FLOAT，DOUBLE，
STRING，TIMESTAMP(V0.8.0+)和 BINARY(V0.8.0+)。
Hive 的集合类型有：STRUCT，MAP 和 ARRAY。

Hive支持的存储数据的格式主要有： TEXTFILE 文本格式文件（行式存储）、 SEQUENCEFILE 二进制序列化文件(行式存储)、ORC（列式存储）、PARQUET（列式存储）、Avro（不是列存储，是一个数据序列化系统）等。

## Hive的数据模型

Hive 主要有四种数据模型(即表)：内部表、外部表、分区表和桶表。

表的元数据保存传统的数据库的表中，当前 hive 只支持 Derby 和 MySQL 数据库。

`HiveQL提示: ROW FORMAT DELIMITED FIELDS TERMINATED BY  以结束的行格式分隔字段`

### Hive 内部表

Hive 中的内部表和传统数据库中的表在概念上是类似的，Hive 的每个表都有自己的存储目录，除了外部表外，所有的表数据都存放在配置在 hive-site.xml 文件的${hive.metastore.warehouse.dir}/table_name 目录下。

**创建内部表：**

```sql
CREATE TABLE IF NOT EXISTS students(user_no INT,name STRING,sex STRING,
grade STRING COMMOT '班级'）COMMONT '学生表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORE AS TEXTFILE;
```

### Hive 外部表

被 external 修饰的为外部表（external table），外部表指向已经存在在 HadoopHDFS 上的数据，除了在删除外部表时只删除元数据而不会删除表数据外，其他和内部表很像。

**创建外部表：**

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS students(user_no INT,name STRING,sex STRING,
class STRING COMMOT '班级'）COMMONT '学生表'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORE AS SEQUENCEFILE
LOCATION '/usr/test/data/students.txt';
```

### Hive 分区表

分区表的每一个分区都对应数据库中相应分区列的一个索引，但是其组织方式和传统的关系型数据库不同。

在 Hive 中，分区表的每一个分区都对应表下的一个目录，所有的分区的数据都存储在对应的目录中。
比如说，分区表 partitinTable 有包含 nation(国家)、ds(日期)和 city(城市)3个分区，其中 nation = china，ds = 20130506，city = Shanghai 则对应 HDFS上的目录为：
/datawarehouse/partitinTable/nation=china/city=Shanghai/ds=20130506/。

分区中定义的变量名不能和表中的列相同。

**创建分区表：**

```sql
CREATE TABLE IF NOT EXISTS students(user_no INT,name STRING,sex STRING,
class STRING COMMOT '班级'）COMMONT '学生表'
PARTITIONED BY (ds STRING,country STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORE AS SEQUENCEFILE;
```

### Hive 分桶表

桶表就是对指定列进行哈希(hash)计算，然后会根据 hash 值进行切分数据，将
具有不同 hash 值的数据写到每个桶对应的文件中。
将数据按照指定的字段进行分成多个桶中去，说白了就是将数据按照字段进行划
分，可以将数据按照字段划分到多个文件当中去。

**创建分桶表：**

```sql
CREATE TABLE IF NOT EXISTS students(user_no INT,name STRING,sex STRING,
class STRING COMMOT '班级',score SMALLINT COMMOT '总分'）COMMONT '学生表'
PARTITIONED BY (ds STRING,country STRING)
CLUSTERED BY(user_no) SORTED BY(score) INTO 32 BUCKETS
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORE AS SEQUENCEFILE;
```

### Hive 视图

在 Hive 中，视图是逻辑数据结构，可以通过隐藏复杂数据操作（Joins, 子查
询, 过滤,数据扁平化）来于简化查询操作。
与关系数据库不同的是，Hive 视图并不存储数据或者实例化。一旦创建 HIve 视
图，它的 schema 也会立刻确定下来。对底层表后续的更改(如 增加新列)并不
会影响视图的 schema。如果底层表被删除或者改变，之后对视图的查询将会
failed。基于以上 Hive view 的特性，我们在 ETL 和数据仓库中对于经常变化
的表应慎重使用视图。

**创建视图：**

```sql
CREATE VIEW employee_skills
AS
SELECT name, skills_score['DB'] AS DB,
skills_score['Perl'] AS Perl,
skills_score['Python'] AS Python,
skills_score['Sales'] as Sales,
skills_score['HR'] as HR
FROM employee;
```

创建视图的时候是不会触发 MapReduce 的 Job，因为只存在元数据的改变。
但是，当对视图进行查询的时候依然会触发一个 MapReduce Job 进程：SHOW
CREATE TABLE 或者 DESC FORMATTED TABLE 语句来显示通过 CREATE
VIEW 语句创建的视图。以下是对 Hive 视图的 DDL 操作：

**更改视图的属性：**

```sql
ALTER VIEW employee_skills
SET TBLPROPERTIES ('comment' = 'This is a view');
```

**重新定义视图：**

```sql
ALTER VIEW employee_skills AS
SELECT * from employee ;
```

**删除视图：**

```sql
DROP VIEW 
```

