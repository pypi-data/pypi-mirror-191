from . import create_funtion
import types
from inspect import Parameter
from . import validate
from . import extract
from . import my_builtins
from . import render_template_obj
from . import exceptions
import copy
import yaml
from pathlib import Path
import inspect
import allure
from .log import log
from .db import ConnectMysql
import mimetypes
from requests_toolbelt import MultipartEncoder
import time


class RunYaml(object):
    """ 运行yaml """

    def __init__(self, raw: dict, module: types.ModuleType, g: dict):
        self.raw = raw   # 读取yaml 原始数据
        self.module = module   # 动态创建的 module 模型
        self.module_variable = {}  # 模块变量
        self.context = {}
        self.hooks = {}  # 全局hooks
        self.g = g  # 全局配置

    def run(self):
        if not self.raw.get('config'):
            self.raw['config'] = {}
        # config 获取用例名称 name 和 base_url
        # config_name = self.raw.get('config').get('name', '')
        base_url = self.raw.get('config').get('base_url', None)
        config_variables = self.raw.get('config').get('variables', {})
        config_fixtures = self.raw.get('config').get('fixtures', [])
        config_params = self.raw.get('config').get('parameters', [])
        config_hooks = self.raw.get('config').get('hooks', {})
        # 模块变量渲染
        self.context.update(__builtins__)  # noqa 内置函数加载
        self.context.update(my_builtins.__dict__)  # 自定义函数对象
        db_obj = self.execute_mysql()
        self.context.update(**self.g)  # 加载全局配置
        self.context.update(**db_obj)  # 加载操作mysql 内置函数
        self.module_variable = render_template_obj.rend_template_any(config_variables, **self.context)
        # 模块变量 添加到模块全局变量
        if isinstance(self.module_variable, dict):
            self.context.update(self.module_variable)
        # 支持 2 种参数化格式数据
        config_params = render_template_obj.rend_template_any(config_params, **self.context)
        config_fixtures = render_template_obj.rend_template_any(config_fixtures, **self.context)
        config_fixtures, config_params = self.parameters_date(config_fixtures, config_params)
        case = {}  # 收集用例名称和执行内容
        for case_name, case_value in self.raw.items():
            if case_name == 'config':
                continue  # 跳过config 非用例部分
            # case_name 必须 test 开头
            if not str(case_name).startswith('test'):
                case_name = 'test_'+str(case_name)
            if isinstance(case_value, list):
                case[case_name] = case_value
            else:
                case[case_name] = [case_value]

            def execute_yaml_case(args):
                # 获取被调用函数名称
                log.info(f'执行文件-> {self.module.__name__}.yml')
                log.info(f'base_url-> {base_url or args.get("request").config.option.base_url}')
                log.info(f'variables-> {self.module_variable}')
                call_function_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]
                log.info(f'运行用例-> {call_function_name}')
                # 添加 allure 报告--> story
                allure.dynamic.feature(f'{self.module.__name__}.yml')

                for step in case[call_function_name]:
                    # 添加 allure 报告--> title
                    allure.dynamic.title(call_function_name)
                    response = None
                    api_validate = []
                    step_name = step.get('name', 'not step name')
                    # 添加 allure 报告--> step
                    with allure.step(step_name):
                        pass
                    for item, value in step.items():
                        # 执行用例里面的方法
                        if item == 'name':
                            pass          # noqa
                        elif item == 'api':
                            root_dir = args.get('request').config.rootdir   # 内置request 获取root_dir
                            api_path = Path(root_dir).joinpath(value)
                            raw_api = yaml.safe_load(api_path.open(encoding='utf-8'))
                            api_validate = raw_api.get('validate')
                            copy_value = copy.deepcopy(raw_api.get('request'))  # 深拷贝一份新的value
                            response = self.run_request(args, copy_value, config_hooks, base_url)
                        elif item == 'request':
                            copy_value = copy.deepcopy(value)  # 深拷贝一份新的value
                            response = self.run_request(args, copy_value, config_hooks, base_url)
                        elif item == 'extract':
                            # 提取变量
                            copy_value = copy.deepcopy(value)
                            extract_value = render_template_obj.rend_template_any(copy_value, **self.context)
                            extract_result = self.extract_response(response, extract_value)
                            log.info(f'extract 提取变量-> {extract_result}')
                            # 添加到模块变量
                            self.module_variable.update(extract_result)
                            if isinstance(self.module_variable, dict):
                                self.context.update(self.module_variable)    # 加载模块变量
                        elif item == 'validate':
                            copy_value = copy.deepcopy(value)
                            # 合并校验
                            api_validate.extend([v for v in copy_value if v not in api_validate])
                            validate_value = render_template_obj.rend_template_any(api_validate, **self.context)
                            log.info(f'validate 校验内容-> {validate_value}')
                            self.validate_response(response, validate_value)
                        elif item == 'sleep':
                            sleep_value = render_template_obj.rend_template_any(value, **self.context)
                            try:
                                log.info(f'sleep time: {sleep_value}')
                                time.sleep(sleep_value)
                            except Exception as msg:
                                log.error(f'Run error: sleep value must be int or float, error msg: {msg}')
                        elif item == 'skip':
                            skip_reason = render_template_obj.rend_template_any(value, **self.context)
                            import pytest
                            pytest.skip(skip_reason)
                        elif item == 'skipif':   # noqa
                            if_exp = render_template_obj.rend_template_any(value, **self.context)
                            log.info(f'skipif : {eval(str(if_exp))}')  # noqa
                            if eval(str(if_exp)):
                                import pytest
                                pytest.skip(str(if_exp))
                        else:
                            try:
                                eval(item)(value)
                            except Exception as msg:
                                raise exceptions.ParserError(f'Parsers error: {msg}') from None

            f = create_funtion.create_function_from_parameters(
                func=execute_yaml_case,
                # parameters 传内置fixture 和 用例fixture
                parameters=self.function_parameters(config_fixtures),
                documentation=case_name,
                func_name=case_name,
                func_filename=f"{self.module.__name__}.py",
            )

            # 向 module 中加入函数
            setattr(self.module, str(case_name), f)
            if config_params:
                # 向 module 中加参数化数据的属性
                setattr(self.module, 'params_data', config_params)

    def run_request(self, args, copy_value, config_hooks, base_url):
        """运行request请求"""
        request_session = args.get('requests_function') or args.get('requests_module') or args.get('requests_session')
        # 加载参数化的值和fixture的值
        self.context.update(args)
        request_value = render_template_obj.rend_template_any(copy_value, **self.context)
        # request 请求参数预处理
        request_pre = self.request_hooks(config_hooks, request_value)
        if request_pre:
            # 执行 pre request 预处理
            self.context.update({"req": request_value})
            self.run_request_hooks(request_pre, request_value)
        # request请求 带上hooks "response"参数
        self.response_hooks(config_hooks, request_value)

        # multipart/form-data 文件上传支持
        root_dir = args.get('request').config.rootdir  # 内置request 获取root_dir
        request_value = self.multipart_encoder_request(request_value, root_dir)

        log.info(f'--------  request info ----------\n'
                 f'{request_value.get("method", "")} {request_value.get("url", "")}\n'
                 f'{request_value}\n'
                 )

        response = request_session.send_request(
            base_url=base_url,
            **request_value
        )

        log.info(f'------  response info  {getattr(response, "status_code")} {getattr(response, "reason", "")}  '
                 f'{getattr(response, "elapsed", "").total_seconds() if getattr(response, "elapsed", "") else ""}s'
                 f'------\n url: {getattr(response, "url", "")} \n'
                 f'headers:\n     {getattr(response, "headers", "")}\n'
                 f'body:\n     {getattr(response, "text", "")}\n'
                 )
        return response

    @staticmethod
    def function_parameters(config_fixtures) -> list:
        """ 测试函数传 fixture """
        # 测试函数的默认请求参数
        function_parameters = [
            Parameter('request', Parameter.POSITIONAL_OR_KEYWORD)  # 内置request fixture
        ]
        # 获取传给用例的 fixtures
        if isinstance(config_fixtures, str):
            config_fixtures = [item.strip(" ") for item in config_fixtures.split(',')]
        if not config_fixtures:
            function_parameters.append(
                Parameter('requests_session', Parameter.POSITIONAL_OR_KEYWORD),
            )
        else:
            if 'requests_function' in config_fixtures:
                function_parameters.append(
                    Parameter('requests_function', Parameter.POSITIONAL_OR_KEYWORD),
                )
            elif 'requests_module' in config_fixtures:
                function_parameters.append(
                    Parameter('requests_module', Parameter.POSITIONAL_OR_KEYWORD),
                )
            else:
                function_parameters.append(
                    Parameter('requests_session', Parameter.POSITIONAL_OR_KEYWORD),
                )
            for fixture in config_fixtures:
                if fixture not in ['requests_function', 'requests_module']:
                    function_parameters.append(
                        Parameter(fixture, Parameter.POSITIONAL_OR_KEYWORD),
                    )
        return function_parameters

    @staticmethod
    def parameters_date(fixtures, parameters):
        """
            参数化实现2种方式：
        方式1：
            config:
               name: post示例
               fixtures: username, password
               parameters:
                 - [test1, '123456']
                 - [test2, '123456']
        方式2：
            config:
               name: post示例
               parameters:
                 - {"username": "test1", "password": "123456"}
                 - {"username": "test2", "password": "1234562"}
        :returns
        fixtures: 用例需要用到的fixtures:  ['username', 'password']
        parameters: 参数化的数据list of list : [['test1', '123456'], ['test2', '123456']]
        """
        if isinstance(fixtures, str):
            # 字符串切成list
            fixtures = [item.strip(" ") for item in fixtures.split(',')]
        if isinstance(parameters, list) and len(parameters) > 1:
            if isinstance(parameters[0], dict):
                # list of dict
                params = list(parameters[0].keys())
                new_parameters = []
                for item in parameters:
                    new_parameters.append(list(item.values()))
                # fixtures 追加参数化的参数
                for param in params:
                    if param not in fixtures:
                        fixtures.append(param)
                return fixtures, new_parameters
            else:
                # list of list
                return fixtures, parameters
        else:
            return fixtures, []

    def hooks_event(self, hooks):
        """
        获取 requests 请求执行钩子, 仅支持2个事件，request 和 response
        :param hooks: yml 文件中读取的原始数据
           hooks = {
                "response": ['fun1', 'fun2'],
                "request": ['fun3', 'fun4']
            }
        :return: 返回结果示例:
            hooks = {
                "response": [fun1, fun2],
                "request": [fun3, fun4]
            }
        """
        # response hook事件
        hooks_response = hooks.get('response', [])
        if isinstance(hooks_response, str):
            # 字符串切成list
            hooks_response = [item.strip(" ") for item in hooks_response.split(',')]
        # 获取 my_builtins 模块函数对象
        hooks_response = [self.context.get(func) for func in hooks_response if self.context.get(func)]
        hooks['response'] = hooks_response
        # request  hook事件
        hooks_request = hooks.get('request', [])
        if isinstance(hooks_request, str):
            # 字符串切成list
            hooks_request = [item.strip(" ") for item in hooks_request.split(',')]
        # 获取 my_builtins 模块函数对象
        hooks_request = [self.context.get(func) for func in hooks_request if self.context.get(func)]
        hooks['request'] = hooks_request
        return hooks

    def request_hooks(self, config_hooks: dict, request_value: dict) -> dict:
        """ 合并全局config_hooks 和 单个请求 hooks 参数
            config_hooks = {
                "response": ['fun1', 'fun2'],
                "request": ['fun3', 'fun4']
            }
            request_value = {
                "method": "GET",
                "hooks": {"response": ['fun5']}
            }
            发送请求，request上带上hooks参数
            :return {"request": ['fun3', 'fun4']} 合并后的request 预处理函数
        """
        # request hooks 事件 (requests 库只有response 事件)
        config_request_hooks = []
        if 'request' in config_hooks.keys():
            config_request_hooks = config_hooks.get('request')
            if isinstance(config_request_hooks, str):
                # 字符串切成list
                config_request_hooks = [item.strip(" ") for item in config_request_hooks.split(',')]
        req_request_hooks = request_value.get('hooks', {})
        if 'request' in req_request_hooks.keys():
            req_hooks = req_request_hooks.get('request')
            if isinstance(req_hooks, str):
                # 字符串切成list
                req_hooks = [item.strip(" ") for item in req_hooks.split(',')]
            for h in req_hooks:
                config_request_hooks.append(h)
        # 更新 request_value
        if config_request_hooks:
            hooks = self.hooks_event({'request': config_request_hooks})
            # 去掉值为空的response 事件
            new_hooks = {key: value for key, value in hooks.items() if value}
            return new_hooks
        return {'request': []}

    def run_request_hooks(self, request_pre: dict, request_value):
        """执行请求预处理hooks内容
        request_pre: 待执行的预处理函数
        """
        funcs = request_pre.get('request', [])
        if not funcs:
            return request_value
        import inspect
        for fun in funcs:
            # 获取函数对象的入参
            ars = [arg_name for arg_name, v in inspect.signature(fun).parameters.items()]
            if 'req' in ars:
                fun(self.context.get('req'))
            else:
                fun()
        return request_value

    def response_hooks(self, config_hooks: dict, request_value: dict) -> dict:
        """ 合并全局config_hooks 和 单个请求 hooks 参数
            config_hooks = {
                "response": ['fun1', 'fun2'],
                "request": ['fun3', 'fun4']
            }
            request_value = {
                "method": "GET",
                "hooks": {"response": ['fun5']}
            }
            发送请求，request上带上hooks参数
            :return request_value  合并后的request请求
        """
        # request hooks 事件 (requests 库只有response 事件)
        if 'response' in config_hooks.keys():
            config_response_hooks = config_hooks.get('response')
            if isinstance(config_response_hooks, str):
                # 字符串切成list
                config_response_hooks = [item.strip(" ") for item in config_response_hooks.split(',')]
        else:
            config_response_hooks = []
        req_response_hooks = request_value.get('hooks', {})
        if 'response' in req_response_hooks.keys():
            resp_hooks = req_response_hooks.get('response')
            if isinstance(resp_hooks, str):
                # 字符串切成list
                resp_hooks = [item.strip(" ") for item in resp_hooks.split(',')]
            for h in resp_hooks:
                config_response_hooks.append(h)
        # 更新 request_value
        if config_response_hooks:
            hooks = self.hooks_event({'response': config_response_hooks})
            # 去掉值为空的response 事件
            new_hooks = {key: value for key, value in hooks.items() if value}
            request_value['hooks'] = new_hooks
        return request_value

    @staticmethod
    def extract_response(response, extract_obj: dict):
        """提取返回结果, 添加到module_variable 模块变量"""
        extract_result = {}
        if isinstance(extract_obj, dict):
            for extract_var, extract_expression in extract_obj.items():
                extract_var_value = extract.extract_by_object(response, extract_expression)  # 实际结果
                extract_result[extract_var] = extract_var_value
            return extract_result
        else:
            return extract_result

    @staticmethod
    def validate_response(response, validate_check: list) -> None:
        """校验结果"""
        for check in validate_check:
            for check_type, check_value in check.items():
                actual_value = extract.extract_by_object(response, check_value[0])  # 实际结果
                expect_value = check_value[1]  # 期望结果
                log.info(f'validate 校验结果-> {check_type}: [{actual_value}, {expect_value}]')
                if check_type in ["eq", "equals", "equal"]:
                    validate.equals(actual_value, expect_value)
                elif check_type in ["lt", "less_than"]:
                    validate.less_than(actual_value, expect_value)
                elif check_type in ["le", "less_or_equals"]:
                    validate.less_than_or_equals(actual_value, expect_value)
                elif check_type in ["gt", "greater_than"]:
                    validate.greater_than(actual_value, expect_value)
                elif check_type in ["ne", "not_equal"]:
                    validate.not_equals(actual_value, expect_value)
                elif check_type in ["str_eq", "string_equals"]:
                    validate.string_equals(actual_value, expect_value)
                elif check_type in ["len_eq", "length_equal"]:
                    validate.length_equals(actual_value, expect_value)
                elif check_type in ["len_gt", "length_greater_than"]:
                    validate.length_greater_than(actual_value, expect_value)
                elif check_type in ["len_ge", "length_greater_or_equals"]:
                    validate.length_greater_than_or_equals(actual_value, expect_value)
                elif check_type in ["len_lt", "length_less_than"]:
                    validate.length_less_than(actual_value, expect_value)
                elif check_type in ["len_le", "length_less_or_equals"]:
                    validate.length_less_than_or_equals(actual_value, expect_value)
                elif check_type in ["contains"]:
                    validate.contains(actual_value, expect_value)
                else:
                    if hasattr(validate, check_type):
                        getattr(validate, check_type)(actual_value, expect_value)
                    else:
                        print(f'{check_type}  not valid check type')

    def execute_mysql(self):
        """执行 mysql 操作"""
        env_obj = self.g.get('env')    # 获取环境配置
        if not hasattr(env_obj, 'MYSQL_HOST'):
            return {
                "query_sql": lambda x: log.error("MYSQL_HOST not found in config.py"),
                "execute_sql": lambda x: log.error("MYSQL_HOST not found in config.py")
            }
        try:
            db = ConnectMysql(
                host=env_obj.MYSQL_HOST,
                user=env_obj.MYSQL_USER,
                password=env_obj.MYSQL_PASSWORD,
                port=env_obj.MYSQL_PORT,
                database=env_obj.MYSQL_DATABASE,
            )
            return {
                "query_sql": db.query_sql,
                "execute_sql": db.execute_sql
            }
        except Exception as msg:
            log.error(f'mysql init error: {msg}')
            return {
                "query_sql": lambda x: log.error("MYSQL connect error in config.py"),
                "execute_sql": lambda x: log.error("MYSQL connect error in config.py")
            }

    @staticmethod
    def upload_file(filepath: Path):
        """根据文件路径，自动获取文件名称和文件mime类型"""
        if not filepath.exists():
            log.error(f"文件路径不存在：{filepath}")
            return
        mime_type = mimetypes.guess_type(filepath)[0]
        return (
            filepath.name, filepath.open("rb"), mime_type
        )

    def multipart_encoder_request(self, request_value: dict, root_dir):
        """判断请求头部 Content-Type: multipart/form-data 格式支持"""
        if 'files' in request_value.keys():
            fields = []
            data = request_value.get('data', {})
            fields.extend(data.items())  # 添加data数据
            for key, value in request_value.get('files', {}).items():
                if Path(root_dir).joinpath(value).is_file():
                    fields.append(
                        (key, self.upload_file(Path(root_dir).joinpath(value).resolve()))
                    )
            m = MultipartEncoder(
                fields=fields
            )
            request_value.pop('files')  # 去掉 files 参数
            request_value['data'] = m
            new_headers = request_value.get('headers', {})
            new_headers.update({'Content-Type': m.content_type})
            request_value['headers'] = new_headers
            return request_value
        else:
            return request_value
