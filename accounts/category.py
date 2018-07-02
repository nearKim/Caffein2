from enum import Enum


class College(Enum):
    HUMANITY = 'hum'
    SOCIAL = 'soc'
    NATURE = 'nat'
    NURSING = 'nur'
    BUSINESS = 'bus'
    ENGINEERING = 'eng'
    AGRICULTURE = 'agr'
    ART = 'art'
    LAW = 'law'
    EDUCATION = 'edu'
    HUMEC = 'cbe'
    VETERINARY = 'vet'
    PHARMACY = 'pha'
    MUSIC = 'mus'
    MEDICINE = 'med'
    FREE = 'cls'
    UNION = 'uni'
    CORRELATION = 'cor'


COLLEGE_CHOICES = (
    (College.HUMANITY.value, '인문대학'),
    (College.SOCIAL.value, '사회과학대학'),
    (College.NATURE.value, '자연과학대학'),
    (College.NURSING.value, '간호대학'),
    (College.BUSINESS.value, '경영대학'),
    (College.ENGINEERING.value, '공과대학'),
    (College.AGRICULTURE.value, '농업생명과학대학'),
    (College.ART.value, '미술대학'),
    (College.LAW.value, '법과대학'),
    (College.EDUCATION.value, '사범대학'),
    (College.HUMEC.value, '생활과학대학'),
    (College.VETERINARY.value, '수의과대학'),
    (College.PHARMACY.value, '약학대학'),
    (College.MUSIC.value, '음악대학'),
    (College.MEDICINE.value, '의과대학'),
    (College.FREE.value, '자유전공학부'),
    (College.UNION.value, '연합전공'),
    (College.CORRELATION.value, '연계전공')
)

DEPARTMENT_COLLEGE_MAP = {
    College.HUMANITY: (
        ('00', '국어국문학과'),
        ('01', '중어중문학과'),
        ('02', '영어영문학과'),
        ('03', '독어독문학과'),
        ('04', '노어노문학과'),
        ('05', '서어서문학과'),
        ('06', '아시아언어문명학부'),
        ('07', '불어불문학과'),
        ('08', '언어학과'),
        ('09', '국사학과'),
        ('10', '동양사학과'),
        ('11', '서양사학과'),
        ('12', '철학과'),
        ('13', '종교학과'),
        ('14', '미학과'),
        ('15', '고고미술사학과')
    ),
    College.SOCIAL: (
        ('16', '정치외교학부'),
        ('17', '경제학부'),
        ('18', '사회학과'),
        ('19', '인류학과'),
        ('20', '심리학과'),
        ('21', '지리학과'),
        ('22', '사회복지학과'),
        ('23', '언론정보학과')
    ),
    College.NATURE: (
        ('24', '수리과학부'),
        ('25', '통계학과'),
        ('26', '물리천문학부'),
        ('27', '화학부'),
        ('28', '생명과학부'),
        ('29', '지구환경과학부')
    ),
    College.NURSING: (
        ('30', '간호학과'),
    ),
    College.BUSINESS: (
        ('31', '경영학과'),
    ),
    College.ENGINEERING: (
        ('32', '건설환경공학부'),
        ('33', '기계항공공학부'),
        ('34', '재료공학부'),
        ('35', '전기정보공학부'),
        ('36', '컴퓨터공학부'),
        ('37', '산업공학과'),
        ('38', '화학생물공학부'),
        ('39', '건축학과'),
        ('40', '건축공학과'),
        ('41', '조선해양공학과'),
        ('42', '에너지자원공학과'),
        ('43', '원자력공학과')
    ),
    College.AGRICULTURE: (
        ('44', '식물생산과학부'),
        ('45', '산림과학부'),
        ('46', '응용생물화학부'),
        ('47', '식품동물생명공학부'),
        ('48', '바비오시스템소재학부'),
        ('49', '조경지역시스템공학부'),
        ('50', '농경제사회학부')
    ),
    College.ART: (
        ('51', '동양화과'),
        ('52', '서양화과'),
        ('53', '조소과'),
        ('54', '공예과'),
        ('55', '디자인과')
    ),
    College.LAW: (
        ('56', '법학부'),
    ),
    College.EDUCATION: (
        ('56', '교육학과'),
        ('57', '국어교육과'),
        ('58', '영어교육과'),
        ('59', '불어교육과'),
        ('60', '독어교육과'),
        ('61', '사회교육과'),
        ('62', '역사교육과'),
        ('63', '지리교육과'),
        ('64', '윤리교육과'),
        ('65', '수학교육과'),
        ('66', '물리교육과'),
        ('67', '화학교육과'),
        ('68', '생물교육과'),
        ('69', '지구과학교육과'),
        ('70', '체육교육과')
    ),
    College.HUMEC: (
        ('71', '소비자아동학부'),
        ('72', '식품영양학과'),
        ('73', '의류학과')
    ),
    College.VETERINARY: (
        ('74', '수의예과'),
        ('75', '수의학과')
    ),
    College.PHARMACY: (
        ('76', '약학과'),
        ('77', '제약학과')
    ),
    College.MUSIC: (
        ('78', '성악과'),
        ('79', '작곡과(이론)'),
        ('80', '작곡과(작곡)'),
        ('81', '기악과'),
        ('82', '국악과')
    ),
    College.MEDICINE: (
        ('83', '의예과'),
        ('84', '의학과')
    ),
    College.FREE: (
        ('85', '자유전공학부'),
    ),
    College.UNION: (
        ('u0', '계산과학'),
        ('u1', '글로벌환경경영학'),
        ('u2', '기술경영'),
        ('u3', '영상매체예술'),
        ('u4', '정보문화학'),
        ('u5', '벤처경영학'),
        ('u6', '동아시아비교인문학')
    ),
    College.CORRELATION: (
        ('c0', '중국학'),
        ('c1', '미국학'),
        ('c2', '러시아학'),
        ('c3', '라틴아메리카학'),
        ('c4', '유럽지역학'),
        ('c5', '뇌마음행동'),
        ('c6', '금융경제'),
        ('c7', '금융수학'),
        ('c8', '과학기술학'),
        ('c9', '공학바이오'),
        ('ca', '통합창의디자인'),
        ('cb', '고전문헌학'),
        ('cc', '인문데이터과학'),
        ('cd', '정치경제철학')
    )
}
# https://stackoverflow.com/questions/3204245/how-do-i-convert-a-tuple-of-tuples-to-a-one-dimensional-list-using-list-comprehe
DEPARTMENT_CHOICES = tuple(element for tupl in DEPARTMENT_COLLEGE_MAP.values() for element in tupl)
