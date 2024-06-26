#
# cd 2024_tokyo/vote_on_the_day/ome
# python make_csv.py
#
import re


########################################
# 設定
########################################

input_file_name = 'input_data.txt'
output_file_name = 'output_data_ome.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
except_lines_as_text = """\

東京都青梅市公式ホームページ	
本文へ
Foreign language
サイトマップ

読み上げる
文字サイズ
標準
拡大
背景色
白
黒
青
くらしの情報
しごとの情報
観光情報
市政情報
防災・防犯
休日・夜間救急
気象情報
 すべて ページ PDF
記事ID番号
現在地トップページ > 組織でさがす > 選挙管理委員会 > 選挙管理委員会事務局 > 投票区および開票区
選挙管理委員会事務局投票区および開票区

記事ID：0000668 更新日：2023年3月10日更新 印刷画面表示   
投票区および開票区
投票区および投票所
現在の投票区および投票所は、次のとおりです。（令和5年3月10日現在）

投票区名

投票所

所在地

区域

地図




開票区および開票所
本市の開票区は1開票区で、開票所については、住友金属鉱山アリーナ青梅（青梅市総合体育館）を充てています。

このページに関するお問い合わせ先
選挙管理委員会事務局
選挙係
〒198-8701 青梅市東青梅1-11-1
Tel：0428-22-1111(2601) Fax：0428-21-2458
みなさんの声をお聞かせください
このページの情報は役に立ちましたか？ はい どちらでもない いいえ
このページは見つけやすかったですか？ はい どちらでもない いいえ
このページを見ている人はこんなページも見ています
令和6年7月7日は東京都知事選挙です
投票日に投票できない方は期日前投票・不在者投票を
AIチャットボットによるごみの分別案内
青梅市空家バンク
50音順ごみ分別一覧
AI(人工知能)は
こんなページをおすすめします
避難場所等一覧
指定収集袋取扱い店一覧
自動体外式除細動器（AED)設置場所・貸出方法
青梅市社会福祉法人一覧
令和6年度家具転倒防止器具等の無料支給・取付け希望の世帯を募集します
よくある質問
見つからないときは
このページの先頭へ
サイトポリシー
 
プライバシーポリシー
 
著作権・リンク等について
 
RSS配信について
青梅市役所 法人番号：8000020132055

〒198-8701　東京都青梅市東青梅1丁目11番地の1[地図]

Tel：0428-22-1111（代表）Fax：0428-22-3508（代表）

開庁日時：月～金曜日（祝日、休日、年末年始を除く）午前8時30分～午後5時

Copyright © Ome City All Rights Reserved.
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
        #   例： `第1投票区`
        #
        # 町？名か判断
        m = re.match(r'第(\d+)投票区', line)
        if m:

            # 前のを flush
            if ward_number != None:
                # 出力フォーマット
                output_table.append(f'''{ward_number}, {double_quote(address)}, {double_quote(name_of_facility)}''')


            ward_number = m.group(1)
            name_of_facility = m.group(2)
            address = None
            #print(f"[ward   ] {ward_number}  施設名:{name_of_facility}")
            continue

        # 投票区の番号の続き
        if ward_number != None and address == None:
            #print(f"[投票区の番号の続き]  line:`{line}`")
            m = re.match(r'[\(（)](\S+)[\)）]\t', line)
            if m:
                address = f'東京都西東京市{m.group(1)}'
                #print(f"[投票区の番号の続き 2]  address:`{address}`")


    # ファイル書出し
    with open(output_file_name, 'w', encoding='utf-8') as f:
        for line in output_table:
            #print(line)
            f.write(f'{line}\n')

    print(f"please read `{output_file_name}` file")
