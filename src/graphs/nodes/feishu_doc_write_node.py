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
    """飞书多维表格HTTP客户端（内存优化版）"""

    def __init__(self):
        self.client = None  # 延迟初始化
        self.access_token = ""  # 延迟初始化
        self.base_url = "https://open.feishu.cn/open-apis"
        self.timeout = 120

    def _init_client(self):
        """延迟初始化客户端和凭证"""
        if self.client is not None and self.access_token:
            return  # 已经初始化过

        logger.info("🔧 初始化飞书客户端...")
        self.client = Client()

        logger.info("🔑 获取飞书 access_token...")
        try:
            self.access_token = self.client.get_integration_credential("integration-feishu-base")
            if not self.access_token:
                raise Exception("飞书集成凭证为空")
            logger.info(f"✅ 成功获取飞书 access_token: {self.access_token[:20]}...")
        except Exception as e:
            logger.error(f"❌ 获取飞书 access_token 失败: {str(e)}")
            self.access_token = ""
            raise

    def _headers(self):
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.access_token}" if self.access_token else "",
            "Content-Type": "application/json; charset=utf-8",
        }

    @observe
    def _request(self, method: str, path: str, params: dict = None, json_body: dict = None) -> dict:
        """发送HTTP请求（简化版，减少内存使用）"""
        try:
            url = f"{self.base_url}{path}"
            resp = requests.request(
                method,
                url,
                headers=self._headers(),
                params=params,
                json=json_body,
                timeout=self.timeout
            )

            if not resp.text or resp.text.strip() == "":
                raise Exception(f"飞书API返回空响应，状态码: {resp.status_code}")

            resp_data = resp.json()

        except Exception as e:
            logger.error(f"请求异常: {str(e)}")
            raise Exception(f"FeishuBitable API error: {e}")

        if resp_data.get("code") != 0:
            raise Exception(f"FeishuBitable API error: {resp_data}")

        return resp_data

    @observe
    def get_or_create_base(self, name: str) -> str:
        """获取或创建多维表格"""
        self._init_client()  # 确保客户端已初始化

        # 搜索
        resp = self._request(
            "GET",
            "/bitable/v1/apps",
            params={"page_size": 20}
        )

        for item in resp.get("data", {}).get("items", []):
            if item.get("name") == name:
                logger.info(f"✅ 找到已有的 Base: {item['app_id']}")
                return item["app_id"]

        # 创建
        logger.info(f"🔨 创建新 Base: {name}")
        resp = self._request(
            "POST",
            "/bitable/v1/apps",
            json_body={"name": name}
        )
        logger.info(f"✅ Base 创建成功: {resp['data']['app']['app_id']}")
        return resp["data"]["app"]["app_id"]

    @observe
    def create_table(self, app_id: str, table_name: str) -> str:
        """创建数据表"""
        logger.info(f"🔨 创建数据表: {table_name}")
        resp = self._request(
            "POST",
            f"/bitable/v1/apps/{app_id}/tables",
            json_body={
                "default": False,
                "name": table_name,
                "fields": [
                    {"name": "视频标题", "type": 1},
                    {"name": "原始文案", "type": 1},
                    {"name": "文案摘要", "type": 1},
                    {"name": "文案改写", "type": 1},
                ]
            }
        )
        logger.info(f"✅ 数据表创建成功: {resp['data']['table']['table_id']}")
        return resp["data"]["table"]["table_id"]

    @observe
    def add_record(self, app_id: str, table_id: str, fields: dict) -> str:
        """添加记录"""
        logger.info(f"📝 添加记录到表格...")
        resp = self._request(
            "POST",
            f"/bitable/v1/apps/{app_id}/tables/{table_id}/records",
            json_body={"fields": fields}
        )
        record_id = resp["data"]["record"]["record_id"]
        logger.info(f"✅ 记录添加成功: {record_id}")
        return record_id


def feishu_doc_write_node(
    state: FeishuDocWriteInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> FeishuDocWriteOutput:
    """
    title: 飞书文档写入
    desc: 将视频文案信息写入飞书多维表格（内存优化版）
    integrations: 飞书多维表格, 对象存储
    """
    logger.info("🚀 开始飞书文档写入节点（内存优化版）")

    try:
        bitable = FeishuBitable()

        base_name = "视频文案提取"
        table_name = "文案记录"

        app_id = bitable.get_or_create_base(base_name)
        table_id = bitable.create_table(app_id, table_name)

        # 直接写入，不存储中间变量
        record_id = bitable.add_record(
            app_id,
            table_id,
            fields={
                "视频标题": state.video_title,
                "原始文案": state.extracted_text[:2000] if state.extracted_text else "",  # 限制长度
                "文案摘要": state.text_summary[:1000] if state.text_summary else "",
                "文案改写": state.text_rewrite[:2000] if state.text_rewrite else "",
            }
        )

        # 构造飞书链接
        spreadsheet_url = f"https://feishu.cn/base/{app_id}?table={table_id}&view=vew"

        logger.info(f"🎉 飞书文档写入成功！链接: {spreadsheet_url}")

        return FeishuDocWriteOutput(
            feishu_link=spreadsheet_url,
            error=""
        )

    except Exception as e:
        logger.error(f"❌ 飞书文档写入失败: {str(e)}", exc_info=True)
        return FeishuDocWriteOutput(
            feishu_link="",
            error=f"飞书文档写入失败: {str(e)}"
        )
