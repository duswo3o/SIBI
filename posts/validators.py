import re
from .models import Hashtag


def validate_hashtags(request_data):
    hashtags = request_data.get("hashtags").split(" ")
    print(hashtags)

    valid_hashtags = []

    for tag in hashtags:
        if tag in Hashtag.objects.all():
            existing_hashtag = Hashtag.objects.filter(name=tag).first()
            tag = existing_hashtag.name

        # 대소문자 구분 X, 해시태그 앞 # 제거
        tag = tag.lstrip("#").lower()

        # 10자 이하, 공백이나 특수문자가 없어야 함
        if (
            len(tag) <= 10
            and not re.search(r"\s", tag)
            and not re.search(r"[^a-z0-9]", tag)
        ):
            valid_hashtags.append(tag)

    return True, valid_hashtags
