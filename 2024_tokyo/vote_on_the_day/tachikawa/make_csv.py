#
# cd 2024_tokyo/vote_on_the_day/tachikawa
# python make_csv.py
#
import re
import csv
import datetime


########################################
# 設定
########################################

input_file_name = 'input_data.txt'
output_file_name = 'output_data_tachikawa.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
except_lines_as_text = """\
エンターキーを押すと、ナビゲーション部分をスキップし本文へ移動します。
立川市トップページ


メニュー
防災・防犯
くらし・環境
健康・福祉
子育て・教育
観光・文化・スポーツ
産業・ビジネス
市政情報
現在の位置：  トップページ > 市政情報 > 選挙 > 選挙管理委員会からのお知らせ > あなたの投票所はこちらです

ここから本文です。
あなたの投票所はこちらです
ページ番号1006715　 更新日 2024年4月18日

Xポストするフェイスブックシェアするライン共有する
いいね！
印刷
大きな文字で印刷

あなたの投票所は下記の表のとおりです。
（施設の改修工事等により、投票所が変更になる場合があります）

建物名称をクリックすると、「各課・施設」のページが表示されます。
表示される地図をご参照ください。

下記の施設の地図については、関連ファイルをご参照ください。

第3投票区東京都立立川高等学校(立川市錦町2-13-5）
第9投票区昭和第一学園高等学校(立川市栄町2-45-8）
第26投票区東京都立川地域防災センター(立川市緑町3233-2)
投票所一覧
投票区名	区域	建物名称




関連ファイル
第3投票区立川高等学校 （Gif 48.5KB）新しいウィンドウで開きます
第9投票区和第一学園高等学校 （Gif 44.0KB）新しいウィンドウで開きます
第26投票区東京都立川地域防災センター （Gif 49.1KB）新しいウィンドウで開きます
このページに関するお問い合わせ
選挙管理委員会事務局
〒190-8666 立川市泉町1156-9
電話番号（代表・内線）：042-523-2111（内線1631・1632・1633）
電話番号（直通）：042-528-4344
ファクス番号：042-528-4316
選挙管理委員会事務局　へのお問い合わせは専用フォームをご利用ください。

よりよいウェブサイトにするために、皆さまのご意見をお聞かせください。
このページの情報は、あなたのお役に立ちましたか？
役に立った どちらともいえない 役に立たなかった
このページの情報は、分かりやすかったですか？
分かりやすかった どちらともいえない 分かりにくかった
このページは、見つけやすかったですか？
見つけやすかった どちらともいえない 見つけにくかった
このページに関してご意見がありましたらご記入ください
（この欄に入力されたご意見等への回答はできません。また、個人情報等は入力しないでください。）

送信

市政情報
選挙
選挙管理委員会からのお知らせ
東京都知事選挙のお知らせ
選挙公報の配布について
くらしとせんきょ（選挙啓発紙）
選挙人名簿に登録されていないと投票はできません
あなたの投票所はこちらです
市外で不在者投票をされる方へ
指定施設での不在者投票
身体の不自由な方などのために、つぎのような投票制度があります
投票支援カード
海外で投票される方へ
衆議院小選挙区の区割り
選挙用具を貸し出します
令和5年度立川市明るい選挙推進大会を開催しました

インターネットで
できる手続き

窓口混雑情報外部リンク・新しいウィンドウで開きます
このページの先頭へ戻る前のページへ戻る トップページへ戻る
多摩モノレールのイラスト立川市の街並みのイラスト
一時停止
立川市役所
〒190-8666 東京都立川市泉町1156-9
電話番号：042-523-2111（代表）
開庁時間：午前8時30分～午後5時（土曜・日曜日、祝・休日、12月29日～1月3日を除く）

法人番号 9000020132021 (法人番号について)

交通アクセス
庁舎案内
お問い合わせ
サイトマップ
リンク集
組織案内
サイト利用案内
Copyright © Tachikawa City. All Rights Reserved.
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
        name_of_facility):
    """出力テキスト形式のデータ"""
    address_2 = f'東京都立川市 {name_of_facility}'
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
        for i in range(1, len(row_list)):
            row = row_list[i]

            #ward_number = row[0]
            address = row[1]
            name_of_facility = row[2]
            #print(f'[{datetime.datetime.now()}]    [processing]  投票区の番号：{ward_number}  住所：`{address}`  施設名：`{name_of_facility}`')

            # 7
            if address == '東京都立川市 曙町2丁目1～10,18,19,29～':
                alternate_name_of_facility = '女性総合センター・アイム'
                alternate_address = f'東京都立川市 {alternate_name_of_facility}'
                print(f"""\
[{datetime.datetime.now()}]  [processing]  住所加工。フォーマットが崩れているから手入力
    before: `{address}`  `{name_of_facility}`
    after : `{alternate_address}`  `{alternate_name_of_facility}`
""")
                row[1] = alternate_address
                row[2] = alternate_name_of_facility
                is_changed = True

            # 9
            elif address == '東京都立川市 栄町4丁目の全部':
                alternate_name_of_facility = '昭和第一学園高等学校'
                alternate_address = f'東京都立川市 {alternate_name_of_facility}'
                print(f"""\
[{datetime.datetime.now()}]  [processing]  住所加工。フォーマットが崩れているから手入力
    before: `{address}`  `{name_of_facility}`
    after : `{alternate_address}`  `{alternate_name_of_facility}`
""")
                row[1] = alternate_address
                row[2] = alternate_name_of_facility
                is_changed = True

            # 10
            elif address == '東京都立川市 栄町6丁目1,4,7～':
                alternate_name_of_facility = '第八小学校'
                alternate_address = f'東京都立川市 {alternate_name_of_facility}'
                print(f"""\
[{datetime.datetime.now()}]  [processing]  住所加工。フォーマットが崩れているから手入力
    before: `{address}`  `{name_of_facility}`
    after : `{alternate_address}`  `{alternate_name_of_facility}`
""")
                row[1] = alternate_address
                row[2] = alternate_name_of_facility
                is_changed = True

            # 12
            elif address == '東京都立川市 砂川町2丁目の全部上砂町1,2丁目の全部':
                alternate_name_of_facility = '第九小学校'
                alternate_address = f'東京都立川市 {alternate_name_of_facility}'
                print(f"""\
[{datetime.datetime.now()}]  [processing]  住所加工。フォーマットが崩れているから手入力
    before: `{address}`  `{name_of_facility}`
    after : `{alternate_address}`  `{alternate_name_of_facility}`
""")
                row[1] = alternate_address
                row[2] = alternate_name_of_facility
                is_changed = True

            # 19
            elif address == '東京都立川市 一番町3,5,6丁目の全部':
                alternate_name_of_facility = '松中小学校'
                alternate_address = f'東京都立川市 {alternate_name_of_facility}'
                print(f"""\
[{datetime.datetime.now()}]  [processing]  住所加工。フォーマットが崩れているから手入力
    before: `{address}`  `{name_of_facility}`
    after : `{alternate_address}`  `{alternate_name_of_facility}`
""")
                row[1] = alternate_address
                row[2] = alternate_name_of_facility
                is_changed = True

            # 21
            elif address == '東京都立川市 砂川町5,6丁目の全部':
                alternate_name_of_facility = '柏小学校'
                alternate_address = f'東京都立川市 {alternate_name_of_facility}'
                print(f"""\
[{datetime.datetime.now()}]  [processing]  住所加工。フォーマットが崩れているから手入力
    before: `{address}`  `{name_of_facility}`
    after : `{alternate_address}`  `{alternate_name_of_facility}`
""")
                row[1] = alternate_address
                row[2] = alternate_name_of_facility
                is_changed = True

            # 23
            elif address == '東京都立川市 一番町2丁目1～13,一番町4丁目1～16':
                alternate_name_of_facility = '立川第五中学校'
                alternate_address = f'東京都立川市 {alternate_name_of_facility}'
                print(f"""\
[{datetime.datetime.now()}]  [processing]  住所加工。フォーマットが崩れているから手入力
    before: `{address}`  `{name_of_facility}`
    after : `{alternate_address}`  `{alternate_name_of_facility}`
""")
                row[1] = alternate_address
                row[2] = alternate_name_of_facility
                is_changed = True

            # 24
            elif address == '東京都立川市 西砂町6丁目のうち次以外':
                alternate_name_of_facility = '立川第七中学校'
                alternate_address = f'東京都立川市 {alternate_name_of_facility}'
                print(f"""\
[{datetime.datetime.now()}]  [processing]  住所加工。フォーマットが崩れているから手入力
    before: `{address}`  `{name_of_facility}`
    after : `{alternate_address}`  `{alternate_name_of_facility}`
""")
                row[1] = alternate_address
                row[2] = alternate_name_of_facility
                is_changed = True

            # 26
            elif address == '東京都立川市 泉町のうち次以外':
                alternate_name_of_facility = '東京都立川地域防災センター'
                alternate_address = f'東京都立川市 {alternate_name_of_facility}'
                print(f"""\
[{datetime.datetime.now()}]  [processing]  住所加工。フォーマットが崩れているから手入力
    before: `{address}`  `{name_of_facility}`
    after : `{alternate_address}`  `{alternate_name_of_facility}`
""")
                row[1] = alternate_address
                row[2] = alternate_name_of_facility
                is_changed = True


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
    # 区域
    name_of_area = None
    name_of_facility = None

    data_table = []

    for line in lines:

        # 末尾がタブかどうかは判定材料
        #line = line.strip()

        # 除外行
        if is_ignore_line(line):
            continue

        #print(f"[{datetime.datetime.now()}]  [read line]  `{line.strip()}`")

        if ward_number == None:
            # ［投票区の番号］か判断
            #
            #   例： `1	富士見町1,2,4,5丁目の全部`
            #
            m = re.match(r'(\d+)\t.*', line)
            if m:
                ward_number = int(m.group(1))
                name_of_area = None
                name_of_facility = None
                #print(f"[{datetime.datetime.now()}]    [parse]  投票区の番号：{ward_number}")

            continue


        # 区域
        if name_of_area == None:
            # ［区域］と［施設名］が１行に書かれているケース
            #
            #   例： `錦町2丁目1,2,5～8,11～	東京都立立川高等学校`
            #
            m = re.match(r'(\S+)\t(\S+)', line)
            if m:
                name_of_area = m.group(1)
                name_of_facility = m.group(2)
                #print(f"[{datetime.datetime.now()}]    [parse]  施設名(case A)：{name_of_facility}")

                # データ・テーブル
                data_table.append([ward_number, name_of_facility])

                ward_number = None
                continue

            # 末尾がタブで終われば［区域］
            #
            #   例： `錦町2丁目3,4,9,10	`
            #
            m = re.match(r'(\S+)\t', line)
            if m:
                name_of_area = m.group(1)
                continue

            # 末尾がタブで終わらなければ［施設名］
            name_of_facility = line.strip()
            #print(f"[{datetime.datetime.now()}]    [parse]  施設名(case B)：{name_of_facility}")

            # データ・テーブル
            data_table.append([ward_number, name_of_facility])

            ward_number = None
            continue


        # 施設名
        if name_of_facility == None:
            name_of_facility = line.strip()
            #print(f"[{datetime.datetime.now()}]    [parse]  施設名(case C)：{name_of_facility}")

            # データ・テーブル
            data_table.append([ward_number, name_of_facility])

            ward_number = None
            continue


    print(f"[{datetime.datetime.now()}]  write `{output_file_name}` file...")

    # ファイル書出し
    with open(output_file_name, 'w', encoding='utf-8') as f:
        # 出力フォーマット
        f.write(f'{to_formatted_header_string()}\n')

        for data_record in data_table:
            # 出力フォーマット
            output_line = to_formatted_data_record_string(
                    ward_number=data_record[0],
                    name_of_facility=data_record[1])

            #print(f"[{datetime.datetime.now()}]    output_line:`{output_line}`")
            f.write(f'{output_line}\n')


    #
    # 以下、データ内容に加工が必要なものは、調整します
    #
    processing_data()

    print(f"[{datetime.datetime.now()}]  please read `{output_file_name}` file")
