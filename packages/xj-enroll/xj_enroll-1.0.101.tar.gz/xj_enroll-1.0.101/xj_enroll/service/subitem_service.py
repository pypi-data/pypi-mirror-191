# encoding: utf-8
"""
@project: djangoModel->subitem_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 报名分项记录
@created_time: 2022/10/15 12:38
"""

from django.core.paginator import Paginator
from django.db.models import F

from ..models import EnrollSubitem, EnrollSubitemExtendField, Enroll, EnrollSubitemRecord
from ..serializers import EnrollSubitemSerializer
from ..service.enroll_status_code_service import EnrollStatusCodeService
from ..service.enroll_subitem_record_service import EnrollSubitemRecordService
from ..service.subitem_extend_service import input_convert, output_convert
from ..utils.custom_tool import format_params_handle


class SubitemService:
    @staticmethod
    def add(params):
        enroll_id = params.get("enroll_id")
        if not enroll_id:
            return None, "请填写报名ID"

        params = input_convert(
            params_dict=params,
            enroll_id=enroll_id
        )
        # print("SubitemService.params", params)
        try:
            instance = EnrollSubitem.objects.create(**params)
            return instance.to_json(), None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def detail(pk=None):
        # 参数验证
        subitem_obj = EnrollSubitem.objects.annotate(category_id=F("enroll__category_id")).filter(id=pk).first()
        if not subitem_obj:
            return None, "找不到ID为" + str(pk) + "的数据"

        subitem_dict = EnrollSubitemSerializer(subitem_obj, many=False).data
        subitem_list = output_convert([subitem_dict])
        subitem_detail = subitem_list[0] if subitem_list else {}

        subitem_detail["subitem_record_list"] = list(EnrollSubitemRecord.objects.filter(enroll_subitem_id=pk).values())
        return subitem_detail, None

    @staticmethod
    def list(params, is_pagination=True):
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        # 字段过滤
        user_id = params.pop("user_id", None)
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["id", "category_id", "enroll_subitem_status_code", "enroll_id", "name", "price", "count", "unit", "description", "remark"],
            alias_dict={"name": "name__contains"}
        )
        try:
            fetch_obj = EnrollSubitem.objects.annotate(category_id=F("enroll__category_id")).filter(**params).values()
            if not is_pagination:
                result_list = output_convert(list(fetch_obj))

                # 拼接分项记录
                subitem_ids = [i["id"] for i in result_list]
                res_list, err = EnrollSubitemRecordService.list({"enroll_subitem_id__in": subitem_ids}, False)
                subitem_record_map = {}
                for item in res_list:
                    if subitem_record_map.get(item["enroll_subitem_id"]):
                        subitem_record_map[item["enroll_subitem_id"]].append(item)
                    else:
                        subitem_record_map[item["enroll_subitem_id"]] = [item]

                for item in result_list:
                    item["subitem_record_list"] = subitem_record_map.get(item.get("id"))
                return result_list, None

            paginator = Paginator(fetch_obj, size)
            page_obj = paginator.page(page)
            result_list = list(page_obj.object_list)
            result_list = output_convert(result_list)

            # 拼接分项记录
            subitem_ids = [i["id"] for i in result_list]
            res_list, err = EnrollSubitemRecordService.list({"enroll_subitem_id__in": subitem_ids}, False)
            subitem_record_map = {}
            for item in res_list:
                if subitem_record_map.get(item["enroll_subitem_id"]):
                    subitem_record_map[item["enroll_subitem_id"]].append(item)
                else:
                    subitem_record_map[item["enroll_subitem_id"]] = [item]

            data = {'total': paginator.count, "size": size, 'page': page, 'list': result_list}
            return data, None
        except Exception as e:
            return [], str(e)

    @staticmethod
    def edit(params, subitem_id=None):
        # 参数验证
        subitem_id = subitem_id or params.pop("id", None) or 0
        subitem_obj = EnrollSubitem.objects.filter(id=subitem_id)
        subitem_obj_first = subitem_obj.first()
        if not subitem_obj_first:
            return None, "找不到ID为" + str(subitem_id) + "的数据"
        # 开始修改
        enroll_id = params.get("enroll_id") or subitem_obj_first.to_json().get("enroll_id")
        print("enroll_id", enroll_id)
        try:
            # 参数解析
            params = input_convert(
                params_dict=params,
                enroll_id=enroll_id
            )
            subitem_obj.update(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)

        # 联动修改全部报名相关得到状态
        unfinish_count = EnrollSubitem.objects.filter(enroll_id=enroll_id).exclude(enroll_subitem_status_code=668).exclude(enroll_subitem_status_code=124).count()
        if unfinish_count == 0 and enroll_id:
            EnrollStatusCodeService.batcch_edit_code(enroll_id, params.get("enroll_subitem_status_code", 668))

        return None, None

    # 批量修改
    @staticmethod
    def batch_edit(params, enroll_id=None):
        enroll_id = enroll_id or params.pop("enroll_id", None)
        if not enroll_id:
            return None, "请填写报名ID"

        # 参数根据类别转化
        params = input_convert(
            params_dict=params,
            enroll_id=enroll_id
        )
        if not params:
            return None, "enroll_id不能为空，或者参数为空"

        subitem_enroll_obj = EnrollSubitem.objects.filter(enroll_id=enroll_id)
        if not subitem_enroll_obj:
            return None, "没有找到enroll_id为" + str(enroll_id) + "的报名分项"
        try:
            subitem_enroll_obj.update(**params)
        except Exception as e:
            return None, "修改参数错误:" + str(e)
        return None, None

    @staticmethod
    def delete(subitem_rule_id):
        subitem_enroll_obj = EnrollSubitem.objects.filter(id=subitem_rule_id)
        if not subitem_enroll_obj:
            return None, None
        try:
            subitem_enroll_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None

    @staticmethod
    def extend_field(params=None, is_pagination=True):
        validate_params = params if isinstance(params, dict) else {}

        size = validate_params.pop('size', 10)
        page = validate_params.pop('page', 1)

        filtered_params = format_params_handle(
            param_dict=validate_params,
            filter_filed_list=["id", "category_id", "field_index", "field", "label", "type", "config", "description", ],
            alias_dict={"field": "field__contains", "label": "label__contains"}
        )

        try:
            extend_obj = EnrollSubitemExtendField.objects.all()
            extend_obj_list = extend_obj.filter(**filtered_params).values()
            if not is_pagination:
                return list(extend_obj_list), None

            paginator = Paginator(extend_obj_list, size)
            paginator_obj_list = paginator.page(page)
            data = {'total': paginator.count, "size": size, 'page': page, 'list': list(paginator_obj_list.object_list)}
            return data, None
        except Exception as e:
            return [], "查询参数错误：" + str(e)

    @staticmethod
    def check_num(enroll_id):
        enroll_obj = Enroll.objects.filter(id=enroll_id).first()
        if not enroll_obj:
            return False
        enroll_count = enroll_obj.to_json().get("count")
        subitem_count = EnrollSubitem.objects.filter(enroll_id=enroll_id).count()
        if enroll_count > subitem_count:
            return True
        return False
