# 第1章 MongoDB 概述

MongoDB 是一个开源文档数据库，提供高性能、高可用性和自动扩展的功能。

## 1.1 基本概念

MongoDB 是文档数据库，文档是处理信息的基本单位。文档数据库的设计思路是尽可能提升数据的读写性能，为此选择性保留了部分关系型数据库的约束，通过减少读写过程的规则约束，提升了读写性能。

## 1.2 文档存储结构

文档数据库的存储结构从小到大依次是：键值对、文档、集合、数据库。

1. 键值对：文档数据库存储结构的基本单位。
2. 文档：类似于关系型数据库的行。
3. 集合：类似于关系型数据库的表。
4. 数据库：存储集合。

## 1.3 数据类型

MongoDB 采用存储的数据格式为 BSON ，是一种基于 JSON 的二进制序列化格式，MongoDB 用其存储文档。

BSON 主要特性：
BSON  改进的主要特性有下面三点。

1. 更快的遍历速度

​	BSON 对 JSON 的一个主要的改进是，在 BSON 元素的头部有一个区域用来存储元素的长度， 当遍历时，如果想跳过某个文档进行读取，就可以先读取存储在 BSON 元素头部的元素的长度， 直接找到到指定的点上就完成了文档的跳过。

​	在 JSON 中，要跳过一个文档进行数据读取，需要在对此文档进行扫描的同时匹配数据结构才可以完成跳过操作。

2. 操作更简易

​	如果要修改 JSON 中的一个值，如将 9 修改为 10，这实际是将一个字符变成了两个，会导致其后面的所有内容都向后移一位。

​	在 BSON 中，可以指定这个列为整型，那么，当将 9 修正为 10 时，只是在整型范围内将数字进行修改，数据总长不会变化。

​	需要注意的是：如果数字从整型增大到长整型，还是会导致数据总长增加。

3. 支持更多的数据类型

​	BSON 在 JSON 的基础上增加了很多额外的类型，BSON 增加了“byte array”数据类型。这使得二进制的存储不再需要先进行 base64 转换再存为 JSON，减少了计算开销。

​	BSON 支持的数据类型如表所示。

| 类型               | 描述示例                                                     |
| ------------------ | ------------------------------------------------------------ |
| NULL               | 表示空值或者不存在的字段，{"x" : null}                       |
| Boolean            | 布尔型有 true 和 false，{"x" : true}                         |
| Number             | 数值：客户端默认使用 64 位浮点型数值。{"x" : 3.14} 或 {"x" : 3}。对于整型值，包括 NumberInt（4 字节符号整数）或 NumberLong（8 字节符号整数），用户可以指定数值类型，{"x" : NumberInt("3")} |
| String             | 字符串：BSON 字符串是 UTF-8，{"x" : "中文"}                  |
| Regular Expression | 正则表达式：语法与 JavaScript 的正则表达式相同，{"x" : /[cba]/} |
| Array              | 数组：使用“[]”表示，{"x" : ["a", "b", "c"]}                  |
| Object             | 内嵌文档：文档的值是嵌套文档，{"a" : {"b" : 3}}              |
| ObjectId           | 对象 id：对象 id 是一个 12 字节的字符串，是文档的唯一标识，{"x" : objectId()} |
| BinaryData         | 二进制数据：二进制数据是一个任意字节的字符串。它不能直接在 Shell 中使用。如果要将非 UTF-8 字符保存到数据库中，二进制数据是唯一的方式 |
| JavaScript         | 代码：查询和文档中可以包括任何 JavaScript 代码，{"x" : function(){/*...*/}} |
| Data               | 日期：{"x" : new Date()}                                     |
| Timestamp          | 时间戳：var a = new Timestamp()                              |



## 1.4 安装 MongoDB

# 第2章 基本操作命令

## 2.1 数据库操作

### 创建数据库

MongoDB 使用 `use` 命令创建数据库，如果数据库不存在，MongoDB 会在第一次使用该数据库时创建数据库。如果数据库已经存在则连接数据库，然后可以在该数据库进行各种操作。

创建一个名为 myDB 的数据库：

```sql
use myDB
```



### 查看数据库

显示当前所处的数据库：

```sql
> db
test   // 当前的数据库为test
```

MongoDB 使用 `show` 命令查看当前数据库列表，代码如下:

```sql
>show dbs        //可以在任意当前数据库上执行该命令
admin 0.000GB    //保留数据库，admin
myDB 0.000GB     //自定义数据库，myDB,该数据库里已经插入记录，没有记录的自定义数据库不会显示 
local 0.000GB    //保留数据库，local
test 0.000GB     //保留数据库，test
```

MongoDB 默认的数据库为 test，如果没有创建新的数据库，集合将存储在 test 数据库中。如果自定义数据库没有插入记录，则用户在查看数据库时是不会显示的，只有插入数据的数据库才会显示相应的信息。

### 统计数据库信息

MongoDB 使用 `stats()` 方法查看某个数据库的具体统计信息，注意对某个数据库进行操作之前，一定要用 `use` 切换至数据库，否则会出错，代码如下：

```sql
>use test              //选择执行的test数据库
switched to db test    //use执行后返回的结果
> db.stats ()         //统计数据信息
{ 
    "db" : "test",     //数据库名
    "collections" : 0, //集合数量
    "views" : 0,
    "objects" : 0,     //文档数量
    "avgObjSize" : 0,  //平均每个文档的大小
    "dataSize" : 0,    //数据占用空间大小，不包括索引，单位为字节
    "storageSize" : 0, //分配的存储空间
    "nuinExtents" : 0, //连续分配的数据块
    "indexes" : 0,     //索引个数
    "indexsize" : 0,   //索引占用空间大小
    "fileSize" : 0,    //物理存储文件的大小
    "ok" : 1 
}
```

### 删除数据库

MongoDB 使用 `dropDatabase()` 方法删除数据库，代码如下：

```sql
>db.dropDatabase()    //删除当前数据库
{ ndropped" : "myDBn Jok" : 1}    //显示结果删除成功
```

## 2.2 集合操作

### 查看集合

MongoDB 使用 `getCollectionNames()` 方法查询当前数据库下的所有集合，代码如下：

```sql
>use test
>db.getCollectionNames()    //查询当前数据下所有的集合名称
```

命令 `show tables` , `show collections`的作用等价于 `getCollectionNames()` 方法：

```sql
> show tables
myCollection   // 当前数据库下有一个名为 myCollectin 的集合
```

```sql
> show collections
myCollection
```



### 创建集合

MongoDB 集合的创建有显式和隐式两种方法。

显式创建集合可通过使用`db.createCollection(name, options)`方法来实现，参数 name 指要创建的集合名称，options 是可选项，指定内存大小和索引等，下表描述 了 options 可使用的选项。



| 参数   | 类型    | 描述                                                         |
| ------ | ------- | ------------------------------------------------------------ |
| capped | Boolean | （可选）如果为 true，则启用封闭的集合。上限集合是固定大小的集合，它在达到其最大时自动覆盖其最旧的条目。如果指定 true，则还需要指定 size 参数 |
| size   | 数字    | （可选）指定上限集合的最大大小（以字节为单位）。如果 capped 为 true，那么还需要指定此字段的值 |
| max    | 数字    | （可选）指定上限集合中允许的最大文档数                       |


注意：在插入文档时，MongoDB 首先检查上限集合 capped 字段的大小，然后检查 max 字段。

显式创建集合的一个例子：

```sql
db.createCollection("mySet", {capped:true,size:6142800, max :10000 })
```

在 MongoDB 中，当插入文档时，如果集合不存在，则 MongoDB 会隐式地自动创建集合，方法如下：

```sql
db.myDB.insert( {"name": "tom"} )
```

### 其他集合操作

创建集合后可以通过 show collections 命令查看集合的详细信息，使用 renamecollection() 方法可对集合进行重新命名。

删除集合使用 drop() 方法，具体代码如下：

```sql
Show collections;
db.mySet.renameCollection( "orders2014");
db.orders2014.drop()
```

要将数据插入 MongoDB 集合中，可以使用 MongoDB 的 insert() 方法，同时 MongoDB 针对插入一条还是多条数据，提供了更可靠的 insertOne() 和 insertMany() 方法。

MongoDB 向集合里插入记录时，无须事先对数据存储结构进行定义。如果待插入的集合不存在，则插入操作会默认创建集合。

在 MongoDB 中，插入操作以单个集合为目标，MongoDB 中的所有写入操作都是单个文档级别的原子操作。

向集合中插入数据的语法如下：

```sql
db.collection.insert(
<document or array of documents>,
{
    writeConcern: <document>,    //可选字段
    ordered: <boolean>    //可选字段
    }
)
```

db 为数据库名，如当前数据库名为“test”，则用 test 代替 db，collection 为集合名，insert() 为插入文档命令，三者之间用连接。

参数说明：

- <document or array of documents> 参数表示可设置插入一条或多条文档。
- writeConcern:<document> 参数表示自定义写出错的级别，是一种出错捕捉机制。
- ordered:<boolean> 是可选的，默认为 true。
  - 如果为 true，在数组中执行文档的有序插入，并且如果其中一个文档发生错误，MongoDB 将返回而不处理数组中的其余文档；
  - 如果为 false，则执行无序插入，若其中一个文档发生错误，则忽略错误，继续处理数组中的其余文档。


插入不指定 _id 字段的文档的代码如下：

```sql
> db.test.insert( { item : "card", qty : 15 })
```

在插入期间，mongod 将创建 _id 字段并为其分配唯一的 Objectld 值，这里的 mongod 是一个 MongoDB 服务器的实例，也就是 MongoDB 服务驻扎在计算机上的进程。

查看集合文档的代码如下：

```sql
> db.test.find()
{"_id":Objectlid("5bacac84bb5e8c5dff78dc21"), "item":"cardn, "qty":15 }
```

这些 Objectld 值与执行操作时的机器和时间有关，因此，用户执行这段命令后的返回值与示例中的值是不同的。

插入指定 _id 字段的文档，值 _id 必须在集合中唯一，以避免重复键错误，代码如下：

```sql
> db.test.insert(
    { _id: 10, item: "box", qty: 20 }
)
> db.test.find()
{ "_id" : 10, "item" : "box" , "qty": 20 }
```

可以看到新插入文档的 id 值为设置的 id 值。

插入的多个文档无须具有相同的字段。例如，下面代码中的第一个文档包含一个 _id 字段和一个 type 字段，第二个和第三个文档不包含 _id 字段。因此，在插入过程中，MongoDB 将会为第二个和第三个文档创建默认 _id 字段，代码如下：

```sql
db.test.insert(
    [
        { _id: 11, item: "pencil", qty: 50, type: "no.2" },
        { item: "pen", qty: 20 },
        { item: "eraser", qty: 25 }
    ]
)
```

查询验证，可以看到在 _id 插入期间，系统自动为第二、第三个文档创建了字段，代码如下：

```sql
> db.test.find()
{ "_id" : 11, "item" : "pencil", "qty" : 50, "type" : "no.2" }
{ "_id" : Objectld("5bacf31728b746e917e06b27"), "item" : "pen"， "qty" : 20 }
{ "_id" : Objectld("5bacf31728b746e917e06b28"), "item" : "eraser", "qty" : 25 }
```


用变量方式插入文档，代码如下：

```sql
> document= ({ name: "c语言", price: 40 })    //document 为变量名.
> db.test.insert(document)
```


有序地插入多条文档的代码如下：

```sql
> db.test.insert([
        {_id:10, item:"pen", price:"20" },
        {_id:12, item:"redpen", price: "30" },
        {_id:11, item:"bluepen", price: "40" }
    ],
    {ordered:true}
)
```

在设置 ordered:true 时，插入的数据是有序的，如果存在某条待插入文档和集合的某文档 \_id 相同的情况，_id 相同的文档与后续文档都将不再插入。在设置 ordered:false 时，除了出错记录（包括 _id 重复）外其他的记录继续插入。

MongoDB 3.2 更新后新增以下两种新的文档插入命令如下：

db.collection.insertone ()
db.collection.insertMany()

使用 insertOne() 插入一条文档的代码如下：

```sql
db.test.iusertone( { item: "card", qty: 15 } );
```

使用 insertMany() 插入多条文档的代码如下：

```sql
db.test.insertMany([
    { item: "card", qty: 15 },
    { item: "envelope", qty: 20 },
    { item: "stamps", qty:30 }
]);
```

**MongoDB使用 update() 和 save() 方法来更新（修改）集合中的文档。**

### update() 方法

MongoDB update() 更新文档的基本语法如下:

```sql
db.collection.update(
  <query>,
  <update>,
  {
    upsert,
    multi,
    writeConcern,
    collation
  }
)
```

参数说明：

- <query＞：参数设置查询条件。
- <update＞：为更新操作符。
- upsert：为布尔型可选项，表示如果不存在 update 的记录，是否插入这个新的文档。true 为插入；默认为 false，不插入。
- multi：也是布尔型可选项，默认是 false，只更新找到的第一条记录。如果为 true，则把按条件查询出来的记录全部更新。
- writeConcem：表示出错级别。
- collation：指定语言。


例如，插入多条数据后，使用 update 进行更改，代码如下：

```sql
db.test.insertMany ([
    { item : "card"，qty : 15 },
    { item : "envelope", qty: 20 },
    { item : "stamps", qty: 30 }
]);
```

将 item 为 card 的数量 qty 更正为 35，代码如下：

```sql
db.test.update(
{
    item : "card"
},
{
    $set: {qty: 35}
}
```

collation 特性允许 MongoDB 的用户根据不同的语言定制排序规则，在 MongoDB 中字符串默认当作一个普通的二进制字符串来对比。而对于中文名称，通常有按拼音顺序排序的需求，这时就可以通过collation来实现。

创建集合时，指定 collation 为 zh，按 name 字段排序时，则会按照 collation 指定的中文规则来排序，代码如下：

```sql
db.createCollection ("person", {collation: {locale: "zh" }})    //创建集合并指定语言
db.person.insert ({name: "张三"})
db.person.insert ({name:"李四"})
db.person.insert ({name: ”王五"})
db.person.insert ({name: "马六"})
db.person.insert ({name:"张七"})
db.person.find().sort({name: 1}) //查询并排序
//查询返回结果
{ "_id" : Objectld ("586b995d0cec8d86881cffae") , "name": "李四" }
{ "_id" : Objectld ("586b995d0cec8d86881cffb0") , "name" : "马六" }.
{ "_id" : Objectld ("586b995d0cec8d86881cffaf"), "name": "王五" }
{ "_id" : Objectld ("586b995d0cec8d86881cffb1"), "name": "张七" }
{ "_id" : Objectld ("586b995d0cec8d86881cffad"), "name" : "张三" }
```

### save() 方法

MongoDB 另一个更新（修改）文档的方法是 save()，语法格式如下：

db.collection.save ( obj )

如下代码会先保存一个 _id 为 100 的记录，然后再执行 save，并对当前已经存在的数据进行修改：

```sql
db.products.save( { _id: 100, item: "watern", qty: 30 })
db.products.save( { _id : 100, item : "juice" })
```

由于`_id`字段包含集合中存在的 value，因此操作会执行更新以替换文档并生成以下文档：

```sql
{ "_id" : 100, "item" : "juice" }
```

如果使用 insert 插入记录，若新增数据的主键已经存在，则会抛出 DuplicateKeyException 异常提示主键重复，不保存当前数据。

MongoDB使用 remove() 和 delete() 方法来删除集合中的文档。

### remove() 方法

如果不再需要 MongoDB 中存储的文档，可以通过删除命令将其永久删除。删除 MongoDB 集合中的数据可以使用 remove() 函数。

remove() 函数可以接受一个查询文档作为可选参数来有选择性地删除符合条件的文档。删除文档是永久性的，不能撤销，也不能恢复。因此，在执行 remove() 函数前最好先用 find()命令来查看是否正确。

remove() 方法的基本语法格式如下所示：

```sql
db.collection.remove(
  <query>,
  {
    justOne: <boolean>, writeConcern: <document>
  }
)
```

参数说明：

- query：必选项，是设置删除的文档的条件。
- justOne：布尔型的可选项，默认为false，删除符合条件的所有文档，如果设为 true，则只删除一个文档。
- writeConcem：可选项，设置抛出异常的级别。


下面举例说明删除集合中的文档，先进行两次插入操作，代码如下：

```sql
>db.test.insert(
    {
        title : 'MongoDB',
        description : 'MongoDB 是一个 NoSQL 数据库',
        by : 'C语言中文网',
        tags : ['mongodb', 'database', 'NoSQL'],
        likes : 100
    }
)
```

使用 find() 函数查询的代码如下：

```sql
> db.test.find()
{ "_id" : Objectld ("5ba9d8b：L24857a5fefclfde6"), "title" : "MongoDB", "description" : "MongoDB 是一个 NoSQL 数据库", "by" : "C语言中文网", "tags" : [ "mongodb", "database", "NoSQL" ], "likes" : 100 }
{ "_id" : ObjectId("5ba9d90924857a5fefclfde7"), "title" : "MongoDB ", "description" : "MongoDB 是一个 NoSQL 数据库", "by" : "C语言中文网", "tags" : [ "mongodb", "database", "NoSQL"], "likes" : 100 }
```

接下来移除 title 为“MongoDB”的文档，执行以下操作后，查询会发现两个文档记录均被删除：

```sql
>db.test.remove({'title': 'MongoDB'})
WriteResult({ 'nRemoved' : 2 })    #删除了两条数据
```

另外，可以设置比较条件，如下操作为删除 likes大于 3 的文档记录：

```sql
>db.test.remove(
    {
        likes:{$gt:3}
    }
)
```

### delete() 方法

官方推荐使用 deleteOne() 和 deleteMany() 方法删除文档，语法格式如下：

```sql
db.collection.deleteMany ({})
db.collection.deleteMany ({ status : "A" })
db.collection.delete.One ({ status : "D" })
```

第一条语句删除集合下所有的文档，第二条语句删除 status 等于 A 的全部文档，第三条语句删除 status 等于 D 的一个文档。

在关系型数据库中，可以实现基于表的各种各样的查询，以及通过投影来返回指定的列，相应的查询功能也可以在 MongoDB中实现。同时由于 MongoDB 支持嵌套文档和数组，MongoDB 也可以实现基于嵌套文档和数组的查询。

### find() 简介

MongoDB 中查询文档使用 find() 方法。find() 方法以非结构化的方式来显示所要查询的文档， 查询数据的语法格式如下：

```sql
>db.collection.find(query, projection)
```

query 为可选项，设置查询操作符指定查询条件；projection （投影）也为可选项，表示使用投影操作符指定返回的字段，如果忽略此选项则返回所有字段。

查询 test 集合中的所有文档时，为了使显示的结果更为直观，可使用 pretty() 方法以格式化的方式来显示所有文档，方法如下：

```sql
> db.test.find().pretty()
```

除了 find() 方法，还可使用 findOne() 方法，它只返回一个文档。

### 查询条件

MongoDB 支持条件操作符，下表为 MongoDB 与 RDBMS 的条件操作符的对比，读者可以通过对比来理解 MongoDB 中条件操作符的使用方法。



| 操作符         | 格式                                                | 实例                                                         | 与 RDBMS where 语句比较                            |
| -------------- | --------------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| 等于（=）      | {<key> : {<value>}}                                 | db.test.find( {price : 24} )                                 | where price = 24                                   |
| 大于（>）      | {<key> : {$gt : <value>}}                           | db.test.find( {price : {$gt : 24}} )                         | where price > 24                                   |
| 小于（<）      | {<key> : {$lt : <value>}}                           | db.test.find( {price : {$lt : 24}} )                         | where price < 24                                   |
| 大于等于（>=） | {<key> : {$gte : <value>}}                          | db.test.find( {price : {$gte : 24}} )                        | where price >= 24                                  |
| 小于等于（<=） | {<key> : {$lte : <value>}}                          | db.test.find( {price : {$lte : 24}} )                        | where price <= 24                                  |
| 不等于（!=）   | {<key> : {$ne : <value>}}                           | db.test.find( {price : {$ne : 24}} )                         | where price != 24                                  |
| 与（and）      | {key01 : value01, key02 : value02, ...}             | db.test.find( {name : "《MongoDB 入门教程》", price : 24} )  | where name = "《MongoDB 入门教程》" and price = 24 |
| 或（or）       | {$or : [{key01 : value01}, {key02 : value02}, ...]} | db.test.find( {$or:[{name : "《MongoDB 入门教程》"},{price : 24}]} ) | where name = "《MongoDB 入门教程》" or price = 24  |

### 特定类型查询

特定类型查询结果在 test 集合中有以下文档为基础：

```sql
> db.test.find()
    {"_id" : Objectld("5ba7342c7f9318ea62161351"), "name" : "《MongoDB教程》", "price" : 24, "tags" : [ "MongoDB", "NoSQL", "database" ], "by": "C语言中文网"}
    {"_id" : Objectld("5ba747bd7f9318ea62161352"), "name" ： "java教程", "price" : 36, "tags" : ["编程语言", "Java语言", "面向对象程序设计语言"], "by" : "C语言中文网"}
    {"_id" : Objectld("5ba75a057f9318ea62161356"), "name" : "王二", "age" : null }
```

查询 age 为 null 的字段的语法格式如下：

```sql
db.test.find({age:null})
```

此语句不仅匹配出 age 为 null 的文档，其他不同类型的文档也会被查出。这是因为 null 不仅会匹配某个键值为 null 的文档，而且还会匹配不包含这个键的文档。

查询 name 为 java教程， price为 36 的文档：

```sql
db.test.find({name:'java教程',price:36})
```

查询 name 为 java教程， price 大于等于 35 的文档：

```sql
db.test.find({name:'java教程',price:{$gte:35})
```

查找 size 为 { h: 14, w: 21, uom: "cm" } 的文档：

```sql
db.inventory.find( { size: { h: 14, w: 21, uom: "cm" } } )
```

查找 size 中的 uom 值为 in 的记录：

```sql
db.inventory.find( { "size.uom": "in" } )
```

查找 status 为 A 或 qty 字段的值小于30的记录：


```sql
db.inventory.find( { $or: [ { status: "A" }, { qty: { $lt: 30 } } ] } )
```

查找 status 字段的值为 A 或 D 的记录：

```sql
db.inventory.find( { status: { $in: [ "A", "D" ] } } )
```

查询数组可使用以下语法格式：

```sql
> db.test.find(
{
    tags:['MongoDB', 'NoSQL', 'database']
}
)
{"_id" : ObjectId("5ba7342c7f9318ea62161351"), "name": "《MongoDB教程》", "price" : 24, "tags" : [ "MongoDB", "NoSQL", "database"], "by" : "C语言中文网"}
```

可以在查询中使用正则表达式，例如，查找status为A  且  qty小于30或item是以p开头的记录：

```sql
db.inventory.find( {
     status: "A",
     $or: [ { qty: { $lt: 30 } }, { item: /^p/ } ]
} )
```

查询有 3 个元素的数组的代码如下：

```sql
> db.test.find(
{
    tags:{$size:3}
}
)
{"_id" : Objectld("5baf9b6663ba0fb3ccccle77"), "name" : "《MongoDB 教程》", ''price" : 24, "tags" : ["MongoDB"，"NoSQL", "database"], "by" : "C语言中文网"}
{"_id" : Objectld ("5baf 9bc763ba0fk>3ccccle78"), "name" : "《Java 教程》", "price" : 36, "tags" : ["编程语言", "Java语言", "面向对象程序设计语言"], "by" : "C语言中文网"}
```


查询数组里的某一个值的代码如下：

```sql
> db.test.find(
{
    tags: "MongoDB"
}
)
{"_id" : Objectld("5baf9b6663ba0fb3ccccle77"), "name" : "《MongoDB 教程》", ''price" : 24, "tags" : ["MongoDB"，"NoSQL", "database"], "by" : "C语言中文网"}
```

查找所有的文档的 _id、item、status 字段：

```sql
db.inventory.find( {}, { _id: 0, item: 1, status: 1 } );
```

limit() 函数与 SQL 中的作用相同，用于限制查询结果的个数，如下语句只返回 3 个匹配的结果。若匹配的结果不到 3 个，则返回匹配数量的结果：

```sql
>db.test.find().limit(3)
```


Skip() 函数用于略过指定个数的文档，如下语句略过第一个文档，返回后两个：

```sql
>db.test.find().skip(1)
```


sort() 函数用于对查询结果进行排序，1 是升序，-1 是降序，如下语句可将查询结果升序显示：

```sql
>db.test.find().sort({"price" : 1})
```


使用 $regex 操作符来设置匹配字符串的正则表达式，不同于全文检索，使用正则表达式无须进行任何配置。如下所示为使用正则表达式查询含有 MongoDB 的文档：

```sql
> db.test.find({tags:{$regex:"MongoDB"}})
{"_id" : Objectld("5baf9b6663ba0fb3ccccle77"), "name" : "《MongoDB 教程》", ''price" : 24, "tags" : ["MongoDB"，"NoSQL", "database"], "by" : "C语言中文网"}
```

## 2.3 游标

游标是指对数据一行一行地进行操作，在 MongoDB 数据库中对游标的控制非常简单，只需使用 firid() 函数就可以返回游标。有关游标的方法参见下表。

| 方法名          | 作用                                   |
| --------------- | -------------------------------------- |
| hasNext         | 判断是否有更多的文档                   |
| next            | 用来获取下一条文档                     |
| toArray         | 将查询结构放到数组中                   |
| count           | 查询的结果为文档的总数量               |
| limit           | 限制查询结果返回数量                   |
| skip            | 跳过指定数目的文档                     |
| sort            | 对查询结果进行排序                     |
| objsLeftlnBatch | 查看当前批次剩余的未被迭代的文档数量   |
| addOption       | 为游标设置辅助选项，修改游标的默认行为 |
| hint            | 为查询强制使用指定索引                 |
| explain         | 用于获取查询执行过程报告               |
| snapshot        | 对查询结果使用快照                     |

使用游标时，需要注意下面 4 个问题。

1.  当调用 find() 函数时，Shell 并不立即查询数据库，而是等真正开始获取结果时才发送查询请求。

2.  游标对象的每个方法几乎都会返回游标对象本身，这样可以方便进行链式函数的调用。

3.  在 MongoDB Shell 中使用游标输出文档包含两种情况，如果不将 find() 函数返回的游标赋值给一个局部变量进行保存，在默认情况下游标会自动迭代 20 次。如果将 find() 函数返回的游标赋值给一个局部变量，则可以使用游标对象提供的函数进行手动迭代。

4.  使用清空后的游标，进行迭代输出时，显示的内容为空。游标从创建到被销毁的整个过程存在的时间，被称为游标的生命周期，包括游标的创建、使用及销毁三个阶段。当客户端使用 find() 函数向服务器端发起一次查询请求时，会在服务器端创建一个游标，然后就可以使用游标函数来操作查询结果。

以下三种情况会让游标被销毁。

- 客户端保存的游标变量不在作用域内。
- 游标遍历完成后，或者客户端主动发送终止消息。
- 在服务器端 10 分钟内未对游标进行操作。


以下语句显示使用游标查找所有文档：

```sql
>var cursor = db.test.find()
>while (cursor.hasNext()){
    var doc = cursor.next();
    print(doc.name);  //把每一条数据都单独拿出来进行逐行的控制
    print(doc);  //将游标数据取出来后，其实每行数据返回的都是一个［object BSON］型的内容
    printjson(doc);  //将游标获取的集合以JSON的形式显示
}
```

## 2.4 索引

### 2.4.1 索引简介

索引可以提升文档的查询速度，但建立索引的过程需要使用计算与存储资源，在已经建立索引的前提下，插入新的文档会引起索引顺序的重排。

MongoDB 的索引是基于 [B-tree](https://zh.wikipedia.org/wiki/B%E6%A0%91)数据结构及对应算法形成的。树索引存储特定字段或字段集的值，按字段值排序。索引条目的排序支持有效的等式匹配和基于范围的查询操作。

下图所示的过程说明了使用索引选择和排序匹配文档的查询过程。



![img](https://cdn.jsdelivr.net/gh/nmydt/LearningNote@main/NoSQL数据库/MongoDB/MongoDB基础.assets/1.gif)


从根本上说，MongoDB 中的索引与其他数据库系统中的索引类似。MongoDB 在集合级别定义索引，并支持 MongoDB 集合中文档的任何字段或子字段的索引。

MongoDB 在创建集合时，会默认在 \_id 字段上创建唯一索引。该索引可防止客户端插入具有相同字段的两个文档，_id 字段上的索引不能被删除。

在分片集群中，如果不将该 _id 字段用作分片键，则应用需要自定义逻辑来确保 _id 字段中值的唯一性，通常通过使用标准的自生成的 Objectld 作为 _id。



MongoDB 中索引的类型大致包含单键索引、复合索引、多键值索引、地理索引、全文索引、 散列索引等，下面简单介绍各类索引的用法。

#### 单键索引

MongoDB 支持文档集合中任何字段的索引，在默认情况下，所有集合在 _id 字段上都有一个索引，应用程序和用户可以添加额外的索引来支持重要的查询操作，单键索引可参考下图。



![img](https://cdn.jsdelivr.net/gh/nmydt/LearningNote@main/NoSQL数据库/MongoDB/MongoDB基础.assets/2.gif)


对于单字段索引和排序操作，索引键的排序顺序（即升序或降序）无关紧要，因为 MongoDB 可以在任意方向上遍历索引。

创建单键索引的语法结构如下：

\>db.collection.createlndex ( { key: 1 } ) //1 为升序，-1 为降序

以下示例为插入一个文档，并在 score 键上创建索引，具体步骤如下：

```sql
>db.records.insert(
    {
        "score" : 1034,
        "location" : { state: "NY", city: "New York"}
    }
)
db.records.createTndex( { score: 1 } )
```

使用 score 字段进行查询，再使用 explain() 函数，可以查看查询过程：

```sql
db.records.find({score:1034}).explain()
```

#### 复合索引

MongoDB 支持复合索引，其中复合索引结构包含多个字段，下图说明了两个字段的复合索引示例。



![img](https://cdn.jsdelivr.net/gh/nmydt/LearningNote@main/NoSQL数据库/MongoDB/MongoDB基础.assets/3.gif)


复合索引可以支持在多个字段上进行的匹配查询，语法结构如下：

db.collection.createIndex ({ <key1> : <type>, <key2> : <type2>, ...})

需要注意的是，在建立复合索引的时候一定要注意顺序的问题，顺序不同将导致查询的结果也不相同。

如下语句创建复合索引：

```sql
>db.records.createIndex ({ "score": 1, "location.state": 1 })
```


查看复合索引的查询计划的语法如下：

```sql
>db.records.find({score:1034, "location.state" : "NY"}).explain()
```

#### 多键值索引

若要为包含数组的字段建立索引，MongoDB 会为数组中的每个元素创建索引键。这些多键值索引支持对数组字段的高效查询，如图所示。



![img](https://cdn.jsdelivr.net/gh/nmydt/LearningNote@main/NoSQL数据库/MongoDB/MongoDB基础.assets/4.gif)

创建多键值索引的语法如下：

\>db.collecttion.createlndex( { <key>: < 1 or -1 > })

需要注意的是，如果集合中包含多个待索引字段是数组，则无法创建复合多键索引。

以下示例代码展示插入文档，并创建多键值索引：

```sql
>db.survey.insert({item : "ABC", ratings: [ 2, 5, 9 ]})
>db.survey.createIndex({ratings:1})
>db.survey.find({ratings:2}).explain()
```

#### 全文索引

MongoDB 的全文检索提供三个版本，用户在使用时可以指定相应的版本，如果不指定则默认选择当前版本对应的全文索引。

MongoDB 提供的文本索引支持对字符串内容的文本搜索查询，但是这种索引因为需要检索的文件比较多，因此在使用的时候检索时间较长。

全文索引的语法结构如下：

db.collection.createIndex ({ key: "text" })

### 2.4.2 索引操作

#### 查看现有索引

若要返回集合上所有索引的列表，则需使用驱动程序的 db.collection.getlndexes() 方法或类似方法。

例如，可使用如下方法查看 records 集合上的所有索引：

```sql
db.records.getIndexes()
```

#### 列出数据库的所有索引

若要列出数据库中所有集合的所有索引，则需在 MongoDB 的 Shell 客户端中进行以下操作：

```sql
db.getCollectionNames().forEach(function(collection){
    indexes = db[collection].getIndexes();
    print("Indexes for " + collection + ":" );
    printjson(indexes);
});
```

#### 删除索引

MongoDB 提供的两种从集合中删除索引的方法如下：

db.collection.dropIndex()

db.collection.dropIndexes()

若要删除特定索引，则可使用该 db.collection.droplndex() 方法。

例如，以下操作将删除集合中 score 字段的升序索引：

```sql
db.records.dropIndex ({ "score" : 1 })  //升序降序不能错，如果为-1，则提示无索引
```

还可以使用 db.collection.droplndexes() 删除除 _id 索引之外的所有索引。

例如，以下命令将从 records 集合中删除所有索引：

```sql
db.records.dropIndexes()
```

#### 修改索引

若要修改现有索引，则需要删除现有索引并重新创建索引。

## 2.5 聚合查询

聚合操作主要用于处理数据并返回计算结果。聚合操作将来自多个文档的值组合在一起，按条件分组后，再进行一系列操作（如求和、平均值、最大值、最小值）以返回单个结果。

MongoDB提供了三种执行聚合的方法：聚合管道、map-reduce 和单一目标聚合方法，聚合管道方法如下。

### 聚合管道方法

MongoDB 的聚合框架就是将文档输入处理管道，在管道内完成对文档的操作，最终将文档转换为聚合结果。

最基本的管道阶段提供过滤器，其操作类似查询和文档转换，可以修改输出文档的形式。其他管道操作提供了按特定字段对文档进行分组和排序的工具，以及用于聚合数组内容（包括文档数组）的工具。

此外，在管道阶段还可以使用运算符来执行诸如计算平均值或连接字符串之类的任务。聚合管道可以在分片集合上运行。

聚合管道方法的流程参见下图。



![img](https://cdn.jsdelivr.net/gh/nmydt/LearningNote@main/NoSQL数据库/MongoDB/MongoDB基础.assets/5.gif)


上图的聚合操作相当于 MySQL中的以下语句：

```sql
select cust_id as _id, sum(amount) as total from orders where status like "%A%" group by cust_id;
```

MongoDB 中的聚合操作语法如下：

```sql
db.collection.aggregate([
{
    $match : {< query >},
}
{
    $group: {< fieldl >: < field2 >}
}
])
```

Query 设置统计查询条件，类似于 SQL 的 where，field1 为分类字段，要求使用 _id 名表示分类字段，field2 为包含各种统计操作符的数字型字段，如 $sum、$avg、$min 等。

这个语法看起来比较难以理解，下面给出一个示例进行对照：

```sql
db.mycol.aggregate([
{
    $group : {_id : "$by_user", num_tutorial : {$sum : 1}}
}
])
```

相当于MySQL中的：

```sql
select by_user as _id, count(*) as num_tutorial from mycol group by by_user;
```


再举一个复杂的例子，按照指定条件对文档进行过滤，然后对满足条件的文档进行统计，并将统计结果输出到临时文件中。

首先插入多条文档，代码如下：

```sql
db.articles.insert([    
    { "_id" : 10, "author" : "dave", "score" : 80, "views" :100 },
    { "_id" : 11, "author" : "dave", "score" : 85, "views" : 521 },
    { "_id" : 12, "author" : "ahn", "score" : 60, "views" : 1000 },
    { "_id" : 13, "author" : "li", "score" : 55, "views" : 5000 },
    { "_id" : 14, "author" : "annT", "score" : 60, "views" : 50 },
    { "_id" : 15, "author" : "1i", "score": 94, "views": 999 },
    { "_id" : 16, "author" : "ty", "score" : 95, "views": 1000 }
]);
```

再进行聚合分类统计，代码如下:

```sql
db.articles.aggregate([
{
    $match: { $or: [{ score: { $gt: 70, $1t: 90 }}, { views: { $gte: 1000 }}]}
    }, 
{ $group: { _id: null, count: { $sum: 1 }}
    }
]);
```

最终统计结果为：

{ "_id" : null, "count" : 5 }

管道阶段的 RAM 限制为 100MB。若要允许处理大型数据集，则可使用 allowDiskUse 选项启用聚合管道阶段，将数据写入临时文件。

# 第3章 MongoDB架构

MongoDB有三种集群部署模式，分别是**主从复制**、**副本集**和**分片模式**。

### 主从复制

此模式只有一个主节点，有多个从节点。每个从节点需要知道主节点的位置以定期轮询主节点获取并执行主节点更新操作。当主节点故障时，只能人工介入，指定新的主节点。

### 副本集

副本集与主从复制的区别为：主节点故障时，副本集可以自动投票选举新的主节点，并引导其余的从节点连接新的主节点。

### 分片

MongoDB支持自动分片。可以将数据分散到不同的机器上。

# 参考文献

> 《MongoDB中文手册》https://docs.mongoing.com/
>
> 《MongoDB》http://m.biancheng.net/mongodb/
