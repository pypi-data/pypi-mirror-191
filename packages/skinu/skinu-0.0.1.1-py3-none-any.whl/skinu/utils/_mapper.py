import os
import sys
import xml.etree.cElementTree as xmlParse

from skinu._internal._logs import _skinuLog
from skinu.core import str_utils


#
# class Mapper
#
class Mapper:
    __Query_map: dict

    @staticmethod
    def init(p_mapper_file: str) -> bool:
        Mapper.__Query_map = dict()

        tmp_is_ret = False
        tmp_mapper_path = os.path.dirname(os.path.realpath(p_mapper_file))

        try:
            tmp_tree = xmlParse.parse(p_mapper_file)
            tmp_iter_configuration = tmp_tree.iter(tag="configuration")
            for tmp_elem_configuration in tmp_iter_configuration:
                # mappers 읽기
                tmp_iter_mappers = tmp_elem_configuration.iter(tag="mappers")
                for tmp_elem_mappers in tmp_iter_mappers:
                    # mapper 읽기
                    tmp_iter_mapper = tmp_elem_mappers.iter(tag="mapper")
                    for tmp_elem_mapper in tmp_iter_mapper:
                        Mapper._read_mapper_file(tmp_mapper_path, tmp_elem_mapper)

        except OSError as err:
            tmp_is_ret = False
            _skinuLog.getLogger().warning(err)

        except ValueError as ve:
            tmp_is_ret = False
            _skinuLog.getLogger().warning(ve)

        except:
            tmp_is_ret = False
            _skinuLog.getLogger().warning("unexpected error: {}".format(sys.exec_info()[0]))

        return tmp_is_ret

    def _read_mapper_file(p_mapper_path: str, p_elem_mapper: str) -> None:
        if p_elem_mapper == None:
            return

        tmp_resource_file = p_elem_mapper.get("resource")
        tmp_mapper_file = p_mapper_path + os.path.sep + tmp_resource_file

        tmp_mapper_tree = xmlParse.parse(tmp_mapper_file)
        tmp_iter_mapper = tmp_mapper_tree.iter(tag="mapper")
        for tmp_elem_mapper in tmp_iter_mapper:
            tmp_namespace_id = tmp_elem_mapper.get("namespace")
            if str_utils.is_not_empty_str(tmp_namespace_id) == True:
                tmp_iter_query = tmp_elem_mapper.iter()
                for tmp_elem_query in tmp_iter_query:
                    tmp_query_tag = tmp_elem_query.tag
                    if tmp_query_tag in ["select", "update", "insert", "delete"]:
                        tmp_query_id = tmp_elem_query.get("id")
                        tmp_query_text = tmp_elem_query.text

                        if str_utils.is_not_empty_str(tmp_query_id) and str_utils.is_not_empty_str(tmp_query_text):
                            tmp_query_key = tmp_namespace_id + "." + tmp_query_id
                            tmp_query_data = " ".join([line.strip() for line in tmp_query_text.strip().splitlines()])

                            Mapper.__Query_map[tmp_query_key] = tmp_query_data

    def get(p_query_id: str) -> str:
        from skinu.core import dict_utils

        tmp_query_data = dict_utils.get_str(Mapper.__Query_map, p_query_id)
        return tmp_query_data

    def clear() -> None:
        Mapper.__Query_map = dict()
