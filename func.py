import time
import requests,datetime,json,traceback

# 当前时间戳
def timestamp():
    return int(time.time()*1000)

# ===重试机制
def retry_wrapper_bina(func, params={}, func_name='', retry_times=5, sleep_seconds=5, if_exit=True):
    """
    需要在出错时不断重试的函数，例如和交易所交互，可以使用本函数调用。
    :param func:            需要重试的函数名
    :param params:          参数
    :param func_name:       方法名称
    :param retry_times:     重试次数
    :param sleep_seconds:   报错后的sleep时间
    :param if_exit:         报错是否退出程序
    :return:
    """
    for _ in range(retry_times):
        try:
            if 'timestamp' in params.keys():
                params['timestamp'] = timestamp()

            result = func(params=params)
            return result
        except Exception as e:
            print(func_name, '报错，报错内容：', str(e), '程序暂停(秒)：', sleep_seconds)


            time.sleep(sleep_seconds)
    else:
        if if_exit:
            raise ValueError(func_name, '报错重试次数超过上限，程序退出。')

def get_price(exchange,symbol):
    result = exchange.request(
            path='ticker/bookTicker',
            api='public',
            method='GET',
            params={
                'symbol': symbol#'USDCUSDT'
            },
            headers={}
        )
    bid_price = result['bidPrice'] # 最优买单
    ask_price = result['askPrice'] # 最优卖单
    return float(bid_price), float(ask_price)

# 企业微信通知
def send_msg_q_wechat(wechat_webhook_url,content,proxies = {}):

    if wechat_webhook_url!="":
        try:
            data = {
                "msgtype": "text",
                "text": {
                    "content": content + '\n' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            r = requests.post(wechat_webhook_url, data=json.dumps(data), timeout=10, proxies=proxies)
            print(f'调用企业微信接口返回： {r.text}')
            print('成功发送企业微信')
        except Exception as e:
            print(f"发送企业微信失败:{e}")
            print(traceback.format_exc())