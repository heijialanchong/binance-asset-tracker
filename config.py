import sys, os,json
# 获取当前脚本文件的绝对路径
script_path = os.path.abspath(__file__)
# 获取脚本文件所在的文件夹（目录）
script_directory = os.path.dirname(script_path)
# 获取脚本文件所在的上一级目录
parent_directory = os.path.dirname(script_directory)
sys.path.append(parent_directory)


# ======================== 参数设置 ========================
# 不需要就直接填"",这样就保存到本地了
controller_path = r""

if os.path.isdir(controller_path):
    pass
else:
    controller_path = ""
    # 不存在的话直接保存到本地

with open(controller_path+"user_config.json", "r", encoding="utf-8") as f:
    data = json.load(f)


wechat_webhook_url = {

    "账户资金" : '', # 企业微信

}