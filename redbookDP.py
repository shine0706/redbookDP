import streamlit as st
from openai import OpenAI # 替换为 OpenAI 库
import time

# --- 页面基础配置 ---
st.set_page_config(
    page_title="🐋 DeepSeek 小红书爆文助手",
    page_icon="🐋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 样式优化 (保持清爽风格) ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #4d6bfe; /* 改用 DeepSeek 蓝 */
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #3b5bdb;
        color: white;
    }
    .reportview-container {
        background: #fbfbfb;
    }
</style>
""", unsafe_allow_html=True)

# --- 核心 AI 逻辑函数 (适配 DeepSeek) ---
def generate_xhs_content(api_key, topic, keywords, style, audience):
    """
    调用 DeepSeek API 生成符合小红书风格的内容
    """
    if not api_key:
        return None, "请先在左侧侧边栏输入 DeepSeek API Key"

    try:
        # 初始化 OpenAI 客户端，指向 DeepSeek 服务器
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com" # DeepSeek 官方接口地址
        )

        # 构建提示词
        system_prompt = """
        你是一位拥有百万粉丝的小红书爆款文案专家。你深知小红书的算法机制和用户心理。
        你的写作特点：
        1. 标题必须极具吸引力（使用夸张、对比、悬念、数字等手法）。
        2. 正文必须使用大量 Emoji 表情，视觉丰富。
        3. 语气要极度口语化，像闺蜜聊天，多用“家人们”、“绝绝子”、“避坑”、“按头安利”等小红书黑话。
        4. 排版要分段清晰，便于快速阅读。
        """

        user_prompt = f"""
        请根据以下信息创作一篇小红书笔记：
        
        【主题】：{topic}
        【关键词】：{keywords}
        【目标受众】：{audience}
        【写作风格】：{style}

        请严格按照以下格式输出（不要包含其他解释性文字）：

        ---
        【🔥 爆款标题方案】
        1. (标题1)
        2. (标题2)
        3. (标题3)

        【📝 正文内容】
        (正文内容，记得多分段，多用Emoji)

        【🏷️ 推荐标签】
        (列出5-8个高热度标签)
        ---
        """

        # 发起请求
        response = client.chat.completions.create(
            model="deepseek-chat", # 使用 DeepSeek V3 或通用模型
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=1.3, # 小红书文案需要高创造力，稍微调高
            stream=False
        )
        
        return response.choices[0].message.content, None

    except Exception as e:
        return None, f"DeepSeek API 调用出错: {str(e)}"

# --- 侧边栏：设置区 ---
with st.sidebar:
    st.title("🐋 设置面板")
    api_key = st.text_input("🔑 输入 DeepSeek API Key", type="password", help="去 DeepSeek 开放平台申请")
    st.markdown("[👉 点击获取 DeepSeek Key](https://platform.deepseek.com/)")
    
    st.markdown("---")
    st.subheader("🎨 风格微调")
    style_option = st.selectbox(
        "选择文案风格",
        ("✨ 种草安利 (真诚、好物分享)", "📚 知识干货 (专业、条理清晰)", "🔥 情绪共鸣 (吐槽、情感故事)", "⚠️ 避坑指南 (警示、实用经验)")
    )
    
    st.markdown("---")
    st.caption("Powered by DeepSeek-V3")

# --- 主界面 ---
st.title("🐋 AIGC 小红书运营智能助手 (DeepSeek版)")
st.markdown("DeepSeek 更加懂中文语境，助你轻松写出**爆款**笔记！")

# 分两列布局
col1, col2 = st.columns([1, 1])

with col1:
    st.info("📝 **第一步：输入笔记信息**")
    topic_input = st.text_input("📌 笔记主题", placeholder="例如：2024年新手怎么做自媒体")
    keywords_input = st.text_area("🏷️ 核心关键词", placeholder="例如：副业、搞钱、甚至0基础、避坑", height=100)
    audience_input = st.text_input("👥 目标受众", placeholder="例如：大学生、宝妈、上班族")
    
    generate_btn = st.button("🚀 呼叫 DeepSeek 生成", type="primary")

with col2:
    st.success("✨ **第二步：查看生成结果**")
    output_container = st.empty()

# --- 响应逻辑 ---
if generate_btn:
    if not topic_input:
        st.warning("请至少输入笔记主题！")
    else:
        with st.spinner('🐋 DeepSeek 正在深度思考中...'):
            result_text, error = generate_xhs_content(api_key, topic_input, keywords_input, style_option, audience_input)
            
            if error:
                st.error(error)
            else:
                output_container.markdown(result_text)
                st.toast('生成成功！DeepSeek 的中文确实溜！', icon='🎉')
                with st.expander("📋 点击展开纯文本 (方便复制)"):
                    st.text_area("结果内容", value=result_text, height=400)

# --- 底部装饰 ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Powered by DeepSeek API & Streamlit</div>", 
    unsafe_allow_html=True
)