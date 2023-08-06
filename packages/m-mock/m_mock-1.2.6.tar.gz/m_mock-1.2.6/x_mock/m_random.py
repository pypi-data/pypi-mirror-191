import random
import re
import string
from datetime import datetime, timedelta

from x_mock.m_random_source import single_family_name, en_family_name, en_name


def inNone(obj):
    if isinstance(obj, (tuple, list)):
        # 都为空的就返回True
        boo = []
        for i in obj:
            boo.append(i in ('', None))
        return False if False in boo else True
    return obj in ('', None)


def tuple_to_str(objects) -> str:
    """
    :param objects: 被转换的元组/列表
    :return: 列表被转换后的字符串
    """
    return str(''.join(objects))


def shuffle_string(strings) -> str:
    """

    :param strings: 被打乱的字符(str/list/tuple)
    :return: 打乱的字符
    """
    if isinstance(strings, (list, tuple)):
        pass
    elif isinstance(strings, str):
        strings = list(strings)
    random.shuffle(strings)
    strings = ''.join(strings)
    return strings


class MockPyExpressionException(Exception):
    def __init__(self, exception='Incorrect mocker expression is used.', remark=''):
        super().__init__()
        self.exception = f'{exception}{remark}'

    def __str__(self):
        return self.exception

    @classmethod
    def min_max_value_exception(cls, min_value, max_value):
        if (max_value is None or min_value is None) is False:
            if min_value >= max_value:
                raise MockPyExpressionException('min_value cannot be greater than or equal to max_value.')


_mock_exception = MockPyExpressionException()

chinese = '一乙二十丁厂七卜人入八九几儿了力乃刀又三于干亏士工土才寸下大丈与万上小口巾山千乞川亿个勺久凡及夕丸么广亡门义之尸弓己已' \
          '子卫也女飞刃习叉马乡丰王井开夫天无元专云扎艺木五支厅不太犬区历尤友匹车巨牙屯比互切瓦止少日中冈贝内水见午牛手毛气升长仁' \
          '什片仆化仇币仍仅斤爪反介父从今凶分乏公仓月氏勿欠风丹匀乌凤勾文六方火为斗忆订计户认心尺引丑巴孔队办以允予劝双书幻玉刊示末' \
          '未击打巧正扑扒功扔去甘世古节本术可丙左厉右石布龙平灭轧东卡北占业旧帅归且旦目叶甲申叮电号田由史只央兄叼叫另叨叹四生失禾丘' \
          '付仗代仙们仪白仔他斥瓜乎丛令用甩印乐句匆册犯外处冬鸟务包饥主市立闪兰半汁汇头汉宁穴它讨写让礼训必议讯记永司尼民出辽奶奴加' \
          '召皮边发孕圣对台矛纠母幼丝式刑动扛寺吉扣考托老执巩圾扩扫地扬场耳共芒亚芝朽朴机权过臣再协西压厌在有百存而页匠夸夺灰达列死' \
          '成夹轨邪划迈毕至此贞师尘尖劣光当早吐吓虫曲团同吊吃因吸吗屿帆岁回岂刚则肉网年朱先丢舌竹迁乔伟传乒乓休伍伏优伐延件任伤价份' \
          '华仰仿伙伪自血向似后行舟全会杀合兆企众爷伞创肌朵杂危旬旨负各名多争色壮冲冰庄庆亦刘齐交次衣产决充妄闭问闯羊并关米灯州汗污' \
          '江池汤忙兴宇守宅字安讲军许论农讽设访寻那迅尽导异孙阵阳收阶阴防奸如妇好她妈戏羽观欢买红纤级约纪驰巡寿弄麦形进戒吞远违运扶' \
          '抚坛技坏扰拒找批扯址走抄坝贡攻赤折抓扮抢孝均抛投坟抗坑坊抖护壳志扭块声把报却劫芽花芹芬苍芳严芦劳克苏杆杠杜材村杏极李杨求' \
          '更束豆两丽医辰励否还歼来连步坚旱盯呈时吴助县里呆园旷围呀吨足邮男困吵串员听吩吹呜吧吼别岗帐财针钉告我乱利秃秀私每兵估体何' \
          '但伸作伯伶佣低你住位伴身皂佛近彻役返余希坐谷妥含邻岔肝肚肠龟免狂犹角删条卵岛迎饭饮系言冻状亩况床库疗应冷这序辛弃冶忘闲间' \
          '闷判灶灿弟汪沙汽沃泛沟没沈沉怀忧快完宋宏牢究穷灾良证启评补初社识诉诊词译君灵即层尿尾迟局改张忌际陆阿陈阻附妙妖妨努忍劲鸡' \
          '驱纯纱纳纲驳纵纷纸纹纺驴纽奉玩环武青责现表规抹拢拔拣担坦押抽拐拖拍者顶拆拥抵拘势抱垃拉拦拌幸招坡披拨择抬其取苦若茂苹苗英' \
          '范直茄茎茅林枝杯柜析板松枪构杰述枕丧或画卧事刺枣雨卖矿码厕奔奇奋态欧垄妻顷转斩轮软到非叔肯齿些虎虏肾贤尚旺具果味昆国昌畅' \
          '明易昂典固忠咐呼鸣咏呢岸岩帖罗帜岭凯败贩购图钓制知垂牧物乖刮秆和季委佳侍供使例版侄侦侧凭侨佩货依的迫质欣征往爬彼径所舍金' \
          '命斧爸采受乳贪念贫肤肺肢肿胀朋股肥服胁周昏鱼兔狐忽狗备饰饱饲变京享店夜庙府底剂郊废净盲放刻育闸闹郑券卷单炒炊炕炎炉沫浅法' \
          '泄河沾泪油泊沿泡注泻泳泥沸波泼泽治怖性怕怜怪学宝宗定宜审宙官空帘实试郎诗肩房诚衬衫视话诞询该详建肃录隶居届刷屈弦承孟孤陕' \
          '降限妹姑姐姓始驾参艰线练组细驶织终驻驼绍经贯奏春帮珍玻毒型挂封持项垮挎城挠政赴赵挡挺括拴拾挑指垫挣挤拼挖按挥挪某甚革荐巷' \
          '带草茧茶荒茫荡荣故胡南药标枯柄栋相查柏柳柱柿栏树要咸威歪研砖厘厚砌砍面耐耍牵残殃轻鸦皆背战点临览竖省削尝是盼眨哄显哑冒映' \
          '星昨畏趴胃贵界虹虾蚁思蚂虽品咽骂哗咱响哈咬咳哪炭峡罚贱贴骨钞钟钢钥钩卸缸拜看矩怎牲选适秒香种秋科重复竿段便俩贷顺修保促侮' \
          '俭俗俘信皇泉鬼侵追俊盾待律很须叙剑逃食盆胆胜胞胖脉勉狭狮独狡狱狠贸怨急饶蚀饺饼弯将奖哀亭亮度迹庭疮疯疫疤姿亲音帝施闻阀阁' \
          '差养美姜叛送类迷前首逆总炼炸炮烂剃洁洪洒浇浊洞测洗活派洽染济洋洲浑浓津恒恢恰恼恨举觉宣室宫宪突穿窃客冠语扁袄祖神祝误诱说' \
          '诵垦退既屋昼费陡眉孩除险院娃姥姨姻娇怒架贺盈勇怠柔垒绑绒结绕骄绘给络骆绝绞统耕耗艳泰珠班素蚕顽盏匪捞栽捕振载赶起盐捎捏埋' \
          '捉捆捐损都哲逝捡换挽热恐壶挨耻耽恭莲莫荷获晋恶真框桂档桐株桥桃格校核样根索哥速逗栗配翅辱唇夏础破原套逐烈殊顾轿较顿毙致柴' \
          '桌虑监紧党晒眠晓鸭晃晌晕蚊哨哭恩唤啊唉罢峰圆贼贿钱钳钻铁铃铅缺氧特牺造乘敌秤租积秧秩称秘透笔笑笋债借值倚倾倒倘俱倡候俯倍' \
          '倦健臭射躬息徒徐舰舱般航途拿爹爱颂翁脆脂胸胳脏胶脑狸狼逢留皱饿恋桨浆衰高席准座脊症病疾疼疲效离唐资凉站剖竞部旁旅畜阅羞瓶' \
          '兼烤烘烦烧烛烟递涛浙涝酒涉消浩海涂浴浮流润浪浸涨烫涌悟悄悔悦害宽家宵宴宾窄容宰案请朗诸读扇袜袖袍被祥课谁调冤谅谈谊剥恳展' \
          '弱陵陶陷陪娱娘通能难预桑绢绣验继球理捧堵描域掩捷排掉堆推掀授教掏掠培接控探据掘职基著勒黄萌萝菌菜萄菊萍菠营械梦梢梅检梳梯' \
          '副票戚爽聋袭盛雪辅辆虚雀堂常匙晨睁眯眼悬野啦晚啄距跃略蛇累唱患唯崖崭崇圈铜铲银甜梨犁移笨笼笛符第敏做袋悠偿偶偷您售停偏假' \
          '盘船斜盒鸽悉欲彩领脚脖脸脱象够猜猪猎猫猛馅馆凑减毫麻痒痕廊康庸鹿盗章竟商族旋望率着盖粘粗粒断剪兽清添淋淹渠渐混渔淘液淡深' \
          '渗情惜惭悼惧惕惊惨惯寇寄宿窑密谋谎祸谜逮敢屠弹随蛋隆隐婚婶颈绩绪续骑绳维绵绸绿琴斑替款堪搭塔越趁趋超提堤博揭喜插揪搜煮援' \
          '搂搅握揉斯期欺联散惹葬葛董葡敬葱落朝辜葵棒棋植森椅椒棵棍棉棚棕惠惑逼厨厦硬确雁殖裂雄暂雅辈悲紫辉敞赏掌晴暑最量喷晶喇遇喊' \
          '跌跑遗蛙蛛蜓喝喂喘喉幅帽赌赔黑铸铺链销锁锄锅锈锋锐短智毯鹅剩稍程稀税筐等筑策筛筒答筋筝傲傅牌堡集焦傍储奥街惩御循艇舒番释' \
          '脾腔鲁猾猴然馋装蛮就痛童阔善羡普粪尊道曾焰港湖渣湿温渴滑湾渡游滋溉愤慌惰愧愉慨割寒富窜窝窗遍裕裤裙谢谣谦属屡强粥疏隔隙絮' \
          '缎缓编骗缘瑞魂肆摄摸填搏塌鼓摆携搬摇搞塘摊蒜勤鹊蓝墓幕蓬蓄蒙蒸献禁楚想槐榆楼概赖酬感碍碑碎碰碗碌雷零雾雹输督龄鉴睛睡睬鄙' \
          '盟歇暗照跨跳跪路跟遣蛾蜂嗓置罪罩错锡锣锤锦键锯矮辞稠愁筹签简毁舅鼠催傻像躲微愈遥腰腥腹腾腿触解酱痰廉新韵意粮数煎塑慈煤煌' \
          '源滤滥滔溪溜滚滨粱滩慎誉塞谨福群殿辟障嫌嫁叠缝缠静碧璃墙撇嘉摧截誓境摘摔聚蔽慕暮蔑模榴榜榨歌遭酷酿酸磁愿需弊裳颗嗽蜻蜡蝇' \
          '锹锻舞稳算箩管僚鼻魄貌膜膊膀鲜疑馒裹敲豪膏遮腐瘦辣竭端旗精歉熄熔漆漂漫滴演漏慢寨赛察蜜谱嫩翠熊凳骡缩慧撕撒趣趟撑播撞撤增' \
          '蕉蔬横槽樱橡飘醋醉震霉瞒题暴瞎影踢踏踩踪蝶蝴嘱墨镇靠稻黎稿稼箱箭篇僵躺僻德艘膝膛熟摩颜毅糊遵潜潮懂额慰劈操燕薯薪薄颠橘整' \
          '餐嘴蹄器赠默镜赞篮邀衡膨雕磨凝辨辩糖糕燃澡激懒壁避缴戴擦鞠藏霜霞瞧蹈螺穗繁辫赢糟糠燥臂翼骤鞭覆蹦镰翻鹰警攀蹲颤瓣爆疆壤耀' \
          '嚷籍魔灌蠢霸露料益拳粉剧屑桶救得衔婆梁裁搁景践禽腊嫂登愚暖满漠蜘赚聪鞋融醒躁嚼'
cn_punctuation = r"""。？！，、；：“”‘’『』「」（）[]〔〕【】——……·—-～《》〈〉___/"""


class BooleanM:
    @classmethod
    def boolean(cls, min_value=None, max_value=None, current=None):
        _mock_exception.min_max_value_exception(min_value, max_value)
        if inNone((max_value, current)) and inNone(min_value) is False:
            # 只输入min_value则返回True
            return True
        min_value = 0 if inNone(min_value) else min_value
        max_value = 1 if inNone(max_value) else max_value
        current = True if inNone(current) else current
        luck_boolean_number = random.randint(min_value, max_value)
        if luck_boolean_number == min_value:
            return current
        else:
            return not current


m_boolean = BooleanM()


class NaturalM:
    @classmethod
    def natural(cls, min_value=None, max_value=None) -> int:
        """

        :param min_value: 最小值,默认值:0
        :param max_value: 最大值,默认值:9999999999999999
        :return: 自然数
        """
        if inNone(min_value):
            min_value = 0
        if inNone(max_value):
            max_value = 9999999999999999
        _mock_exception.min_max_value_exception(min_value, max_value)
        return random.randint(min_value, max_value)


m_natural = NaturalM()


class NumberM:
    number_str_max_length = None

    @classmethod
    def number_str(cls, min_length=None, max_length=number_str_max_length) -> str:
        """

        :param min_length:
        :param max_length:
        :return: 随机长度的数字字符
        """
        _mock_exception.min_max_value_exception(max_length, min_length)
        if inNone(min_length):
            min_length = random.randint(0, 15)
        if inNone(max_length):
            max_length = random.randint(min_length, 16)
        number_string_list = []
        range_size = cls.number_not_start_with_zero(min_length, max_length)
        for kk in range(range_size):
            number_string_list.append(str(random.randint(0, 9)))
        number_str = ''.join(number_string_list)
        return number_str

    @classmethod
    def number_not_start_with_zero(cls, start_number: int, end_number: int) -> int:
        """

        :param end_number: 随机数的最大值,包含
        :param start_number: 随机数的最小值,包含,默认=1
        :return: 从1开始的整数类型的随机数;[start_number,end_number] 取值范围为闭区间
        """
        return random.randint(start_number if start_number != 0 else 1, end_number if end_number != 1 else 2)


m_number = NumberM()


class IntegerM:
    @classmethod
    def integer(cls, min_value=None, max_value=None) -> int:
        """

        :param min_value: 最小值,默认值:0
        :param max_value: 最大值,默认值:9999999999999999
        :return: 自然数[min_value,max_value]
        """
        _mock_exception.min_max_value_exception(min_value, max_value)
        if inNone(min_value):
            min_value = -9999999999999999
        if inNone(max_value):
            max_value = 9999999999999999
        if min_value > max_value:
            raise MockPyExpressionException()
        return random.randint(min_value, max_value)


m_integer = IntegerM()


class CharacterM:
    @classmethod
    def character(cls, character_type=None):
        character_type = random.choice(
            ('lower', 'upper', 'number', 'symbol')) if character_type is None else character_type
        return StringM.string(character_type, 1)


m_character = CharacterM()


class FloatM:
    @classmethod
    def float(cls, min_value=None, max_value=None, d_min_value=None,
              d_max_value=None):
        """
        随机浮点数,example:
        @float(95,100,12,19)
        @float(1,2)
        @float(952)  # 不小于992
        @float()  # 随机
        @float
        :param min_value:个位部分最小值
        :param max_value:个位部分最大值
        :param d_min_value:小数部分最小长度
        :param d_max_value:小数部分最大长度
        :return:
        """

        def __luck():
            return random.randint(1, 4) in (1, 2, 3)

        _mock_exception.min_max_value_exception(min_value, max_value)
        if inNone(min_value):
            min_value = -9999999999999999
        if inNone(max_value):
            max_value = 9999999999999999
        if inNone(d_min_value):
            d_min_value = random.randint(2, 5) if random.randint(1, 2) == 1 else 0
        if inNone(d_max_value):
            min_d_max_value = d_min_value if 14 > d_min_value > 0 else d_min_value + 1
            d_max_value = random.randint(min_d_max_value + 1, 16)
        decimals = StringM.string_number(d_min_value, d_max_value)
        if __luck():
            while True:
                # 满足最小值和最大值的浮点数
                random_float = random.uniform(min_value, max_value)
                val = str(random_float)
                if '.' in val:
                    break
            int_part = val.split(".")[0]
            int_part = int_part if len(int_part) + len(decimals) <= 15 else int_part[:len(decimals)]
            val = f'{int_part}.{decimals}'
            random_float = float(val)
        else:
            random_float = random.uniform(min_value, max_value)
            if __luck():
                random_float = float(f'{str(random_float)[:-1]}{random.randint(1, 9)}')
        round_num = random.randint(d_min_value, d_max_value)
        return float(round(random_float, round_num))


m_float = FloatM()


class StringM:
    @classmethod
    def string_lower(cls, min_value=None, max_value=None) -> str:
        """
        :return: 随机小写英文字符
        """
        return cls.get_random_string_by_source(string.ascii_lowercase, min_value, max_value)

    @classmethod
    def get_random_string_by_source(cls, source=None, min_value: int = None, max_value: int = None) -> str:
        _mock_exception.min_max_value_exception(min_value, max_value)
        if inNone(min_value):
            length = random.randint(1, 9)
        elif inNone(max_value):
            length = min_value
        else:
            length = random.randint(min_value, max_value)
        str_list = []
        for i in range(length):
            str_list.append(random.choice(source))
        random.shuffle(str_list)
        return tuple_to_str(str_list)

    @classmethod
    def string_upper(cls, min_value=None, max_value=None) -> str:
        """

        :return: 随机大写英文字符
        """
        return cls.get_random_string_by_source(string.ascii_uppercase, min_value, max_value)

    @classmethod
    def string_number(cls, min_value=None, max_value=None) -> str:
        """

        :return: 随机长度数字字符
        """
        return cls.get_random_string_by_source(string.digits, min_value, max_value)

    @classmethod
    def string_symbol(cls, min_value=None, max_value=None) -> str:
        """

        :return: 随机标点符号字符
        """
        return cls.get_random_string_by_source(string.punctuation, min_value, max_value)

    @classmethod
    def strings(cls, min_value=None, max_value=None) -> str:
        """

        :return: 包含(英文/英文标点/数字)的随机字符
        """
        source = string.ascii_letters + string.digits + string.punctuation
        return cls.get_random_string_by_source(source, min_value, max_value)

    @classmethod
    def chinese(cls, min_value=None, max_value=None) -> str:
        """

        :return: 纯中文随机字符
        """
        return cls.get_random_string_by_source(chinese, min_value, max_value)

    @classmethod
    def cn_symbol(cls, min_value=None, max_value=None) -> str:
        """

        :return: 随机中文标点符号
        """
        return cls.get_random_string_by_source(cn_punctuation, min_value, max_value)

    @classmethod
    def cn_string(cls, min_value=None, max_value=None) -> str:
        """


        :return: 随机标点符号字符
        """

        def __cn_sting():
            cn_min_value = random.randint(1, max_value - 1)
            cn_str = cls.get_random_string_by_source(chinese, cn_min_value)
            cn_symbol = cls.cn_symbol(max_value - cn_min_value)
            cn_strings = list(cn_str + cn_symbol)
            random.shuffle(cn_strings)
            return tuple_to_str(cn_strings)

        if min_value >= 2 and inNone(max_value):
            max_value = min_value
            return __cn_sting()
        elif inNone(max_value) or min_value == 1:
            return cls.get_random_string_by_source(cn_punctuation + chinese, min_value, max_value)
        else:
            return __cn_sting()

    @classmethod
    def string(cls, *args) -> str:
        """

        :param args: 参数,例如:返回字符的长度
        :return: 随机长度的英/数/英文标点符号的混合字符
        """
        if len(args) <= 1 or isinstance(args[0], int):
            return cls.strings(*args)
        elif 3 >= len(args) >= 2:
            string_type = args[0]
            new_args = args[1:]
            if string_type == 'lower':
                return cls.string_lower(*new_args)
            elif string_type == 'upper':
                return cls.string_upper(*new_args)
            elif string_type == 'number':
                return cls.string_number(*new_args)
            elif string_type == 'symbol':
                return cls.string_symbol(*new_args)
            elif string_type == 'string':
                return cls.strings(*new_args)
            elif string_type == 'chinese':
                return cls.chinese(*new_args)
            elif string_type == 'cn_symbol':
                return cls.cn_symbol(*new_args)
            elif string_type == 'cn_string':
                return cls.cn_string(*new_args)
            else:
                return cls.get_random_string_by_source(string_type, *new_args)
        elif len(args) > 3:
            raise MockPyExpressionException('only 3 parameters are allowed.')


m_string = StringM()


class DateM:
    @classmethod
    def datetime(cls, format_str=None, time_interval: str = None):
        """
        example:
        @date('%Y-%m-%d %H:%M:%S')  2022-12-09 16:50:00
        @date('%Y-%m-%d %H:%M:%S','-1')  2022-12-08 16:50:00
        @date('%Y-%m-%d %H-%M-%S')
        @date()
        :param format_str:
        :param time_interval:'+1min'/'-1mil'
        :return:
        """
        # 判断是否满足表达式
        if not inNone(time_interval) and (len(time_interval) <= 1 or time_interval[:1] not in ('+', '-')):
            raise MockPyExpressionException(remark="The correct expression for time:'+1h' or '-1h'.")
        # '@date("%Y.%m.%d %H:%M:%S","+1")'
        if inNone(format_str):
            format_str = '%Y-%m-%d %H:%M:%S'
        # 定义初始化变量
        days = 0
        seconds = 0
        microseconds = 0
        milliseconds = 0
        minutes = 0
        hours = 0
        # 当前时间
        curr_time = datetime.now()
        today = (curr_time.strftime(format_str))
        # 处理时间的计算
        if not inNone(time_interval):
            calculate = time_interval[:1]
            # 正则获取时间单位
            regular = '[a-zA-Z]+'  # 正则匹配英文
            match = re.search(regular, time_interval)
            group = match.group(0)
            unit = group
            # 时间的间隔量
            amount = int(time_interval[1:-len(unit)])
            # 处理时间的量
            if 'hours'.startswith(unit):
                hours = amount
            elif 'minutes'.startswith(unit):
                minutes = amount
            elif 'milliseconds'.startswith(unit):
                milliseconds = amount
            elif 'microseconds'.startswith(unit):
                microseconds = amount
            elif 'seconds'.startswith(unit):
                seconds = amount
            elif 'days'.startswith(unit):
                days = amount
            timedelta_value = timedelta(days=days, seconds=seconds, microseconds=microseconds,
                                        milliseconds=milliseconds, minutes=minutes, hours=hours)
            if calculate == '+':
                random_data = (curr_time + timedelta_value).strftime(format_str)
                return random_data
            elif calculate == '-':
                random_data = (curr_time - timedelta_value).strftime(format_str)
                return random_data
        return today

    @classmethod
    def date(cls, format_str=None, time_interval: str = None):
        """
        example:
        @date('%Y-%m-%d')  2022-12-09
        @date('%Y-%m-%d','-1')  2022-12-08
        @date()
        可以传参'%Y-%m-%d %H:%M:%S'
        :param format_str:'%Y-%m-%d';'%Y:%m:%d'/'%Y-%m-%d %H:%M:%S'
        :param time_interval: 加或减
        :return: 随机日期(年月日/年月日时分秒)
        """
        format_str = '%Y-%m-%d' if inNone(format_str) else format_str
        return cls.datetime(format_str, time_interval)

    @classmethod
    def time(cls, format_str=None, time_interval: str = None):
        """
        example:
        @time('%Y-%m-%d')  15:03:49
        @time('%Y-%m-%d','-1')  2022-12-08
        @time()
        可以传参'%Y-%m-%d %H:%M:%S'
        :param time_interval: 加或减
        :param format_str:'%H:%M:%S'/'%Y:%m:%d';'%Y-%m-%d %H:%M:%S'
        :return: 随机日期(时分秒/年月日时分秒)
        """
        format_str = '%H:%M:%S' if inNone(format_str) else format_str
        return cls.datetime(format_str, time_interval=time_interval)


m_date = DateM()


class HelperM:
    @classmethod
    def pick(cls, pick_list):
        if inNone(pick_list):
            raise MockPyExpressionException('pick_list cannot be empty.')
        assert isinstance(pick_list, (str, list, tuple))
        if isinstance(pick_list, str):
            pick_list = eval(pick_list)
        return random.choice(pick_list)


m_helper = HelperM()


class NameM:
    @classmethod
    def first(cls):
        """

        :return: 获取中文姓名的首个字符-姓
        """
        return random.choice(en_family_name)

    @classmethod
    def last(cls):
        """

        :return: 获取中文姓名的首个字符-名
        """
        return random.choice(en_name)

    @classmethod
    def name(cls, middle=None):
        """

        :return: 中文姓氏
        """
        if middle is not None and middle in ('true', 'True',True, '1', 1):
            a = cls.first()
            c = cls.last()
            b = None
            for i in range(20):
                b = cls.first()
                if cls.first() != a:
                    break
            return f'{a} {b} {c}'
        return f'{cls.first()} {cls.last()}'

    @classmethod
    def cfirst(cls):
        """

        :return: 获取中文姓名的首个字符-姓
        """
        return random.choice(single_family_name)

    @classmethod
    def clast(cls):
        """

        :return: 获取中文姓名的首个字符-名
        """
        return m_string.chinese(1, 2)

    @classmethod
    def cname(cls, length=None):
        """

        :return: 中文姓氏
        """
        length = random.randint(2, 3) if length is None else length
        if 3 <= length < 2:
            raise MockPyExpressionException()
        return cls.cfirst() + m_string.chinese(length - 1)


m_name = NameM()
