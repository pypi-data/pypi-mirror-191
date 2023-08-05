from stonewave.sql.udtfs.base_function import BaseFunction, udtf
from stonewave.sql.udtfs.logger import logger


# TODO: change `is_parser` to True if your table function parses an event and extracts fields from the event.
# Each event parsing SHOULD produce exactly one event.
# by specifying `is_parser` property, the performance will be better
@udtf(is_parser=False)
class {{ func_class }}(BaseFunction):
    def get_name(self):
        """
        :return: the name of table function
        """
        return "{{ func_name }}"

    def initialize(self, table_writer):
        """
        This method will be called once for every batch in the input table with function applied operation
        :param table_writer: table writer for writing produced results
        :return: None
        """
        pass

    def __init__(self):
        pass

    def process(self, params, table_writer, context):
        """
        This method is main body of function using input parameters.
        When applying table function, it will be called once for every row from input table.
        :param params: a list containing all of the input parameters
        :param table_writer: Use the `table_writer` to write the produced rows and columns into the result table.
            `table_writer` has three writing mode:
                - row oriented
                - column oriented
                - batch oriented
            in a function process, single writing mode is required. related apis are:
                - write_row(kv_pairs) (all values are turned into string type)
                - write_column(column_name, column_type, [column_values])
                - batch_iterator
        :param context: context that maintaining more information, which is reserved for future
        :return: None
        """    
        # method 1:
        # using kv pairs to append row, kv pairs means column name and column value
        # all results are appended in string datatype
        num1 = params[0]
        num2 = params[1]
        table_writer.write_row({"add_result": num1+num2 })
        # ===>  | add_result |
        #       |  num1+num2 |

        """
        # method 2 (Advanced):
        # using write_column to add a column using pyarrow datatype
        # using extend to append multiple value for column
        num1 = params[0]
        num2 = params[1]
        import pyarrow
        table_writer.write_column("add_result", pyarrow.int64(), [int(num1) + int(num2)])
        """
