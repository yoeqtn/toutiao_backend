from langchain_core.tools import tool
from sqlalchemy import or_, select
from config.db_conf import AsyncSessionLocal
from models.news import News

def _fmt(n: News) -> dict:
    return {
        "newsId": n.id,
        "title": n.title,
        "summary": (n.description or n.content or "")[:150],
        "author": n.author,
        "publishTime": n.publish_time.strftime("%Y-%m-%d %H:%M") if n.publish_time else None,
        "categoryId": n.category_id,
    }

@tool
async def get_news_summary(news_title: str | None = None, news_id: int | None = None) -> dict:
    """按 news_id 精确查询，或按标题/简介关键词模糊检索新闻，返回 newsId、标题、摘要、发布时间。
    当用户询问某个话题、事件或人物相关的新闻时调用。
    知道 id 就传 news_id；否则传 news_title，放 2-4 个核心词，不要传整句。
    不要用它回答常识性问题。
    """
    if news_id is None and not news_title:
        return {"error": "需要提供 news_id 或 news_title 其中之一"}

    async with AsyncSessionLocal() as db:
        # ① 有 id 就精确查，优先级最高
        if news_id is not None:
            n = await db.get(News, int(news_id))
            if not n:
                return {"error": f"新闻 {news_id} 不存在"}
            return {"count": 1, "items": [_fmt(n)]}

        # ② 没有 id，按关键词模糊检索
        kw = f"%{news_title.strip()}%"
        stmt = (
            select(News)
            .where(or_(News.title.ilike(kw), News.description.ilike(kw)))
            .order_by(News.publish_time.desc())
            .limit(5)
        )
        rows = (await db.execute(stmt)).scalars().all()

        if not rows:
            return {"error": f"没有找到与「{news_title}」相关的新闻，换个关键词试试"}

        return {"count": len(rows), "items": [_fmt(n) for n in rows]}
