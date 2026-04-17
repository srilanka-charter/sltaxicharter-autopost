#!/usr/bin/env python3
"""
SLtaxicharter Auto Post Bot (Thread Version)
Posts engaging, human-like Japanese tweets about Sri Lanka to X (@SLtaxicharter).
Randomly selects one of multiple thread topics to post.
"""
import os
import random
import hashlib
from datetime import datetime, timezone, timedelta
import tweepy

# X API Keys (from GitHub Secrets)
API_KEY             = os.environ["X_API_KEY"]
API_KEY_SECRET      = os.environ["X_API_KEY_SECRET"]
ACCESS_TOKEN        = os.environ["X_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["X_ACCESS_TOKEN_SECRET"]

# JST timezone
JST = timezone(timedelta(hours=9))

# Collection of different thread topics
THREADS = [
    # Thread 1: Cultural Heritage Sites
    [
        "スリランカは狭い国土に6個の文化遺産と2個の自然遺産があります！今回は文化遺産について説明しますね！🇱🇰✨\n\n#スリランカ #世界遺産 #スリランカ旅行 #文化遺産",
        "【世界遺産①：古代都市シギリヤ】\n通称「シギリヤロック」。ジャングルの中にそびえ立つ高さ約200mの巨大な一枚岩の上に、5世紀の狂気の王カーシャパが築いた空中宮殿の跡です。岩肌に残る美しいフレスコ画「シギリヤ・レディ」は必見！登頂後の絶景は一生の思い出になります🧗‍♂️✨",
        "【世界遺産②：ダンブッラ石窟寺院】\nスリランカ最大の石窟寺院。巨大な岩山をくり抜いて作られた5つの洞窟の中に、150体以上の黄金の仏像がずらりと並ぶ圧巻の空間です🙏 紀元前から2000年以上も信仰の場として守られてきた場所で、足を踏み入れた瞬間に神聖な空気を感じます。",
        "【世界遺産③：古代都市ポロンナルワ】\n11世紀から13世紀にかけてスリランカの首都として栄えた仏教都市の遺跡群。巨大な一枚岩に彫られた見事な「ガル・ヴィハーラ（石仏）」の寝仏や立仏の美しさは、スリランカ仏教美術の最高傑作と言われています🐘",
        "【世界遺産④：聖地アヌラーダプラ】\n紀元前3世紀から約1000年にわたって都が置かれたスリランカ最古の古都。仏教伝来の地でもあり、巨大な仏塔（ルワンウェリサーヤ大塔など）や、樹齢2000年以上と言われる「スリ・マハー菩提樹」があり、今も多くの巡礼者が訪れる聖地です🌿",
        "【世界遺産⑤：聖地キャンディ】\nシンハラ王朝最後の都。緑豊かな山々に囲まれた美しい古都で、スリランカ仏教の最も神聖な場所「仏歯寺」があります。ここには仏陀の歯が祀られており、毎日行われるプージャ（礼拝）の時間は太鼓の音が響き渡り、とても神秘的な雰囲気です🙏",
        "【世界遺産⑥：ゴールの旧市街と要塞】\nスリランカ南部にある港町。17世紀にオランダ人によって築かれた巨大な城壁の中に、ヨーロッパの建築様式と南アジアの伝統が融合した美しい街並みが残っています。おしゃれなカフェや雑貨屋さんも多く、夕暮れ時の城壁の散歩は最高です🌅"
    ],
    
    # Thread 2: Natural Heritage Sites
    [
        "スリランカには6つの文化遺産のほかに、豊かな自然を守る「2つの自然遺産」があります！今回はその自然遺産をご紹介します🌿🐘\n\n#スリランカ #世界遺産 #スリランカ旅行 #自然遺産",
        "【自然遺産①：シンハラジャ森林保護区】\nスリランカ南西部に広がる、国内最後の熱帯雨林。1988年に世界遺産に登録されました。ここにはスリランカの固有種の樹木が密集し、珍しい鳥類や昆虫、両生類の宝庫となっています🦜 森林浴トレッキングはマイナスイオンたっぷり！",
        "【自然遺産②：スリランカの中央高地】\n2010年に登録された比較的新しい世界遺産。ホートン・プレインズ国立公園、ピーク・ウィルダネス保護区、ナックルズ保護森林の3つのエリアからなります。標高2000m級の山々が連なり、涼しく神秘的な雲霧林が広がっています⛰️",
        "中央高地の中でも特に有名なのが「ホートン・プレインズ国立公園」にある「ワールズ・エンド（地の果て）」。落差約1000mの断崖絶壁から見下ろす景色は圧巻です！早朝の霧が晴れる瞬間を狙ってトレッキングするのがおすすめ🥾✨",
        "スリランカの自然遺産は、固有種の動植物を守る重要な役割を果たしています。ヒョウや紫色の顔をしたサルの仲間など、ここでしか見られない動物もたくさん。自然の力強さと美しさを全身で感じられる場所です🌱"
    ],
    
    # Thread 3: Sri Lankan Food
    [
        "スリランカ旅行の大きな楽しみの一つ、それは「スリランカカレー」！🍛 日本のカレーとは全く違う、奥深いスパイスの世界をご紹介します✨\n\n#スリランカ #スリランカカレー #スリランカ料理 #旅行",
        "【特徴①：ワンプレートに盛りだくさん】\nスリランカカレーは、ご飯の周りに数種類のカレーやおかず（副菜）を盛り付け、すべてを少しずつ混ぜ合わせながら食べるのが基本スタイル。混ぜることで味が変化し、一口ごとに違う美味しさが楽しめます🤤",
        "【特徴②：ココナッツミルクのまろやかさ】\nインドカレーとの大きな違いは、ココナッツミルクをたっぷり使うこと。スパイスの辛さをココナッツの甘みとコクが包み込み、マイルドで食べやすい味わいになっています🥥",
        "【特徴③：モルディブ・フィッシュ】\n実はスリランカ料理には「鰹節」によく似た「モルディブ・フィッシュ」という食材が使われます。これが料理に深い旨味（ダシ）を与えており、日本人の口にとてもよく合う理由の一つと言われています🐟",
        "【定番のおかず：サンボル】\nカレーの横に必ず添えられるのが「サンボル」と呼ばれる和え物。特にココナッツの果肉と唐辛子、ライムを和えた「ポル・サンボル」は絶品！これだけでご飯が何杯でも食べられます🔥",
        "スリランカを訪れたら、ぜひ地元の人に混ざって手で食べてみてください！指先でカレーとご飯を混ぜ合わせることで、温度や食感も感じられ、不思議とスプーンで食べるより美味しく感じますよ🙌"
    ],
    
    # Thread 4: Ceylon Tea
    [
        "「セイロンティー」の故郷、スリランカ☕️ 実は産地の標高によって、紅茶の味も香りも全く違うんです！代表的な産地をご紹介します🌿\n\n#スリランカ #紅茶 #セイロンティー #スリランカ旅行",
        "【ハイグロウン（高地産）：ヌワラエリヤ】\n標高1200m以上の冷涼な気候で育つ紅茶。緑茶にも似た爽やかな渋みと、花のようなデリケートな香りが特徴で「紅茶のシャンパン」とも呼ばれます。ストレートで飲むのがおすすめ！✨",
        "【ハイグロウン（高地産）：ウバ】\nこちらも高地産ですが、独特のメントール系の香りが特徴。世界三大銘茶の一つにも数えられます。水色が明るく美しく、ミルクティーにしても香りが負けません🥛",
        "【ミディアムグロウン（中地産）：ディンブラ】\n標高600〜1200mで栽培される、日本人に最も馴染み深い味わいの紅茶。マイルドでバランスが良く、ストレート、ミルク、アイスティーなど、どんな飲み方でも美味しく楽しめます万能選手です😊",
        "【ロウグロウン（低地産）：ルフナ】\n標高600m以下の温暖な地域で育つ紅茶。中東やロシアで特に人気があります。色が濃く、渋みが少なくてコクがあり、濃厚なミルクティーにぴったり！チャイのベースにもよく使われます☕️",
        "スリランカの紅茶畑（ティーエステート）を訪れると、見渡す限りの緑の絨毯に感動します。茶摘み体験ができたり、工場見学で紅茶ができるまでの工程を学んだり、テイスティングを楽しんだり。紅茶好きにはたまらない国です🌱"
    ],
    
    # Thread 5: Train Journey
    [
        "スリランカを旅するなら、絶対に体験してほしいのが「鉄道の旅」🚂 イギリス植民地時代に紅茶を運ぶために作られた路線が、今では世界有数の絶景路線として人気です✨\n\n#スリランカ #スリランカ旅行 #鉄道の旅 #絶景",
        "【絶景ルート①：キャンディ〜エッラ（高原列車）】\n世界中の旅行者が憧れるルート。標高の高い茶畑の中を縫うように走り、深い緑の渓谷や滝、小さな村々を通り抜けます。窓から吹き込む涼しい風と紅茶の香りが最高です🌿",
        "【ハイライト：ナイン・アーチ・ブリッジ】\nエッラ近くにある、石とレンガだけで作られた9つのアーチを持つ美しい橋。ジャングルの中に突如現れるこの橋を列車が渡る姿は、まるで映画のワンシーンのよう！撮影スポットとしても大人気です📸",
        "【絶景ルート②：コロンボ〜ゴール（海岸列車）】\nこちらはインド洋の海岸線ギリギリを走るルート。車窓いっぱいに青い海とヤシの木が広がり、夕暮れ時には海に沈む美しい夕日を眺めながらのロマンチックな旅が楽しめます🌊🌅",
        "スリランカの列車の楽しみ方は「ドアから身を乗り出す」こと！自己責任ですが、開けっ放しのドアに座って足をブラブラさせながら風を感じるのがスリランカスタイル。車内販売の温かいピーナッツやサモサをかじりながら、のんびり旅を楽しんでください🥜"
    ]
]

def get_thread_for_this_run() -> list[str]:
    """Select a thread based on the current time seed to ensure rotation."""
    now_jst = datetime.now(JST)
    
    # Create a seed based on year, month, day, hour
    # This ensures that runs at different hours get different threads
    seed_str = f"{now_jst.year}-{now_jst.month}-{now_jst.day}-{now_jst.hour}"
    seed = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16)
    rng = random.Random(seed)
    
    return rng.choice(THREADS)


def post_thread(tweets: list[str]):
    """Post a list of tweets as a thread."""
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_KEY_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    
    previous_tweet_id = None
    posted_ids = []
    
    for i, text in enumerate(tweets):
        now_jst = datetime.now(JST)
        print(f"[{now_jst}] Posting tweet {i+1}/{len(tweets)} ({len(text)} chars)")
        
        try:
            if previous_tweet_id is None:
                # First tweet in the thread
                response = client.create_tweet(text=text)
            else:
                # Reply to the previous tweet to form a thread
                response = client.create_tweet(text=text, in_reply_to_tweet_id=previous_tweet_id)
            
            tweet_id = response.data['id']
            posted_ids.append(tweet_id)
            previous_tweet_id = tweet_id
            print(f"[{now_jst}] SUCCESS: Posted tweet ID={tweet_id}")
            
        except Exception as e:
            print(f"[{now_jst}] ERROR posting tweet {i+1}: {e}")
            raise
            
    return posted_ids


if __name__ == "__main__":
    now_jst = datetime.now(JST)
    print(f"[{now_jst}] Starting SLtaxicharter Auto Post Bot (Multi-Thread Version)")
    
    try:
        selected_thread = get_thread_for_this_run()
        print(f"[{now_jst}] Selected thread with {len(selected_thread)} tweets.")
        
        tweet_ids = post_thread(selected_thread)
        print(f"[{now_jst}] Successfully posted thread with {len(tweet_ids)} tweets.")
    except Exception as e:
        print(f"[{now_jst}] Failed to post thread: {e}")
        import sys
        sys.exit(1)
