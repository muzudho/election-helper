#
# cd 2024_tokyo/vote_on_the_day/akishima
# python make_csv.py
#
import re
import datetime


########################################
# 設定
########################################

input_file_name = 'input_data.txt'
output_file_name = 'output_data_akishima.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
except_lines_as_text = """\

昭島市
音声読み上げ
Foreign Language
文字サイズ
小
標準
大
表示色
標準配色
ハイコントラスト
ローコントラスト
サイト内検索
サイト内検索
くらし・手続きLiving guide
子育て・教育Parenting&Education
健康・福祉Health&Welfare
文化・スポーツCulture&Sports
施設情報Facility information
市政情報City administration
トップページ > 選挙 > 投票区および投票所 > 投票区及び投票所

投票区及び投票所
更新日：2024年5月8日




投票所名	住所	区域




注：投票所の建て替え工事等により、投票場所が変わる場合があります。

お問い合わせ先
選挙管理委員会事務局（2階）
郵便番号：196-8511 昭島市田中町1-17-1
電話番号：042-544-4487（直通）
ファックス番号：042-544-7205

メールでお問い合わせ

このページに関するアンケート
情報は役に立ちましたか？
役に立った ふつう 役に立たなかった
このページは探しやすかったですか？
探しやすかった ふつう 探しにくかった
送信

選挙
おしらせ（選挙）
投票区および投票所
選挙Q＆A
過去の選挙
昭島市役所
アクセス
〒196-8511 東京都昭島市田中町1-17-1

電話番号：042-544-5111（代表）

ファックス番号：042-546-5496

開庁時間：平日午前8時30分から午後5時15分

法人番号：8000020132071

各ページの掲載記事、及び写真の無断転載は固くお断りします。

ホームページについて
ウェブ・アクセシビリティについて
ホームページ利用者アンケート
サイトマップ
リンク集
携帯サイト
QRコード
Copyright © Akishima City All Rights Reserved.
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

    # 特殊パターン２フラグ
    is_pattern2 = False

    output_table = []

    # 出力フォーマット
    output_table.append(to_formatted_header_string())

    for line in lines:

        # 前後の空白、改行を除去
        line = line.strip()

        # 除外行
        if is_ignore_line(line):
            continue

        print(f"[{datetime.datetime.now()}]  [read line]  {line}")

        # 特殊パターン２
        #
        #   例： `3-8-1	美堀町一丁目から美堀町五丁目まで`
        #       ※ 番地が br タグで改行されているケース
        #
        if is_pattern2:
            m = re.match(r'^(.*)\t.*$', line)
            if m:
                address = f'{address}{m.group(1)}'

                # flush
                #
                # 出力フォーマット
                output_line = to_formatted_data_record_string(
                        ward_number=ward_number,
                        address=address,
                        name_of_facility=name_of_facility)
                print(f"[{datetime.datetime.now()}]    [parse 2]  出力行：{output_line}")
                output_table.append(output_line)

                ward_number = None
                is_pattern2 = False
                continue

        if ward_number == None:
            # 投票区の番号か判断
            #
            #   例： `第1投票区`
            #
            m = re.match(r'^第(\d+)投票区$', line)
            if m:
                ward_number = int(m.group(1))
                print(f"[{datetime.datetime.now()}]    [ward num]  投票区番号：{ward_number}")
                name_of_facility = None
                address = None
                continue

        # 投票区の番号の続き（パターンが複数）
        #
        #   例１： `市立東小学校	東町2-2-18	東町一丁目から東町五丁目まで`
        #
        #   例２： '''環境コミュニケーションセンター	美堀町
        #         3-8-1	美堀町一丁目から美堀町五丁目まで'''
        #           ※番地の途中で br タグを使って改行されている（ワードラップではなく）
        #
        if address == None:
            #print(f"[投票区の番号の続き]  line:`{line}`")

            # パターン１
            m = re.match(r'(.*)\t(.*)\t.*', line)
            if m:
                name_of_facility = m.group(1)
                address = f'東京都昭島市{m.group(2)}'
                print(f"[{datetime.datetime.now()}]    [parse]  住所：{address}　施設名：{name_of_facility}")

                # flush
                #
                # 出力フォーマット
                output_line = to_formatted_data_record_string(
                        ward_number=ward_number,
                        address=address,
                        name_of_facility=name_of_facility)
                print(f"[{datetime.datetime.now()}]    [parse]  出力行：{output_line}")
                output_table.append(output_line)

                ward_number = None
                continue

            # パターン２
            m = re.match(r'^(.*)\t(.*)$', line)
            if m:
                is_pattern2 = True
                name_of_facility = m.group(1)
                address = f'東京都昭島市{m.group(2)}'
                print(f"[{datetime.datetime.now()}]    [parse]  住所：{address}　施設名：{name_of_facility}")


    print(f"[{datetime.datetime.now()}]  write `{output_file_name}` file...")

    # ファイル書出し
    with open(output_file_name, 'w', encoding='utf-8') as f:
        for line in output_table:
            #print(line)
            f.write(f'{line}\n')

    print(f"[{datetime.datetime.now()}]  please read `{output_file_name}` file")
