"""Process Shopify Return."""
import logging
from typing import Dict, List, Optional, Union, Tuple
import pandas as pd
from numpy import nan
import sqlalchemy as sa
import sqlalchemy.dialects.mssql as mssql
import sqlalchemy.dialects.mysql as mysql
from pyshopify.db_model import DBModel
logger = logging.getLogger(__name__)


def products_work(json_list: list) -> Dict[str, pd.DataFrame]:
    """Parse Products data"""
    products_dict = {}

    prod_table = products_parse(json_list)
    if prod_table is not None:
        products_dict['products'] = prod_table

    variants_table = variants_parse(json_list)
    if variants_table is not None:
        products_dict['variants'] = variants_table

    options_table = options_parse(json_list)
    if options_table is not None:
        products_dict['product_options'] = options_table
    return products_dict


def locations_parse(data: List[dict]) -> pd.DataFrame:
    """Parse inventory locations response."""
    loc_df = pd.DataFrame.from_records(data)
    loc_df = DFWork.convert_df('inventory_locations', loc_df)
    return loc_df


def inventory_levels_parse(data: List[dict]) -> pd.DataFrame:
    """Parse inventory levels response."""
    inv_df = pd.DataFrame.from_records(data)
    inv_df = DFWork.convert_df('inventory_levels', inv_df)
    return inv_df


def products_parse(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse products into dataframe from API response."""
    products = pd.json_normalize(data, sep='_')
    if len(products.index) > 0:
        products = DFWork.convert_df('products', products)
        return products
    return None


def variants_parse(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse variants into dataframe from API response."""
    variants = pd.json_normalize(data, ['variants'])
    if len(variants.index) > 0:
        variants = DFWork.convert_df('variants', variants)
        return variants
    return None


def options_parse(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse Product Options Data."""
    options = pd.json_normalize(data, ['options'])
    if len(options.index) > 0:
        options['values'] = options['values'].apply(",".join)
        options = DFWork.convert_df('product_options', options)

        return options
    return None


def pandas_work(json_list: list) -> Dict[str, pd.DataFrame]:
    """Parse orders API return data."""
    table_dict = {}

    orders, prices = orders_work(json_list)
    if orders is not None:
        table_dict['orders'] = orders
    if prices is not None:
        table_dict['order_prices'] = prices

    ship_lines = ship_lines_work(json_list)
    if ship_lines is not None:
        table_dict['ship_lines'] = ship_lines

    refunds = refunds_work(json_list)
    if refunds is not None:
        table_dict['refunds'] = refunds

        refund_li = refund_line_items_work(json_list)
        if refund_li is not None:
            table_dict['refund_line_item'] = refund_li

        adjustments = adjustments_works(json_list)
        if adjustments is not None:
            table_dict['adjustments'] = adjustments

    discount_apps = discount_app_work(json_list)
    if discount_apps is not None:
        table_dict['discount_apps'] = discount_apps

    discount_codes = discount_code_work(json_list)
    if discount_codes is not None:
        table_dict['discount_codes'] = discount_codes

    line_items = line_item_work(json_list)
    if line_items is not None:
        table_dict['line_items'] = line_items

    order_attr = order_attr_work(json_list)
    if order_attr is not None:
        table_dict['order_attr'] = order_attr

    return table_dict


def order_attr_work(data: list) -> Optional[pd.DataFrame]:
    """Parse order attribution data."""
    attr = pd.json_normalize(data, ['orders'], max_level=1)
    if len(attr.index) > 0:
        attr.rename(columns={'id': 'order_id'}, inplace=True)
        attr = DFWork.convert_df('order_attr', attr)
        return attr
    return None


def orders_work(data: list
                ) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """Parse order lines into dataframe from API response."""
    order_data = pd.json_normalize(data, ['orders'], sep='_')
    if len(order_data) > 0:
        orders = DFWork.convert_df('orders', order_data.copy())

        orders['payment_gateway_names'] = (orders['payment_gateway_names']
                                           .astype(str)
                                           .str.replace('[', '', regex=False))
        orders['payment_gateway_names'] = (orders['payment_gateway_names']
                                           .str.replace(']', '', regex=False))
        orders['payment_gateway_names'] = (orders['payment_gateway_names']
                                           .str.replace("'", '', regex=False))

        prices = order_data.rename(columns={
            'total_shipping_price_set_shop_money_amount': 'total_shipping_price',
            'id': 'order_id'
        })
        prices = DFWork.convert_df('order_prices', prices)
        return orders, prices
    return None, None


def ship_lines_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse shipping lines to dataframe from API response."""
    shiplines = pd.json_normalize(data, ['orders', 'shipping_lines'],
                                  meta=[['orders', 'id'],
                                        ['orders', 'processed_at']])
    if len(shiplines.index) > 0:
        shiplines.rename(columns={
            'orders.id': 'order_id',
            'orders.processed_at': 'processed_at'
            },
                         inplace=True)
        shiplines = DFWork.convert_df('ship_lines', shiplines)
        return shiplines
    return None


def refunds_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse refunds into dataframe from API Response."""
    refunds = pd.json_normalize(data, ['orders', 'refunds'],
                                meta=[['orders', 'processed_at']])
    if len(refunds.index) > 0:
        refunds.rename(columns={'orders.processed_at': 'order_date'},
                       inplace=True)
        refunds = DFWork.convert_df('refunds', refunds)
        return refunds
    return None


def refund_line_items_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse refund line items from API response into dataframe."""
    refundli = pd.json_normalize(data,
                                 ['orders', 'refunds', 'refund_line_items'],
                                 meta=[['orders', 'refunds', 'id'],
                                       ['orders', 'id'],
                                       ['orders', 'refunds', 'processed_at'],
                                       ['orders', 'processed_at']])
    if len(refundli.index) > 0:
        refundli.rename(columns={
            'orders.refunds.id': 'refund_id',
            'orders.id': 'order_id',
            'orders.refunds.processed_at': 'processed_at',
            'orders.processed_at': 'order_date',
            'line_item.variant_id': 'variant_id',
            'line_item.line_item_id': 'line_item_id'},
            inplace=True)
        refundli = DFWork.convert_df('refund_line_item', refundli)
        return refundli
    return None


def adjustments_works(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse adjustments into dataframe from API response."""
    adjusts = pd.json_normalize(data,
                                ['orders', 'refunds', 'order_adjustments'],
                                meta=[['orders', 'refunds', 'processed_at'],
                                      ['orders', 'processed_at']])
    if len(adjusts.index) > 0:
        adjusts.rename(columns={'orders.refunds.processed_at': 'processed_at',
                                'orders.processed_at': 'order_date'},
                       inplace=True)
        adjusts = DFWork.convert_df('adjustments', adjusts)
        return adjusts
    return None


def discount_app_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse discount application into dataframe."""
    discapp = pd.json_normalize(data, ['orders', 'discount_applications'],
                                meta=[['orders', 'id'],
                                      ['orders', 'processed_at']],
                                sep='_')
    if len(discapp.index) > 0:
        discapp.rename(columns={
            'orders_id': 'order_id',
            'orders_processed_at': 'processed_at'
            }, inplace=True)
        discapp['id_cnt'] = discapp.groupby('order_id').cumcount() + 1
        discapp['id'] = discapp['order_id'].astype(str) + discapp['id_cnt'].astype(str)
        discapp = DFWork.convert_df('discount_apps', discapp)
        return discapp
    return None


def discount_code_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse discount code lines from API response into dataframe."""
    disccode = pd.json_normalize(data, ['orders', 'discount_codes'],
                                 meta=[['orders', 'id'],
                                       ['orders', 'processed_at']],
                                 sep='_')
    if len(disccode.index) > 0:
        disccode.rename(columns={
            'orders_id': 'order_id',
            'orders_processed_at': 'processed_at'
        }, inplace=True)
        disccode = DFWork.convert_df('discount_codes', disccode)
        return disccode
    return None


def line_item_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse order line items into dataframe from API response."""
    lineitems = pd.json_normalize(data, ['orders', 'line_items'],
                                  meta=[['orders', 'id'],
                                        ['orders', 'processed_at']],
                                  max_level=1)

    if len(lineitems.index) > 0:
        lineitems.rename(columns={'orders.id': 'order_id',
                                  'orders.processed_at': 'processed_at'},
                         inplace=True)
        lineitems = DFWork.convert_df('line_items', lineitems)
        return lineitems
    return None


def customers_work(data: List[dict]) -> Optional[pd.DataFrame]:
    """Parse order customers into dataframe from API response."""
    customers = pd.json_normalize(data, ['customers'], sep='_')
    if len(customers) > 0:
        customers.rename(columns={
                'default_address_city': 'city',
                'default_address_province': 'province',
                'default_address_country': 'country',
                'default_address_zip': 'zip'
                }, inplace=True)
        customers = DFWork.convert_df('customers', customers)
        return customers
    return None


def clean_num_cols(df: pd.DataFrame,
                   col_list: Union[List[str], str]) -> pd.DataFrame:
    """Clean columns in dataframe."""
    if isinstance(col_list, str):
        col_list = [col_list]
    for col in col_list:
        if col not in df.columns:
            logger.debug("Column % not in dataframe", col)
            continue
        df[col] = (df[col].replace(r'^\s*$', nan, regex=True))
        df[col] = df[col].fillna(0)
    return df


def fill_string_cols(df: pd.DataFrame,
                     exclude_list: Optional[list] = None) -> pd.DataFrame:
    """Fill string columns with empty string."""
    for col in df:
        if exclude_list is not None and col in exclude_list:
            continue
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('')
    return df


class DFWork:
    dtypes = {
        'int64': [sa.BIGINT, sa.BigInteger],
        'int32': [sa.INTEGER, sa.Integer],
        'str': [sa.String, sa.VARCHAR, sa.NVARCHAR, sa.NCHAR,
                sa.Text, sa.Unicode, sa.CHAR, sa.UnicodeText, sa.TEXT,
                mssql.NTEXT, mysql.TEXT, mysql.NCHAR, mysql.NVARCHAR,
                mysql.VARCHAR, mysql.CHAR],
        'int16': [sa.SMALLINT, sa.SmallInteger],
        'bool': [sa.BOOLEAN, sa.Boolean, mssql.BIT],
        'float': [sa.Float, sa.FLOAT, sa.Numeric, sa.NUMERIC, sa.DECIMAL,
                  sa.REAL, mssql.MONEY, mssql.SMALLMONEY, mysql.NUMERIC,
                  mysql.DECIMAL, mysql.FLOAT, mysql.REAL],
    }
    num_types = [
        *dtypes['int64'],
        *dtypes['int32'],
        *dtypes['int16'],
        *dtypes['float']
    ]

    date_types = [sa.DateTime, sa.Date, sa.DATETIME, sa.TIMESTAMP, sa.DATE,
                  mssql.DATETIMEOFFSET]

    @classmethod
    def convert_df(cls, tbl_name: str, df: pd.DataFrame):
        """Convert DataFrame Types Based on SQL Table."""
        model = DBModel().model
        meta = model.metadata
        table = meta.tables[tbl_name]
        df = cls._get_columns(df, table)
        df = cls._fill_null(df, table)
        df_types = cls._get_types(table)
        if df_types:
            df = df.astype(df_types)
        df = cls._convert_dates(df, table)
        return df

    @classmethod
    def _fill_null(cls, df: pd.DataFrame, table: sa.Table) -> pd.DataFrame:
        for col in table.columns:
            if type(col.type) in cls.num_types:
                df[col.name].replace(r'^\s*$', nan, regex=True, inplace=True)
            if col.nullable is False and type(col.type) in cls.num_types:
                df[col.name].fillna(0, inplace=True)
            elif type(col.type) in cls.dtypes['str']:
                df[col.name].fillna('', inplace=True)
        return df

    @classmethod
    def _get_columns(cls, df: pd.DataFrame, table: sa.Table) -> pd.DataFrame:
        """Get columns from table."""
        df.drop(df.columns.difference(table.c.keys()),
                inplace=True, axis='columns')
        df = df.reindex(columns=table.c.keys())
        return df

    @classmethod
    def _get_types(cls, tbl: sa.Table) -> dict:
        type_dict = {}
        for col in tbl.c:
            for str_type, sa_types in cls.dtypes.items():
                if type(col.type) in sa_types:
                    type_dict[col.name] = str_type
                    if col.nullable and str_type in ['int64', 'int32', 'int16']:
                        type_dict[col.name] = str_type.replace('i', 'I')
        return type_dict

    @classmethod
    def _convert_dates(cls, df: pd.DataFrame, tbl: sa.Table) -> pd.DataFrame:
        for col in tbl.c:
            if type(col.type) in cls.date_types:
                df[col.name] = pd.to_datetime(df[col.name], errors='coerce', utc=True)
                df[col.name] = df[col.name].dt.tz_convert(None)
        return df
