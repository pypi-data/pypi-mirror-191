import base64
import datetime
import json
import xlrd2

import pyDes
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission
from django.http import JsonResponse, HttpResponse
import django_filters as filters
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from base_system.models import Hospital, Office, Doctor, PositionTitle, User, ExtraGroup, InspectionDictionaries, \
    ExaminationDictionaries, DrugDirectory, PharmacyManagement
from base_system.serializers import ExportHospitalSerializer, ExportOfficeSerializer, UserSerializer, \
    PasswordSerializer, InspectionDictionariesSerializer, ExaminationDictionariesSerializer, \
    ExportInspectionDictionariesSerializer, ExportExaminationDictionariesSerializer, ExportDrugDirectorySerializer, \
    PharmacyManagementSerializer, ExportDoctorSerializer, ExportUserSerializer, DrugDirectorySerializer
from base_system.serializers import PermissionSerializer, ExportGroupSerializer

import xlrd as xlrd
from xlrd import xldate_as_tuple
import re
import pinyin


def register(request):
    """注册详情页"""
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        phone = data['phone']
        username = data['username']  # 工号
        user = User.objects.filter(username=username).first()

        if user and user.is_active is False:
            # 用户在所给的数据中验证通过，保存密码并激活
            user.is_active = True
            user.set_password('123456')
            user.phone = phone
            user.save()
            return JsonResponse({'data': True})
        else:
            return JsonResponse({'data': '该工号错误或者已被注册，请确认工号'})


def change_password(request):
    """修改用户信息"""
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    user_id = data['user_id']
    password = data['password']
    user = User.objects.get(id=user_id)

    if password:
        user.set_password(password)
        user.error_times = 0
        user.last_change_time = datetime.datetime.now()
        user.is_change_pwd = True
        user.save()
        res = {'data': True}
        return JsonResponse(res)


class PermissionsView(ListAPIView):
    """
    获取当前用户前端权限
    """
    serializer_class = PermissionSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """
        得到角色权限
        """
        # defaultgroup = self.request.user.get_default_group
        groups = self.request.user.groups.all()
        if groups:
            permissions = Permission.objects.filter(group__in=groups).distinct()
        else:
            permissions = Permission.objects.none()
        return permissions


class OverrideUserAuthentication(ModelBackend):
    """
    重写用户验证
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, request, username=None, password=None, appss=None, **kwargs):
        try:
            key = 'K3bDD6Zytur5RLCJ'
            pdes2 = PyDES3(key)
            decrypt_username = pdes2.decrypt(username)
            decrypt_password = pdes2.decrypt(password)
            user = User.objects.get(username=decrypt_username)
        except Exception as e:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            return None
        else:
            if user.check_password(decrypt_password):
                return user


'''
# 随机生成密钥
def __createkey(request):
    N = 16
    newkey = ''.join(secrets.choice(string.ascii_letters+string.digits) for _ in range(N))
    base64.b64decode(newkey.encode())
    return JsonResponse({'newkey': newkey})
'''


class PyDES3():
    def __init__(self, key):
        """
        三重DES加密、对称加密。py2下不可用
        :param key: 密钥
        """
        self.cryptor = pyDes.triple_des(key, padmode=pyDes.PAD_PKCS5)

    def encrypt(self, text):
        """
        加密
        :param text:
        :return:
        """
        x = self.cryptor.encrypt(text.encode())
        return base64.standard_b64encode(x).decode()

    def decrypt(self, text):
        """
        解密
        :param text:
        :return:
        """
        x = base64.standard_b64decode(text.encode())
        x = self.cryptor.decrypt(x)
        return x.decode()


column_header = {
    'height': 25,
    'style': {
        'fill': {
            'fill_type': 'solid',
            'start_color': 'FFCCFFCC',
        },
        'alignment': {
            'horizontal': 'center',
            'vertical': 'center',
            'wrapText': True,
            'shrink_to_fit': True,
        },
        'border_side': {
            'border_style': 'thin',
            'color': 'FF000000',
        },
        'font': {
            'name': 'Arial',
            'size': 14,
            'bold': True,
            'color': 'FF000000',
        },
    },
}

body = {
    'style': {
        'fill': {
            'fill_type': 'solid',
            'start_color': 'FFCCFFCC',
        },
        'alignment': {
            'horizontal': 'center',
            'vertical': 'center',
            'wrapText': True,
            'shrink_to_fit': True,
        },
        'border_side': {
            'border_style': 'thin',
            'color': 'FF000000',
        },
        'font': {
            'name': 'Arial',
            'size': 14,
            'bold': False,
            'color': 'FF000000',
        }
    },
    'height': 40,
}


class HospitalInfoFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    codenum = filters.CharFilter(field_name="codenum", lookup_expr='icontains')
    parent = filters.CharFilter(field_name="parent")

    class Meta:
        model = Hospital
        fields = (
            "name",
            "codenum",
            "parent",
        )


class HospitalInfoExportViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    pagination_class = None
    xlsx_use_labels = True
    xlsx_boolean_labels = {True: "是", False: "否"}
    queryset = Hospital.objects.all()
    serializer_class = ExportHospitalSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'hospital_export.xlsx'
    filterset_class = HospitalInfoFilter
    # filterset_fields = {"name": ["exact", "iexact", "contains", "icontains"], "is_active": ["exact", "in"]}

    header = {
        'tab_title': "医院信息",
        'header_title': "医院信息",
        'height': 25,
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': True,
                'color': 'FF000000',
            },
        },
    }

    def get_body(self):
        return body

    def get_column_header(self):
        return column_header


class OfficeInfoExportViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    pagination_class = None
    xlsx_use_labels = True
    xlsx_boolean_labels = {True: "是", False: "否"}
    queryset = Office.objects.all()
    serializer_class = ExportOfficeSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'office_export.xlsx'
    filterset_fields = {"name": ["exact", "iexact", "contains", "icontains"], "is_active": ["exact", "in"]}

    header = {
        'tab_title': "科室信息",
        'header_title': "科室信息",
        'height': 25,
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': True,
                'color': 'FF000000',
            },
        },
    }

    def get_body(self):
        return body

    def get_column_header(self):
        return column_header


class DoctorInfoExportViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    """医生信息导出接口"""
    pagination_class = None
    xlsx_use_labels = True
    xlsx_boolean_labels = {True: "是", False: "否"}
    queryset = Doctor.objects.all()
    serializer_class = ExportDoctorSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'doctor_export.xlsx'
    filterset_fields = {"name": ["exact", "iexact", "contains", "icontains"], "is_active": ["exact", "in"]}

    header = {
        'tab_title': "医生信息",
        'header_title': "医生信息",
        'height': 25,
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': True,
                'color': 'FF000000',
            },
        },
    }

    def get_body(self):
        return body

    def get_column_header(self):
        return column_header


import xlrd


def import_position_title(request):
    """导入excel表数据"""
    created_user = request.POST.get('created_user')
    excel_file = request.FILES.get('excel_file', '')  # 获取前端上传的文件
    file_type = excel_file.name.split('.')[1].split('"')[0]  # 拿到文件后缀
    # file_type = excel_file.name.split('.')[1]  # 拿到文件后缀
    data_list = []
    # PositionTitle
    if file_type in ['xlsx', 'xls']:  # 支持这两种文件格式
        # 打开工作文件
        try:
            data = xlrd.open_workbook(filename=None, file_contents=excel_file.read(), ragged_rows=True)
            sheets = data.sheets()
            for sheet in sheets:
                rows = sheet.nrows  # 总行数
                for row in range(2, rows):  # 从1开始是为了去掉表头
                    row_values = sheet.row_values(row)  # 每一行的数据
                    if row_values:
                        # codenum = row_values[0]  # 匹配编码
                        ctype = sheet.cell(row, 0).ctype  # 表格的数据类型
                        codenum = sheet.cell_value(row, 0)
                        if ctype == 2 and codenum % 1 == 0:  # 如果是整形
                            codenum = int(codenum)
                        name = row_values[1]
                        hospital_name = row_values[2]
                        hospital = Hospital.objects.get(name=hospital_name).id
                        created_time = row_values[3]
                        created_by = row_values[4]
                        positiontitle = PositionTitle.objects.filter(codenum=codenum)
                        if positiontitle:
                            positiontitle.update(**{"codenum": codenum,
                                                    "name": name,
                                                    "hospital": hospital,
                                                    "created_time": created_time,
                                                    "created_by": created_by,
                                                    })
                        else:
                            positiontitle.create(**{"codenum": codenum,
                                                    "name": name,
                                                    "hospital": hospital,
                                                    "created_time": created_time,
                                                    "created_by": created_by,
                                                    })
                        excel_data = {
                            "codenum": codenum,
                            "name": name,
                            "hospital": hospital,
                            "created_time": created_time,
                            "created_by": created_by,
                        }
                        data_list.append(excel_data)
        except Exception as e:
            raise e

    if data_list:
        res = {"data": data_list}
    else:
        res = {"data": "文件内容格式有误，请检查内容格式是否正确！"}
    return JsonResponse(res)


class UserFilter(filters.FilterSet):
    # company_id = filters.NumberFilter(field_name="company_id")
    # department_id = filters.NumberFilter(field_name="department_id")
    # job_id = filters.NumberFilter(field_name="job_id")
    gender = filters.NumberFilter(field_name="gender")
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    avatar_url = filters.CharFilter(field_name="avatar_url")

    class Meta:
        model = User
        fields = "__all__"


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    filterset_class = UserFilter
    filter_fields = "__all__"

    @action(methods=["PUT"], detail=True)
    def change_password(self, request, pk):
        # 更改密码
        serializer = PasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        password = serializer.data.get("password")
        user = self.get_object()
        user.set_password(password)
        user.last_change_time = datetime.datetime.now()
        user.error_times = 0
        user.is_change_pwd = False
        user.save()

        return Response(data={"message": "修改成功"}, status=status.HTTP_205_RESET_CONTENT)


class GroupExportViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    pagination_class = None
    xlsx_use_labels = True
    xlsx_boolean_labels = {True: "是", False: "否"}
    queryset = ExtraGroup.objects.all()
    serializer_class = ExportGroupSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'group_export.xlsx'
    # filterset_fields = {"name": ["exact", "iexact", "contains", "icontains"], "is_active": ["exact", "in"]}

    header = {
        'tab_title': "角色信息",
        'header_title': "角色信息",
        'height': 25,
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': True,
                'color': 'FF000000',
            },
        },
    }

    def get_body(self):
        return body

    def get_column_header(self):
        return column_header


class InspectionDictFilter(filters.FilterSet):
    project_code = filters.CharFilter(field_name="project_code", lookup_expr="icontains")
    project_name = filters.CharFilter(field_name="project_name", lookup_expr="project_name")
    hospital_code = filters.CharFilter(field_name="hospital_code", lookup_expr="icontains")
    office_code = filters.CharFilter(field_name="office_code", lookup_expr="icontains")
    distinguish = filters.CharFilter(field_name="distinguish", lookup_expr="icontains")

    class Meta:
        model = InspectionDictionaries
        fields = "__all__"


class InspectionDictionariesViewSet(ModelViewSet):
    """检查字典"""
    queryset = InspectionDictionaries.objects.all().order_by('id')
    serializer_class = InspectionDictionariesSerializer
    # filter_fields = "__all__"
    filterset_class = InspectionDictFilter


class InspectionDictionariesInfoExportViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    """导出检查字典"""
    pagination_class = None
    xlsx_use_labels = True
    xlsx_boolean_labels = {True: "是", False: "否"}
    queryset = InspectionDictionaries.objects.all()
    serializer_class = ExportInspectionDictionariesSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'InspectionDictionaries_export.xlsx'
    filterset_fields = {"project_name": ["exact", "iexact", "contains", "icontains"], "is_active": ["exact", "in"]}

    header = {
        'tab_title': "检查字典",
        'header_title': "检查字典",
        'height': 25,
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': True,
                'color': 'FF000000',
            },
        },
    }

    def get_body(self):
        return body

    def get_column_header(self):
        return column_header


class ExaminationDictFilter(filters.FilterSet):
    project_code = filters.CharFilter(field_name="project_code", lookup_expr="icontains")
    project_name = filters.CharFilter(field_name="project_name", lookup_expr="project_name")
    hospital_code = filters.CharFilter(field_name="hospital_code", lookup_expr="icontains")
    office_code = filters.CharFilter(field_name="office_code", lookup_expr="icontains")
    distinguish = filters.CharFilter(field_name="distinguish", lookup_expr="icontains")

    class Meta:
        model = ExaminationDictionaries
        fields = "__all__"


class ExaminationDictionariesViewSet(ModelViewSet):
    """检验字典"""
    queryset = ExaminationDictionaries.objects.all().order_by('id')
    serializer_class = ExaminationDictionariesSerializer
    # filter_fields = "__all__"
    filterset_class = ExaminationDictFilter


class ExaminationDictionariesInfoExportViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    """导出检验字典"""
    pagination_class = None
    xlsx_use_labels = True
    xlsx_boolean_labels = {True: "是", False: "否"}
    queryset = ExaminationDictionaries.objects.all()
    serializer_class = ExportExaminationDictionariesSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'ExaminationDictionaries_export.xlsx'
    filterset_fields = {"project_name": ["exact", "iexact", "contains", "icontains"], "is_active": ["exact", "in"]}

    header = {
        'tab_title': "检验字典",
        'header_title': "检验字典",
        'height': 25,
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': True,
                'color': 'FF000000',
            },
        },
    }

    def get_body(self):
        return body

    def get_column_header(self):
        return column_header


class DrugDirectoryExportViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    """导出药品目录"""
    pagination_class = None
    xlsx_use_labels = True
    xlsx_boolean_labels = {True: "是", False: "否"}
    queryset = DrugDirectory.objects.all()
    serializer_class = ExportDrugDirectorySerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'drug_directory.xlsx'
    filterset_fields = {"drug_name": ["exact", "iexact", "contains", "icontains"], "is_active": ["exact", "in"]}

    header = {
        'tab_title': "药品目录",
        'header_title': "药品目录",
        'height': 25,
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': True,
                'color': 'FF000000',
            },
        },
    }

    def get_body(self):
        return body

    def get_column_header(self):
        return column_header


class PharmacyManagementViewSet(ModelViewSet):
    """药房管理"""
    queryset = PharmacyManagement.objects.all().order_by('id')
    serializer_class = PharmacyManagementSerializer
    filter_fields = "__all__"


def import_office(request):
    """导入excel表科室数据"""
    created_user = request.POST.get('created_user')
    excel_file = request.FILES.get('excel_file', '')  # 获取前端上传的文件
    file_type = excel_file.name.split('.')[1].split('"')[0]  # 拿到文件后缀
    # file_type = excel_file.name.split('.')[1]  # 拿到文件后缀
    data_list = []
    # PositionTitle
    if file_type in ['xlsx', 'xls']:  # 支持这两种文件格式
        # 打开工作文件
        try:
            data = xlrd2.open_workbook(filename=None, file_contents=excel_file.read(), ragged_rows=True)
            sheets = data.sheets()
            for sheet in sheets:
                rows = sheet.nrows  # 总行数
                for row in range(2, rows):  # 从1开始是为了去掉表头
                    row_values = sheet.row_values(row)  # 每一行的数据
                    if row_values:
                        # codenum = row_values[0]  # 匹配编码
                        ctype = sheet.cell(row, 0).ctype  # 表格的数据类型
                        codenum = sheet.cell_value(row, 0)
                        if ctype == 2 and codenum % 1 == 0:  # 如果是整形
                            codenum = int(codenum)
                        name = row_values[1]
                        hospital_name = row_values[2]
                        hospital = Hospital.objects.get(name=hospital_name).id
                        parent_name = row_values[3]
                        if parent_name:
                            parent = Office.objects.get(name=parent_name).id
                        else:
                            parent = None
                        address = row_values[4]
                        phone = row_values[5]
                        introduce = row_values[6]
                        # created_time = row_values[7]
                        # # created_by = row_values[8]
                        office = Office.objects.filter(codenum=codenum)
                        if office:
                            office.update(**{"codenum": codenum,
                                             "name": name,
                                             "hospital_id": hospital,
                                             "parent_id": parent,
                                             "address": address,
                                             "phone": phone,
                                             "introduce": introduce,
                                             "created_time": datetime.datetime.now(),
                                             "created_by": created_user,
                                             })
                        else:
                            office.create(**{"codenum": codenum,
                                             "name": name,
                                             "hospital_id": hospital,
                                             "parent_id": parent,
                                             "address": address,
                                             "phone": phone,
                                             "introduce": introduce,
                                             "created_time": datetime.datetime.now(),
                                             "created_by": created_user,
                                             })
                        excel_data = {
                            "codenum": codenum,
                            "name": name,
                            "hospital": hospital,
                            "parent": parent,
                            "address": address,
                            "phone": phone,
                            "introduce": introduce,
                            "created_time": datetime.datetime.now(),
                            "created_by": created_user,
                        }
                        data_list.append(excel_data)
        except Exception as e:
            raise e

    if data_list:
        res = {"data": data_list}
    else:
        res = {"data": "文件内容格式有误，请检查内容格式是否正确！"}
    return JsonResponse(res)


def import_doctor(request):
    """导入excel表医生数据"""
    created_user = request.POST.get('created_user')
    excel_file = request.FILES.get('excel_file', '')  # 获取前端上传的文件
    file_type = excel_file.name.split('.')[1].split('"')[0]  # 拿到文件后缀
    # file_type = excel_file.name.split('.')[1]  # 拿到文件后缀
    data_list = []
    # PositionTitle
    if file_type in ['xlsx', 'xls']:  # 支持这两种文件格式
        # 打开工作文件
        try:
            data = xlrd2.open_workbook(filename=None, file_contents=excel_file.read(), ragged_rows=True)
            sheets = data.sheets()
            for sheet in sheets:
                rows = sheet.nrows  # 总行数
                for row in range(2, rows):  # 从1开始是为了去掉表头
                    row_values = sheet.row_values(row)  # 每一行的数据
                    if row_values:
                        # codenum = row_values[0]  # 匹配编码
                        ctype = sheet.cell(row, 2).ctype  # 表格的数据类型
                        job_number = sheet.cell_value(row, 2)
                        if ctype == 2 and job_number % 1 == 0:  # 如果是整形
                            job_number = int(job_number)
                        name = row_values[3]
                        hospital_name = row_values[0]
                        hospital = Hospital.objects.get(name=hospital_name).id
                        office_name = row_values[1]
                        if office_name:
                            office = Office.objects.get(name=office_name).id
                        else:
                            office = None
                        doc_rank_name = row_values[4]
                        if doc_rank_name:
                            doc_rank = PositionTitle.objects.get(name=doc_rank_name).id
                        else:
                            doc_rank = None
                        describe = row_values[5]
                        is_online_consult = row_values[6]
                        if is_online_consult == '是':
                            is_true = True
                        else:
                            is_true = False
                        doctor = Doctor.objects.filter(job_number=job_number)
                        if doctor:
                            doctor.update(**{"job_number": job_number,
                                             "name": name,
                                             "hospital_id": hospital,
                                             "office_id": office,
                                             "doc_rank_id": doc_rank,
                                             "describe": describe,
                                             "is_online_consult": is_true,
                                             "created_time": datetime.datetime.now(),
                                             "created_by": created_user,
                                             })
                        else:
                            doctor.create(**{"job_number": job_number,
                                             "name": name,
                                             "hospital_id": hospital,
                                             "office_id": office,
                                             "doc_rank_id": doc_rank,
                                             "describe": describe,
                                             "is_online_consult": is_true,
                                             "created_time": datetime.datetime.now(),
                                             "created_by": created_user,
                                             })
                        excel_data = {
                            "job_number": job_number,
                            "name": name,
                            "hospital_id": hospital,
                            "office_name": office_name,
                            "doc_rank_name": doc_rank_name,
                            "describe": describe,
                            "is_online_consult": is_online_consult,
                            "created_time": datetime.datetime.now(),
                            "created_by": created_user,
                        }
                        data_list.append(excel_data)
        except Exception as e:
            raise e

    if data_list:
        res = {"data": data_list}
    else:
        res = {"data": "文件内容格式有误，请检查内容格式是否正确！"}
    return JsonResponse(res)


class UserInfoExportViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    """用户信息导出接口"""
    pagination_class = None
    xlsx_use_labels = True
    xlsx_boolean_labels = {True: "是", False: "否"}
    queryset = User.objects.all()
    serializer_class = ExportUserSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'user_export.xlsx'
    filterset_fields = {"name": ["exact", "iexact", "contains", "icontains"], "is_active": ["exact", "in"]}

    header = {
        'tab_title': "用户信息",
        'header_title': "用户信息",
        'height': 25,
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': True,
                'color': 'FF000000',
            },
        },
    }

    def get_body(self):
        return body

    def get_column_header(self):
        return column_header


class DrugDirectoryFilter(filters.FilterSet):
    drug_code = filters.CharFilter(field_name="drug_code", lookup_expr="icontains")
    drug_name = filters.CharFilter(field_name="drug_name", lookup_expr="icontains")
    specification = filters.CharFilter(field_name="standards", lookup_expr="icontains")
    measure_unit = filters.CharFilter(field_name="measure_unit", lookup_expr="icontains")
    preparation_type = filters.CharFilter(field_name="preparation_type__name", lookup_expr="icontains")
    category = filters.CharFilter(field_name="category__name", lookup_expr="icontains")
    drug_type = filters.CharFilter(field_name="drug_type__name", lookup_expr="icontains")
    unit_dose = filters.CharFilter(field_name="unit_dose", lookup_expr="icontains")
    stock_left = filters.CharFilter(field_name="stock_left", lookup_expr="icontains")
    stock_unit = filters.CharFilter(field_name="stock_unit", lookup_expr="icontains")
    mic = filters.CharFilter(field_name="mic", lookup_expr="icontains")
    rcc_category = filters.CharFilter(field_name="rcc_category", lookup_expr="icontains")
    is_essential = filters.BooleanFilter(field_name="is_essential")
    hr_level = filters.CharFilter(field_name="hr_level", lookup_expr="icontains")
    gb_code = filters.CharFilter(field_name="gb_code", lookup_expr="icontains")
    gb_name = filters.CharFilter(field_name="gb_name", lookup_expr="icontains")
    origin_place = filters.CharFilter(field_name="origin_place", lookup_expr="icontains")
    manufacturer = filters.CharFilter(field_name="manufacturer", lookup_expr="icontains")
    is_active = filters.BooleanFilter(field_name="is_active")

    class Meta:
        model = DrugDirectory
        fields = "__all__"


class DrugDirectoryViewSet(ModelViewSet):
    queryset = DrugDirectory.objects.all()
    serializer_class = DrugDirectorySerializer
    filterset_class = DrugDirectoryFilter
