#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('/Users/dywang/Desktop/1999年小浣熊水浒')
PROJECT = ROOT / 'character-model-sheets'

DATA = {
    '002': dict(g='男性', age='中年', face='长方脸、浓眉、目光威严', hair='黑发大部被金色尖顶盔遮挡', beard='浓黑长髭与及胸长须', body='高大健壮、骑将体型', costume='金红重甲、尖顶金盔、红披风、紫灰围巾与金色护腿', palette='金、红、黑、紫灰、白', weapon='长柄金属兵器与红色战旗组合装备', mount='白色战马，金色额甲、黑色颈甲、蓝色胸穗与金色马具', pet=None, asym='战旗和长柄兵器的位置不得跨视角镜像', unknown='马匹远侧甲具、兵器完整头部和人物背甲被遮挡'),
    '003': dict(g='男性', age='中年', face='清瘦长脸、眉目沉静', hair='黑发藏于黑色方巾帽内', beard='细上髭与短山羊胡', body='修长文士体型', costume='多层白色与浅蓝宽袖长袍、灰蓝披风、银灰护腕', palette='白、浅蓝、灰蓝、银灰', weapon=None, mount=None, pet=None, asym='手持长卷属于动作，不作为左右永久结构', unknown='长袍背面闭合、鞋履与卷轴背面不可见'),
    '004': dict(g='男性', age='成年', face='窄长脸、眉目锐利', hair='黑发与头顶大部被紫黑高帽和宽袖遮挡', beard='无清晰胡须', body='修长灵活', costume='紫色宽袖外袍、白色层叠袖口、深色裤与白色绑腿', palette='紫、白、黑、淡粉', weapon='窄身直剑，简单护手与深色握柄', mount=None, pet=None, asym='直剑握持侧保持一致', unknown='面部、发型与袍服背面被动作和袖口大面积遮挡'),
    '005': dict(g='男性', age='中年', face='方脸、浓眉、神情强悍', hair='黑发藏于黑红兜鍪', beard='浓黑长须', body='高大结实', costume='绿色战袍、金色札甲与护腿、红披风、黑红头盔', palette='绿、金、红、黑', weapon='超长黑金杆战刀，宽大银色月牙形刃', mount='枣红战马，白色长鬃与白尾、红绿金马具', pet=None, asym='长刀持握和披风方向保持一致', unknown='长刀杆尾、马匹远侧马具和背甲结构被遮挡'),
    '006': dict(g='男性', age='成年', face='清瘦方脸、目光冷静', hair='黑发藏于白盔与红缨下', beard='无清晰胡须', body='高挑结实', costume='白盔红缨、蓝白轻甲、红色甲裙、紫灰大披风与黑色长靴', palette='白、蓝、红、紫灰、黑', weapon='银色长枪，细长枪头；随身圆形铜锣状附件', mount=None, pet=None, asym='披风与圆形附件位置不得镜像', unknown='披风背面、枪尾和远侧甲片被遮挡'),
    '007': dict(g='男性', age='中年', face='方脸、浓眉、怒目', hair='红褐发束于金红盔内', beard='红褐短髭与短须', body='高大强壮', costume='金色重甲、红色甲绦、黑灰披肩与紫色护腿', palette='金、红、黑、紫、棕', weapon='长柄狼牙棒／锯齿钉头重兵器，黑银钉刺与金色杆身', mount='栗棕战马，黑鬃、紫鞍垫与金属马具', pet=None, asym='狼牙棒持握侧与马具保持一致', unknown='兵器杆尾、马匹远侧鞍具和背甲不可见'),
    '008': dict(g='男性', age='中年', face='面部被黑色重盔部分遮挡、双目发亮', hair='头发完全被盔甲遮挡', beard='无可确认胡须', body='矮壮厚重', costume='黑色重甲、银色铆钉、红色大披风与红黑护腿', palette='黑、红、银、金', weapon='黑红大月牙戟／镰形长兵器，金色刃缘与金色杆', mount=None, pet=None, asym='红色月牙刃方向保持一致', unknown='面部、背甲和兵器反面纹样不可见'),
    '009': dict(g='男性', age='成年', face='长脸、锐利侧目', hair='银白长发束起并覆白色毛领', beard='无清晰胡须', body='高挑健壮', costume='银白鳞甲、绿色袖衣、白色毛领、蓝紫腰带与箭囊', palette='银白、绿、蓝紫、金', weapon='紫色反曲弓、成组白羽箭与背负箭囊', mount='白色战马，金色额饰、红色缰绳与银金马具', pet=None, asym='弓、箭囊与佩挂侧不得镜像', unknown='马匹后躯、弓反面和甲具远侧不可见'),
    '010': dict(g='男性', age='成年', face='窄长脸、神情机警', hair='黑发藏于紫色软帽与后结内', beard='无清晰胡须', body='修长灵活', costume='黄色宽袖外袍、深红长裙裤、紫帽、黑靴、棕金腰带', palette='黄、深红、紫、棕、黑', weapon='腰挂短剑／匕首与手持竹筒状标志器具', mount=None, pet=None, asym='短剑鞘与竹筒持握侧保持一致', unknown='竹筒内部用途、短剑完整刃形和袍服背面不可见'),
    '011': dict(g='男性', age='青年', face='尖脸、浓眉、露齿笑', hair='白色长发高束并有金色头箍', beard='无胡须', body='精瘦灵活', costume='金黑轻甲、白色围巾与长袖、红色腰绳、绿色护腿', palette='金、黑、白、红、绿', weapon='成组短剑／飞刀与一柄长直剑，白银刃、深色握柄', mount=None, pet=None, asym='背负和腰挂短剑数量与位置保持一致', unknown='多把短剑的精确数量、收纳结构和背甲不可见'),
    '012': dict(g='男性', age='中年', face='方脸、浓眉、神情严厉', hair='黑发藏于深色高帽', beard='浓黑长须随风向侧面飘', body='高大厚实', costume='银灰札甲、紫色宽袖内袍、米黄裤、黑帽与护腕', palette='银灰、紫、米黄、黑', weapon='长杆枪／棍状兵器，木色杆身与被裁切头部', mount=None, pet=None, asym='长须流向不作为永久左右结构', unknown='兵器头部、背部甲带和鞋履被裁切或遮挡'),
    '013': dict(g='男性', age='中年', face='宽脸、怒目张口', hair='黑发极短或剃发', beard='浓黑络腮长须', body='极其魁梧、裸臂肌肉夸张', costume='红色披巾与短裙、黄色腰带、黑裤、白色绑腿和大念珠', palette='红、黄、黑、白、棕', weapon='长柄月牙铲／环形刃禅杖，金属月牙头与深色杆', mount=None, pet=None, asym='念珠与长柄兵器持握侧保持一致', unknown='兵器完整另一端、披巾背面与腰带背扣不可见'),
    '014': dict(g='男性', age='青年', face='窄长俊朗脸、浓眉锐目', hair='黑色长发高束并向后飘', beard='无胡须', body='高挑结实、动作敏捷', costume='亮蓝长袍、黑色宽裤、白色绑腿、蓝色披肩与大红念珠', palette='亮蓝、黑、白、红、金', weapon='大弧度单刃长刀，银白刃与金色圆护手', mount=None, pet=None, asym='刀鞘与大念珠位置保持一致', unknown='长刀反面、刀鞘固定方式与袍服背面不可见'),
    '015': dict(g='男性', age='成年', face='窄脸、神情专注', hair='黑发藏于绿色双角形头饰', beard='无清晰胡须', body='修长灵活', costume='红紫短袍、绿色大型弧形肩背构件、红色甲裙、蓝裤与黑靴', palette='绿、红、紫、蓝、黑', weapon='双头长枪，红杆两端均为蓝银枪头，并带大型绿色月牙护刃', mount=None, pet=None, asym='双头枪两端与绿色弧形构件结构保持一致', unknown='绿色弧形构件与身体连接、枪杆中段和背部被遮挡'),
    '016': dict(g='男性', age='青年', face='清秀方脸、浓眉、目光坚决', hair='黑发高束成马尾并有金色头带', beard='无胡须', body='健壮敏捷', costume='银色胸甲与鳞甲裙、金色包边、白色披肩、红腰带和银色护腿', palette='银白、金、红、黑', weapon=None, mount=None, pet=None, asym='拳击姿势不作为左右永久结构', unknown='背甲闭合、远侧肩甲和鞋后结构不可见'),
    '017': dict(g='男性', age='中年', face='长脸、浓眉、神情冷峻', hair='黑发与头顶被宽檐草帽和白色披巾遮挡', beard='黑色短髭与短须', body='高挑结实', costume='绿色上衣、黑色宽裤、白色大披巾、蓝色围巾与草帽', palette='绿、黑、白、蓝、棕', weapon='直身长剑，银白刃、金色柄首与白色剑鞘', mount=None, pet=None, asym='剑鞘与披巾垂落侧保持一致', unknown='草帽下发型、剑反面与披巾背部结构不可见'),
    '018': dict(g='男性', age='成年', face='清瘦方脸、目光锐利', hair='黑发藏于银金头盔与白色盔缨', beard='无清晰胡须', body='高挑健壮', costume='银金重甲、紫色披肩、红色甲绦与蓝紫护腿', palette='银、金、紫、红、白', weapon='银色长柄月牙戟，双侧弧刃与红色杆尾', mount='白色战马，金色面甲、银色胸甲与黑色缰具', pet=None, asym='月牙戟刃向与马具挂载保持一致', unknown='马匹远侧甲具、戟杆完整末端与人物背甲不可见'),
    '019': dict(g='男性', age='成年', face='侧脸清瘦、神情专注', hair='黑发藏于银盔和红色盔缨下', beard='无清晰胡须', body='高挑骑手体型', costume='棕银轻甲、白色披风、红色围巾、护臂与箭囊', palette='棕、银、白、红、黑', weapon='大弧度银白骑战刀，另有背负弓箭／箭囊', mount='灰白斑纹战马，黑鬃、紫鞍垫与金属马具', pet=None, asym='骑战刀、箭囊和鞍具侧位不得镜像', unknown='弓完整轮廓、马匹远侧斑纹和人物背部不可见'),
    '020': dict(g='男性', age='成年', face='瘦长脸、夸张笑容', hair='黑发被黑色高帽遮住', beard='细黑短髭与下巴短须', body='精瘦灵活', costume='黑色短袍与披肩、蓝色裤、红腰带、白色绑腿及写有红字的垂布', palette='黑、蓝、红、白', weapon='成组小型飞刀／投掷刃与腰挂短兵器', mount=None, pet=None, asym='飞刀收纳位置与红色垂布保持一致', unknown='投掷刃数量、帽后结构与背部收纳不可见'),
    '021': dict(g='男性', age='中年', face='宽脸、怒目露齿', hair='鲜红长乱发向后披散', beard='红色浓须沿下颌生长', body='极其魁梧、裸臂肌肉夸张', costume='米白无袖短衣、蓝紫宽裤、深色绑腿，手足多处裸露', palette='红、米白、蓝紫、银', weapon='巨型宽刃朴刀／砍刀，银白弧刃与长浅色柄', mount=None, pet=None, asym='大刀持握侧不镜像', unknown='大刀反面、背部衣料和鞋履结构不可见'),
    '022': dict(g='男性', age='中年', face='宽脸、怒目张口', hair='黑红蓬乱长发', beard='浓黑短须', body='极魁梧、上身肌肉裸露', costume='黑色大披风、红腰带、深色短裤与脚踝绑带', palette='黑、红、银、棕', weapon='一对巨型双刃战斧，并带连接腰身的金属锁链', mount=None, pet=None, asym='双斧与锁链连接侧保持一致', unknown='锁链完整长度、双斧反面和披风背部不可见'),
    '023': dict(g='男性', age='成年', face='方脸、浓眉、神情桀骜', hair='黑色中长发束于脑后', beard='无清晰胡须', body='精壮、上身裸露并有大面积纹身', costume='紫色宽裤、红腰带、白色绑腿与简洁护腕', palette='肤色、紫、红、白、棕', weapon='长木棍／哨棒，棕色杆身与简单包缠', mount=None, pet=None, asym='纹身位置和棍棒收纳侧不得镜像', unknown='背部纹身全貌、棍棒两端与腰带背结不可见'),
    '024': dict(g='男性', age='青年', face='清秀长脸、眉目温和', hair='黑发整齐高束并佩金色小冠', beard='无胡须', body='修长文雅', costume='翠绿色宽袖外袍、白色交领长衣、红腰带与白鞋', palette='翠绿、白、红、金', weapon=None, mount=None, pet=None, asym='手中金色小葫芦属于一次性标志动作', unknown='外袍背面纹样、袖后结构和鞋后不可见'),
    '025': dict(g='男性', age='中年', face='方脸、浓眉、神情严厉', hair='黑发藏于红黑头巾与头盔', beard='浓黑络腮长须', body='高大结实', costume='银灰胸甲、红披巾、米黄裤、黑靴与金属护腕', palette='银灰、红、米黄、黑', weapon='长柄单刃战刀，银白弧刃、金色护手与浅色杆', mount=None, pet=None, asym='战刀持握和红披巾垂落侧保持一致', unknown='战刀杆尾、背甲扣带与远侧护臂不可见'),
    '026': dict(g='男性', age='青年', face='长脸、目光冷峻', hair='绿色长发向后披落', beard='无胡须', body='高挑健壮', costume='白色无袖上衣、黄褐短裤、银色护臂与长靴', palette='白、黄褐、银、绿色', weapon='宽大弧形水色长刀／弯刃，半透明蓝白刃面', mount=None, pet=None, asym='长刀持握侧与绿色长发流向保持一致', unknown='刃部是否为实体或水效果、背部服装与鞋后不可见'),
    '027': dict(g='男性', age='成年', face='方脸、浓眉、神情凶悍', hair='绿色短发向上竖立', beard='无清晰胡须', body='极强壮、上身裸露', costume='紫色宽裤、红腰带、脚部赤裸', palette='绿、紫、红、银白', weapon='极长新月形弧刀／水月弯刃，银白宽刃与深色柄', mount=None, pet=None, asym='弧刃弯曲方向不得镜像', unknown='弯刃背面、柄尾和腰带背结不可见'),
    '028': dict(g='男性', age='成年', face='长方脸、浓眉、露齿笑', hair='黑发高束成短马尾', beard='无清晰胡须', body='强壮、上身裸露', costume='深灰宽裤、红色腰带、赤脚', palette='肤色、深灰、红、银', weapon='大型宽背单刃弯刀，银灰刃身与红黑握柄', mount=None, pet=None, asym='弯刀持握和腰带结侧保持一致', unknown='刀反面、刀鞘和背部服装不可见'),
    '029': dict(g='男性', age='成年', face='尖长脸、冷峻侧目', hair='红棕长发向后飞散', beard='无清晰胡须', body='精瘦结实、上身裸露', costume='紫色短裙裤、红棕金属护臂与赤足', palette='冷绿肤色、紫、红棕、银', weapon='前臂固定的三枚长钢爪，银灰刃与棕色护臂', mount=None, pet=None, asym='钢爪固定手臂不可跨视角翻转', unknown='钢爪收放结构、背部绑带和另一手装备不可见'),
    '030': dict(g='男性', age='青年', face='清秀长脸、神情平静', hair='黑色长发高束并向后飘', beard='无胡须', body='修长健壮', costume='白色宽袖交领长衣、黑腰带、深蓝绑腿与赤足', palette='白、深蓝、黑、银', weapon='一对细银链／水链状软兵器，双手分别操控', mount=None, pet=None, asym='双链长度和握点保持一致', unknown='软兵器末端、背部衣襟与鞋履设置不可见'),
    '031': dict(g='男性', age='成年', face='宽脸、浓眉、神情凶狠', hair='深蓝短发向上竖立', beard='无清晰胡须', body='极魁梧、上身裸露', costume='深紫短裤与简洁腕带，整体受蓝色水光照亮', palette='蓝、深紫、银白', weapon='一对短银刺／水下短刃，细长白银刃身', mount=None, pet=None, asym='双短刃数量保持为二', unknown='短刃完整柄形、实际肤色与背部结构受水光遮挡'),
    '032': dict(g='男性', age='中年', face='方脸、浓眉、神情严肃', hair='黑发藏于黑色高帽', beard='无清晰胡须', body='高大结实', costume='黑色大披风、红围巾、黄色领口、黑裤与黑靴', palette='黑、红、黄、银', weapon='巨型宽刃战斧，银灰方形斧头与深色长柄', mount=None, pet=None, asym='战斧持握和披风开口侧保持一致', unknown='战斧反面、披风背部与腰间固定不可见'),
    '033': dict(g='男性', age='青年', face='长脸、眉目凌厉、带轻笑', hair='黑色长发后束', beard='无胡须', body='精壮、上身裸露并有胸部伤痕', costume='黄色宽裤、绿色腰裙与腰带、蓝色护腕和绿色绑腿', palette='黄、绿、蓝、银、肤色', weapon='短柄弧刃匕首／短刀，银白刃与深色握柄', mount=None, pet=None, asym='胸部伤痕与匕首持握侧不得镜像', unknown='匕首反面、背部伤痕和腰裙闭合不可见'),
    '034': dict(g='男性', age='中年', face='宽脸、浓眉、神情凶猛', hair='黑发大部被虎头皮帽遮挡', beard='黑色短须', body='高大强壮', costume='完整虎皮披风与虎头帽、深色短衣、白色宽裤、金属护臂', palette='虎纹橙黑、白、棕、银', weapon='长柄钢叉／猎叉，以及弓与成组白羽箭', mount=None, pet=None, asym='虎皮纹样、箭囊和钢叉持握侧保持一致', unknown='虎皮背面纹样、钢叉完整叉头与弓的收纳关系不可见'),
    '035': dict(g='男性', age='成年', face='瘦长脸、神情专注', hair='黑发被灰色头巾遮住', beard='短黑髭与下巴短须', body='精瘦敏捷', costume='灰色短袍、深色裤、棕色护臂、灰头巾与绑腿', palette='灰、黑、棕、蓝绿', weapon='背负与腰挂的双短剑／双刀，蓝绿握柄与银色刃', mount=None, pet=None, asym='双刀鞘的背负和腰挂位置不得镜像', unknown='双刀完整刃形、背带连接和鞋履被攀爬动作遮挡'),
    '036': dict(g='男性', age='青年', face='清秀瓜子脸、眼神专注', hair='黑色长发高束并配红色长飘带', beard='无胡须', body='修长灵活', costume='紫蓝短袍、灰黑裤、白色护臂、红围巾与白羽箭囊', palette='紫蓝、灰黑、红、白、金', weapon='金红反曲弓、白羽箭与背负箭囊', mount=None, pet=None, asym='箭囊、弓持握和红飘带方向保持一致', unknown='弓反面、箭囊背带与袍服背部不可见'),
    '037': dict(g='男性', age='中年', face='长方脸、浓眉、神情深沉', hair='黑发短束并向后梳', beard='黑色短髭与尖短胡', body='高挑结实', costume='蓝色交领长袍、绿色无袖外褂、红白领缘、深色宽裤', palette='蓝、绿、红、白、黑', weapon='背负的双直剑，黑色剑鞘与银色柄首', mount=None, pet=None, asym='双剑背负角度和外褂开襟方向保持一致', unknown='双剑完整刃形、背带和外褂背面不可见'),
    '038': dict(g='男性', age='中年', face='方脸、浓眉、侧目警觉', hair='黑发被红色头巾与后飘巾尾遮住', beard='黑色短髭与短须', body='高大强壮', costume='红色长披巾、银灰轻甲、米灰宽裤、金属护胫与棕色长靴', palette='红、银灰、米灰、棕', weapon='长皮绳套索／软鞭与腰挂短剑组合装备', mount=None, pet=None, asym='绳圈持握与剑鞘侧位不得镜像', unknown='套索完整长度、短剑刃形和披巾背面不可见'),
    '039': dict(g='男性', age='中年', face='方脸、怒目张口', hair='黑发藏于黑红头盔', beard='浓黑长须', body='高大结实', costume='黑银甲、绿色胸腹袍、红黑头盔与黑披肩', palette='黑、银、绿、红、金', weapon='长柄银色枪／戟，红黑杆身与被裁切枪头', mount='浅棕战马，长银白鬃、黑色马具与绿色缨坠', pet=None, asym='长枪与马具侧位保持一致', unknown='枪头、马匹远侧马具和背甲被裁切'),
    '040': dict(g='男性', age='中年', face='宽脸、浓眉、露齿笑', hair='黑发藏于金色翼形头盔', beard='黑色短髭与短须', body='高大魁梧', costume='金色重甲、白色肩带、红披风、紫色裤裙与金护腿', palette='金、红、白、紫、黑', weapon='大弧度银白骑战刀，金色护手与深色握柄', mount='黑色战马，灰白鬃、金色额饰与黑金马具', pet=None, asym='骑战刀与披风开口侧保持一致', unknown='刀反面、马匹远侧马具和人物背甲不可见'),
    '041': dict(g='男性', age='成年', face='清瘦长脸、目光冷静', hair='黑发藏于银蓝头盔与白色盔缨', beard='无清晰胡须', body='高挑健壮', costume='银蓝札甲、青蓝大围巾、白色披肩与金色护腿', palette='银白、青蓝、深蓝、金', weapon='银色长枪，细长尖头与红色杆身', mount='白色战马，红色缰绳、红色胸穗与银蓝马具', pet=None, asym='枪、围巾垂落与马具挂载侧保持一致', unknown='枪尾、马匹远侧结构和背甲不可见'),
    '042': dict(g='男性', age='成年', face='方脸、浓眉、目光锐利', hair='黑发藏于银色盔与红黑盔缨', beard='无清晰胡须', body='高挑结实', costume='银金菱格甲、红披风、白色肩披、黑色护腿', palette='银、金、红、白、黑', weapon='长黑杆重兵器，尾端带链系铜色圆锤／流星锤', mount='赤棕战马，白色鼻梁、深色鬃与黑绿马具', pet=None, asym='链锤、长杆和披风方向不得镜像', unknown='长杆头部、链锤连接、马匹远侧马具被裁切'),
    '043': dict(g='男性', age='成年', face='长方脸、浓眉、神情专注', hair='黑发束于深色头巾内', beard='短黑髭', body='精壮敏捷', costume='红色胸衣、灰蓝袖袍、白披带、深色裤与金属护臂', palette='红、灰蓝、白、黑、银', weapon='长柄银色枪，宽三角枪头与深色木杆', mount=None, pet=None, asym='枪持握与白披带垂落侧保持一致', unknown='枪杆尾、背带和远侧护臂不可见'),
    '044': dict(g='男性', age='青年', face='清秀方脸、神情沉稳', hair='黑色卷发以蓝色头带束住', beard='无清晰胡须', body='高挑健壮', costume='深浅蓝交叠长袍、绿色袖口护具、绿色飘带与紫色球形配饰', palette='深蓝、浅蓝、绿、紫', weapon=None, mount=None, pet=None, asym='紫色球形配饰和绿色飘带位置保持一致', unknown='球形配饰用途、袍服背面和鞋履受水流遮挡'),
    '045': dict(g='男性', age='中年', face='宽脸、怒目露齿', hair='鲜红竖立长发', beard='红色短须', body='高大强壮', costume='红黄轻甲、黑色大围巾、红色裙裤、金色护肩与护腿', palette='红、黄、黑、金', weapon='成组黑红投掷飞刀／飞梭，带紫色尾穗与金珠', mount=None, pet=None, asym='飞刀数量、尾穗方向和收纳侧保持一致', unknown='投掷器具体数量、背部收纳结构与围巾背面不可见'),
    '046': dict(g='男性', age='青年', face='长脸、细眉、目光自信', hair='黑色长发半束发髻、两侧垂肩', beard='细黑短髭与小山羊胡', body='高挑精壮、胸腹裸露', costume='黄色宽袖短外袍、黄色宽裤、红腰带与红护腕', palette='黄、红、蓝灰、黑、白', weapon='巨型白毫笔杖、黑色笔匣与成组书写／投射笔具', mount=None, pet=None, asym='笔匣持握和腰带结侧保持一致', unknown='笔匣内部数量、巨笔背面纹饰与长袍背部不可见'),
    '047': dict(g='男性', age='成年', face='方长脸、浓眉、神情冷峻', hair='黑色长发高束并配蓝色发带', beard='无清晰胡须', body='高挑结实', costume='蓝色短袍、白色宽袖、深色裤与黑靴，胸前圆形黑色纹样', palette='蓝、白、黑、金', weapon='一对直身短剑／长剑，银白刃与金色护手', mount=None, pet=None, asym='双剑持握和胸前圆形纹样保持一致', unknown='剑鞘、双剑长度差和袍服背部不可见'),
    '048': dict(g='男性', age='中年', face='宽脸、浓眉、神情傲然', hair='黑发高束成短髻', beard='黑色短髭与下巴短须', body='极高大魁梧、肩臂肌肉夸张', costume='绿色无袖战袍、银色长甲裙、白色毛边护肩、红黑腰甲与白靴', palette='绿、银白、红、黑', weapon=None, mount=None, pet=None, asym='白毛边和甲裙分片保持近似对称', unknown='背甲闭合、远侧肩部和鞋后结构不可见'),
    '049': dict(g='男性', age='中年', face='方脸、浓眉、张口怒吼', hair='黑发藏于红黑头盔', beard='黑色短髭与络腮短须', body='高大强壮、裸臂', costume='绿色大披风、红色短甲、蓝色破损裤、银色护臂与护腿', palette='绿、红、蓝、银、黑', weapon='超长银杆枪／钩枪，长直杆与金属尖头；腰挂短剑', mount=None, pet=None, asym='长枪持握、披风开口和剑鞘侧位保持一致', unknown='枪头完整轮廓、披风背面与腰挂结构不可见'),
    '050': dict(g='男性', age='中年', face='宽脸、浓眉、神情沉着', hair='黑发梳成两侧短角髻', beard='浓黑络腮短须', body='极魁梧、胸腹裸露', costume='红色宽裤与腰布、黑靴、黑色铆钉腕甲与腰带', palette='红、黑、银、肤色', weapon='短柄弯刀，狭长金黄刃与红黑握柄', mount=None, pet=None, asym='弯刀佩挂侧与双角髻保持一致', unknown='刀鞘、背部腰带和裤装背结不可见'),
    '051': dict(g='男性', age='中年', face='方脸、浓眉、侧目警觉', hair='红褐短发以红头巾束住', beard='红褐短髭与短须', body='高大结实', costume='绿色长袍、黄色袖衣、银色甲片、红披巾与护腿', palette='绿、黄、红、银', weapon='长柄银色枪／戟，宽大钩形枪头与深色杆', mount=None, pet=None, asym='长枪、披巾和袍摆流向保持一致', unknown='枪尾、背甲和远侧鞋履受动作遮挡'),
    '052': dict(g='男性', age='青年', face='方脸、浓眉、神情阴沉', hair='黑色短发分成两束向侧后翘起', beard='无胡须', body='强壮、胸腹裸露', costume='黑紫条纹宽袖外袍、黄色宽裤、红腰带与胸前圆形布章', palette='黑、紫、黄、红、橙火光', weapon='黑色长杆火把／燃烧棍，顶部包裹黄色火焰状材料', mount=None, pet=None, asym='燃烧棍持握侧和胸前布章位置保持一致', unknown='燃烧头内部结构、背部布章与袍服闭合不可见'),
    '053': dict(g='男性', age='成年', face='长脸、眉眼机灵、面带笑意', hair='黑发被绿色头巾包裹', beard='细黑上髭与尖短胡', body='修长灵活', costume='绿色内袍、紫色铜钱纹外袍、粉色腰袋、米白宽裤与黑靴', palette='绿、紫、粉、米白、金', weapon='大型木框算盘与账册组成的标志装备', mount=None, pet=None, asym='算盘、账册和腰袋侧位保持一致', unknown='算盘背面、腰袋内部与外袍背面纹样不可见'),
    '054': dict(g='男性', age='成年', face='方脸、浓眉、神情冷峻', hair='黑发束于金色冠饰下', beard='无清晰胡须', body='高挑健壮、骑手体型', costume='橙棕战袍、金黑轻甲、白色披带、金色护臂与护腿', palette='橙棕、金、黑、白', weapon='弓与箭囊／成组箭矢，背后另有黑白旗形装备', mount='深棕战马，黑鬃、金色额饰与金橙马具', pet=None, asym='弓箭、旗形装备和马具挂载侧保持一致', unknown='弓完整轮廓、旗杆连接、马匹远侧马具不可见'),
    '055': dict(g='男性', age='成年', face='方脸、浓眉、怒目', hair='红棕短发束于银盔下', beard='无清晰胡须', body='高大健壮', costume='银白重甲、白色大披风、紫红腰带与银色护腿', palette='银白、紫红、黑', weapon='银色长枪／骑枪，枪头被动作光影部分遮挡', mount='白色战马，银色重甲、白鬃与紫红马具', pet=None, asym='骑枪、披风和马甲侧位保持一致', unknown='枪头、马匹后躯甲具与人物背甲受光影遮挡'),
    '056': dict(g='男性', age='老年', face='瘦长脸、眉眼和善', hair='灰黑头发藏于深色软帽', beard='灰黑细髭与短山羊胡', body='清瘦矮小', costume='橄榄绿长袍、深色宽裤、红腰带与布鞋', palette='橄榄绿、深灰、红、棕', weapon=None, mount=None, pet=None, asym='手中酒壶属于小型一次性道具', unknown='帽后发型、长袍背面闭合与鞋后不可见'),
    '057': dict(g='男性', age='中老年', face='长方脸、浓眉、神情专注', hair='紫色长发高束并向后飘', beard='紫色长髭与及胸长须', body='高挑结实', costume='浅绿色宽袖长袍、深红大披肩与红腰带', palette='浅绿、深红、紫、金棕', weapon='大型金棕双联葫芦状标志器具', mount=None, pet=None, asym='葫芦持握和披肩开口侧保持一致', unknown='葫芦用途、背面结构与长袍闭合不可见'),
    '058': dict(g='男性', age='成年', face='宽脸、浓眉、露齿笑', hair='黑发高束并用红头带固定', beard='无清晰胡须', body='极强壮、裸臂', costume='黑灰轻甲、黄褐短裤、红头带与红飘带、黑色护腿', palette='黑灰、黄褐、红、金', weapon='长金色棍棒，杆身分布均匀圆形铆钉／凸点', mount=None, pet=None, asym='棍棒和红飘带方向保持一致', unknown='棍棒两端、背甲和腰带背结不可见'),
    '059': dict(g='女性', age='青年', face='瓜子脸、细眉、神情沉静', hair='黑色长发藏于金色珠花头盔与红披巾内', beard='无胡须', body='修长健美、骑手体型', costume='红紫金女式札甲、红披风、紫色裙甲与金色护臂', palette='红、紫、金、白、粉', weapon='细长银色佩剑与背负弓箭／箭囊', mount='红棕战马，白色长鬃、金红鞍具与花纹鞍垫', pet=None, asym='佩剑、弓箭和披风侧位不得镜像', unknown='佩剑刃形、马匹远侧鞍具和背甲不可见'),
    '060': dict(g='男性', age='中年', face='宽脸、浓眉、怒目', hair='银白长发与长鬃状发束向后飘', beard='银白浓短须', body='极高大强壮、裸臂', costume='白色短袍、黑白腰甲、白色护腿与蓝黑腰带', palette='白、银、黑、蓝', weapon='超长直身银剑，蓝绿握柄与简单护手', mount=None, pet=None, asym='长剑持握和发束流向保持一致', unknown='长剑反面、剑鞘与背部腰甲不可见'),
    '061': dict(g='男性', age='成年', face='长脸、浓眉、露齿笑', hair='黑色长发披散并向后飘', beard='黑色短髭与尖短胡', body='高挑结实', costume='黑灰短袍、白色宽裤、银色护臂与深色长靴', palette='黑灰、白、银、金', weapon='长金属锁链软鞭，末端为短柄／钩形连接件', mount=None, pet=None, asym='锁链握点与腰间收纳侧保持一致', unknown='锁链完整末端、背部收纳与袍服背面不可见'),
    '062': dict(g='男性', age='成年', face='方脸、浓眉、露齿笑', hair='黑发高束马尾并配白头带', beard='无清晰胡须', body='高大健壮', costume='黑银鳞甲、灰蓝宽裤、绿色腰裙、白头带与绿色绑腿', palette='黑、银、灰蓝、绿、白', weapon='短金色柄链锤，黑链连接银黑多刺流星锤', mount=None, pet=None, asym='链锤持握和腰裙开口侧保持一致', unknown='链长、锤头反面和背甲绑带不可见'),
    '063': dict(g='男性', age='成年', face='方脸、浓眉、神情严厉', hair='黑发藏于白头巾与发带下', beard='黑色短髭', body='高挑结实', costume='红色胸衣、白色宽袖披袍、白色宽裤、黑色甲裙与红护腕', palette='红、白、黑、银', weapon='直身长剑，红黑握柄、银色剑刃与简单护手', mount=None, pet=None, asym='长剑持握与白披袍垂落侧保持一致', unknown='剑鞘、剑反面和披袍背部不可见'),
    '064': dict(g='男性', age='成年', face='方脸、浓眉、神情严肃', hair='浅色短发被金色额箍固定', beard='无清晰胡须', body='高大结实', costume='银金轻甲、绿色战裙、红黑护肩、金色护腿', palette='银、金、绿、红、黑', weapon='银色长枪、金色圆盾与背负成组短枪／投枪', mount=None, pet=None, asym='圆盾、投枪背架和长枪侧位不得镜像', unknown='投枪数量、圆盾背面与背架连接不可见'),
    '065': dict(g='男性', age='成年', face='面部大部被蓝色蒙面巾遮挡、目光锐利', hair='头发完全藏于蓝色头巾', beard='胡须不可见', body='高挑健壮', costume='深浅蓝甲衣、蓝色大围巾、黑色圆盾、棕色护腿与箭囊式背架', palette='深蓝、浅蓝、黑、棕、银', weapon='银色长枪、黑色圆盾与背负成组投枪／短矛', mount=None, pet=None, asym='圆盾、长枪和背架侧位保持一致', unknown='蒙面下容貌、圆盾背面和投枪连接结构不可见'),
    '066': dict(g='男性', age='中年', face='宽脸、浓眉、露齿笑', hair='头顶半秃并束小发髻', beard='黑色短髭与两侧短须', body='极魁梧、裸背肌肉夸张', costume='米色单肩布、橄榄绿短裤、厚布护腕护腿与工具腰架', palette='米色、橄榄绿、棕、银', weapon='双头铁锤、手持钢錾／短凿与腰挂成组小工具', mount=None, pet=None, asym='工具腰架、铁锤和凿子侧位保持一致', unknown='工具数量、腰架背面与单肩布闭合不可见'),
    '067': dict(g='男性', age='青年', face='长脸、眉目专注', hair='黑色长发高束并向后飘', beard='无胡须', body='修长健壮', costume='紫蓝宽袖短袍、黑色宽裤、红腰带与黑靴', palette='紫蓝、黑、红、银', weapon='银色横笛与腰挂直剑／长剑组合装备', mount=None, pet=None, asym='横笛持握与剑鞘佩挂侧保持一致', unknown='长剑刃形、横笛背面孔位和袍服背面不可见'),
    '068': dict(g='男性', age='青年', face='长方脸、浓眉、神情自信', hair='深蓝黑长发高扬向后', beard='无清晰胡须', body='极强壮、胸腹裸露', costume='仅着蓝紫短裤、金属腰带与深色护腕，赤足', palette='肤色、蓝紫、银、红', weapon='大弧度宽刃弯刀，银色刃、深色握柄与红色护手', mount=None, pet=None, asym='弯刀持握与腰带装饰侧保持一致', unknown='刀鞘、刀反面和腰带背扣不可见'),
    '069': dict(g='男性', age='成年', face='圆宽脸、双目夸张、神情滑稽', hair='头发被绿色头巾／水帽遮挡', beard='无清晰胡须', body='矮壮灵活', costume='蓝色短裤、棕红腰带与绿色头饰，四肢裸露', palette='冷绿色肤色、蓝、棕红', weapon=None, mount=None, pet=None, asym='倒立动作不作为左右永久结构', unknown='真实肤色、头饰结构、背部和鞋履均被水下动作影响'),
    '070': dict(g='男性', age='青年', face='方脸、浓眉、神情凶悍', hair='红黑中长乱发', beard='无清晰胡须', body='精壮、上身裸露', costume='黄色宽裤、绿色腰布、黄绿绑腿与简洁护腕', palette='黄、绿、红黑、银', weapon='大型双刃飞斧／月牙斧，银色双刃与短深色柄', mount=None, pet=None, asym='飞斧弧刃方向与腰布结侧保持一致', unknown='飞斧反面、背部衣料和是否另有收纳不可见'),
    '071': dict(g='男性', age='青年', face='清秀长脸、目光专注', hair='黑色长发披散并向后飘', beard='无胡须', body='修长灵活', costume='浅青宽袖长袍、白色内衣、红腰带与白色鞋裤', palette='浅青、白、红、黑', weapon='成组红线牵引的细针／飞索暗器，双手操控多根细线', mount=None, pet=None, asym='飞索线束的手部连接和腰带结侧保持一致', unknown='暗器数量、线束收纳和袍服背面不可见'),
    '073': dict(g='男性', age='中年', face='宽脸、浓眉、露齿笑', hair='黑发高束短髻', beard='黑色短髭与下巴短须', body='高大结实', costume='银灰鳞甲、绿色围巾、白色宽裤、紫腰带与绿色绑腿', palette='银灰、绿、白、紫、棕', weapon='木色短杖／棍与银色链鞭／软索组合装备', mount=None, pet=None, asym='短杖、链鞭和腰挂鞘侧位保持一致', unknown='链鞭末端、短杖用途和背甲结构不可见'),
    '074': dict(g='男性', age='青年', face='窄长脸、眉目冷峻', hair='橙棕长发披肩并配红色额带', beard='无清晰胡须', body='高挑修长', costume='黑色短袍与披肩、紫色内衣、金色腰带、黑裤与黑靴', palette='黑、紫、金、橙棕', weapon='背负直剑／长刀，金色柄首与深色剑鞘', mount=None, pet=None, asym='剑鞘背负和披肩开口侧保持一致', unknown='刃形、背带连接和袍服背面被黑色剪影遮挡'),
    '075': dict(g='男性', age='成年', face='宽脸、浓眉、露齿笑', hair='绿色短发向上竖立', beard='无清晰胡须', body='极魁梧、胸背肌肉裸露', costume='灰褐短裤、蓝腰带、蓝色护腕与赤足', palette='灰褐、蓝、绿、银白', weapon='巨型方头铁锹／铲形重兵器，银白方刃与长木柄', mount=None, pet=None, asym='巨铲持握和腰带结侧保持一致', unknown='铲背面、木柄尾端和背部衣料不可见'),
    '076': dict(g='男性', age='青年', face='清秀长脸、眉目沉静', hair='黑发藏于亮蓝方巾帽与后飘巾尾', beard='无胡须', body='修长灵活', costume='亮蓝宽袖长袍、白色宽裤、蓝帽与白鞋', palette='亮蓝、白、银灰', weapon='一对白色折扇／铁扇，展开扇面与蓝色握柄', mount=None, pet=None, asym='双扇数量和持握方向保持一致', unknown='折扇闭合结构、帽后发型和袍服背面不可见'),
    '077': dict(g='男性', age='成年', face='长方脸、浓眉、侧脸专注', hair='黑发藏于黑色方帽', beard='无清晰胡须', body='高大强壮、裸臂', costume='黑色无袖长袍、红色宽腰带、红色长裙摆与金边袖口', palette='黑、红、金、肤色', weapon='红棕横笛／长笛标志器具，细长圆管与深色孔位', mount=None, pet=None, asym='横笛持握与红裙摆开口侧保持一致', unknown='笛孔背面、方帽后部和长袍背面不可见'),
    '078': dict(g='男性', age='成年', face='长脸、浓眉、神情警觉', hair='黑发被橄榄绿兜帽和头巾遮挡', beard='黑色短髭与短须', body='高挑结实', costume='橄榄绿兜帽披肩、紫色宽裤、棕色护臂护腿与黑鞋', palette='橄榄绿、紫、棕、黑', weapon='背负弯刀／短剑，金色柄首与深色弯鞘', mount=None, pet=None, asym='弯刀背负、披肩开口和护臂绑带侧位保持一致', unknown='弯刀刃形、兜帽下发型和披肩背部不可见'),
    '079': dict(g='男性', age='中年', face='宽脸、仰头怒吼', hair='黑发向后披散', beard='黑色短髭与络腮短须', body='高大强壮', costume='灰白短甲、紫色宽裤、金黑护腿、绿色腰布与红腰带', palette='灰白、紫、金黑、绿、红', weapon='单手直剑／短刀，银色刃与深色柄；身体另中多支箭', mount=None, pet=None, asym='剑持握与箭伤分布不得镜像', unknown='剑反面、箭支来源和背甲闭合不可见'),
    '080': dict(g='男性', age='青年', face='方脸、浓眉、神情专注', hair='黑发高束成短髻', beard='无清晰胡须', body='极强壮、胸腹裸露', costume='绿色宽裤、白色短披带、红腰绳与黑靴', palette='绿、白、红、黑、银', weapon='超长双头枪／长矛，银色枪头、白色缨与蓝灰杆身', mount=None, pet=None, asym='双头枪两端结构和腰绳结侧保持一致', unknown='枪杆中部、远端枪头和背部披带不可见'),
    '081': dict(g='男性', age='中年', face='宽脸、浓眉、神情凶狠', hair='黑发剃短并束小顶髻', beard='黑色短髭与下巴短须', body='极魁梧、胸腹裸露', costume='蓝色宽裤、红腰带、黑色长靴与简洁护腕', palette='蓝、红、黑、银白', weapon='大型屠刀／宽刃砍刀，银白弧刃与浅色长柄', mount=None, pet=None, asym='屠刀持握和腰带结侧保持一致', unknown='刀反面、刀鞘和背部裤腰闭合不可见'),
    '082': dict(g='男性', age='中年', face='长方脸、浓眉、神情冷静', hair='深蓝黑长发高束并向后飘', beard='黑色细髭与尖短胡', body='高挑结实', costume='米白黑边长袍、红色腰裙与披带、金色护腿、黑色宽裤', palette='米白、黑、红、金、银', weapon='一对长直剑／弯剑，银白刃、黑色握柄与背负剑鞘', mount=None, pet=None, asym='双剑持握与背负鞘位不得镜像', unknown='双剑长度差、剑鞘固定与长袍背面不可见'),
    '083': dict(g='男性', age='成年', face='宽脸、浓眉、露齿笑', hair='黑发藏于绿色头巾', beard='无清晰胡须', body='极强壮、胸腹裸露', costume='黑银胸甲、绿色宽裤、黑色甲裙、绿色头巾与黑靴', palette='黑、银、绿、金', weapon='超长黑银杆枪／棍，细长金属杆与被裁切端头', mount=None, pet=None, asym='长杆持握和甲裙开口侧保持一致', unknown='长杆两端、背甲和头巾后结不可见'),
    '084': dict(g='男性', age='成年', face='面部被红色蒙面巾遮挡、眼神锐利', hair='头发完全藏于红色头巾和披巾', beard='胡须不可见', body='高挑敏捷', costume='红色蒙面头巾、红黑宽袍、金色腰带与黑色护臂', palette='红、黑、金、银蓝', weapon='一对巨大银蓝弧形短斧／翼形双刃，短柄与宽刃', mount=None, pet=None, asym='双刃数量和持握方向保持一致', unknown='蒙面下容貌、双刃反面和披巾背部不可见'),
    '085': dict(g='男性', age='中老年', face='清瘦长脸、眉目沉静', hair='灰黑头发藏于灰色高帽', beard='无胡须', body='修长文士体型', costume='紫灰宽袖长袍、黑色胸带、绿色宽裤与灰色高帽', palette='紫灰、黑、绿、白', weapon=None, mount=None, pet=None, asym='双手结印属于动作，不作为永久左右结构', unknown='帽后发型、长袍背面与腰带闭合不可见'),
    '086': dict(g='男性', age='成年', face='方脸、浓眉、神情警觉', hair='黑发被青绿色头巾遮挡', beard='黑色短髭与短须', body='精壮、上身裸露', costume='青绿色宽裤与头巾、黑色护腕、黑鞋，腰边散落铜钱', palette='青绿、黑、金铜、肤色', weapon=None, mount=None, pet=None, asym='背景兵器架不归入角色装备', unknown='人物是否拥有背景长兵器、裤装背结与鞋后不可见'),
    '087': dict(g='男性', age='青年', face='清秀瓜子脸、细眉、神情自信', hair='黑发高束并配紫红大蝴蝶结／头巾', beard='无胡须', body='高挑健壮、裸臂', costume='紫红大披巾与胸花、红腰带、浅蓝宽裤、金色首饰', palette='紫红、浅蓝、金、白', weapon=None, mount=None, pet=None, asym='胸花、披巾结与首饰侧位保持一致', unknown='披巾背面、发结固定与鞋履被裁切'),
    '088': dict(g='男性', age='中年', face='方脸、粗眉、神情严厉', hair='短金棕发向上竖立', beard='金棕短须', body='极魁梧、裸臂并有烧灼斑痕', costume='绿色工匠围裙、黄色宽裤、绿色厚手套与黑色护腕', palette='绿、黄、黑、金棕、银', weapon='铁匠钳、锻锤与正在锻造的长刀胚组合工具', mount=None, pet=None, asym='钳、锤和围裙系带位置保持一致', unknown='工具完整数量、围裙背带和刀胚最终形制不可见'),
    '089': dict(g='男性', age='青年', face='尖脸、眉目夸张、露齿大笑', hair='浅绿色超长直发披肩', beard='无胡须', body='修长', costume='深红紫宽袖长袍、白色大型软帽／披巾与黑色内衣', palette='浅绿、深红紫、白、黑', weapon=None, mount=None, pet=None, asym='白色大型软帽和红袍开口侧保持一致', unknown='软帽完整形状、长发背面层次和袍服下装被裁切'),
    '090': dict(g='男性', age='成年', face='面部仰起、轮廓方正', hair='银灰长发向后披散', beard='无清晰胡须', body='极强壮、胸腹裸露', costume='青蓝宽裤与交叉胸带、简洁腕带，赤足', palette='青蓝、银灰、黑、肤色', weapon=None, mount=None, pet=None, asym='交叉胸带按原图方向保持一致', unknown='正面五官、背带连接、腰带背结和鞋履设置不可见'),
    '091': dict(g='男性', age='青年', face='方脸、浓眉、神情凶猛', hair='银蓝乱发向后飘', beard='无清晰胡须', body='极强壮、裸臂', costume='黑蓝无袖短衣、绿色宽裤、金色腰带与黑靴', palette='银蓝、黑蓝、绿、金', weapon=None, mount=None, pet=None, asym='奔跑姿势不作为左右永久结构', unknown='短衣背面、腰带背扣和远侧鞋履被动作遮挡'),
    '092': dict(g='男性', age='青年', face='长脸、眉目自信', hair='黑发藏于绿色头巾与帽尾', beard='无清晰胡须', body='高挑结实', costume='绿色短袍与头巾、白色披肩和宽裤、黑色护腿', palette='绿、白、黑、红', weapon='红黑小型弩／折叠弓弩与腰挂短刀', mount=None, pet=None, asym='弩、短刀鞘和披肩侧位保持一致', unknown='弩机内部结构、短刀刃形与背部收纳不可见'),
    '093': dict(g='女性', age='中老年', face='圆脸、细眉、笑容温和', hair='深蓝头发以蓝色头巾整齐包住', beard='无胡须', body='矮胖圆润', costume='深浅蓝长袍、白色交领与围裙式前襟、黑色布鞋', palette='蓝、白、黑、棕红', weapon=None, mount=None, pet=None, asym='背景酒坛不作为独立角色装备', unknown='头巾后结、长袍背面与围裙闭合不可见'),
    '094': dict(g='男性', age='成年', face='方脸、浓眉、神情凶狠', hair='黑发剃短并束小顶髻', beard='无清晰胡须', body='极强壮、胸腹裸露', costume='红色宽裤与腰带、白色绑腿、银色护腕', palette='红、白、银、黑', weapon='巨型宽刃弯刀／斩刀，银色刀身、黑红柄与红色环状柄首', mount=None, pet=None, asym='大刀持握与腰带结侧保持一致', unknown='刀反面、刀鞘与背部裤装不可见'),
    '095': dict(g='男性', age='中年', face='面部部分被红头巾遮挡、目光凶狠', hair='黑发藏于红色头巾', beard='黑色短须', body='极魁梧、裸臂', costume='全红宽袍与裤装、粗麻腰绳、红头巾和黑鞋', palette='红、银、麻色、黑', weapon='巨型长柄宽刃鬼头刀／锯齿大刀，银刃带孔纹与短锯齿', mount=None, pet=None, asym='大刀刃向和麻绳结侧保持一致', unknown='刀反面孔纹、柄尾和红袍背面不可见'),
    '096': dict(g='男性', age='老年', face='长脸、深皱纹、神情豪放', hair='灰白长发与红棕头巾混合披散', beard='浓密灰白长髭与及胸长须', body='高挑结实', costume='浅蓝宽袖上衣、棕色短裙裤、蓝色护腿与白布袜', palette='浅蓝、棕、红棕、白、灰', weapon='大型木制船桨／宽头棍棒，棕色长柄与宽扁桨面', mount=None, pet=None, asym='船桨持握和头巾垂落侧保持一致', unknown='桨面反面纹样、背部衣料和手中小物用途不可见'),
    '097': dict(g='女性', age='青年', face='瓜子脸、细眉、目光凌厉', hair='红棕长发高束并配蓝色头巾', beard='无胡须', body='修长健美', costume='亮蓝短袍与披巾、黑色裤、白色绑腿、银色护臂', palette='亮蓝、黑、白、银、红棕', weapon='银色弧刃长刀与一根长枪／棍状副武器', mount=None, pet=None, asym='长刀、长杆和披巾开口侧保持一致', unknown='长杆两端、刀鞘和背部收纳不可见'),
    '098': dict(g='男性', age='成年', face='宽脸、浓眉、神情专注', hair='黑发藏于高耸黑色软帽', beard='无清晰胡须', body='极矮壮、四肢肌肉夸张', costume='仅着浅蓝腰布与黑色高帽，赤足裸身', palette='肤色、浅蓝、黑', weapon=None, mount=None, pet=None, asym='蹲伏姿势不作为左右永久结构', unknown='帽后结构、腰布背结与直立身材比例不可见'),
    '099': dict(g='男性', age='成年', face='面部大部处于阴影、轮廓方正', hair='银白短发露于黑色蒙面巾上方', beard='胡须不可见', body='高挑敏捷', costume='全黑紧身短袍、黑色蒙面巾、黑色护腕与绑腿', palette='黑、银白、银灰', weapon='一对弧形短刀／忍刀，银白单刃与黑色握柄', mount=None, pet=None, asym='双刀数量与腰间收纳侧保持一致', unknown='阴影下面容、刀鞘和背部绑带不可见'),
    '100': dict(g='男性', age='中年', face='方脸、浓眉、神情警觉', hair='黑发被黑色皮帽与灰围巾遮挡', beard='黑色短髭与短须', body='高大结实', costume='黑灰皮帽、灰黑披肩、蓝色围巾、棕色圆点护腿甲与黄色长靴', palette='灰黑、蓝、棕、黄、金', weapon='一对金黑短棍／双节短杖，另有腰背长刀鞘', mount=None, pet=None, asym='双短杖与背负刀鞘侧位保持一致', unknown='长刀刃形、短杖端头和披肩背部不可见'),
    '101': dict(g='女性', age='中年', face='圆宽脸、细眉、神情强势', hair='黑发盘成高髻并佩粉紫珠花', beard='无胡须', body='高大丰腴、肩臂结实', costume='亮粉无袖上衣、紫绿领缘、浅蓝宽裙裤、红腰绳与粉色布鞋', palette='亮粉、浅蓝、紫、绿、红、金', weapon=None, mount=None, pet=None, asym='珠花、腰绳与裙边花饰位置保持一致', unknown='发髻背面、裙裤后部与鞋后结构不可见'),
    '102': dict(g='男性', age='成年', face='方脸、浓眉、面带笑意', hair='黑色短发', beard='无清晰胡须', body='强壮、上身裸露', costume='浅蓝宽裤、紫腰带、黄色布鞋与简洁护腕', palette='浅蓝、紫、黄、棕、银', weapon='超长木柄鹤嘴锄／尖头矿镐，银色弯尖头与棕木杆', mount=None, pet=None, asym='长镐靠肩与腰带结侧保持一致', unknown='镐头反面、杆尾和裤装背结不可见'),
    '103': dict(g='女性', age='青年', face='瓜子脸、细眉、目光凌厉', hair='黑色长发高束并配紫色发带', beard='无胡须', body='修长敏捷', costume='浅蓝宽袖长衣、深蓝裤、紫红腰带与白色腰布', palette='浅蓝、深蓝、紫红、银', weapon='一对小型弧刃短刀与成组星形飞镖／手里剑', mount=None, pet=None, asym='双短刀、飞镖和腰带飘带侧位保持一致', unknown='飞镖数量、短刀收纳和长衣背面不可见'),
    '104': dict(g='男性', age='青年', face='长方脸、浓眉、露齿笑', hair='红棕短发向上竖立', beard='无清晰胡须', body='高挑健壮、裸臂', costume='浅青无袖短衣与宽裤、黑色护腿、蓝色腰带', palette='浅青、黑、蓝、红棕、银', weapon='小型短匕首／金属短棒，银色尖头与深色握柄', mount=None, pet=None, asym='短兵器持握与腰带结侧保持一致', unknown='短兵器用途、背部衣料和远侧鞋履受残影遮挡'),
    '105': dict(g='男性', age='成年', face='方长脸、浓眉、神情严肃', hair='黑发高束并佩金色额冠', beard='无清晰胡须', body='高大健壮', costume='金色重甲、红色大披风、红裙甲、金护腿与白色内衣', palette='金、红、白、黑、银', weapon='银色佩刀与超高红黑军旗／长柄旗杆组合装备', mount=None, pet=None, asym='军旗、佩刀和披风开口侧保持一致', unknown='旗杆尾端、旗背文字纹样和背甲不可见'),
    '106': dict(g='男性', age='中年', face='窄长苍白脸、深眼窝、神情狡黠', hair='黑发完全被破旧草帽与紫色头巾遮挡', beard='黑色细髭与尖短胡', body='清瘦、四肢修长', costume='破旧白灰披布、浅绿内衣、黑色短裤、紫腰带与赤足', palette='白灰、浅绿、黑、紫、棕红', weapon=None, mount=None, pet=None, asym='手中纸包与木桶属于工作动作，不强制拆表', unknown='草帽下发型、披布背面与纸包内物质不可见'),
    '107': dict(g='男性', age='成年', face='面部完全被绿色蒙面巾遮挡', hair='头发完全被绿色头巾遮挡', beard='胡须不可见', body='精瘦敏捷', costume='深绿色蒙面紧身衣、蓝色护腕绑腿、棕黄色大包袱与赤足', palette='深绿、蓝、棕黄、黑', weapon=None, mount=None, pet=None, asym='大包袱背负和绑带侧位保持一致', unknown='蒙面下身份特征、包袱内部与背部固定方式不可见'),
}


def entity(presence: str, item: str | None, kind: str) -> dict:
    if presence == 'present':
        return {
            'presence': 'present',
            'items': [item],
            'notes': [
                f'按可独立建模、拿取或动画化的{kind}拆分独立设定表。',
                '只保留原图可见轮廓、配色、材质、握持或连接关系；不可见反面作最简补全。',
            ],
        }
    return {'presence': 'absent', 'items': [], 'notes': [f'原图未见需要独立拆分的{kind}。']}


def build_spec(identifier: str, d: dict) -> dict:
    confirmed = [
        f"身份与外形：{d['face']}；{d['hair']}；{d['beard']}；{d['body']}。",
        f"服装：{d['costume']}。",
        f"主配色：{d['palette']}。",
    ]
    if d['weapon']:
        confirmed.append(f"武器或标志装备：{d['weapon']}。")
    if d['mount']:
        confirmed.append(f"坐骑：{d['mount']}。")
    if d['pet']:
        confirmed.append(f"宠物：{d['pet']}。")

    inferred = [
        '人物背部服装按正侧面同材质、同层级连续闭合，不新增徽章、纹样或第二套配件。',
        '被动作遮挡的左右肢体、鞋履和服装侧缝采用最克制、近似对称且易修改的补全。',
    ]
    if d['weapon']:
        inferred.append('武器或标志装备的反面、薄侧面与被裁切末端采用无额外装饰的结构性补全。')
    if d['mount']:
        inferred.append('坐骑远侧四肢、尾部和被遮挡马具按可见体型与同类连接关系自然补全。')

    unknown = [d['unknown'], '原图未展示的背面精确扣合、内层闭合、远侧细节与所有隐藏连接方式仍为未知。']

    must = [d['face'], d['hair'], d['body'], d['costume'], d['palette']]
    if d['weapon']:
        must.append(d['weapon'])
    if d['mount']:
        must.append(d['mount'])

    return {
        'schema_version': 1,
        'id': identifier,
        'name': '',
        'source': str(ROOT / f'{identifier}.png'),
        'status': 'spec-ready',
        'evidence': {'confirmed': confirmed, 'inferred': inferred, 'unknown': unknown},
        'character': {
            'identity': {
                'gender_presentation': d['g'],
                'apparent_age': d['age'],
                'face': d['face'],
                'hair': d['hair'],
                'facial_hair': d['beard'],
                'body_type': d['body'],
                'body_proportions': '保持原图人物独有的高矮、胖瘦和头身比例，不为批量整齐而统一体型',
            },
            'costume_layers': [part.strip() for part in d['costume'].split('、')],
            'palette': [part.strip() for part in d['palette'].split('、')],
            'materials': ['织物按原图褶皱与厚薄表现', '金属、皮革、毛皮或木材仅在原图可见时保留相应质感'],
            'patterns_and_symbols': ['只保留原图清楚可见的纹样、甲片分格和装饰位置，不生成文字或新徽记'],
            'left_right_asymmetry': [d['asym']],
            'must_preserve': must,
        },
        'entities': {
            'weapon': entity('present' if d['weapon'] else 'absent', d['weapon'], '武器或标志装备'),
            'mount': entity('present' if d['mount'] else 'absent', d['mount'], '坐骑'),
            'pet': entity('present' if d['pet'] else 'absent', d['pet'], '宠物'),
        },
        'generation': {
            'views': ['front', 'front-three-quarter', 'side', 'back-three-quarter', 'back'],
            'pose': 'neutral model-sheet pose with arms slightly separated',
            'background': 'plain warm light gray neutral',
            'notes': [
                '沿用 001、072、108 已批准基准的暖浅灰画布、强黑墨线、1990 年代手绘赛璐璐与水彩着色。',
                '人物五视图中不手持大型独立武器，避免遮挡服装；握持、收纳与比例放入实体表。',
                '五个视角必须同高、同脚底基线、同一身份，且纯侧面与纯背面结构清晰。',
            ],
        },
        'review': {'approved_by': '', 'approved_at': '', 'notes': ['等待生成后逐项复核。']},
    }


def main() -> None:
    changed = 0
    for identifier, data in DATA.items():
        path = PROJECT / 'characters' / identifier / 'character-spec.json'
        current = json.loads(path.read_text(encoding='utf-8'))
        if current.get('status') != 'pending':
            raise RuntimeError(f'{identifier}: expected pending, found {current.get("status")}')
        spec = build_spec(identifier, data)
        path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        changed += 1
    print(f'written {changed} specs')


if __name__ == '__main__':
    main()
