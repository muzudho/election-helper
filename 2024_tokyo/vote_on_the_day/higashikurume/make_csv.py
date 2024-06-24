#
# cd 2024_tokyo/vote_on_the_day/higashikurume
# python make_csv.py
#
import re


########################################
# 設定
########################################

input_file_name = 'input_data.txt'
output_file_name = 'output_data.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
except_lines_as_text = """\
エンターキーを押すと、ナビゲーション部分をスキップし本文へ移動します。
東久留米市

文字サイズの変更 縮小 標準 拡大 配色の変更 背景色を元に戻す 背景色を青色にする 背景色を黒色にする 背景色を黄色にする
音声読み上げ English・簡体中文・繁體中文・한국어・がいこくのかたへ
サイト内検索 
暮らしの情報施設案内市政情報文化・スポーツイベント
現在位置：  トップページ > 市政を身近に > 選挙管理委員会 > 投票区域と投票所一覧表

ここから本文です。
投票区域と投票所一覧表
ページ番号　1022305　更新日　 令和4年6月20日
投票区域と投票所一覧表（町名五十音順）
町名	区域	投票区	投票所




このページに関するお問い合わせ
東久留米市役所
〒203-8555 東京都東久留米市本町3-3-1
電話：042-470-7777
お問い合わせは専用フォームをご利用ください。

市政を身近に
選挙管理委員会
投票区域と投票所一覧表
投票支援カードのご案内
東京都知事選挙の投票日は7月7日(日曜日)午前7時から午後8時です
選挙管理員会委員の構成及び任期
これからの選挙
これまでの選挙
選挙の仕組み
明るい選挙
検察審査会
マイページ
前のページへ戻る トップページへ戻る 表示 PC スマートフォン
サイトマップ このサイトの使い方 免責事項・リンクについて 著作権について お問い合わせ 携帯サイト
東久留米市役所
〒203－8555　東京都東久留米市本町3-3-1 東久留米市役所の地図 交通案内
電話：042-470-7777
法人番号：3000020132225

Copyright © Higashikurume city. All rights reserved.

読み上げる
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
    building_name = None
    address = None

    output_table = []

    # 出力フォーマット
    output_table.append(f'''投票区番号, 住所, 施設名''')

    # 以前の行の［町名］
    town_name_backup = None

    # 以前の行の［施設名］
    building_name_backup = None

    for line in lines:

        # 前後の空白、改行を除去
        line = line.strip()

        # 除外行
        if is_ignore_line(line):
            continue

        #print(f"[raw line] {line}")

        # とりあえず１行をタブでスプリット
        tokens = line.split('\t')
        #print(f'len(tokens):{len(tokens)}')

        # 👇 下記のようなデータがあった場合、
        #
        #   例： `上の原	一丁目・二丁目	20	グリーンヒルズ2号棟集会所`
        #
        # 住所は `東京都東久留米市上の原 グリーンヒルズ2号棟集会所` になる
        # ※ ［グリーンヒルズ2号棟集会所］の番地はこの表に載ってないということに注意
        # ※ ［一丁目・二丁目］は［グリーンヒルズ2号棟集会所］の番地ではない。そこへ投票に行く人たちの［区域］
        #
        # 👇 しかし
        #
        #   例： `東京都東久留米市上の原 グリーンヒルズ2号棟集会所`
        #   例： `東京都東久留米市神宝町 グリーンヒルズ2号棟集会所`
        #
        # どうもこの［地域］の人はどの［施設］へ行けと書いてるだけで、［グリーンヒルズ2号棟集会所］がどこにあるのかはこの表の中には無いようだ
        #

        town_name = None
        ward_num = None
        building_name = None

        for token in tokens:
            # 半角数字だけのセルが出てくるまでは、［町名］か、［区域］
            if ward_num is None:
                m = re.match(r'(\d+)', token)
                if m:
                    ward_num = m.group(1)

                else:
                    # 住所だが、「二丁目」という住所は、その前の町名が欠けている恐れがある
                    # セル結合で起こる
                    if token.startswith('二丁目') or token.startswith('三丁目'):
                        #print(f"# 「二丁目」で始まる住所を検知した。その前の町名が欠けている恐れがある。町名のバックアップ：{town_name_backup}")
                        # その前の町名を追加
                        town_name = town_name_backup

                    # ［町名］
                    elif town_name is None:
                        town_name = token
                        town_name_backup = town_name
                        #print(f"town_name_backup:{town_name_backup}")

                    # ［区域］は無視する

            # 半角数字が出てきて以降は施設名
            else:
                building_name = token
                building_name_backup = building_name

        # 施設名が空なら、以前の行の施設名とする
        if building_name is None:
            building_name = building_name_backup

        ## デバッグ表示
        #if 1 < len(address_list):
        #    for address in address_list:
        #        print(f"[multiple address] `{address}`")

        ## トークンを１行で出力
        #output_tokens = []
        #for token in tokens:
        #    output_tokens.append(token)
        #
        #output_line = ', '.join(double_quote(output_tokens))

        # 出力フォーマット
        address_cell = double_quote(f"東京都東久留米市{town_name} {building_name}")
        building_cell = double_quote(building_name)
        output_line = f'{ward_num}, {address_cell}, {building_cell}'
        print(f'[output] {output_line}')
        output_table.append(output_line)

        ## 投票区の番号か判断
        ##
        ##   例： ［第1］
        ##
        ## 町？名か判断
        #m = re.match(r'第(\d+)\t(.*)', line)
        #if m:
        #
        #    # 前のを flush
        #    if ward_number != None:
        #        # 出力フォーマット
        #        output_table.append(f'''{ward_number}, {double_quote(address)}, {double_quote(building_name)}''')
        #
        #
        #    ward_number = m.group(1)
        #    building_name = m.group(2)
        #    address = None
        #    #print(f"[ward   ] {ward_number}  building_name:{building_name}")
        #    continue
        #
        ## 投票区の番号の続き
        #if ward_number != None and address == None:
        #    #print(f"[投票区の番号の続き]  line:`{line}`")
        #    m = re.match(r'[\(（)](\S+)[\)）]\t', line)
        #    if m:
        #        address = f'東京都東久留米市{m.group(1)}'
        #        #print(f"[投票区の番号の続き 2]  address:`{address}`")


    # ファイル書出し
    with open(output_file_name, 'w', encoding='utf-8') as f:
        for line in output_table:
            #print(line)
            f.write(f'{line}\n')

    print(f"please read `{output_file_name}` file")
