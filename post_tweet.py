#!/usr/bin/env python3
"""
SLtaxicharter Auto Post Bot
Generates a viral Japanese tweet about Sri Lanka using OpenAI and posts it to X.
"""
import os
import random
from datetime import datetime
from openai import OpenAI
import tweepy

# X API Keys (from GitHub Secrets)
API_KEY             = os.environ["X_API_KEY"]
API_KEY_SECRET      = os.environ["X_API_KEY_SECRET"]
ACCESS_TOKEN        = os.environ["X_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["X_ACCESS_TOKEN_SECRET"]
OPENAI_API_KEY      = os.environ["OPENAI_API_KEY"]

TOPICS = [
    "スリランカの世界遺産シギリヤ（ライオン岩）の絶景と歴史",
    "スリランカのビーチリゾート（ミリッサ、ウナワトゥナ、パシクダー）",
    "スリランカのグルメ（カレー、ホッパー、コットゥロティ、スパイス料理）",
    "スリランカのセイロンティー（紅茶）の産地ヌワラエリヤ",
    "スリランカのアーユルヴェーダ・スパ体験",
    "スリランカのタクシーチャーターで快適に観光する方法",
    "スリランカのサファリ・野生動物（ゾウ、ヒョウ、クジャク）",
    "スリランカのインスタ映えスポット（ナインアーチブリッジ、エッラロック）",
    "スリランカの列車の旅（キャンディ〜エッラの絶景ルート）",
    "スリランカのお土産（サファイア、ルビー、セイロンティー、スパイス）",
    "スリランカの旅行情報（ビザ無料、治安、ベストシーズン）",
    "スリランカの世界遺産キャンディ（仏歯寺）と文化",
    "スリランカの古都アヌラーダプラとポロンナルワの遺跡",
    "スリランカのコロンボ市内観光とショッピング",
    "スリランカのホエールウォッチング（ミリッサ沖）",
    "スリランカのサーフィンスポット（アルガムベイ、ヒッカドゥワ）",
    "スリランカの世界遺産ゴール旧市街（オランダ要塞）",
    "スリランカの仏教文化とダンブッラ石窟寺院",
    "スリランカのエレファントサファリ（ピンナワラ象の孤児院）",
    "スリランカの日本人旅行者向けチャータータクシーサービス",
    "スリランカのシーギリヤ周辺の秘境スポット",
    "スリランカの夕日が美しいビーチ（トリンコマリー）",
    "スリランカのスパイス農園ツアー体験",
    "スリランカの伝統舞踊（カンディアンダンス）と文化体験",
    "スリランカの海鮮料理と新鮮なシーフード",
]

def generate_tweet(topic: str) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"""あなたはスリランカ専門の旅行ライターです。
以下のテーマについて、日本人旅行者向けにXでバズる日本語ツイートを1件だけ作成してください。

テーマ: {topic}

条件:
- 完全に日本語で書く
- 140文字以内（絵文字含む）
- 絵文字を2〜4個使う
- ハッシュタグを2〜3個つける（例: #スリランカ #海外旅行 #旅行好きと繋がりたい など）
- 日本人が「いいね」「リツイート」したくなる内容
- 具体的な情報や驚きのある事実を含める
- 必要に応じてチャータータクシーや旅行の利便性にも触れる

ツイート本文のみを出力してください。説明や前置きは不要です。"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.9,
    )
    return response.choices[0].message.content.strip()

def post_tweet(text: str) -> str:
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_KEY_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    response = client.create_tweet(text=text)
    return response.data['id']

if __name__ == "__main__":
    print(f"[{datetime.now()}] Starting SLtaxicharter Auto Post Bot")
    
    topic = random.choice(TOPICS)
    print(f"[{datetime.now()}] Topic: {topic}")
    
    print(f"[{datetime.now()}] Generating tweet with AI...")
    tweet_text = generate_tweet(topic)
    print(f"[{datetime.now()}] Generated: {tweet_text}")
    
    if len(tweet_text) > 280:
        tweet_text = tweet_text[:277] + "..."
    
    tweet_id = post_tweet(tweet_text)
    print(f"[{datetime.now()}] SUCCESS: Posted tweet ID={tweet_id}")
