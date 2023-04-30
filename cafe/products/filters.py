from jamo import h2j, j2hcj
import django_filters
from .models import Product

def remove_vowels_and_space(string):
    # 모음과 ' ' 제거 메서드
    vowels = ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅔ', 'ㅐ', 'ㅢ', 'ㅟ','ㅙ','ㅞ',' ']
    result = ''

    for char in string:
        if char not in vowels:
            result += char

    return result


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='name_filter')

    class Meta:
        model = Product
        fields = ['name']

    def name_filter(self, queryset, name, value):
        # 검색어에서 초성 추출
        flag = False
        value_jamo = j2hcj(h2j(value))
        db_jamo = []
        for q in queryset: # 0 1
            db_jamo.append(remove_vowels_and_space(j2hcj(h2j(q.name)))) # ㅋㄹㅁㄹㄸ ㅇㅁㄹㅋㄴ

        # 초성 검색어가 존재하면, 초성 검색 결과를 상품 목록에 추가
        for chk in range(len(db_jamo)):
            if value_jamo in db_jamo[chk]:
                idx = chk
                flag = True
        
        if flag == True:
            queryset = queryset.filter(name=queryset[idx].name)


        # 초성 검색어가 없으면, 일반 검색 결과만 리턴
        else:
            queryset = queryset.filter(name__icontains=value)

        return queryset

"""
밑에는 jamo 없이 시도하다가 pass...
"""

# import django_filters
# from .models import Product

# class ProductFilter(django_filters.FilterSet):
#     name = django_filters.CharFilter(method='name_filter')

#     class Meta:
#         model = Product
#         fields = ['name']

#     def name_filter(self, queryset, name, value):
#         # 검색어에서 초성 추출
#         chosung_table = {
#             'ㄱ': 'ㄱ ㄲ ㅋ',
#             'ㄴ': 'ㄴ',
#             'ㄷ': 'ㄷ ㄸ ㅌ',
#             'ㄹ': 'ㄹ',
#             'ㅁ': 'ㅁ',
#             'ㅂ': 'ㅂ ㅃ ㅍ',
#             'ㅅ': 'ㅅ ㅆ',
#             'ㅇ': 'ㅇ',
#             'ㅈ': 'ㅈ ㅉ ㅊ',
#             'ㅊ': 'ㅈ ㅉ ㅊ',
#             'ㅋ': 'ㄱ ㄲ ㅋ',
#             'ㅌ': 'ㄷ ㄸ ㅌ',
#             'ㅍ': 'ㅂ ㅃ ㅍ',
#             'ㅎ': 'ㅎ'
#         }

#         chosung_list = []
#         for c in value:
#             if '가' <= c <= '힣':
#                 chosung_index = (ord(c) - ord('가')) // 588
#                 if 0 <= chosung_index < len(chosung_table):
#                     chosung = list(chosung_table.keys())[chosung_index]
#                     chosung_list.append(chosung_table[chosung])
#             else:
#                 chosung_list.append(c)

#         chosung_value = ' '.join(chosung_list)

#         # 검색어를 포함하는 상품 검색 (like 검색)
#         queryset = queryset.filter(name__icontains=value)

#         # 초성 검색어가 존재하면, 초성 검색 결과를 상품 목록에 추가
#         if chosung_value != value:
#             for chosung in chosung_value.split():
#                 queryset |= Product.objects.filter(name__istartswith=chosung)

#         return queryset
