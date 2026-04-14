# SLtaxicharter Auto Post Bot

スリランカ関連の日本語ツイートを毎日自動投稿するGitHub Actionsボット。

## 投稿スケジュール
- 毎日 JST 06:00
- 毎日 JST 12:00
- 毎日 JST 19:00

## 仕組み
1. OpenAI GPT-4.1-miniがスリランカ関連のバズりやすい日本語ツイートを生成
2. X（Twitter）APIで @SLtaxicharter アカウントに自動投稿
