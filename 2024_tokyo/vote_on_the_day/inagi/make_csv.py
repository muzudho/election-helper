#
# cd 2024_tokyo/vote_on_the_day/inagi
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
output_file_name = 'output_data_inagi.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
except_lines_as_text = """\
このページの本文へ移動
稲城市サイトマップ検索の使い方

くらし・手続き
子育て・教育
健康・福祉・医療
環境・ごみ・リサイクル
観光・文化
施設の案内
市政の情報
サイトメニューここまで
現在のページトップページ市政の情報選挙管理委員会選挙人名簿
本文ここから
選挙人名簿
更新日：2024年6月3日
投票するためには、選挙権を有するだけでなく、選挙人名簿に登録されている必要があります。

選挙人名簿の登録
毎年3月、6月、9月、12月の1日を基準日とし、定時登録を行います。
また、選挙があるときには、基準日を定めて選挙時登録を行います。

登録の資格
次の要件を満たす方が登録されます。

満18歳以上の日本国民
住民票が作成された日から基準日まで、引続き3カ月以上、稲城市の住民基本台帳に記載されている方
基準日の4カ月前の応当日以降転出者であって、転出前に引き続き3カ月以上稲城市の住民基本台帳に記録されていた方
登録の抹消
次の場合、選挙人名簿から抹消されます。

死亡または日本国籍を喪失したとき
稲城市外に転出してから、4カ月を経過したとき
稲城市の選挙人名簿登録者数
選挙人名簿登録者数（定時登録）　令和6年6月3日現在
投票区	投票所名	投票所所在地	男	女	計




合計	38,058	38,532	76,590
このページについてのお問い合わせ
稲城市　選挙管理委員会　事務局
東京都稲城市東長沼2111番地
電話：042-378-2111　ファクス：042-377-4781

本文ここまで
このページの先頭へ
サブナビゲーションここから
選挙管理委員会
令和6年7月7日（日曜日）は東京都知事選挙・東京都議会議員補欠選挙（南多摩選挙区）です
衆議院小選挙区が東京都第30区に変更となりました
選挙の結果
選挙人名簿
期日前投票制度
不在者投票（市外滞在地・病院等での投票）
滞在先での不在者投票
指定病院等における不在者投票
郵便等による不在者投票と代理記載制度
投票で支援が必要な方へ
在外選挙制度
明るい選挙推進協議会・明るい選挙推進委員会
選挙啓発広報誌「いなぎ・しろばら」
明るい選挙啓発ポスター入選作品
いなぎ市民まつりこども体験模擬投票結果
政治家の寄附禁止「贈らない！求めない！受け取らない！」
街頭等における文書図画の掲示（使用）の規制について
よくある質問
期日前投票は、いつからできますか。
選挙権について教えてください。
選挙管理委員会（事務局）はどこにありますか。
よくある質問一覧へ
情報がみつからないときは

サブナビゲーションここまで以下フッターです。
稲城市公式キャラクター稲城なしのすけ
このホームページについて個人情報の取り扱いリンク集携帯サイトスマートフォン版
稲城市役所
市役所へのアクセス休日窓口開庁
〒206-8601　東京都稲城市東長沼2111番地
開庁時間　午前8時30分から午後5時　代表電話：042-378-2111　ファクス：042-377-4781
Copyright （C）Inagi City. All rights reserved.　
Copyright （C）K.Okawara ・ Jet Inoue. All rights reserved.フッターここまでこのページのトップに戻る
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

        # 3	
        # 発達支援センター分室
        # （レスポーいなぎ大丸）
        #
        # 大丸607－2　都営稲城アパート17号棟1階	1,550	1,642	3,192
        record = ['3', '東京都稲城市大丸607-2 都営稲城アパート17号棟', '発達支援センター分室（レスポーいなぎ大丸）']
        pprint.pprint(record)
        row_list.append(record)


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

        # ［投票区の番号］、［施設名］、［住所］か判断
        #
        #   例： `1	第一小学校	東長沼956	3,041	2,866	5,907`
        #
        m = re.match(r'(\d+)\t(\S*)\t(\S*)\t.*', line)
        if m:
            ward_number = int(m.group(1))
            name_of_facility = m.group(2)
            address = f'東京都稲城市{m.group(3)}'
            #print(f"[ward   ] {ward_number}  施設名:{name_of_facility}")

            # 出力フォーマット
            output_table.append(to_formatted_data_record_string(
                    ward_number=ward_number,
                    address=address,
                    name_of_facility=name_of_facility))
            continue


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
