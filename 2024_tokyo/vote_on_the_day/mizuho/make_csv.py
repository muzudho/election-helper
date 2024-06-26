#
# cd 2024_tokyo/vote_on_the_day/mizuho
# python make_csv.py
#
import re


########################################
# 設定
########################################

input_file_name = 'input_data.txt'
output_file_name = 'output_data_mizuho.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
except_lines_as_text = """\
本文へ
Language
日本語
配色
白背景に黒文字
文字
標準
音声読上
ふりがな
瑞穂町 みらいに ずっと ほこれるまち
サイト内検索
役場案内（アイコン／ヘッダー）
役場案内

組織一覧（アイコン／ヘッダー）
組織一覧

施設一覧（アイコン／ヘッダー）
施設一覧

よくあるご質問（アイコン／ヘッダー）
よくあるご質問

くらし・手続き健康・福祉子育て・教育観光・イベント環境・まちづくり事業者向けの情報町政情報
ホーム>町政情報>選挙>選挙管理委員会からのお知らせ>投票所一覧

  
投票所一覧
更新日 令和6年1月26日 ページID 2802 印刷
投票所一覧
期日前投票所一覧
投票所一覧




期日前投票所一覧
瑞穂町役場期日前投票所（1階ホール）
東京都西多摩郡瑞穂町大字箱根ケ崎2335番地
武蔵野コミュニティセンター期日前投票所
東京都西多摩郡瑞穂町むさし野1丁目5番地（瑞穂アパート27号棟1階）
箱根ケ崎駅東西自由通路期日前投票所
東京都西多摩郡瑞穂町大字箱根ケ崎397番地
このページについてのお問い合わせ先
選挙管理委員会事務局
〒190-1292 東京都西多摩郡瑞穂町大字箱根ケ崎2335番地
電話 042-557-0614 ファクス 042-556-3401 メールフォーム
受付時間 平日の午前8時30分から午後5時まで

このページを評価する
ウェブサイトの品質向上のため、このページについてのご意見・ご感想をお寄せください。

より詳しくご意見・ご感想をいただける場合は、メールフォームからお送りください。
いただいた情報は、プライバシーポリシーに沿ってお取り扱いいたします。

分かりやすかった 探しにくかった 知りたい内容が書かれていなかった 聞き慣れない用語があった
選挙
令和6年7月7日 東京都知事選挙
令和5年4月23日 瑞穂町議会議員選挙
令和4年7月10日 参議院議員選挙
令和3年10月31日 衆議院議員選挙
令和3年7月4日 東京都議会議員選挙
令和3年4月25日 瑞穂町長選挙
令和2年7月5日 東京都知事選挙
令和元年7月21日 参議院議員選挙
平成31年4月21日 瑞穂町議会議員選挙
平成29年10月22日 衆議院議員選挙
平成29年7月2日 東京都議会議員選挙
平成29年4月23日 瑞穂町長選挙
選挙管理委員会からのお知らせ
選挙制度について
これまでの選挙情報
バナー広告(募集案内)
JAにしたま武陽ガス株式会社交通事故 弁護士（弁護士法人サリュ）青梅信用金庫福祉瑞穂葬祭株式会社加藤商事西多摩支店フリーランスエンジニアのIT求人案件ならエンジニアルートクローバー歯科クリニックバナー広告募集中
ホーム>町政情報>選挙>選挙管理委員会からのお知らせ>投票所一覧

ページ上部に戻る
瑞穂町役場
法人番号：1000020133035

〒190-1292
東京都西多摩郡瑞穂町大字箱根ケ崎2335番地

代表電話 042-557-0501

ファクス 042-556-3401

役場案内（アイコン／フッター）
役場案内

組織一覧（アイコン／フッター）
組織一覧

施設一覧（アイコン／フッター）
施設一覧

よくあるご質問（アイコン／フッター）
よくある
ご質問

ご意見お問い合わせ（アイコン／フッター）
ご意見
お問い合わせ

Facebook（アイコン）Twitter（アイコン）Youtube（アイコン）
サイトポリシー|プライバシーポリシー|サイトマップCopyright © 2017 Mizuho Town. All Rights Reserved.
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

        if ward_number == None:
            # ［投票区の番号］か判断
            #
            #   例： `第1投票所`
            #
            m = re.match(r'第(\d+)投票所', line)
            if m:
                ward_number = int(m.group(1))
                name_of_facility = None
                address = None

                #print(f"[ward num] {ward_number}")
                continue


        # ［投票区の番号］には［施設名］と［住所］が続く
        #
        #   例： `殿ケ谷会館(東京都西多摩郡瑞穂町大字殿ケ谷988番地)`
        #
        if name_of_facility == None:
            #print(f"[投票区の番号の続き]  line:`{line}`")
            m = re.match(r'(.*)[\(（](.*)[\)）]', line)
            if m:
                name_of_facility = m.group(1)
                address = m.group(2)

                #
                # flush
                #
                # 出力フォーマット
                output_table.append(to_formatted_data_record_string(
                        ward_number=ward_number,
                        address=address,
                        name_of_facility=name_of_facility))

                ward_number = None
                continue


    # flush
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
