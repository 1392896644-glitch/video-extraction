#!/usr/bin/env python3
"""获取对象存储配置信息"""
import os
import sys

def get_storage_config():
    """从 Coze 工作负载身份获取对象存储配置"""
    print("正在获取对象存储配置信息...\n")

    try:
        from coze_workload_identity import Client as CozeEnvClient
        coze_env_client = CozeEnvClient()
        env_vars = coze_env_client.get_project_env_vars()
        coze_env_client.close()

        endpoint_url = None
        bucket_name = None

        for env_var in env_vars:
            if env_var.key == "COZE_BUCKET_ENDPOINT_URL":
                endpoint_url = env_var.value.replace("'", "'\\''")
            elif env_var.key == "COZE_BUCKET_NAME":
                bucket_name = env_var.value

        if endpoint_url:
            print(f"✅ COZE_BUCKET_ENDPOINT_URL: {endpoint_url}")
        else:
            print("❌ COZE_BUCKET_ENDPOINT_URL: 未找到")

        if bucket_name:
            print(f"✅ COZE_BUCKET_NAME: {bucket_name}")
        else:
            print("❌ COZE_BUCKET_NAME: 未找到")

        print("\n请在 Render 环境变量中配置上述值。\n")

    except Exception as e:
        print(f"❌ 获取配置失败: {e}")
        print("\n请手动在 Coze 平台的对象存储集成中查看配置信息。")

if __name__ == "__main__":
    get_storage_config()
