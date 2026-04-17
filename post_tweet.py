#!/usr/bin/env python3
"""
SLtaxicharter Auto Post Bot (AI Thread Version)
Posts engaging, human-like Japanese tweets about Sri Lanka to X (@SLtaxicharter).
Uses OpenAI API to search for recent topics from specified accounts and generates a thread.
"""
import os
import json
from datetime import datetime, timezone, timedelta
import tweepy
from openai import OpenAI

# API Keys (from GitHub Secrets)
X_API_KEY             = os.environ["X_API_KEY"]
X_API_KEY_SECRET      = os.environ["X_API_KEY_SECRET"]
X_ACCESS_TOKEN        = os.environ["X_ACCESS_TOKEN"]
X_ACCESS_TOKEN_SECRET = os.environ["X_ACCESS_TOKEN_SECRET"]
OPENAI_API_KEY        = os.environ.get("OPENAI_API_KEY")

# JST timezone
JST = timezone(timedelta(hours=9))

# Target accounts to monitor for news/topics
TARGET_ACCOUNTS = [
    "@Shenelle_r", "@iAnuradhaS", "@indunilw", "@Estelle_Vasude1", "@tourismlk", 
    "@sltda_srilanka", "@srilankatourism", "@SriLankaMOT", "@SLinJapan", "@flysrilankan", 
    "@JetwingHotels", "@JetwingTravels", "@AitkenTravels", "@SriLankaSafaris", "@ayuinthewild", 
    "@adaderana", "@SriLankaTweet", "@NewsWireLK", "@Dailymirror_SL", "@colombotelegrap", 
    "@roelraymond", "@KumarSanga2", "@OfficialSLC", "@anuradisanayake", "@PresRajapaksa", 
    "@MFA_SriLanka", "@lankaspice", "@surirankahoumon", "@JapanEmb_SL"
]

def generate_thread_with_ai() -> list[str]:
    """Use OpenAI API to generate a thread about recent Sri Lanka topics."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in environment variables.")
        
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    accounts_str = ", ".join(TARGET_ACCOUNTS[:10]) + " etc."
    now_jst = datetime.now(JST)
    
    system_prompt = f"""
    あなたはスリランカの魅力を日本の旅行者に伝えるプロのX（旧Twitter）運用担当者です。
    以下の指定されたアカウントの最新の話題や、現在のスリランカの観光・文化・ニュース・トレンドに関する情報を基に、
    魅力的で有益な日本語の「スレッド形式（連続ツイート）」を作成してください。
    
    指定アカウント例: {accounts_str}
    現在日時: {now_jst.strftime('%Y年%m月%d日')}
    
    【ルール】
    1. 過去に投稿したような一般的な観光地紹介ではなく、「最新の話題」「今の季節ならではのトピック」「タイムリーなニュース」をテーマにすること。
    2. スレッドは3〜7つのツイートで構成すること。
    3. 各ツイートは140文字以内（ハッシュタグ含む）に収めること。
    4. 1つ目のツイートは導入とし、スレッド全体の内容がわかるようにすること。
    5. 絵文字を適度に使用し、親しみやすいトーン（〜です/〜ます調）で書くこと。
    6. 出力は必ず以下のJSON形式のみとすること（Markdownブロックや他のテキストを含めない）。
    
    {{
        "tweets": [
            "ツイート1の内容...",
            "ツイート2の内容...",
            "ツイート3の内容..."
        ]
    }}
    """
    
    print(f"[{now_jst}] Calling OpenAI API to generate thread...")
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "最新のスリランカの話題を1つ選び、スレッド形式のツイートを生成してください。"}
        ],
        temperature=0.7,
        response_format={"type": "json_object"}
    )
    
    content = response.choices[0].message.content
    try:
        result = json.loads(content)
        tweets = result.get("tweets", [])
        if not tweets or not isinstance(tweets, list):
            raise ValueError("Invalid JSON structure: 'tweets' array not found.")
        return tweets
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON from OpenAI: {content}")
        raise e


def post_thread(tweets: list[str]):
    """Post a list of tweets as a thread."""
    client = tweepy.Client(
        consumer_key=X_API_KEY,
        consumer_secret=X_API_KEY_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_TOKEN_SECRET
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
    print(f"[{now_jst}] Starting SLtaxicharter Auto Post Bot (AI Thread Version)")
    
    try:
        # Generate thread content using AI
        thread_tweets = generate_thread_with_ai()
        print(f"[{now_jst}] AI generated a thread with {len(thread_tweets)} tweets.")
        
        # Post the thread to X
        tweet_ids = post_thread(thread_tweets)
        print(f"[{now_jst}] Successfully posted thread with {len(tweet_ids)} tweets.")
    except Exception as e:
        print(f"[{now_jst}] Failed to post thread: {e}")
        import sys
        sys.exit(1)
