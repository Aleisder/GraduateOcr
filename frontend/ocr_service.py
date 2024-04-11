from abc import ABC, abstractmethod


class OcrModule(ABC):
    @abstractmethod
    def recognize_text(self, image, lang) -> list[str]:
        pass


class OcrServiceAbstract(ABC):

    @abstractmethod
    def get_recognitions(self, image, lang):
        pass

    @abstractmethod
    def set_reference_ocr_module(self, module: OcrModule):
        pass

    @abstractmethod
    def set_experimental_ocr_module(self, module: OcrModule):
        pass


test_data_jpn = [
    '里長ウヱ無芸せ波生もへ型近ーはゅ記体支ノロサハ豊車ノセ提入提応意ね',
    'ほむか必切シモト万月ヱ兵難修みる。化ヲ棋氏ラ送主つづ松物シヤ育命ぽ',
    'に記聞シワセ取13横よちレぜ国果ま中必能ナマリ会劇フほやね。図ばぼす',
    'だ式筋ノニヨ祝民モロソ属入スったび入城モル水7質ホ吾職ユモ省業よさ',
    'らば精64棋能く端銚ーふラ価川じせ性立リっ湾表ナミテワ治9浴め流教整',
    '慎甲トめきす。',

    '京スノ同稚アモム予大ざそ江8残98一ホネア護外巳タホオ福問な自意権ウ',
    '治短ゆはわ。広と猛龍めょ編権りはばし聞8適特フトモロ質津ロユム週未',
    'ごぎへぼ属玲ソ内整航べぶせど索津ドリスび伊前王位板植じーフ。置みせ',
    '認間テタロ発過まゆじは稿兼ヌ率改ま形表ム題民数ロキク菜恵み八長がほ',
    'みし法載るは断国説まぜびラ男号財ぴリ。',

    '32護ヘヨカ作満ごこよリ統際づさでぱ根壁ぴあ心益もな行社登ネメク幕飲',
    '身向わごろた定子ろ掲神8記サカコ激部べ立魚楽め。総ソ氏肩ワフハ長9物',
    'でゃ三整ワレ親旧ぴ山版資カ電制ごリ越従セヤナ組陸ソヨ一69神ハネ会嫌',
    'ぼべうど制付社シマトミ人暮ぼ。快さげめ滅解提ムケホト力絡ちべぴ建分',
    'だどひ用発さち速事フオ読政3合レオ発高そつび点散よ北写やをく之切ル',
    'コツヤ更校涼耕荘ぞあ。',

    '87善盤5怪のへ阿7車善アエナ者聖びさひふ情合キ拉難ふの越図覧確ばち山',
    '昇拳い。荒サノヨオ要事ユシイ勤健セ自木メエヤホ摘台治キエ本8先ホカ',
    'レ稿囲もル健色どッみ化政ネトユ第住じ劇松んド治産しがづ巨録ムルウ堺',
    '債育サヱスハ闇意づド文際りけげ称考が。紀マ専問ドた全念歴ごレぴ反続',
    '質ミ場物が盟報るスびば樹模時ぱぼり車口セ際促コ竹殺字ょれク図39会と',
    '角位切でこ。'
]


class OcrService(OcrServiceAbstract):
    def __init__(self, reference: OcrModule, experimental: OcrModule):
        self.reference_module = reference
        self.experimental_module = experimental

    def get_recognitions(self, image, lang) -> tuple[list[str], list[str]]:
        reference = test_data_jpn
        # experimental = self.experimental_module.recognize_text(image)
        experimental = self.experimental_module.recognize_text(image, lang)
        return reference, experimental

    def set_reference_ocr_module(self, module: OcrModule):
        self.reference_module = module

    def set_experimental_ocr_module(self, module: OcrModule):
        self.experimental_module = module
