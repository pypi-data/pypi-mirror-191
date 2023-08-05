import sys
import os
sys.path.append(os.path.dirname(__file__))

import warnings
import random
import happybase
import pandas as pd
from reconnection import reconnection
from conf_reader import read_conf

# logger = get_logger(__name__, format_level='runtime_with_time')


class HBaseClient(object):
    def __init__(self,
                 host=None, port=9090,
                 file_path=None,
                 server_type=None,
                 connection_num=5,
                 time_out=15,
                 env='test'):
        """
        :param host(str): 指定hbase库ip地址
        :param port(str, int): 指定hbase库端口号,数字形式
        :param file_path(str): 配置文件路径
        :param server_type(str): 指定需要连接的服务器类型(pro/dev)
        :param connection_num(int): 连接池中的连接数
        :param time_out(int): 获取连接时的最大等待时间
        :param env (str): 'test' or 'prd', 由于生产环境与测试环境版本不一致，短暂使用
        """
        self.connection_num = connection_num
        self.time_out = time_out
        self.host = host
        self.port = port
        self.env = env

        if (file_path is not None) & (server_type is not None):
            try:
                confs = read_conf(file_path, server_type)
                if isinstance(confs, (list, tuple)):
                    conf = random.choice(confs)
                else:
                    conf = confs
                self.host = conf['host']
                self.port = conf['port']
            except FileNotFoundError:
                warnings.warn('You specified "server_type" but there is no .yml file was found.')
                pass
            except KeyError:
                warnings.warn('Yaml file has no key called "host" or "port".')
                pass

        if (self.host is None) | (self.port is None):
            raise ValueError('Host and port cannot be None.')

        self.connection_pool = None
        # logger.info(f"host={self.host},port={self.port}")

    @reconnection
    def build_pool(self):
        """
        :func: 建立可选size的连接池
        :return: None
        """
        self.connection_pool = happybase.ConnectionPool(
            size=self.connection_num, 
            host=self.host, 
            port=self.port,
            # Below is a bug fix for hbase version over 2.0
            transport='framed',  # Default: 'buffered'  <---- Changed.
            protocol='compact'   # Default: 'binary'    <---- Changed.
        )

    @reconnection
    def create_tbl(self, table_name, table_desc):
        """
        :func: 在当前库中创建数据表
        :param table_name（str）– 创建的表名
        :param table_desc（dict）– 指定列族选项，格式为families = {
            'cf1': dict(max_versions=10),
            'cf2': dict(max_versions=1, block_cache_enabled=False),
            'cf3': dict(),  # use defaults
            }
        :return: None
        """
        with self.connection_pool.connection() as connect:
            table_list = connect.tables()
            if table_name.encode() not in table_list:
                connect.create_table(table_name, table_desc)
            else:
                # logger.warn(f"{self.table_name} exist, pass create operation")
                print('exist')
                
    @reconnection
    def show_tables(self):
        """
        :func: 获取当前库中所有表名
        :return: 表名list
        """
        with self.connection_pool.connection() as connect:
            table_list = connect.tables()
        return table_list

    @reconnection
    def scan_tables(self, table_name, row_start=None, row_stop=None,
                    row_prefix=None, columns=None, timestamp=None, 
                    include_timestamp=False, batch_size=1000, limit=None, 
                    sorted_columns=False):
        """
        :func: 获取当前库中所有表名
        :param table_name(str) - 表名
        :param row_start (str) – 开始的行健（包含）
        :param row_stop (str) – 结束的行健（不包含）
        :param row_prefix (str) – 扫描以该字符串开头的行健
        :param columns (list_or_tuple) – 需要返回的列
        :param timestamp (int) – 时间戳区间
        :param include_timestamp (bool) – 返回结果是否包含时间戳
        :param batch_size (int) – 查询结果的batch size
        :param limit (int) – 限制返回结果的条数
        :param sorted_columns (bool) – 是否将列排序
        :return: (table_size,表数据)
        """
        if not(row_start or row_stop or row_prefix or columns):
            with self.connection_pool.connection() as connect:
                table = connect.table(table_name)
                scan_data = table.scan(row_start=row_start, row_stop=row_stop, 
                                       row_prefix=row_prefix, columns=columns, timestamp=timestamp,
                                       include_timestamp=include_timestamp,
                                       batch_size=batch_size, limit=limit,
                                       sorted_columns=sorted_columns)
            scan_data = list(scan_data)
            return len(scan_data), scan_data
        if row_start and not isinstance(row_start, str):
            raise TypeError(f"{type(row_start)} not str")  
        elif row_start:
            row_start = row_start.encode()
        if row_stop and not isinstance(row_stop, str):
            raise TypeError(f"{type(row_stop)} not str")
        elif row_stop:
            row_stop = row_stop.encode()
        if row_prefix and not isinstance(row_prefix, str):
            raise TypeError(f"{type(row_prefix)} not str")
        elif row_prefix:
            row_prefix = row_prefix.encode()
        if columns and not isinstance(columns, (list, tuple)):
            raise TypeError(f"{type(columns)} not list/tuple") 
        elif columns:
            columns = [str(k).encode() for k in columns]
        with self.connection_pool.connection() as connect:
            table = connect.table(table_name)
            scan_data = table.scan(row_start=row_start, row_stop=row_stop, 
                                   row_prefix=row_prefix, columns=columns, timestamp=timestamp,
                                   include_timestamp=include_timestamp,
                                   batch_size=batch_size, limit=limit,
                                   sorted_columns=sorted_columns)
        scan_data = list(scan_data)
        return len(scan_data), scan_data
        
    @reconnection
    def get_families(self, table_name):
        with self.connection_pool.connection() as connect:
            table = connect.table(table_name)
            families = table.families()
        return families
    
    @reconnection
    def get_regions(self, table_name):
        with self.connection_pool.connection() as connect:
            table = connect.table(table_name)
            regions = table.regions()
        return regions
    
    @reconnection
    def insert(self, table_name, datas, timestamp=None, batch_size=1000):
        # datas: {row_key: {'column_family:feature': value}}
        with self.connection_pool.connection() as connect:
            table = connect.table(table_name)
            with table.batch(batch_size=batch_size, timestamp=timestamp) as batch_ops:
                for row_key, values in datas.items():
                    row_key = row_key if isinstance(row_key, bytes) else str(row_key).encode()
                    output_values = {}
                    for k, v in values.items():
                        k = k if isinstance(k, bytes) else str(k).encode()
                        v = v if isinstance(v, bytes) else str(v).encode()
                        output_values.update({k: v})
                    # values = {str(k).encode(): str(v).encode() for k, v in values.items()}
                    batch_ops.put(row_key, output_values)
                    
    
    @reconnection
    def insert_df(self, table_name, df, rowkeys_col, batch_size=1000, timestamp=None):
        if not isinstance(df, pd.DataFrame) and isinstance(rowkeys_col, str):
            raise TypeError(f"{type(df)} not DataFrame or {type(rowkeys_col)} not str")
        if len(df[rowkeys_col]) != df[rowkeys_col].nunique():
            raise ValueError(f"columns:{rowkeys_col} must be unique")
        datas = df.set_index([rowkeys_col]).to_dict(orient='index')
        self.insert(table_name=table_name, datas=datas, batch_size=batch_size, timestamp=timestamp)
        # with self.connection_pool.connection() as connect:
        #     table = connect.table(table_name)
        #     with table.batch(batch_size=batch_size, timestamp=timestamp) as batch_ops:
        #         for row_key, values in datas.items():
        #             values = {str(k).encode(): str(v).encode() for k, v in values.items()}
        #             batch_ops.put(row_key.encode(), values)
    
    @reconnection
    def insert_csv(self, table_name, file_path, rowkeys_col, batch_size=1000, timestamp=None):
        if not isinstance(file_path, str):
            raise TypeError(f"{type(file_path)} not str")
        df = pd.read_csv(file_path)
        self.insert_df(table_name, df, rowkeys_col, batch_size, timestamp)
    
    @reconnection
    def delete(self, table_name, row_key, timestamp=None, columns=None, batch_size=1000):
        """
        根据行健删除数据
        Args:
            table_name:
            row_key:
            timestamp:
            columns:
            batch_size:

        Returns:

        """
        if isinstance(columns, (list, tuple)):
            columns = [str(v).encode() for v in columns]
        with self.connection_pool.connection() as connect:
            table = connect.table(table_name)
            if isinstance(row_key, str):
                table.delete(row_key.encode(), timestamp=timestamp, columns=columns)
            elif isinstance(row_key, (list, tuple)):
                with table.batch(batch_size=batch_size, timestamp=timestamp) as b:
                    for i in row_key:
                        b.delete(i.encode(), columns=columns)
            else:
                raise TypeError(f"{type(row_key)} not str/list/tuple")

    @reconnection
    def query(self, table_name, row_keys):
        with self.connection_pool.connection() as connect:
            table = connect.table(table_name)
            if isinstance(row_keys, str):
                row = [(row_keys, table.row(row_keys.encode())), ]
            elif isinstance(row_keys, (list, tuple)):
                row_keys = [str(v).encode() for v in row_keys]
                row = list(table.rows(row_keys))
            else:
                raise TypeError(f"{type(row_keys)} not str/list/tuple")
        return len(row), row

    @reconnection
    def delete_tbl(self, table_name):
        with self.connection_pool.connection() as connect:
            table_list = connect.tables()
            if table_name.encode() in table_list:
                connect.disable_table(table_name)
                connect.delete_table(table_name)
            else:
                # logger.warn(f"{self.table_name} not exist")
                pass

    @reconnection
    def truncate_tbl(self, table_name, table_desc):
        with self.connection_pool.connection() as connect:
            self.delete_tbl(table_name)
            connect.create_table(table_name, table_desc)


if __name__ == '__main__':
    connection = HBaseClient(
        host='192.168.39.3',
        port='9090',
        server_type='pro'
    )
    connection.build_pool()
    print(connection.show_tables())
    print(connection.scan_tables(
        table_name='pred_system:dim_dm_routing_plan_gd_transform_factor',
        limit=10
    ))
