from schemas.jd import JDInfo
from schemas.resume import ResumeInfo
from schemas.match import MatchResult


# Schema 健康检查：确保模型可实例化且序列化正常。
def run_schema_check():
    # 使用默认值构造对象，主要验证字段定义是否有效。
    jd = JDInfo()
    resume = ResumeInfo()
    match = MatchResult()

    # 打印结构化结果，便于观察默认字段输出。
    print("JDInfo schema ok:", jd.model_dump())
    print("ResumeInfo schema ok:", resume.model_dump())
    print("MatchResult schema ok:", match.model_dump())