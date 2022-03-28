# 1. HBase 架构

![](https://cdn.jsdelivr.net/gh/nmydt/LearningNote@main/NoSQL数据库/HBase/https://img-blog.csdnimg.cn/20200803183420279.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MDg2MTcwNw==,size_16,color_FFFFFF,t_70)

- 每个HBase集群包含一个HMaster节点和多个HRegionServer节点(其中HMaster和HRegionServer的注册信息保存在Zookeeper上),同时Client进行读写操作时,也要通过Zookeeper访问
META表的元信息；
- 每个HRegionServer对应一个HLog日志文件(主要用于数据恢复),HLog日志文件的LOG_SPLIT信息,存储在Zookeeper中每个HRegionServer包含多个HRegion,每个HRegion对应多个store,每个store存储的是一个列簇的数据每个store包含一个Memstore和多个StoreFile,其中StoreFile的数据以HFile的形式存储在HDFS上。
# 2. HBase 数据写入流程

1) 客户端访问 ZooKeeper，从 Meta 表得到写入数据对应的 Region 信息和相应 的Region 服务器。

2) 客户端访问相应的 Region 服务器，把数据分别写入 HLog 和 MemStore。MemStore 数据容量有限，当达到一个阈值后，则把数据写入磁盘文件 StoreFile 中，在 HLog 文件中写入一个标记，表示 MemStore 缓存中的数据已被写入 StoreFile 中。如果 MemStore 中的数据丢失，则可以从 HLog 上恢复。

3) 当多个 StoreFile 文件达到阈值后，会触发 Store.compact() 将多个 StoreFile 文件合并为一个 大文件。

# 3. HBase 数据读取流程

1) 客户端先访问 ZooKeeper，从 Meta 表读取 Region 信息对应的服务器。

2) 客户端向对应 Region 服务器发送读取数据的请求，Region 接收请求后，先从 MemStore 查找数据；如果没有，再到 StoreFile 上读取，然后将数据返回给客户端。

# 4. HDFS 和 HBase 各自使用场景

首先一点需要明白：Hbase 是基于 HDFS 来存储的。
HDFS：
1. 一次性写入，多次读取。

2. 保证数据的一致性。

3. 主要是可以部署在许多廉价机器中，通过多副本提高可靠性，提供了容错和恢复机制。

HBase：

1. 瞬间写入量很大，数据库不好支撑或需要很高成本支撑的场景。
2. 数据需要长久保存，且量会持久增长到比较大的场景。
3. HBase 不适用与有 join，多级索引，表关系复杂的数据模型。
4. 大数据量（100s TB 级数据）且有快速随机访问的需求。如：淘宝的交易历史记录。数据量巨大无容置疑，面向普通用户的请求必然要即时响应。
5. 业务场景简单，不需要关系数据库中很多特性（例如交叉列、交叉表，事务，连接等等）。

# 5.  Hbase 的存储结构

Hbase 中的每张表都通过行键(rowkey)按照一定的范围被分割成多个子表（HRegion），默认一个 HRegion 超过 256M 就要被分割成两个，由 HRegionServer管理，管理哪些 HRegion 由 Hmaster 分配。 HRegion 存取一个子表时，会创建一个 HRegion 对象，然后对表的每个列族（Column Family）创建一个 store实例， 每个 store 都会有 0 个或多个 StoreFile 与之对应，每个 StoreFile都会对应一个 HFile，HFile 就是实际的存储文件，一个 HRegion 还拥有一个MemStore 实例。

# 6. 热点现象（数据倾斜）怎么产生的，以及解决方法有哪些

热点现象：
某个小的时段内，对 HBase 的读写请求集中到极少数的 Region 上，导致这些region 所在的 RegionServer 处理请求量骤增，负载量明显偏大，而其他的RgionServer 明显空闲。
热点现象出现的原因：
HBase 中的行是按照 rowkey 的字典顺序排序的，这种设计优化了 scan 操作，可以将相关的行以及会被一起读取的行存取在临近位置，便于 scan。然而糟糕的rowkey 设计是热点的源头。热点发生在大量的 client 直接访问集群的一个或极少数个节点（访问可能是读，写或者其他操作）。大量访问会使热点 region 所在的单个机器超出自身承受能力，引起性能下降甚至 region 不可用，这也会影响同一个 RegionServer 上的其他 region，由于主机无法服务其他 region 的请求。

热点现象解决办法：
为了避免写热点，设计 rowkey 使得不同行在同一个 region，但是在更多数据情况下，数据应该被写入集群的多个 region，而不是一个。常见的方法有以下这些：

1. **加盐**：在 rowkey 的前面增加随机数，使得它和之前的 rowkey 的开头不同。分配的前缀种类数量应该和你想使用数据分散到不同的 region 的数量一致。加盐之后的 rowkey 就会根据随机生成的前缀分散到各个 region 上，以避免热点。

2. **哈希**：哈希可以使负载分散到整个集群，但是读却是可以预测的。使用确定的哈希可以让客户端重构完整的 rowkey，可以使用 get 操作准确获取某一个行数据

3. **反转**：第三种防止热点的方法时反转固定长度或者数字格式的 rowkey。这样可以使得 rowkey 中经常改变的部分（最没有意义的部分）放在前面。这样可以有效的随机 rowkey，但是牺牲了 rowkey 的有序性。反转 rowkey的例子以手机号为 rowkey，可以将手机号反转后的字符串作为 rowkey，这样的就避免了以手机号那样比较固定开头导致热点问题

4. **时间戳反转**：一个常见的数据处理问题是快速获取数据的最近版本，使用反转的时间戳作为 rowkey 的一部分对这个问题十分有用，可以用Long.Max_Value - timestamp 追加到 key 的末尾，例如
    \[key][reverse_timestamp],[key]的最新值可以通过 scan [key]获得[key]的第一条记录，因为 HBase 中rowkey 是有序的，第一条记录是最后录入的数据。 
    
      - 比如需要保存一个用户的操作记录，按照操作时间倒序排序，在设计 rowkey 的时候，可以这样设计[userId 反转] [Long.Max_Valuetimestamp]，在查询用户的所有操作记录数据的时候，直接指定反转后的 userId，startRow 是\[userId 反转][000000000000],stopRow 是\[userId 反转][Long.Max_Value -timestamp]
    
    
      - 如果需要查询某段时间的操作记录，startRow 是\[user 反转][Long.Max_Value - 起始时间]，stopRow 是\[userId 反转][Long.Max_Value - 结束时间]
    

5. **HBase 建表预分区**：创建 HBase 表时，就预先根据可能的 RowKey 划分出多个 region 而不是默认的一个，从而可以将后续的读写操作负载均衡到不同的 region 上，避免热点现象。

# 7. HBase 的 rowkey 设计原则

**rowkey长度原则**
rowkey是一个二进制码流，可以是任意字符串，最大长度 64kb ，实际应用中一般为10-100bytes，以 byte[] 形式保存，一般设计成定长。

建议越短越好，不要超过16个字节，原因如下：

- 数据的持久化文件HFile中是按照KeyValue存储的，如果rowkey过长，比如超过100字节，1000w行数据，光rowkey就要占用100*1000w=10亿个字节，将近1G数据，这样会极大影响HFile的存储效率；
- MemStore将缓存部分数据到内存，如果rowkey字段过长，内存的有效利用率就会降低，系统不能缓存更多的数据，这样会降低检索效率；
- 目前操作系统都是64位系统，内存8字节对齐，控制在16个字节，8字节的整数倍利用了操作系统的最佳特性。

**rowkey散列原则**
如果rowkey按照时间戳的方式递增，不要将时间放在二进制码的前面，建议将rowkey的高位作为散列字段，由程序随机生成，低位放时间字段，这样将提高数据均衡分布在每个RegionServer，以实现负载均衡的几率。如果没有散列字段，首字段直接是时间信息，所有的数据都会集中在一个RegionServer上，这样在数据检索的时候负载会集中在个别的RegionServer上，造成热点问题，会降低查询效率。

**rowkey唯一原则**
必须在设计上保证其唯一性，rowkey是按照字典顺序排序存储的，因此，设计rowkey的时候，要充分利用这个排序的特点，将经常读取的数据存储到一块，将最近可能会被访问的数据放到一块。

# 8. HBase 的列簇设计

原则：在合理范围内能尽量少的减少列簇就尽量减少列簇，因为列簇是共享region 的，每个列簇数据相差太大导致查询效率低下。
最优：将所有相关性很强的 key-value 都放在同一个列簇下，这样既能做到查询效率最高，也能保持尽可能少的访问不同的磁盘文件。以用户信息为例，可以将必须的基本信息存放在一个列族，而一些附加的额外信息可以放在另一列族。

# 9. HBase 中 compact 用途是什么，什么时候触发，分为哪两种，有什么区别

在 hbase 中每当有 memstore 数据 flush 到磁盘之后，就形成一个 storefile，当 storeFile 的数量达到一定程度后，就需要将 storefile 文件来进行compaction 操作。
Compact 的作用：

1. 合并文件

2. 清除过期，多余版本的数据

3. 提高读写数据的效率 

HBase 中实现了两种 compaction 的方式：minor and major. 这两种 compaction 方式的 区别是：

- Minor 操作只用来做部分文件的合并操作以及包括 minVersion=0 并且设置 ttl 的过 期版本清理，不做任何删除数据、多版本数据的清理工作。

- Major 操作是对 Region 下的 HStore 下的所有 StoreFile 执行合并操作，最终的结果 是整理合并出一个文件。
