#
# cd 2024_tokyo/vote_on_the_day/fussa
# python make_csv.py
#
import re
import datetime


########################################
# 設定
########################################

input_file_name = 'input_data.txt'
output_file_name = 'output_data_fussa.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
#
#   ※ `投票所：市役所（住所：福生市本町5）` が２か所に出てくるので、見落としてここに含まないように注意
#
except_lines_as_text = """\
エンターキーを押すと、ナビゲーション部分をスキップし本文へ移動します。
福生市

サイトマップ 文字サイズ・配色 やさしい日本語 ふりがな Foreign language 音声読み上げ
サイト内検索 
 
くらしの情報
観光・イベント情報
施設マップ
市政情報
事業者向け情報
現在の位置：  トップページ > 市政情報 > 制度のあらまし > 選挙 > 投票について > 投票所及び投票区域一覧

ここから本文です。
投票所及び投票区域一覧
ページ番号1003513　 更新日 令和6年6月18日 印刷　
福生市内の投票所一覧です。

投票所及び投票区域一覧
福生以内の投票所及び投票区の一覧です。

画像：投票所及び投票区域一覧地図
投票所及び投票区域一覧




期日前不在者
画像：福生市市役所　第二棟1階
期日前不在者　福生市市役所　第二棟1階




投票区域：福生市内全域
ただし、投票できるのは、公（告）示日の翌日から、投票日の前日までです。
より良いウェブサイトにするためにアンケートを行っています
このページの感想をお聞かせください（複数回答可）
見やすかった 内容が分かりにくい ページを探しにくい 情報が少ない 文章量が多い
送信

このページに関するお問い合わせ
選挙管理委員会事務局　選挙係
〒197-8501 東京都福生市本町5
電話：042-551-1802

市政情報
制度のあらまし
選挙
投票について
投票について
投票所及び投票区域一覧
期日前投票
不在者投票
郵便等による不在者投票
指定施設における不在者投票事務
在外選挙制度
マイページ
前のページへ戻る トップページへ戻る 表示PC スマートフォン
福生市ホームページについて プライバシーポリシー リンク集 携帯サイト
福生市役所市役所へのアクセス
〒197-8501　東京都福生市本町5　代表電話：042-551-1511
開庁時間：午前8時30分から午後5時15分　水曜日夜間と土曜日に業務を行う窓口

法人番号：8000020132187

Copyright © Fussa City. All Rights Reserved.
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
            #print(f"[{datetime.datetime.now()}]  [ignored line]  `{line}`")
            continue

        #print(f"[{datetime.datetime.now()}]  [read line]  `{line}`")

        if ward_number == None:
            # 投票区の番号か判断
            #
            #   例： `第1投票区`
            #
            m = re.match(r'^第(\d+)投票区$', line)
            if m:
                ward_number = int(m.group(1))
                #print(f"[{datetime.datetime.now()}]    [parse]  投票区番号：{ward_number}")
                address = None
                name_of_facility = None
                continue

        # 投票区の番号の続き
        #
        #   例： `投票所：市役所（住所：福生市本町5）`
        #       ※ この投票所は２回出てくるので、この行が除外する行に入っていないように注意
        #
        if address == None:
            #print(f"[投票区の番号の続き]  line:`{line}`")
            m = re.match(r'^投票所：(.*)[\(（)]住所：(\S+)[\)）]$', line)
            if m:
                name_of_facility = m.group(1)
                address = f'東京都福生市{m.group(2)}'
                #print(f"[{datetime.datetime.now()}]    [投票区の番号の続き]  住所：{address}  施設名：{name_of_facility}")
                #print(f"[投票区の番号の続き 2]  address:`{address}`")

                # flush
                # 出力フォーマット
                output_line = to_formatted_data_record_string(
                        ward_number=ward_number,
                        address=address,
                        name_of_facility=name_of_facility)
                #print(f"[{datetime.datetime.now()}]    [出力]  {output_line}")
                output_table.append(output_line)
                ward_number = None
                continue
            #else:
            #    print(f"[{datetime.datetime.now()}]    [投票区の番号の続き else]  住所：{address}  施設名：{name_of_facility}")


    print(f"[{datetime.datetime.now()}]  write `{output_file_name}` file...")

    # ファイル書出し
    with open(output_file_name, 'w', encoding='utf-8') as f:
        for line in output_table:
            #print(line)
            f.write(f'{line}\n')

    print(f"[{datetime.datetime.now()}]  please read `{output_file_name}` file")
