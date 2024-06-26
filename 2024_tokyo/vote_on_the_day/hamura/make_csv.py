#
# cd 2024_tokyo/vote_on_the_day/hamura
# python make_csv.py
#
import re
import csv
import datetime


########################################
# 設定
########################################

input_file_name = 'input_data.txt'
output_file_name = 'output_data_hamura.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
except_lines_as_text = """\
ページの先頭です
共通メニューなどをスキップして本文へ

羽村市

はむらってこんなまち

サイトマップForeign language
読み上げ読み上げ設定
やさしい日本語ひらがなをつける
文字サイズ標準拡大
検索

トップ

暮らしの情報

市政情報

観光・イベント

事業者の方へ

施設案内

現在位置

トップ市政情報報告書・統計・データ選挙
あしあと

羽村市選挙管理委員会投票所と投票区域
投票所と投票区域
初版公開日:[2019年03月09日]更新日：[2019年3月9日]ID:322

投票所一覧
投票所（所在地）一覧
投票区名	投票所建物名称	所在地	地図




投票所区域図
投票所の区域を表示した画像

投票区該当住所
投票区該当住所一覧
投票区	投票場所	該当住所
第1投票区	市立羽村東小学校多目的室	羽村市川崎一丁目から四丁目
羽村市羽690から741
羽村市玉川一丁目から二丁目
羽村市羽東一丁目1から28番
羽村市羽東一丁目29番2から34
羽村市羽東二丁目4番7から20
羽村市羽東二丁目5番3から21
羽村市羽東二丁目6から19番
羽村市羽東三丁目1番7から16
羽村市羽東三丁目2番5から
羽村市羽東三丁目3番
羽村市羽東三丁目4番10から22
羽村市羽東三丁目8番1から35
羽村市羽東三丁目8番45から
羽村市羽東三丁目9から21番
第2投票区	市立羽村第一中学校特別支援学級教室	羽村市羽東一丁目29番1
羽村市羽東一丁目29番35から
羽村市羽東一丁目30から35番
羽村市羽東二丁目1から3番
羽村市羽東二丁目4番1から6
羽村市羽東二丁目4番21から
羽村市羽東二丁目5番1から2
羽村市羽東二丁目5番22から
羽村市羽東三丁目1番1から6
羽村市羽東三丁目1番17から
羽村市羽東三丁目2番1から3
羽村市羽東三丁目4番1から9
羽村市羽東三丁目4番23から
羽村市羽東三丁目5から7番
羽村市羽東三丁目8番36から44
羽村市羽中一丁目3から8番
羽村市羽中一丁目9番7から30
羽村市羽中二丁目2番1から43
羽村市羽中二丁目6から14番
羽村市羽中二丁目19番
羽村市羽中三丁目2番35から43
羽村市羽中三丁目4から9番
羽村市羽中三丁目10番17から36
羽村市羽中三丁目11番14から25
羽村市羽中三丁目13番7から33
羽村市羽中三丁目14から19番
羽村市羽中四丁目1番16から
羽村市羽中四丁目2から8番
羽村市羽中四丁目9番6
羽村市羽中四丁目10から12番
羽村市羽中四丁目13番1から7
羽村市羽中四丁目14から17番
第3投票区	市立羽村西小学校ミーティング室	羽村市羽中一丁目1から2番
羽村市羽中一丁目9番1から6
羽村市羽中一丁目9番31から
羽村市羽中二丁目1番
羽村市羽中二丁目2番44から
羽村市羽中二丁目3から5番
羽村市羽中二丁目15から18番
羽村市羽中三丁目1番
羽村市羽中三丁目2番1から34
羽村市羽中三丁目2番44から
羽村市羽中三丁目3番
羽村市羽中三丁目10番1から16
羽村市羽中三丁目10番37から
羽村市羽中三丁目11番1から13
羽村市羽中三丁目11番26から
羽村市羽中三丁目12番
羽村市羽中三丁目13番1から6
羽村市羽中三丁目13番34から
羽村市羽中四丁目1番1から15
羽村市羽中四丁目13番8から
羽村市羽加美一丁目27から41番地
羽村市羽加美二丁目から四丁目
羽村市羽西一丁目3番
羽村市羽西一丁目4番21から
羽村市羽西一丁目5番
羽村市羽西一丁目6番1から33
羽村市羽西一丁目6番46から
羽村市羽西一丁目7番
羽村市羽西一丁目13番29から31
羽村市羽西一丁目15番5から15
羽村市羽西一丁目16から22番
羽村市羽西二丁目6番11から22
羽村市羽西二丁目6番25から
羽村市羽西二丁目7から10番
第4投票区	市立小作台小学校体育館	羽村市羽加美一丁目1から26番地
羽村市羽西一丁目1番
羽村市羽西一丁目4番1から20
羽村市羽西一丁目6番34から45
羽村市羽西一丁目8から12番
羽村市羽西一丁目13番1から28
羽村市羽西一丁目13番32から
羽村市羽西一丁目14番
羽村市羽西一丁目15番1から3
羽村市羽西一丁目15番16から
羽村市羽西二丁目1から5番
羽村市羽西二丁目6番1から10
羽村市羽西二丁目6番23
羽村市羽西三丁目
羽村市小作台一丁目から五丁目
第5投票区	市立栄小学校体育館	羽村市栄町一丁目
羽村市栄町二丁目1から11番地
羽村市栄町二丁目14から21番地
羽村市栄町三丁目
第6投票区	羽村市役所1階市民ホール	羽村市栄町二丁目12から13番地
羽村市栄町二丁目22から23番地
羽村市栄町二丁目28番地
羽村市緑ヶ丘一丁目1から10番地
羽村市緑ヶ丘二丁目1から10番地
羽村市緑ヶ丘四丁目から五丁目
第7投票区	市立富士見小学校体育館	羽村市五ノ神一丁目から四丁目
羽村市緑ヶ丘一丁目11から26番地
羽村市緑ヶ丘二丁目11から19番地
第8投票区	市立羽村第二中学校特別支援教室（旧第2美術室）	羽村市緑ヶ丘三丁目
羽村市富士見平一丁目から三丁目
羽村市五ノ神362番地
羽村市羽4,141番地
第9投票区	市立武蔵野小学校プレイルーム	羽村市神明台三丁目から四丁目
羽村市双葉町一丁目から三丁目
羽村市川崎693番地から1,221番地
羽村市横田基地内
羽村市羽4,207番地
第10投票区	神明台会館	羽村市神明台一丁目から二丁目
この記事を見ている人はこんな記事も見ています
東京都知事選挙について
期日前投票・不在者投票
東京都知事選挙の期日前投票状況について
羽村市の選挙啓発活動について（出前授業）
各種選挙区別選挙人名簿登録者数
この記事と同じ分類の記事
各種選挙区別選挙人名簿登録者数
選挙人名簿登録者数
在外選挙人名簿登録者数
選挙人名簿登録者・新有権者数
羽村市投票区別選挙人名簿登録者数
お問い合わせ
羽村市選挙管理委員会事務局選挙管理委員会事務局（市役所分庁舎内）

電話: 042-555-1111　（選挙係）内線681

ファクス: 042-554-2921

電話番号のかけ間違いにご注意ください！

お問い合わせフォーム

投票所と投票区域への別ルート
ホーム市政情報羽村市選挙管理委員会選挙について
マイページこのページをチェックする 編集
現在登録されていません。
ページの先頭にもどる

羽村市役所 

〒205-8601 東京都羽村市緑ヶ丘5丁目2番地1 

電話：042-555-1111（代表） 

ファクス：042-554-2921 

法人番号：1000020132276

開庁時間 祝日と年末年始を除く 午前8時30分から午後5時15分（受付は午後5時まで）
　　　　　　※令和4年1月から毎月第2・第4土曜日の午前８時30分から正午まで一部の窓口を開庁し、それ以外の土曜日と日曜日は閉庁します。

個人情報の取り扱いについてウェブアクセシビリティ方針羽村市公式サイトについてリンク集お問い合せ休日の市役所窓口開庁について
Copyright (C) Hamura City. All Rights Reserved.

羽村市


トップ

暮らしの情報

市政情報

観光・イベント

事業者の方へ

施設案内
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
        for i in range(1, len(row_list)):
            row = row_list[i]

            #print(f'[{datetime.datetime.now()}]  [processing]  {row}')
            address = row[1]

            if address == '東京都羽村市富士見平一丁目16番地 市立羽村第二中学校特別支援教室':
                alternate = '東京都羽村市富士見平一丁目16番地 市立羽村第二中学校'
                print(f"""\
[{datetime.datetime.now()}]  [processing]  住所加工。グーグル　マイマップでエラーになるから。教室までは書かない方がいい？
    before: `{address}`
    after : `{alternate}`
""")
                row[1] = alternate
                is_changed = True

            elif address == '東京都羽村市川崎693番1号 市立武蔵野小学校プレイルーム':
                alternate = '東京都羽村市川崎693番1号 市立武蔵野小学校'
                print(f"""\
[{datetime.datetime.now()}]  [processing]  住所加工。 グーグル　マイマップでエラーになるから。教室までは書かない方がいい？
    before: `{address}`
    after : `{alternate}`
""")
                row[1] = alternate
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
        #   例： `第1投票区	市立羽村東小学校多目的室	羽村市羽東二丁目18番1号	施設の地図はこちら`
        #
        m = re.match(r'^第(\d+)投票区\t(\S+)\t(\S+)\t.*$', line)
        if m:
            ward_number = int(m.group(1))
            name_of_facility = m.group(2)
            address = f'東京都{m.group(3)}'
            #print(f"[parse] {ward_number}  施設名:{name_of_facility}")

            # flush
            if ward_number != None:
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
