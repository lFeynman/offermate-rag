def route_query(query: str):
    query = query.lower()

    if "匹配" in query or "技能" in query:
        return "skill_matcher"
    if "岗位要求" in query or "jd" in query:
        return "jd_parser"
    if "简历" in query:
        return "resume_parser"
    if "面试题" in query or "问题" in query:
        return "interview_generator"
    return "rag"