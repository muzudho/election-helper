#
# cd 2024_tokyo/vote_on_the_day/kunitachi
# python make_csv.py
#
import re
import csv
import datetime
import pprint


########################################
# 設定
########################################

input_file_name = 'input_data.txt'
output_file_name = 'output_data_kunitachi.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
except_lines_as_text = """\
本文へ

国立市 KUNITACHI CITY 文教都市くにたち

もしもの時は
文字サイズ
標準（初期状態）
拡大する
背景色
背景色を黒色にする
背景色を青色にする
背景色を元に戻す
音声読み上げ

Foreign Language
Go
メニュー

くらし・手続き

子育て・教育

健康・福祉

文化・スポーツ
観光

まちづくり・産業

市政情報

現在の位置
ホーム 市政情報 選挙 令和6年7月7日(日曜日)は東京都知事選挙の投票日です
令和6年7月7日(日曜日)は東京都知事選挙の投票日です
更新日：2024年06月28日
期日前投票の状況
日程	曜日	男	女	合計	
今回

類計

令和2年

(前回累計)

6月21日	金曜日	95	87	182	182	179
6月22日	土曜日	183	151	334	516	518
6月23日	日曜日	156	137	293	809	863
6月24日	月曜日	174	159	333	1142	1070
6月25日	火曜日	166	194	360	1502	1484
6月26日	水曜日	168	178	346	1848	1898
6月27日	木曜日	161	177	338	2186	2276
6月28日	金曜日	89	79	168	2354	2683
 

7月7日(日曜日)は東京都知事選挙の投票日です
7月7日(日曜日)は東京都知事選挙の投票日です。

これからの都政を担う人を選ぶ大切な選挙です。あなたの貴重な一票を生かすため積極的に投票にいきましょう。

投票時間は、午前7時から午後8時までです。

国立市で投票ができる方
以前国立市で投票をしたことがある方で、住所などの異動がない方
平成18年7月8日以前に生まれた方で、令和6年3月19日までに転入届をし、引き続き国立市に住民票がある方
国立市の住民登録が3ヵ月以上あり、令和6年2月19日以降、都内の他区市町村に転出した方。(新住所地の選挙人名簿に登録されていない方)﻿
(注)引き続き都内に住所があることを確認いたしますので、時間がかかる場合もあります。新住所地の選挙用住民票等があれば、確認に伴う時間が省略できるため、スムーズに投票することができます。

国立市で投票ができない方
平成18年7月9日以降に生まれた方
都外に転出された方
令和6年3月20日以降、国立市に転入された方
国立市から都内の区市町村に転出した方で、新住所地の選挙人名簿の登録されている方
令和6年2月18日以前に国立市から転出された方
詳しくは選挙管理委員会までお問い合わせください

入場整理券をお忘れなく
入場整理券は、紫色の封書で告示日に合わせて郵送します。なお、世帯単位で封書に入れ、一括して郵送いたしますので、必ずご確認ください。同居されていても世帯が別の場合は、別々に届く場合もあります。
投票所にお越しになる際は、必ず入場整理券をお持ちください。
入場整理券が何らかの事情で届かない場合や紛失した場合でも、選挙人名簿に登録されていれば投票できますので、投票所の係員にお申し出ください。
国立市の投票所とその投票区について
国立市内には12箇所の投票所があります。各投票所には定められた投票区があり、選挙の投票日当日はあらかじめ選挙時に送付している入場整理券に記載されている投票所で投票していただくことになります。
 市内12箇所の投票所ならどこでも投票できるわけではありませんのでご注意ください。詳しくは下記の国立市の投票所一覧表をご覧ください。

国立市の投票所一覧
投票区名	投票所	住所




期日前投票・不在者投票について
投票日当日、次のような理由で投票所へ行くことができない方は、期日前投票または不在者投票をご利用できます。

仕事または冠婚葬祭等の用務がある方

(1)以外の用務等のため投票区の区域外に旅行または滞在する方

病気やけが、妊娠等により、投票所へ行くことが困難な方

病院・施設等に入所されている方(不在者投票のみ。指定されている病院・施設に限ります)

住所移転のため、他の区市町村に居住している方

天災、悪天候により投票所に到達することが困難である方

期日前投票のご案内
 

期日前投票所	日時
市役所北庁舎1階第7会議室
(富士見台2-47-1)

  6月21日(金曜日)から7月6日(土曜日)まで
  午前8時30分から午後8時まで
くにたち北市民プラザ
(北3-1-1  9号棟)

6月29日(土曜日)、30日(日曜日)
午前9時30分から午後8時まで

くにたち南市民プラザ
(泉2-3-2  1号棟)

くにたち駅前市民プラザ
(北1-14-1)

7月5日(金曜日)、6日(土曜日)
午前9時30分から午後8時まで

  南区公会堂
  (泉3-29-11)
(注)市内在住の方で期日前投票をされる方は、事前にご自身が入場整理券裏面の期日前投票宣誓書に必要事項を記入のうえ、期日前投票所へご持参ください。

(注)期日前投票ができるのは国立市の選挙人名簿に登録のある方ですのでご注意ください。

(注)くにたち駅前市民プラザには駐車場・駐輪場はありませんのでご注意ください。

不在者投票のご案内
不在者投票の手続き・期間等
不在者投票宣誓書兼請求書または、任意の様式に国立市の住所・氏名・生年月日・電話番号・書類の送付先・理由等を記載した文書を国立市選挙管理委員会へ郵送し、不在者投票の請求をしてください。

郵送による手続きとなりますので、お早めに請求してください。電話、ファックス、Eメールではできません。詳しくは、国立市選挙管理委員会にお尋ねください。
(注)不在者投票関係書類が届いたら、速やかにお近くの選挙管理委員会等の不在者投票所で不在者投票をお願いします。

東京都知事選挙 不在者投票宣誓書兼請求書 (PDFファイル: 713.1KB)

国立市の不在者投票所について
期間
6月21日(金曜日)から7月6日(土曜日)まで

午前8時30分から午後8時まで

 場所
国立市役所北庁舎1階 選挙管理委員会事務局室

東京都知事選挙特設サイト
東京都選挙管理委員会のホームぺージにて、東京都知事選挙特設サイトが公開されています。以下よりアクセスのうえ、ご確認ください。

東京都知事選挙特設サイト(外部リンク)

18歳以上の方ができること、してはいけないこと
選挙権年齢が18歳に引き下げられたことにより、18歳以上の方は次のことができるようになりました。


次の事項は、これまでの18歳は選挙運動が禁止でしたが、これからはできるようになります。
投票依頼
街頭演説行為
選挙事務所での活動
SNSや動画の拡散
ただし、誰もが下記のとおり禁止されていることがありますのでご注意ください。


誰もがしてはいけないこと(禁止事項)
事前運動の禁止
買収罪・利害誘導罪
自由は妨害の犯罪です
秘密の侵入
詐偽投票などの罪
人気投票公表の禁止
飲食物提供の禁止
候補者等以外メールの禁止
「Adobe Reader（Acrobat Reader）」ダウンロードPDFファイルを閲覧するには「Adobe Reader（Acrobat Reader）」が必要です。お持ちでない方は、左記の「Adobe Reader（Acrobat Reader）」ダウンロードボタンをクリックして、ソフトウェアをダウンロードし、インストールしてください。
キーワード検索


選挙
選挙管理委員会からのお知らせ
選挙制度
過去に実施された選挙の投票及び開票結果
投票区の見直し案に対する意見募集(パブリックコメント)について
国立市長選挙の選挙期日について
令和6年7月7日(日曜日)は東京都知事選挙の投票日です
有料広告
Advertisement
株式会社リスト
うえの税理士事務所
多摩信用金庫
住友不動産販売株式会社
バナー広告掲載のお申し込みやお問い合わせは、こちらをクリックしてください。
国立市
Kunitachi City 東京都の多摩地域中部に位置する市の場所を示す地図 位置は緑で塗りつぶし。
住所

〒186-8501 東京都国立市富士見台2-47-1

電話番号

042-576-2111（代表）

法人番号

1000020132152

開庁時間

平日 午前8時30分から午後5時まで

・一部の窓口は第2・第4土曜日もご利用いただけます（土曜開庁について）
・土曜日の開庁時間は午前9時から正午、午後1時から4時30分です
・年末年始(12月29日から1月3日)は閉庁です
市役所への
行き方
市役所庁舎の
ご案内
各課の
仕事・連絡先
サイトマップ
国立市のホームページについて
ページトップへ
Copyright (c) Kunitachi City. All rights reserved.
"""

# 除外行のリスト
except_lines = []

for line in except_lines_as_text.split("\n"):
    line = line.strip()
    # 空行は除外
    if line != '':
        except_lines.append(line)


def is_ignore_line(line):
    """この行を無視するか？"""

    # 空行
    if line == '':
        return True

    return line in except_lines


def double_quote(text):
    """カンマが含まれていれば、二重引用符で囲む"""
    if ',' in text:
        return f'"{text}"'

    return text


def to_formatted_header_string():
    """出力テキスト形式のヘッダー"""
    return f'投票区番号,住所,施設名'


def to_formatted_data_record_string(
        ward_number,
        address,
        name_of_facility):
    """出力テキスト形式のデータ"""
    address_2 = f'{address} {name_of_facility}'
    return f'''{ward_number},{double_quote(address_2)},{double_quote(name_of_facility)}'''


########################################
# 人間の目視確認によるデータの手調整
########################################

def processing_data():
    print(f"[{datetime.datetime.now()}]  processing `{output_file_name}` file...")

    is_changed = False

    with open(output_file_name, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        # 二次元配列
        row_list = [row for row in reader]

        # 追加
        print(f'[{datetime.datetime.now()}]  [processing]  レコード追加。フォーマットが崩れているため。')
        is_changed = True

        record = ['4', '東京都国立市北1-14-1 くにたち駅前市民プラザ', 'くにたち駅前市民プラザ']
        pprint.pprint(record)
        row_list.append(record)



        for i in range(1, len(row_list)):
            row = row_list[i]

            #print(f'[{datetime.datetime.now()}]  [processing]  {row}')
            address = row[1]

            # ※［９号棟］が漏れてるが、漏れてる方がグーグル　マイマップでエラーが出ないので良い
            #if address == '東京都国立市北3-1-1 くにたち北市民プラザ多目的ホール':
            #    alternate = '東京都国立市北3-1-1 9号棟 くにたち北市民プラザ多目的ホール'
            #    print(f"""\
#[{datetime.datetime.now()}]  [processing]  住所加工。フォーマット崩れの［号棟］漏れ
#    before: `{address}`
#    after : `{alternate}`
#""")
            #    row[1] = alternate
            #    is_changed = True

            if address == '東京都国立市東4-24-1 第三小学校体育館':
                alternate = '東京都国立市東4-24-1 第三小学校'
                print(f"""\
[{datetime.datetime.now()}]  [processing]  住所加工。グーグル　マイマップでエラーが出るから。「体育館」を除去
    before: `{address}`
    after : `{alternate}`
""")
                row[1] = alternate
                is_changed = True


    # ［投票区の番号］順にソートしたい（二次元配列）
    print(f"[{datetime.datetime.now()}]  sort by 投票区の番号")

    # ヘッダーを退避
    header = row_list[0]

    # ヘッダー以外をソート
    row_list = sorted(row_list[1:],
            key=lambda row: int(row[0]))

    # ヘッダーを先頭に付ける
    row_list.insert(0, header)
    #pprint.pprint(row_list)


    # 変更があれば、再びファイル書出し
    if is_changed:
        print(f"[{datetime.datetime.now()}]  rewrite `{output_file_name}` file...")

        with open(output_file_name, 'w', encoding='utf-8') as f:
            for row in row_list:
                line = ','.join(row)
                #print(f"[{datetime.datetime.now()}]  [rewrite]  {line}")
                f.write(f'{line}\n')
    else:
        print(f"[{datetime.datetime.now()}]  no chagned")


########################################
# スクリプト実行時
########################################

if __name__ == '__main__':
    """スクリプト実行時"""

    # ファイル読取
    print(f'[{datetime.datetime.now()}]  read `{input_file_name}` file...')

    with open(input_file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()


    # 見出し
    ward_number = None
    name_of_facility = None
    address = None

    line_1_ok = False

    output_table = []

    # 出力フォーマット
    output_table.append(to_formatted_header_string())

    for line in lines:

        # 前後の空白、改行を除去
        line = line.strip()

        # 除外行
        if is_ignore_line(line):
            continue

        #print(f"[read line]  {line}")

        if ward_number == None:
            # ［投票区の番号］、［施設名］か判断
            #
            #   例： `第1投票区	市役所1階`
            #
            m = re.match(r'^第(\d+)投票区\t(\S+)$', line)
            if m:
                ward_number = int(m.group(1))
                name_of_facility = m.group(2)
                address = None
                line_1_ok = True

                #print(f"[parse]  投票区の番号：{ward_number}  施設名A:`{name_of_facility}`")
                continue

        # ［施設名］の続きと［住所］か判断
        #
        #   例： `市民ロビー	富士見台2-47-1`
        #
        if line_1_ok:
            m = re.match(r'^(\S+)\t(\S+)$', line)
            if m:
                name_of_facility = f'{name_of_facility}{m.group(1)}'
                address = f'東京都国立市{m.group(2)}'

                #print(f"[parse]  施設名:`{name_of_facility}`  住所：`{address}`")

                # 出力フォーマット
                output_table.append(to_formatted_data_record_string(
                        ward_number=ward_number,
                        address=address,
                        name_of_facility=name_of_facility))

                ward_number = None
                line_1_ok = False


    print(f"[{datetime.datetime.now()}]  write `{output_file_name}` file...")

    # ファイル書出し
    with open(output_file_name, 'w', encoding='utf-8') as f:
        for line in output_table:
            #print(line)
            f.write(f'{line}\n')


    #
    # 以下、データ内容に加工が必要なものは、調整します
    #
    processing_data()

    print(f"[{datetime.datetime.now()}]  please read `{output_file_name}` file")
