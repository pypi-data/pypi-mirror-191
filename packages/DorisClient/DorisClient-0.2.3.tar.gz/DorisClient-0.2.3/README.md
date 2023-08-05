# DorisClient

python for apache-doris

# Install

```shell
pip install DorisClient
```

# Use

## Create Test Table

```sql
CREATE TABLE `streamload_test` (
  `id` int(11) NULL COMMENT "",
  `shop_code` varchar(64) NULL COMMENT "",
  `sale_amount` decimal(18, 2) NULL COMMENT ""
) ENGINE=OLAP
UNIQUE KEY(`id`)
COMMENT "test"
DISTRIBUTED BY HASH(`id`) BUCKETS 3
PROPERTIES (
"replication_allocation" = "tag.location.default: 3",
"in_memory" = "false",
"storage_format" = "V2"
);

-- If you want to enable sequence streamload, make sure Doris table enable sequence load first
-- ALTER TABLE streamload_test ENABLE FEATURE "SEQUENCE_LOAD" WITH PROPERTIES ("function_column.sequence_type" = "bigint");
```

## streamload

```python
from DorisClient import DorisSession, DorisLogger, Logger

# DorisLogger.setLevel('ERROR')  # default:INFO

doris_cfg = {
    'fe_servers': ['10.211.7.131:8030', '10.211.7.132:8030', '10.211.7.133:8030'],
    'database': 'testdb',
    'user': 'test',
    'passwd': '123456',
}
doris = DorisSession(**doris_cfg)

# append
data = [
    {'id': '1', 'shop_code': 'sdd1', 'sale_amount': '99'},
    {'id': '2', 'shop_code': 'sdd2', 'sale_amount': '5'},
    {'id': '3', 'shop_code': 'sdd3', 'sale_amount': '3'},
]
doris.streamload(table='streamload_test', dict_array=data)

# delete
data = [
    {'id': '1'},
]
doris.streamload(table='streamload_test', dict_array=data, merge_type='DELETE')

# merge
data = [
    {'id': '10', 'shop_code': 'sdd1', 'sale_amount': '99', 'delete_flag': 0},
    {'id': '2', 'shop_code': 'sdd2', 'sale_amount': '5', 'delete_flag': 1},
    {'id': '3', 'shop_code': 'sdd3', 'sale_amount': '3', 'delete_flag': 1},
]
doris.streamload(table='streamload_test', dict_array=data, merge_type='MERGE', delete='delete_flag=1')

# Sequence append
data = [
    {'id': '1', 'shop_code': 'sdd1', 'sale_amount': '99', 'source_sequence': 11, },
    {'id': '1', 'shop_code': 'sdd2', 'sale_amount': '5', 'source_sequence': 2},
    {'id': '2', 'shop_code': 'sdd3', 'sale_amount': '3', 'source_sequence': 1},
]
doris.streamload(table='streamload_test', dict_array=data, sequence_col='source_sequence')

## Sequence merge
data = [
    {'id': '1', 'shop_code': 'sdd1', 'sale_amount': '99', 'source_sequence': 100, 'delete_flag': 0},
    {'id': '1', 'shop_code': 'sdd2', 'sale_amount': '5', 'source_sequence': 120, 'delete_flag': 0},
    {'id': '2', 'shop_code': 'sdd3', 'sale_amount': '3', 'source_sequence': 100, 'delete_flag': 1},
]
doris.streamload(table='streamload_test', dict_array=data, sequence_col='source_sequence', merge_type='MERGE',
                 delete='delete_flag=1')
```

## execute doris-sql

```python
from DorisClient import DorisSession

doris_cfg = {
    'fe_servers': ['10.211.7.131:8030', '10.211.7.132:8030', '10.211.7.133:8030'],
    'database': 'testdb',
    'user': 'test',
    'passwd': '123456',
}
doris = DorisSession(**doris_cfg)

# fetch all the rows by sql
rows = doris.read('select * from streamload_test limit 1')
print(rows)

# execute sql commit
doris.execute('truncate table streamload_test')
```

## collect meta

```python
from DorisClient import DorisMeta

doris_cfg = {
    'fe_servers': ['10.211.7.131:8030', '10.211.7.132:8030', '10.211.7.133:8030'],
    'database': 'testdb',
    'user': 'test',
    'passwd': '123456',
}
dm = DorisMeta(**doris_cfg)

# auto create table for collect doris meta
# 1. meta_table for saving all table meta
# 2. meta_tablet for saving all tablet meta
# 3. meta_partition for saving all partition meta
dm.create_tables()

# collect table meta >> meta_table
dm.collect_table()

# collect tablet meta >> meta_tablet
dm.collect_tablet()

# collect partition meta >> meta_partition
dm.collect_partition()
```
