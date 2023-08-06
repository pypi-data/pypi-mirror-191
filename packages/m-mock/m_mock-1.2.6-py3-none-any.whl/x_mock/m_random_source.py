import random

# 单个中文姓氏
single_family_name = """赵钱孙李周吴郑王冯陈楮卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章
云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常
乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞
熊纪舒屈项祝董梁杜阮蓝闽席季麻强贾路娄危江童颜郭梅盛林刁锺徐丘骆高夏蔡田樊胡凌霍
虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚程嵇邢滑裴陆荣翁
荀羊於惠甄麹家封芮羿储靳汲邴糜松井段富巫乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫
宁仇栾暴甘斜厉戎祖武符刘景詹束龙叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙
池乔阴郁胥能苍双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍郤璩桑桂濮牛寿通边扈燕冀郏浦尚农
温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘匡国文寇广禄阙东
欧殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空曾毋沙乜养鞠须丰巢关蒯相查后荆红
游竺权逑盖益桓公"""

# 单个英文姓氏
en_family_name = ['Laura', 'Melissa', 'Kennet', 'Timothy', 'Betty', 'Scott', 'Mary', 'Susan', 'Brenda', 'Mark', 'Paul',
                  'Donna', 'Richard', 'Thomas', 'Jose', 'Gary', 'Amy', 'Robert', 'Jennifer', 'Steven', 'Charles',
                  'Jessica']
# 英文名
en_name = ['Martin', 'Clark', 'Walker', 'Taylor', 'Lewis', 'Allen', 'Lee', 'Williams', 'Jackson', 'Moore', 'Lopez',
           'Jones', 'Wilson', 'Garcia', 'Harris', 'Davis', 'White', 'Thomas', 'Perez', 'Hall', 'Young', 'Robinson',
           'Smith', 'Gonzalez']

# ss = single_family_name.split('\n')
# ss = [i.replace(' ', '') for i in ss if len(i) > 4]
# n = 5
# ss = [ss[i:i + n] for i in range(0, len(ss), n)]
# for i in ss:
#     print(''.join(i))
