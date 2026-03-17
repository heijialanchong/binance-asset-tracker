# binance-asset-tracker
币安持有资产统计快照 Binance Asset Holdings Snapshot ⭐

1.【config.py】文件里配置企业微信

wechat_webhook_url = {

"账户资金" : '', # 企业微信
}

2.【user_config.json】里配置币安账户和子账户基本信息

username: Main account name

secret: Google Authenticator code

phone: Phone number

user: All accounts including master account

A, B: Account identifiers

key_0: API Key

secret_0: API Secret

{ "username": "", "secret": "", "phone": "", "user": { "A": { "key_0": "", "secret_0": "" }, "B": { "key_0": "", "secret_0": "" } } }
