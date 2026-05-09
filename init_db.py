import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "knowledge.db"


def init_database() -> None:
    """初始化数据库结构并写入演示数据。"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 为了保证脚本可重复执行，先删除旧表再重建。
    cursor.execute("DROP TABLE IF EXISTS predicted_questions")
    cursor.execute("DROP TABLE IF EXISTS wiki_articles")

    # 创建知识文章表，保存 LLM-WIKI 中的知识条目。
    cursor.execute(
        """
        CREATE TABLE wiki_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            source TEXT NOT NULL
        )
        """
    )

    # 创建预测问题表，保存从文章逆向生成的客户问题。
    cursor.execute(
        """
        CREATE TABLE predicted_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            question_type TEXT NOT NULL,
            FOREIGN KEY (article_id) REFERENCES wiki_articles (id)
        )
        """
    )

    # 插入演示文章数据，模拟 LLM-WIKI 的知识架构内容。
    articles = [
        (
            "LLM-WIKI 知识架构总览",
            "LLM-WIKI 通过主题分层、实体关联和问题闭环形成知识架构。"
            "核心目标是让知识可检索、可追踪、可复用。",
            "LLM-WIKI",
        ),
        (
            "客户问题逆向生成方法",
            "逆向问题生成从已有知识条目中提炼客户会问的问题，"
            "可按基础认知、排障、选型、流程等问题类型拆分。",
            "LLM-WIKI",
        ),
        (
            "提示词工程最佳实践",
            "提示词工程建议采用角色设定、约束条件、示例驱动和结果格式化四步法，"
            "并通过 A/B 对比持续优化。",
            "LLM-WIKI",
        ),
        (
            "RAG 检索增强问答",
            "RAG 将向量检索与生成模型结合，先找证据再生成回答。"
            "关键环节包括切片、召回、重排和引用追溯。",
            "LLM-WIKI",
        ),
        (
            "客服场景知识运营",
            "客服知识运营强调高频问题沉淀、知识更新机制、质量评估指标"
            "和人工反馈闭环，最终提升首解率。",
            "LLM-WIKI",
        ),
    ]
    cursor.executemany(
        "INSERT INTO wiki_articles (title, content, source) VALUES (?, ?, ?)", articles
    )

    # 插入“逆向问题生成”结果，问题通过 article_id 与文章关联。
    questions = [
        (1, "LLM-WIKI 的知识架构为什么比传统文档更适合客服团队？", "价值认知"),
        (1, "如何判断一个知识条目是否应该进入核心知识图谱？", "流程方法"),
        (1, "知识架构里实体关系应如何定义才能便于后续检索？", "架构设计"),
        (2, "逆向问题生成和常规 FAQ 整理有什么区别？", "概念辨析"),
        (2, "怎样从一篇文章中拆出不同层级的客户问题？", "流程方法"),
        (2, "问题类型 question_type 应该如何划分才实用？", "实施策略"),
        (3, "提示词中如何写约束才能减少答非所问？", "排障优化"),
        (3, "是否需要给每个客服场景设计固定提示词模板？", "落地实践"),
        (3, "提示词 A/B 测试结果该如何评估？", "指标评估"),
        (4, "RAG 场景下为什么经常出现检索到了却回答不准？", "排障优化"),
        (4, "知识切片长度应该如何设置更合理？", "参数策略"),
        (4, "如何让回答中展示可追溯的知识来源？", "可信输出"),
        (5, "客服知识多久更新一次比较合适？", "运营策略"),
        (5, "如何通过反馈闭环发现缺失知识？", "流程方法"),
        (5, "首解率提升和知识图谱之间的关系是什么？", "价值认知"),
    ]
    cursor.executemany(
        """
        INSERT INTO predicted_questions (article_id, question, question_type)
        VALUES (?, ?, ?)
        """,
        questions,
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()
    print(f"数据库初始化完成: {DB_PATH}")
