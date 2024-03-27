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


data = """
写ラーふぼ親碁ス大強へぱ試大ソ福根ヌメ腎図モス選長ルじっ逆一メアミツ知交クサヌ批辺ヒミナ城禁ノヌセチ加使ち著断思ぼ語9明中更らつぼご区義幹がほ。掲るぞっが元覧レヨヒ宙組事村ヒ調家よげ提事んす味彦めもび記飼ずは広強らルそ死書マヨツヤ界町リぼは対16県ツヒカヲ禁引氏院存訪うね。

住ク日相ん績報ばぴほざ真発改もッが停加エリマコ元棋キモ第官く権議ニシイ能著カソス価記界ニノ包90権戒78用テノクサ立調で備同そッてれ真表クチミ掲治くげふ鎖健リさラ何儀問宇油ほ。考コ球宮ぐ容84本コ文商8通ヒヲロイ圧週ぞあ神製航んれえ医聞無フレけね関記キ長領不棄スよう。新タケ高8吉ちぶっぼ治業クヲ辺火フちイめ九岡日めがべご佐構少イ都空こせふぜ瞬恐況ーイ数台クナ怖食よどうに。

提ぞ水選はまやち失1気ヤヱ食科川ぜぽ記項べ巨復フぜゆ線時タオヤ界売5央学に容1弟じで成半ざ著60力互札るざー。果さが刺評エマムヘ女練ナルミマ死並つぱんも記注キハ状稿オフ印修ユス拶非ク争年済イ史整熊総父丘おぴふそ。白ルミヨ抗携業エク術見進みとっ防真禁ミハト給岸っいスど新件ぜよイ覧情ヌヤケチ詰71劇ヨ全村吏坦らた。

政い検碁蓄ヨスルオ問何アメテヒ数演申ヨ唯米ー救45治ねスひあ田記めン騰窓づなべよ置金収ぼ征囲と原石とさ。建カト観世セマム田頭ヨク副質クご告足読け軽更いがをゅ翌裁ヨヤ仏帳リキホソ予占ドづリ河要フりく暮6稿磨ホヌ授情海ぴぼど生円ネ次種ヒヱラニ能芝ハヨ催定逃真ふほへだ。報スネウ越覚せ年上すイ軽46卓捨縦01朝申つえ閲向へクし続潜ツユムシ議競皐ハヘメ携今気ごやよゅ碁島関跡フ。

海ネハタ断74円まご的座らゆづ事付メウソモ腹政ニト逃品イネヌ西球くぼえだ載論家ホヤル送成ラシセ品漢ッぴラ負億スひえ。庫を想難ーげが日改坂クちがべ昭読ふラ人却むひが利路るほ治的まち語計成が方開能ムシツ面51文9原住セ調76地クユヨ取原単ヱ午棋伐唄庵ねぴず。闘26水ゃイ再道へるッ広体ミエス費昨しはん瀬睦神トニタハ学書意つ上応ソエミ午高ね稿税ユリ出水ら見児フト暮融長煙畿ラぶ。

毎じさまス歩上コ領38平水コス賃優ドも図欧マイサフ界近お熊潟ソ書票ツハオ供阜派れご北立36名マミ旅計源託はためぜ。団速フ組8聞ぐきそは勢参ひざくぼ位当ぶ著吉ヨサ岡宇ーひ図続ネ目察モホ競目オテク書権幅きリうぴ済革協領色むぴんぞ。播スにち自例ミ見心ツネ法民にれ終70目ッンふレ共事ね報信険用キヘ最財68拘肌陶奏さあた。

賞ずるたわ感違ヲナユウ元空タホツ阪48語学べ手日歓転ひずば残応変ヤワテ記背のほ外記てーイ愛会線収代備ぽぴで。田ヌヤアヒ士95作でれきそ需済謙マノ治会ほみ面景わめ畑害さ基促ユ子馬不ミオナ府別つえは無政レ版研モキワサ人資氷僚このクイ。成スハリ聞真ムトヘハ防気50必セタ満図キエメ有済ゆラど石護チクツ形持にむフは象東ずでだゅ供98民ッが持英イアサワ温英院旗昼ぐぞラめ。

復うッみ者銭ナヘカノ万流へや献3試郎えリば委2皮るい料報クロマケ商売ろやたむ弁方ヌアス満億コハ天中げぞうゃ般動例兵城集すずふな。裁メ今技カセケス艦聞満までばラ出優剤ずょめむ業必ウタ後次庭金石ライく螺書キケチ童生リぐふ属参都構満トん。報早ぶラ求敏ひれづざ確健で留刊ツエムリ内26手ウ阪4賢をるド組3界テチユ総省真ンいじ危新ヘヌコム掲森とまーす社更み望五イぼむふ。

活げ通失セモソ私由ゅづっき走行っうぴぎ要28車評林9探モルヌ一自供いゆばぎ内協サケオ質出備フ大者ねお決倒停塚やご。極よクめレ芸自アハ想不すせど重政ケ未目2扱ッむレ葉潟宜ハフリマ入同ス掲開めゅフつ業婚紙む委終エ策場夢巻為へゅこむ。市シエ総5能ラマ覚注ヲケ役買ょずにた朝待の中青びぼ出予値ユ購録ハムメス送英シ初要れてルり開慈もえじ。

橋スレニ決海ょゆ授決ぴふッ関1航ステヱウ近便けあくで炎意ひぜへ金晴ま子打氏ぼリん人安じだをめ種書タ別仕ラマ善9平ツレタ山授ヤニヨ道使少婦項ゅもほ。報らンぜく末19後うに新59感は歴双ムヱ乗刺ミトクメ植止康無ごへす獲合ゃほけっ鳥質サ態夜ぎね鳥健ぼで野供テ藤掲ホケ定生ワトユ球職カ祝派彼精ぴ。牛じか顔野埼討のが覧93理ぞ俳署作チ止独コヤ真形河稿育まばスと模負観せん。"""

data1 = '''細かい部分を描く前に
必要な全ての図が描けるように
まず全体の配置を決定する
'''

data3 = '''
What is Lorem Ipsum?

Lorem Ipsum is simply dummy text of the printing and typesetting
industry. Lorem Ipsum has been the industry's standard dummy
text ever since the 1500s, when an unknown printer took a galley
of type and scrambled it to make a type specimen book. It has
survived not only five centuries, but also the leap into electronic
typesetting, remaining essentially unchanged. It was popularised in
the 1960s with the release of Letraset sheets containing Lorem
Ipsum passages, and more recently with desktop publishing
software like Aldus PageMaker including versions of Lorem Ipsum.

Why do we use it?

It is a long established fact that a reader will be distracted by the
readable content of a page when looking at its layout. The point of
using Lorem Ipsum is that it has a more-or-less normal distribution
of letters, as opposed to using 'Content here, content here',
making it look like readable English. Many desktop publishing
packages and web page editors now use Lorem Ipsum as their
default model text, and a search for 'lorem ipsum' will uncover
many web sites still in their infancy. Various versions have evolved
over the years, sometimes by accident, sometimes on purpose
(injected humour and the like)'''

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
