#
# cd 2024_tokyo/vote_on_the_day/hachioji
# python make_csv.py
#
import re


########################################
# 設定
########################################

input_file_name = 'input_data.txt'
output_file_name = 'output_data_hachioji.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
except_lines_as_text = """\
エンターキーで、ナビゲーションをスキップして本文へ移動します

八王子市
English
한국어
簡体字
繁体字
RSSサイトマップ 
文字サイズ
標準拡大
文字色・背景色
黒白音声読み上げふりがな
くらしの情報	観光・文化	イベント情報	市政情報	施設案内	事業者の方へ
キーワード検索
検索
現在の場所 :	トップ > 市政情報 > 市の政策・計画とまちづくり > 選挙 > 選挙に関するよくある質問 > 投票所一覧（所在地・地図・案内図）
投票所一覧（所在地・地図・案内図）
更新日：令和6年5月22日 ページID：P0009895 印刷する
投票区検索（町名別索引）
投票所




このページに掲載されている情報のお問い合わせ先
選挙管理委員会事務局選挙課
〒192-8501　八王子市元本郷町三丁目24番1号
電話：042-620-7319　ファックス：042-626-3275
お問い合わせメールフォーム
よくあるご質問（バナー）	よくあるご質問
選挙の分類一覧
選挙管理委員会からのお知らせ
選挙に関するよくある質問
これまでの選挙
八王子市役所（画像）八王子市役所
郵便番号：192-8501 東京都八王子市元本郷町三丁目24番1号 [ 地図・フロア案内 ]
電話： 042-626-3111（代表） 午前8時30分から午後5時まで （土曜、日曜、祝日は、閉庁です。）
法人番号： 1000020132012
このサイトについて プライバシーポリシー 免責事項 リンク集
八王子市モバイルサイト
Copyright © Hachioji-City. All Rights Reserved.
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
    print(f'read `{input_file_name}` file...')

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

        #print(f"[read   ] {line}")

        # 投票区の番号か判断
        #
        #   例： `1 第一投票区`
        #
        m = re.match(r'(\d+) .*', line)
        if m:

            # 前のを flush
            if ward_number != None:
                # 出力フォーマット
                output_table.append(to_formatted_data_record_string(
                        ward_number=ward_number,
                        address=address,
                        name_of_facility=name_of_facility))


            ward_number = m.group(1)
            #print(f"[ward num] {ward_number}")
            continue

        # 投票所（施設名）か判断
        #
        #   例： `建物名称：市立第一小学校`
        #
        m = re.match(r'建物名称：(.*)', line)
        if m:
            name_of_facility = m.group(1)
            #print(f"[name of facility] {name_of_facility}")
            continue

        # 住所か判断
        #
        #   例： `所在地：東京都八王子市元横山町二丁目14番3号`
        #
        m = re.match(r'所在地：(.*)', line)
        if m:
            address = f'{m.group(1)}'
            #print(f"[address] {address}")
            continue


    # 前のを flush
    if ward_number != None:
        # 出力フォーマット
        output_table.append(to_formatted_data_record_string(
                ward_number=ward_number,
                address=address,
                name_of_facility=name_of_facility))


    # ファイル書出し
    with open(output_file_name, 'w', encoding='utf-8') as f:
        for line in output_table:
            #print(line)
            f.write(f'{line}\n')

    print(f"please read `{output_file_name}` file")
