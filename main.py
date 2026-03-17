import os,sys,time,json
import pandas as pd
# 获取当前脚本文件的绝对路径
script_path = os.path.abspath(__file__)
# 获取脚本文件所在的文件夹（目录）
script_directory = os.path.dirname(script_path)
# 获取脚本文件所在的上一级目录
parent_directory = os.path.dirname(script_directory)
sys.path.append(parent_directory)
import ccxt,time
import datetime
from func import *
from config import *



user_list = data["user"]



# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':

    df_list = []
    for user in user_list:
        print(user+" : \n")
        BINANCE_CONFIG = {
            'apiKey': data["user"][user]["key_0"],
            'secret': data["user"][user]["secret_0"],
            'timeout': 3000,  # API请求超时时间(毫秒)
            'rateLimit': 10,  # API请求最小间隔时间(毫秒)
            'verbose': False,  # 是否打印调试信息
            'enableRateLimit': True,  # 是否启用请求频率限制
            'options': {
                'adjustForTimeDifference': True,  # 自动调整服务器时间差
                'recvWindow': 10000,  # 服务器接收请求的有效时间窗口(毫秒)
            },
        }
        bn_exchange = ccxt.binance(BINANCE_CONFIG)

        # ===== 调用 SAPI 接口：GET /sapi/v1/asset/wallet/balance =====
        resp = bn_exchange.sapiGetAssetWalletBalance()
        bid , ask = get_price(bn_exchange,"BTCUSDT")

        data_list = []
        for i in resp:
            if float(i['balance']) > 0:
                data_list.append(i)

        # 没数值就不统计
        if len(data_list)!=0:
            df = pd.DataFrame(data_list)[['balance','walletName']]
            df['btc_usdt'] = ask
            df['usdt'] = df['balance'].astype(float)  * ask
            df['user'] = user
            # 当前 UTC 时间
            now_utc = datetime.datetime.utcnow()
            # 转为北京时间
            now_bj = now_utc +datetime.timedelta(hours=8)
            df['now_utc'] = now_utc.strftime("%Y-%m-%d %H:%M:%S")
            df['now_utc_date'] = pd.to_datetime(df['now_utc']).dt.date
            df["now_bj"] = now_bj.strftime("%Y-%m-%d %H:%M:%S")
            df["username"] = data["username"]
            df = df[["username",'user','now_utc','now_utc_date','now_bj','walletName','balance','btc_usdt','usdt']]
            print(df.to_markdown())
            df_list.append(df)
            print()

    df = pd.concat(df_list, ignore_index=True)
    print(df.to_markdown())

    # 保存文件
    file_path = controller_path + data["username"] + '_Balance.csv'
    # 1️⃣ 判断文件是否存在
    if os.path.exists(file_path):
        # 2️⃣ 读取已有 CSV
        df_old = pd.read_csv(file_path)
        # 3️⃣ 合并新旧 df
        df_all = pd.concat([df_old, df], ignore_index=True)
    else:
        df_all = df.copy()

    # 4️⃣ 去重（根据所有列去重，如果只想根据特定列去重可以加 subset）
    df_all = df_all.drop_duplicates(ignore_index=True)
    # 5️⃣ 保存回 CSV
    df_all.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f"已保存 {len(df_all)} 条数据到 {file_path}\n")

    total_usdt = df['usdt'].sum()
    print(f"USDT 总和：{total_usdt:.2f}")

    # 假设 df 已经有 'user' 和 'usdt' 列
    usdt_sum_by_user = df.groupby('user')['usdt'].sum().reset_index()
    # 可选：给列重命名
    usdt_sum_by_user.columns = ['user', 'total_usdt']
    print(usdt_sum_by_user)
    msg = "\n".join([f"{row['user']} ：{row['total_usdt']:.2f}" for _, row in usdt_sum_by_user.iterrows()])
    send_msg_q_wechat(wechat_webhook_url['账户资金'],f"{data['username']} ：{total_usdt:.2f}\n{msg}", proxies={})

