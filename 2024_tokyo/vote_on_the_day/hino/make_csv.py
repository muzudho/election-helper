#
# cd 2024_tokyo/vote_on_the_day/hino
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
output_file_name = 'output_data_hino.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
#
#   ※ `第1投票所(日野第四小学校)` は２か所あるので不要なを除去
#   ※ `日野市豊田2-11-2` は２か所あるので不要なを除去
#
except_lines_as_text = """\
エンターキーを押すと、ナビゲーション部分をスキップし本文へ移動します。
日野市
サイトマップ Other language 文字サイズ・配色の変更 やさしい日本語 ふりがな
サイト内検索 
 
サイト全体からさがす
  
検索の使い方
くらし・手続き
健康・医療・福祉
子ども・子育て・教育
文化・スポーツ
産業・仕事
市政情報
現在の位置：  トップページ > 施設案内 > 投票所 > 投票所一覧

ここから本文です。
投票所一覧
このページの情報をツイッターでツイートできますこのページの情報をフェイスブックでシェアできますこのページの情報をラインでシェアできますページID1005979　 更新日 令和6年1月18日
印刷　大きな文字で印刷

地図

日野市石田430第2投票所(日野第一中学校)
日野市日野本町7-7-7第3投票所(日野第一小学校)
日野市日野本町2-14-1第4投票所(東光寺小学校)
日野市新町3-24-1第5投票所(日野台地区センター)
日野市日野台4-17第6投票所(日野第三小学校)
日野市日野台2-1-1第7投票所(日野第二中学校)
日野市多摩平4-5-2第8投票所(豊田小学校)
日野市東豊田2-14-1第9投票所(日野第八小学校)
日野市三沢200第10投票所(夢が丘小学校)
日野市程久保1-14-2第11投票所(七生中学校)
日野市南平6-7-1第12投票所(平山小学校)
日野市平山4-8-6第13投票所(七生緑小学校)
日野市百草896-1第14投票所(日野第五小学校)
日野市多摩平6-21-1第15投票所(日野第六小学校)
日野市多摩平3-21第16投票所(旭が丘小学校)
日野市旭が丘5-21-1第17投票所(南平体育館)
日野市南平4-23-1第18投票所(潤徳小学校)
日野市高幡402第19投票所(もぐさだい児童館)
日野市百草999第20投票所(高幡台団地第一集会所（74号棟）)
日野市程久保650第21投票所(日野第四中学校)
日野市旭が丘2-42第22投票所(滝合小学校)
日野市西平山2-3-1第23投票所(日野第七小学校)
日野市神明3-2第24投票所(大坂上中学校)
日野市大坂上4-17-1第25投票所(落川都営住宅地区センター)
日野市落川819第26投票所(第二武蔵野台地区センター)
日野市程久保2-7-2第27投票所(ひらやま児童館)
日野市平山3-26-3第28投票所(新井地区センター)
日野市石田2-4-6第29投票所(鹿島台地区センター)
日野市南平1-28-13第30投票所（上田地区センター）
日野市川辺堀之内190番地先第31投票所（豊田南地区センター）




このページに関するお問い合わせ
選挙管理委員会事務局
直通電話：042-514-8806
代表電話：042-585-1111
ファクス：042-583-9684
〒191-8686
東京都日野市神明1丁目12番地の1　日野市役所5階
選挙管理委員会事務局へのお問い合わせは専用フォームをご利用ください。

ホームページにご意見をお寄せください

施設案内
投票所
投票所一覧
このページの先頭へ戻る前のページへ戻る トップページへ戻る 表示
PC
スマートフォン
ウェブアクセシビリティ ホームページの使い方 ホームページの考え方
日野市役所
〒191-8686　東京都日野市神明1の12の1
代表電話：042-585-1111
ファクス：042-581-2516（業務時間内）
042-587-8981（夜間・休日ファクス番号）
業務時間：午前8時30分から午後5時（月曜日から金曜日）

法人番号：1000020132128

市役所のご案内
各課のご案内
Copyright © 2018 HINO-City All Rights Reserved.

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

    row_list_2 = []

    with open(output_file_name, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        # 二次元配列
        row_list = [row for row in reader]

        #pprint.pprint(row_list)

        for row in row_list:

            # 誤ヒットによる間違ったデータが入ってるのを除去
            #print(f'[row]  [0]{row[0]}  [1]{row[1]}  [2]{row[2]}')
            if row[0] == '1' and row[1] == '東京都日野市豊田2-11-2 日野第四小学校' and row[2] == '日野第四小学校':
                print(f"[{datetime.datetime.now()}]  [processing]  誤ヒットによる混ざったデータが入ってるのを除去")
                pprint.pprint(row)
                is_changed = True

            else:

                address = row[1]

                if address == '東京都日野市川辺堀之内190番地先 上田地区センター':
                    alternate = '東京都日野市川辺堀之内 上田地区センター'
                    print(f"""\
[{datetime.datetime.now()}]  [processing]  住所加工。 グーグル　マイマップでエラーになるから。「先」という番地表現は無理？
    before: `{address}`
    after : `{alternate}`
""")
                    row[1] = alternate
                    is_changed = True

                row_list_2.append(row)


    row_list = row_list_2


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

        #print(f"[read line]  ward_number:{ward_number}  {line}")

        if ward_number == None:
            # ［投票区の番号］、［施設名］か判断
            #
            #   例： `第1投票所(日野第四小学校)`
            #
            m = re.match(r'^第(\d+)投票所[\(（](\S+)[\)）]$', line)
            if m:
                ward_number = int(m.group(1))
                name_of_facility = m.group(2)
                address = None
                #print(f"[parse]  投票区の番号：{ward_number}  施設名:{name_of_facility}")

            # ［投票区の番号］が取れるまで繰り返します
            continue

        # 無視
        #
        #   例： `所在地〒191-0011`
        #
        if line.startswith('所在地〒'):
            continue


        # ［住所］だろう
        #
        #   例： `日野市石田430`
        #
        address = f'東京都{line}'
        #print(f"[parse]  住所：{address}")

        # 出力フォーマット
        output_table.append(to_formatted_data_record_string(
                ward_number=ward_number,
                address=address,
                name_of_facility=name_of_facility))

        ward_number = None


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
