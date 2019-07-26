import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime, timedelta
import csv

#コンフィグファイルのパス
FilePath = "Config.ini"

with open(FilePath) as f:
    ConfigLine = f.readlines()

#この辺は外部ファイルに書いておいて各自設定出来る感じかなと思っている
#トークン
TOKEN = ConfigLine[0].strip("\n")
#チャンネルID
CHANNEL_ID = int(ConfigLine[1])

DefencePath = 'Defence.csv'
BossLevelPath = 'BossLevel.csv'

#Botのコマンドの指定（うまく起動できていない）
bot = commands.Bot(command_prefix='!')

#防衛軍スケジュールを開く
def OpenDefence():
    with open(DefencePath,'r') as fp:
        return list(csv.reader(fp))

#エンドボスのレベルテーブルを開く
def OpenBossLevel():
    with open(BossLevelPath,'r') as fp:
        return list(csv.reader(fp))

#クライアント情報
client = discord.Client()

#loop処理
#@tasks.loop(seconds=60)
#async def loop():
#    channel = client.get_channel(CHANNEL_ID) 
#    now = datetime.now().strftime('%H:%M')
#    if now == '06:00':
#        if channel != None:
#            print(channel)
#            channel.send('６時です')
#    if channel != None:
#        await channel.send(now)

#メッセージが来た時のイベント
@client.event
async def on_message(message):
    #自分の発言には反応しない
    if message.author == client.user:
        return
    #指定チャンネル以外なら反応しない
    if message.channel.id != CHANNEL_ID:
        return
    #防衛軍情報をメッセージ送信する
    if message.content == '/defence':
        lst = OpenDefence()
        line = lst[datetime.now().weekday()]
        text = datetime.now().strftime("[%m/%d %H:%M:%S]\n")
        text += "現在の防衛軍\n"
        text += line[datetime.now().hour] + "\n"
        text += "今日の防衛軍\n\n"
        for i in range(len(line)):
            text += str(i) + "時 : " + line[i] + "\n"
        await message.channel.send(text)
        return
    #ボスレベルをメッセージ送信する
    if message.content == "/bosslevel":
        lst = OpenBossLevel()
        #一番上は基準となる時間データが入っている
        StandardTime = datetime(int(lst[0][0]),int(lst[0][1]),int(lst[0][2]))
        #現在の時間から標準時間を引いてその差で今日の強さを求める（ドラクエⅩは翌日６時更新のため６時間分マイナスする）
        days = (datetime.now() - timedelta(hours = 6) - StandardTime).days
        text = datetime.now().strftime("[%m/%d %H:%M:%S]\n")
        text += "今日のつよさ\n"
        num = 1
        while num < len(lst):
            text += lst[num][0] + ":" + str((days + int(lst[num][2])) % int(lst[num][1]) + 1) + "\n"
            num += 1
        await message.channel.send(text)
        return

#コマンド動作のbot（うまく動いていない）
@bot.command()
async def defence():
    channel = client.get_channel(CHANNEL_ID)
    if channel != None:
        lst = OpenDQX()
        line = lst[datetime.now().weekday()]
        text = datetime.now().strftime("[%m/%d %H:%M:%S]\n")
        text += "現在の防衛軍\n"
        text += line[datetime.now().hour] + "\n"
        text += "今日の防衛軍\n\n"
        for i in range(len(line)):
            text += str(i) + "時:" + line[i] + "\n"
        await channel.send(text)

#接続完了イベント
#@client.event
#async def on_connect():
    #loop.start()

#ループのスタート
#loop.start()
#クライアントを走らせる
client.run(TOKEN)

