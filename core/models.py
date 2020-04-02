from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):

    """Time stamped model"""

    # abstract를 쓴다 -> 함수가 실행될 때마다 값이 저장되지 않아도 됨
    # abstract User도 그래,, language, currency 등이 저장되는 거라기 보다는
    # 선택지를 제공하는거에서 끝낼 수 있도록 하는 느낌
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
