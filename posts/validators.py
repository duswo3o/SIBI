import re
from .models import Hashtag

def validate_hashtags(request_data):
    hashtags = request_data.get("hashtags").split(" ")
    print(hashtags)

    valid_hashtag = []

    for tag in hashtags:
        if tag in Hashtag.objects.all():
            continue

        # 대소문자 구분 X
        tag = tag.lower()

        # 해시태그 앞 # 제거
        tag = tag.lstrip("#")

        # 10자 이하
        if len(tag) > 10:
            continue

        # 공백 없음
        if re.search(r'\s', tag):
            continue

        # 특수문자 허용 X
        if re.search(r'[^a-z0-9]', tag):
            continue
        
        valid_hashtag.append({'name': tag})
        
    return True, valid_hashtag