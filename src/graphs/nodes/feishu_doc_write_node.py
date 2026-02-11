import logging
import requests
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import FeishuDocWriteInput, FeishuDocWriteOutput
from coze_workload_identity import Client
from cozeloop.decorator import observe

logger = logging.getLogger(__name__)

class FeishuBitable:
    """飞书多维表格HTTP客户端"""
    
    def __init__(self):
        self.client = Client()
        self.base_url = "https://open.larkoffice.com/open-apis"
        self.timeout = 30
        self.access_token = self.get_access_token()
        logger.info(f"成功获取飞书access_token: {self.access_token[:20]}..." if self.access_token else "未获取到access_token")
    
    def get_access_token(self) -> str:
        """获取飞书多维表格的租户访问令牌"""
        access_token = self.client.get_integration_credential("integration-feishu-base")
        return access_token
    
    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.access_token}" if self.access_token else "",
            "Content-Type": "application/json; charset=utf-8",
        }
    
    @observe
    def _request(self, method: str, path: str, params: dict = None, json_body: dict = None) -> dict:
        """发送HTTP请求"""
        try:
            url = f"{self.base_url}{path}"
            logger.info(f"发送请求: {method} {url}")
            resp = requests.request(
                method, 
                url, 
                headers=self._headers(), 
                params=params, 
                json=json_body, 
                timeout=self.timeout
            )
            resp_data = resp.json()
            logger.info(f"响应状态码: {resp.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"请求异常: {str(e)}")
            raise Exception(f"FeishuBitable API request error: {e}")
        
        if resp_data.get("code") != 0:
            logger.error(f"飞书API错误: {resp_data}")
            raise Exception(f"FeishuBitable API error: {resp_data}")
        
        return resp_data
    
    def create_base(self, name: str) -> dict:
        """创建多维表格Base"""
        body = {"name": name}
        logger.info(f"创建Base，名称: {name}")
        return self._request("POST", "/bitable/v1/apps", json_body=body)
    
    def list_tables(self, app_token: str) -> dict:
        """列出Base下所有数据表"""
        return self._request("GET", f"/bitable/v1/apps/{app_token}/tables")
    
    def create_table(self, app_token: str, table_name: str, fields: list = None) -> dict:
        """创建数据表"""
        body = {
            "table": {
                "name": table_name,
                "table_type": "bitable"
            }
        }
        if fields is not None:
            body["table"]["fields"] = fields
        logger.info(f"创建数据表，名称: {table_name}")
        return self._request("POST", f"/bitable/v1/apps/{app_token}/tables", json_body=body)
    
    def add_field(self, app_token: str, table_id: str, field: dict) -> dict:
        """新增字段"""
        return self._request(
            "POST", 
            f"/bitable/v1/apps/{app_token}/tables/{table_id}/fields", 
            json_body=field
        )
    
    def add_records(self, app_token: str, table_id: str, records: list) -> dict:
        """批量新增记录"""
        body = {"records": records}
        return self._request(
            "POST", 
            f"/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create", 
            json_body=body
        )

def feishu_doc_write_node(
    state: FeishuDocWriteInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> FeishuDocWriteOutput:
    """
    title: 飞书文档写入
    desc: 将提取的文案、摘要和改写文案写入飞书多维表格
    integrations: 飞书多维表格
    """
    try:
        # 初始化飞书客户端
        bitable = FeishuBitable()
        
        # 确定或创建 Base
        if state.feishu_app_token:
            app_token = state.feishu_app_token
            logger.info(f"使用现有的飞书Base: {app_token}")
        else:
            # 创建新的Base
            base_result = bitable.create_base(name="VideoTextExtractionWorkflow")
            app_token = base_result["data"]["app"]["app_token"]
            logger.info(f"创建新的飞书Base: {app_token}")
            logger.info(f"Base详细信息: {base_result}")
        
        # 确定或创建 Table
        if state.feishu_table_id:
            table_id = state.feishu_table_id
            logger.info(f"使用现有的数据表: {table_id}")
        else:
            # 创建新的数据表（不预定义字段）
            table_result = bitable.create_table(app_token, "TextExtractionRecords")
            table_id = table_result["data"]["table_id"]
            logger.info(f"创建新的数据表: {table_id}")
            
            # 创建字段
            fields = [
                {
                    "field_name": "提取文案信息",
                    "type": 1  # 文本类型
                },
                {
                    "field_name": "提取文案信息_摘要_",
                    "type": 1  # 文本类型
                },
                {
                    "field_name": "文案分析",
                    "type": 1  # 文本类型
                },
                {
                    "field_name": "文案改写1_痛点直击型",
                    "type": 1  # 文本类型
                },
                {
                    "field_name": "文案改写2_情感共鸣型",
                    "type": 1  # 文本类型
                },
                {
                    "field_name": "文案改写3_数据说服型",
                    "type": 1  # 文本类型
                },
                {
                    "field_name": "文案改写4_场景化描述型",
                    "type": 1  # 文本类型
                },
                {
                    "field_name": "文案改写5_简洁有力型",
                    "type": 1  # 文本类型
                }
            ]
            
            for field in fields:
                field_result = bitable.add_field(app_token, table_id, field)
                logger.info(f"创建字段响应: {field_result}")
                logger.info(f"创建字段成功: {field['field_name']}")
        
        # 创建记录
        # 确保5条改写文案
        rewritten_texts = state.rewritten_texts
        if len(rewritten_texts) < 5:
            # 如果不足5条，用空字符串补齐
            rewritten_texts.extend([""] * (5 - len(rewritten_texts)))
        
        records = [
            {
                "fields": {
                    "提取文案信息": state.extracted_text,
                    "提取文案信息_摘要_": state.text_summary,
                    "文案分析": state.text_analysis,
                    "文案改写1_痛点直击型": rewritten_texts[0] if len(rewritten_texts) > 0 else "",
                    "文案改写2_情感共鸣型": rewritten_texts[1] if len(rewritten_texts) > 1 else "",
                    "文案改写3_数据说服型": rewritten_texts[2] if len(rewritten_texts) > 2 else "",
                    "文案改写4_场景化描述型": rewritten_texts[3] if len(rewritten_texts) > 3 else "",
                    "文案改写5_简洁有力型": rewritten_texts[4] if len(rewritten_texts) > 4 else ""
                }
            }
        ]
        
        add_result = bitable.add_records(app_token, table_id, records)
        record_id = add_result["data"]["records"][0]["record_id"]
        
        # 生成飞书多维表格访问链接
        # 飞书Base的正确URL格式
        feishu_url = f"https://feishu.cn/base/{app_token}"
        
        logger.info(f"成功写入飞书文档，记录ID: {record_id}")
        logger.info(f"飞书多维表格访问链接: {feishu_url}")
        
        return FeishuDocWriteOutput(
            feishu_app_token=app_token,
            feishu_table_id=table_id,
            record_id=record_id,
            feishu_url=feishu_url
        )
        
    except Exception as e:
        logger.error(f"飞书文档写入失败: {str(e)}")
        raise Exception(f"飞书文档写入失败: {str(e)}")
