#!/usr/bin/env python3
"""
SLtaxicharter Auto Post Bot (Thread Version)
Posts engaging, human-like Japanese tweets about Sri Lanka to X (@SLtaxicharter).
This version posts a thread about Sri Lanka's 6 cultural heritage sites.
"""
import os
from datetime import datetime, timezone, timedelta
import tweepy

# X API Keys (from GitHub Secrets)
API_KEY             = os.environ["X_API_KEY"]
API_KEY_SECRET      = os.environ["X_API_KEY_SECRET"]
ACCESS_TOKEN        = os.environ["X_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["X_ACCESS_TOKEN_SECRET"]

# JST timezone
JST = timezone(timedelta(hours=9))

# The thread content about Sri Lanka's 6 cultural heritage sites
THREAD_TWEETS = [
    # Tweet 1: Introduction
    "スリランカは狭い国土に6個の文化遺産と2個の自然遺産があります！今回は文化遺産について説明しますね！🇱🇰✨\n\n#スリランカ #世界遺産 #スリランカ旅行 #文化遺産",
    
    # Tweet 2: Sigiriya
    "【世界遺産①：古代都市シギリヤ】\n通称「シギリヤロック」。ジャングルの中にそびえ立つ高さ約200mの巨大な一枚岩の上に、5世紀の狂気の王カーシャパが築いた空中宮殿の跡です。岩肌に残る美しいフレスコ画「シギリヤ・レディ」は必見！登頂後の絶景は一生の思い出になります🧗‍♂️✨",
    
    # Tweet 3: Dambulla
    "【世界遺産②：ダンブッラ石窟寺院】\nスリランカ最大の石窟寺院。巨大な岩山をくり抜いて作られた5つの洞窟の中に、150体以上の黄金の仏像がずらりと並ぶ圧巻の空間です🙏 紀元前から2000年以上も信仰の場として守られてきた場所で、足を踏み入れた瞬間に神聖な空気を感じます。",
    
    # Tweet 4: Polonnaruwa
    "【世界遺産③：古代都市ポロンナルワ】\n11世紀から13世紀にかけてスリランカの首都として栄えた仏教都市の遺跡群。巨大な一枚岩に彫られた見事な「ガル・ヴィハーラ（石仏）」の寝仏や立仏の美しさは、スリランカ仏教美術の最高傑作と言われています🐘",
    
    # Tweet 5: Anuradhapura
    "【世界遺産④：聖地アヌラーダプラ】\n紀元前3世紀から約1000年にわたって都が置かれたスリランカ最古の古都。仏教伝来の地でもあり、巨大な仏塔（ルワンウェリサーヤ大塔など）や、樹齢2000年以上と言われる「スリ・マハー菩提樹」があり、今も多くの巡礼者が訪れる聖地です🌿",
    
    # Tweet 6: Kandy
    "【世界遺産⑤：聖地キャンディ】\nシンハラ王朝最後の都。緑豊かな山々に囲まれた美しい古都で、スリランカ仏教の最も神聖な場所「仏歯寺」があります。ここには仏陀の歯が祀られており、毎日行われるプージャ（礼拝）の時間は太鼓の音が響き渡り、とても神秘的な雰囲気です🙏",
    
    # Tweet 7: Galle
    "【世界遺産⑥：ゴールの旧市街と要塞】\nスリランカ南部にある港町。17世紀にオランダ人によって築かれた巨大な城壁の中に、ヨーロッパの建築様式と南アジアの伝統が融合した美しい街並みが残っています。おしゃれなカフェや雑貨屋さんも多く、夕暮れ時の城壁の散歩は最高です🌅"
]

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
            # If a tweet in the thread fails, we might want to stop or continue
            # For now, we raise the exception to fail the action
            raise
            
    return posted_ids


if __name__ == "__main__":
    now_jst = datetime.now(JST)
    print(f"[{now_jst}] Starting SLtaxicharter Auto Post Bot (Thread Version)")
    
    try:
        tweet_ids = post_thread(THREAD_TWEETS)
        print(f"[{now_jst}] Successfully posted thread with {len(tweet_ids)} tweets.")
    except Exception as e:
        print(f"[{now_jst}] Failed to post thread: {e}")
        import sys
        sys.exit(1)
