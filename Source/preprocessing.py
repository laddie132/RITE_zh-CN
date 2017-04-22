#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Second step for RITE: preprocess data"""

from text_pair import *


def _convert_time(text):
    return text


def _convert_num(text):
    return text


def _convert_char(text):
    """
    replace '两' and '双' to '二'
    """

    idiom_with_two1 = ['国士无双', '比翼双飞', '才貌双全', '才气无双', '慈明无双', '当世无双', '德艺双馨',
                     '雕玉双联', '福禄双全', '福无双至', '福慧双修', '盖世无双', '寡二少双', '海内无双',
                     '举世无双', '名利双收', '日下无双', '双瞳剪水', '双斧伐孤树', '双管齐下', '双柑斗酒',
                     '天下无双', '文武双全', '一双两好', '智勇双全', '一箭双雕', '成双成对', '成双作对',
                     '斗酒双柑', '福寿双全', '福无双至，祸不单行', '贯斗双龙', '进退双难', '绝世无双',
                     '双凫一雁', '双桂联芳', '双宿双飞', '双喜临门', '双足重茧', '形单影双', '一雕双兔',
                     '一矢双穿', '一语双关', '才貌双绝', '双栖双宿', '好事成双']
    idiom_with_two2 = ['半斤八两', '掂斤播两', '公私两济', '两次三番', '两肋插刀', '两意三心', '磨盘两圆',
                     '搬斤播两', '秤斤注两', '此地无银三百两', '二心两意', '分斤掰两', '公私两便',
                     '汉贼不两立', '脚踏两只船', '进退两难', '两全其美', '两手空空', '两瞽相扶', '两脚书橱',
                     '两相情愿', '两面二舌', '两小无猜', '两袖清风', '两世为人', '两部鼓吹', '两面三刀', '两败俱伤',
                     '两豆塞耳', '两头白面', '两叶掩目', '两虎相斗', '麦穗两歧', '两脚野狐', '模棱两可', '判若两人',
                     '清风两袖', '人财两空', '去住两难', '三头两绪', '三天两头', '三长两短', '三三两两', '三瓦两舍',
                     '三天打鱼，两天晒网', '三言两语', '三差两错', '三头两面', '势不两立', '首鼠两端', '一身两役',
                     '一长两短', '一举两得', '一蛇两头', '一簧两舌', '一口两匙', '一双两好', '一床两好', '一刀两断',
                     '一丝两气', '依违两可', '一搭两用', '执两用中', '左右两难', '铢两分寸', '着三不着两', '铢两悉称',
                     '两虎相争', '并世无两', '擘两分星', '参天两地', '魑魅罔两', '颠斤播两', '掂斤估两', '掂斤抹两',
                     '调停两用', '分金掰两', '分斤拨两', '分三别两', '分星擘两', '分星拨两', '分星劈两', '公私两利',
                     '合两为一', '尖担两头脱', '进退两端', '两般三样', '两鬓如霜', '两道三科', '两耳塞豆', '两肩荷口',
                     '两脚居间', '两两三三', '两鼠斗穴', '两头和番', '两头三面', '两头三绪', '两相情原', '麦穗两岐',
                     '麦秀两岐', '麦秀两歧', '模棱两端', '拈斤播两', '人琴两亡', '三般两样', '三步两脚', '三番两次',
                     '三好两歹', '三好两歉', '三饥两饱', '三脚两步', '三街两市', '三节两寿', '三婆两嫂', '三汤两割',
                     '三头两日', '三瓦两巷', '三窝两块', '三心两意', '三言两句', '身名两泰', '势不两存', '誓不两立',
                     '首施两端', '弹斤估两', '心不两用', '一差两讹', '一刀两段', '一饥两饱', '一举两全', '一栖两雄',
                     '一身两头', '一推两搡', '一言两语', '音问两绝', '忠孝两全', '铢两相称', '铢施两较', '才貌两全',
                     '两雄不并立', '人财两失', '三拳两脚', '三日打鱼，两日晒网', '首尾两端', '一渊不两蛟', '两面讨好',
                     '两情两愿', '取舍两难', '百两烂盈', '一举两失', '一身两任', '一马不跨两鞍', '扁担没扎，两头打塌',
                     '扁担脱，两头虚', '两虎共斗', '两虎相斗，必有一伤', '两贤相厄']

    for i in range(len(idiom_with_two1)):
        if idiom_with_two1[i] in text:
            text = text.replace(idiom_with_two1[i], '<%d>' % i)

    for i in range(len(idiom_with_two2)):
        if idiom_with_two2[i] in text:
            text = text.replace(idiom_with_two2[i], '[%d]' % i)

    text = text.replace('两', '二').replace('双', '二')

    for i in range(len(idiom_with_two1)):
        if '<%d>' % i in text:
            text = text.replace('<%d>' % i, idiom_with_two1[i])

    for i in range(len(idiom_with_two2)):
        if '[%d]' % i in text:
            text = text.replace('[%d]' % i, idiom_with_two2[i])

    return text


def _convert_unit(text):
    return text


def preprocess(textPair):
    """
    preprocessing function for using
    """
    t1 = textPair.t1
    t2 = textPair.t2

    def _prepro(text):
        text_n = _convert_num(text)
        text_c = _convert_char(text_n)
        text_m = _convert_time(text_c)
        return _convert_unit(text_m)

    return TextPair(_prepro(t1), _prepro(t2), textPair.label)


if __name__ == '__main__':
    textPair = TextPair('两个 一双 半斤八两', '车位成为', 'Y')
    newText = preprocess(textPair)
    print(newText.t1, newText.t2, newText.label, sep='\n')
