#
# cd 2024_tokyo/vote_on_the_day/machida
# python make_csv.py
#
import re
import csv
import datetime


########################################
# 設定
########################################

input_file_name = 'input_data.txt'
output_file_name = 'output_data_machida.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
except_lines_as_text = """\
このページの先頭ですこのページの本文へ移動
町田市　MACHIDA City：トップページへ
English
中文
한국어
tagalog
Tiếng Việt
ภาษาไทย
Bahasa Indonesia
音声読み上げ
サイトマップ
暮らし
子育て・教育
医療・福祉
文化・スポーツ
産業・観光
市政情報
事業者の方へ
 検索
よくある質問
市役所業務案内
トップページ市政情報選挙投票方法と投票所投票所一覧
本文ここから
投票所一覧
このページの情報をフェイスブックでシェアします

このページの情報をツイッターでシェアします

このページの情報をラインでシェアします

印刷
更新日：2024年6月1日

町田市の投票所一覧
投票区	投票所名称	所在地




ファイルダウンロード　新規ウィンドウで開きます。町田市の投票所一覧（PDF・80KB）

PDF形式のファイルを開くには、Adobe Acrobat Reader DC（旧Adobe Reader）が必要です。お持ちでない方は、Adobe社から無償でダウンロードできます。

Adobe Acrobat Reader DCのダウンロードへ（外部サイト）

ご自宅にプリンタなどの印刷機器をお持ちでない方は、お近くのコンビニエンスストアなどのプリントサービスを利用して申請書等を印刷することができます。詳細はプリントサービスのご案内ページをご覧ください。

このページの担当課へのお問い合わせ
選挙管理委員会事務局
電話：042-724-2168

ファックス：042-724-1195

WEBでのお問い合わせ

この情報はお役に立ちましたか？
お寄せいただいた評価はサイト運営の参考といたします。

質問：このページの情報は役に立ちましたか。
役に立った 役に立たなかった どちらともいえない
質問：このページは見つけやすかったですか。
見つけやすかった 見つけにくかった どちらともいえない
質問：このページはどのようにしてたどり着きましたか。
トップページから順に サイト内検索 検索エンジンから直接 その他
質問：町田市ホームページはどれくらいの頻度でご覧になりますか。
はじめて ときどき いつも
ご意見がありましたらご記入ください。
ご質問や個人情報が含まれるご意見は、トップページ「市へのご意見」の「各課へのご意見・質問」をご利用下さい。
入力されたご意見は、より良いホームページにするための参考にさせていただきますが、回答はできませんのでご了承ください。

投票方法と投票所
投票支援カード
投票所入場券と投票のしかた
期日前投票
滞在地での不在者投票
郵便等による不在者投票
病院・老人ホーム等の施設での不在者投票
投票所で支援が必要な方へ
投票所一覧
投票区早見表と投票区域一覧表
これにも注目
期日前投票
投票日当日の投票所について
マイナンバーカード（個人番号カード）を紛失したとき（再交付申請）
情報が見つからないときは

町田市役所　法人番号6000020132098
公式SNSページ
〒194-8520　東京都町田市森野2-2-22
代表電話：042-722-3111（代表)
代表電話受付時間：午前7時から午後7時
窓口受付時間：午前8時30分から午後5時
市役所・市施設のご案内
市へのご意見
このサイトについて
個人情報の取扱いについて
市庁舎への交通アクセス
Copyright Machida City. All rights reserved.
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

            if address == '東京都町田市南大谷1327番地 町田第二中学校':
                alternate = '東京都町田市南大谷1327番地 第二中学校'
                print(f"""\
[{datetime.datetime.now()}]  [processing]  住所加工。グーグル　マイマップでエラーになるから。「町」の字がノイズになってる？
    before: `{address}`
    after : `{alternate}`
""")
                row[1] = alternate
                is_changed = True

            elif address == '東京都町田市図師町1853番地 図師町内会館':
                alternate = '東京都町田市図師町1853番地 町内会館'
                print(f"""\
[{datetime.datetime.now()}]  [processing]  住所加工。 グーグル　マイマップでエラーになるから。「図師町」と「図師　町内会館」の切れ目が見分けられない？
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
        #   例： `第1投票区	鶴間小学校	鶴間4丁目17番1号`
        #
        m = re.match(r'第(\d+)投票区\t(\S+)\t(\S+)', line)
        if m:
            ward_number = int(m.group(1))
            name_of_facility = m.group(2)
            address = f'東京都町田市{m.group(3)}'
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
