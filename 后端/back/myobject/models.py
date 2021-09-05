from datetime import datetime

from django.db import models


# Create your models here.


# user账号信息模型
class User(models.Model):
    username = models.CharField(max_length=50)  # 账号
    nickname = models.CharField(max_length=50)  # 昵称
    password_hash = models.CharField(max_length=100)  # 密码
    password_salt = models.CharField(max_length=50)  # 密码干扰值
    status = models.IntegerField(default=1)  # 状态:1正常/2禁用/9删除
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 修改时间

    def toDict(self):
        return {'id': self.id, 'username': self.username, 'nickname': self.nickname,
                'password_hash': self.password_hash, 'password_salt': self.password_salt, 'status': self.status,
                'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "user"  # 更改表名


# survey信息模型
class Survey(models.Model):
    user_id = models.IntegerField()
    type = models.IntegerField(default=1)
    name = models.CharField(max_length=255)  # 名称
    description = models.TextField(blank=True, null=True)  # 描述
    status = models.IntegerField(default=0)  # 状态:1正常/9删除
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 修改时间
    stop_at = models.DateTimeField()  # 修改时间
    recoveryNum = models.IntegerField(default=0)
    isNeed = models.BooleanField()  # 是否需要添加题号
    quota = models.IntegerField(default=0)

    def toDict(self):
        return {'id': self.id, 'user_id': self.user_id, 'name': self.name, 'status': self.status,
                'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "survey"  # 更改表名


# question信息模型
class QuestionSelect(models.Model):
    type = models.IntegerField()  # 问题类型
    required = models.BooleanField()  # 是否必填
    survey_id = models.IntegerField()  # survey_id
    name = models.CharField(max_length=50)  # 名称
    sequenceNumber = models.IntegerField(blank=True)  # 顺序号
    description = models.TextField(blank=True, null=True)  # 题目描述
    result = models.CharField(max_length=10, blank=True)
    score = models.IntegerField(default=0)
    status = models.IntegerField(default=0)  # 状态:1正常/9删除
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 修改时间

    def toDict(self):
        return {'id': self.id, 'survey_id': self.survey_id, 'name': self.name,
                'result': self.result, 'status': self.status, 'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "questionselect"  # 更改表名


class QuestionSelectData(models.Model):
    sequenceNumber = models.IntegerField(blank=True)  # 顺序号
    survey_id = models.IntegerField()  # survey_id
    ip = models.CharField(max_length=30)  # ip地址
    answer = models.IntegerField(blank=True, null=True)


class Option(models.Model):
    questionId = models.IntegerField()  # 题目id
    content = models.CharField(max_length=100)  # 选项内容
    numbers = models.IntegerField(default=0)  # 选择人数


class QuestionMulSelect(models.Model):
    score = models.IntegerField(default=0)
    type = models.IntegerField()  # 问题类型
    required = models.BooleanField()  # 是否必填
    survey_id = models.IntegerField()  # survey_id
    sequenceNumber = models.IntegerField()  # 顺序号
    name = models.CharField(max_length=50)  # 名称
    description = models.TextField(blank=True, null=True)  # 题目描述
    result = models.CharField(max_length=10, blank=True)
    status = models.IntegerField(default=0)  # 状态:1正常/9删除
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 修改时间

    def toDict(self):
        return {'id': self.id, 'survey_id': self.survey_id, 'name': self.name,
                'result': self.result, 'status': self.status, 'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "questionmulSecect"  # 更改表名


class QuestionMulSelectData(models.Model):
    sequenceNumber = models.IntegerField(blank=True)  # 顺序号
    survey_id = models.IntegerField()  # survey_id
    ip = models.CharField(max_length=30)  # ip地址
    answer = models.CharField(max_length=30, blank=True, null=True)  # 答案


class QuestionFillBlank(models.Model):
    score = models.IntegerField(default=0)
    type = models.IntegerField()  # 问题类型
    required = models.BooleanField()  # 是否必填
    survey_id = models.IntegerField()  # survey_id
    sequenceNumber = models.IntegerField(blank=True)  # 顺序号
    name = models.CharField(max_length=50)  # 名称"
    description = models.TextField(blank=True, null=True)  # 题目描述
    result = models.CharField(max_length=100, blank=True, default="")
    status = models.IntegerField(default=1)  # 状态:1正常/9删除
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 修改时间

    def toDict(self):
        return {'id': self.id, 'survey_id': self.survey_id, 'name': self.name, 'result': self.result,
                'status': self.status, 'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "questionfillblank"  # 更改表名


class QuestionFillBlankData(models.Model):
    sequenceNumber = models.IntegerField(blank=True)  # 顺序号
    survey_id = models.IntegerField()  # survey_id
    ip = models.CharField(max_length=30)  # ip地址
    answer = models.CharField(max_length=30, blank=True, null=True)  # 答案


class MulOption(models.Model):
    questionId = models.IntegerField()  # 题目id
    content = models.CharField(max_length=100)  # 选项内容
    numbers = models.IntegerField(default=0)  # 选择人数


class QuestionRemark(models.Model):
    type = models.IntegerField()  # 问题类型
    required = models.BooleanField()  # 是否必填
    survey_id = models.IntegerField()  # survey_id
    name = models.CharField(max_length=50)  # 名称
    score = models.IntegerField(default=0)
    sequenceNumber = models.IntegerField(blank=True)  # 顺序号
    description = models.TextField(blank=True, null=True)  # 题目描述
    status = models.IntegerField(default=1)  # 状态:1正常/9删除
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 修改时间
    result = models.IntegerField(blank=True, default=0)
    starNum = models.IntegerField()

    def toDict(self):
        return {'id': self.id, 'survey_id': self.survey_id, 'name': self.name,
                'status': self.status, 'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "questionremark"  # 更改表名


class QuestionRemarkData(models.Model):
    sequenceNumber = models.IntegerField(blank=True)  # 顺序号
    survey_id = models.IntegerField()  # survey_id
    ip = models.CharField(max_length=30)  # ip地址
    answer = models.IntegerField(blank=True, null=True)  # 答案


class QuestionJudgement(models.Model):
    type = models.IntegerField()  # 问题类型
    required = models.BooleanField()  # 是否必填
    survey_id = models.IntegerField()  # survey_id
    name = models.CharField(max_length=50)  # 名称
    sequenceNumber = models.IntegerField(blank=True)  # 顺序号
    description = models.TextField(blank=True, null=True)  # 题目描述
    status = models.IntegerField(default=1)  # 状态:1正常/9删除
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 修改时间
    result = models.IntegerField(blank=True, null=True)
    score = models.IntegerField(default=0)
    correctAnswers = models.IntegerField(default=0)
    wrongAnswers = models.IntegerField(default=0)


class QuestionJudgementData(models.Model):
    sequenceNumber = models.IntegerField(blank=True)  # 顺序号
    survey_id = models.IntegerField()  # survey_id
    ip = models.CharField(max_length=30)  # ip地址
    answer = models.IntegerField(blank=True, null=True)  # 答案


class Record(models.Model):
    survey_id = models.IntegerField()  # survey_id
    ip = models.CharField(max_length=30)  # ip地址
    username = models.CharField(max_length=100, default="匿名用户")
    submitTime = models.DateTimeField(default=datetime.now)


class Node(models.Model):
    surveyId = models.IntegerField()
    node = models.IntegerField()


# 限额题
class QuestionQuota(models.Model):
    type = models.IntegerField()  # 问题类型
    required = models.BooleanField()  # 是否必填
    survey_id = models.IntegerField()  # survey_id
    name = models.CharField(max_length=50)  # 名称
    sequenceNumber = models.IntegerField(blank=True)  # 顺序号
    description = models.TextField(blank=True, null=True)  # 题目描述
    result = models.CharField(max_length=10, blank=True)
    status = models.IntegerField(default=0)  # 状态:1正常/9删除
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 修改时间

    def toDict(self):
        return {'id': self.id, 'survey_id': self.survey_id, 'name': self.name,
                'result': self.result, 'status': self.status, 'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "questionquota"  # 更改表名


class QuestionQuotaOption(models.Model):
    questionId = models.IntegerField()  # 题目id
    content = models.CharField(max_length=100)  # 选项内容
    numbers = models.IntegerField(default=0)  # 选择人数
    quota = models.IntegerField(default=0)  # 限额


class QuestionQuotaData(models.Model):
    sequenceNumber = models.IntegerField(blank=True)  # 顺序号
    survey_id = models.IntegerField()  # survey_id
    ip = models.CharField(max_length=30)  # ip地址
    answer = models.IntegerField(blank=True, null=True)  # 答案


class QuestionPunch(models.Model):
    score = models.IntegerField(default=0)
    type = models.IntegerField()  # 问题类型
    required = models.BooleanField()  # 是否必填
    survey_id = models.IntegerField()  # survey_id
    sequenceNumber = models.IntegerField(blank=True)  # 顺序号
    name = models.CharField(max_length=50)  # 名称
    description = models.TextField(blank=True, null=True)  # 题目描述
    result = models.CharField(max_length=100, blank=True, default=True)
    status = models.IntegerField(default=1)  # 状态:1正常/9删除
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 修改时间

    def toDict(self):
        return {'id': self.id, 'survey_id': self.survey_id, 'name': self.name, 'result': self.result,
                'status': self.status, 'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "questionpunch"  # 更改表名


class QuestionPunchData(models.Model):
    sequenceNumber = models.IntegerField(blank=True)  # 顺序号
    survey_id = models.IntegerField()  # survey_id
    ip = models.CharField(max_length=30)  # ip地址
    answer = models.CharField(max_length=100, blank=True, null=True)  # 答案
