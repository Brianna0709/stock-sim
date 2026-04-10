"""
共享配置：域名列表、路径、Gateway 连接参数
"""
import json
import os

# ── 路径 ──────────────────────────────────────────────
OPENCLAW_CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
SKILLS_DIR = os.path.expanduser("~/.openclaw/skills")
SNAPSHOT_PATH = os.path.join(os.path.dirname(__file__), "snapshot.json")
WORKSPACE_DIR = os.path.expanduser("~/.openclaw/workspace")

# ── Gateway ───────────────────────────────────────────
def get_gateway_config():
    with open(OPENCLAW_CONFIG_PATH) as f:
        cfg = json.load(f)
    port = cfg.get("gateway", {}).get("port", 18789)
    token = cfg.get("gateway", {}).get("auth", {}).get("token", "")
    return {
        "base_url": f"http://127.0.0.1:{port}",
        "token": token,
        "headers": {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    }

# ── 网络域名列表 ──────────────────────────────────────
INTRANET_HOSTS = [
    "example.mt",
    "example.lan",
    "example.sankuai.cc",
    "s.sankuai.com",
    "example.51ping.com",
    "example.neixin.cn",
    "example.daxiang.com",
]

# 外网抽样（只取可预期返回 HTTP 的域名，不依赖内容）
# 注意：10086.cn 有 SSL 旧协议问题，jiepang.com 代理返回 403
EXTRANET_HOSTS = [
    "www.adobe.com",
    "www.tvb.com",
    "www.baidu.com",
    "www.51job.com",
    "www.zhihu.com",
    "s3.meituan.net",
]

# 内网域名后缀（判断用）
INTRANET_SUFFIXES = (
    ".mt", ".lan", ".sankuai.cc", ".sankuai.com",
    ".51ping.com", ".neixin.cn", ".daxiang.com",
)

# 环境变量过滤关键词
ENV_KEY_PATTERNS = ["catclaw", "openclaw", "http_proxy", "https_proxy",
                    "upstream_proxy", "supervisor"]

# 冒烟测试用的 session key
# 使用 agent:main:main（webchat session），避免 daxiang session 因当前对话繁忙导致排队超时
SMOKE_SESSION_KEY = "agent:main:main"
