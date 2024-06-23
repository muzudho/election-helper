#
# cd 2024_tokyo/vote_on_the_day
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

# 除外行の行頭の語句
starts_text_of_ignore_row = """\
このページの先頭です
このページの本文へ移動

西東京市Web　Nishitokyo City Official Website
文字サイズ・色合い変更 | 音声読み上げ
サイトマップ
Multilingual
くらし・手続き
子育て・教育
健康・福祉
学ぶ・楽しむ
市政情報
施設案内

よくある質問
市の組織一覧
検索の使い方
情報が見つからないときは
現在のページ

トップページ市政情報選挙管理委員会投票所の案内
本文ここから
投票所の案内
ページ番号 131-520-173

最終更新日 2024年5月17日

このページの情報をXでポストします

このページの情報をフェイスブックでシェアします

印刷
大きな文字で印刷
各投票所と投票区域をお知らせします。

投票所案内図
市内投票所
投票区域一覧表
詳細な地図で投票所を御確認いただく場合は、該当の投票区の地図情報欄をクリックしてください。

投票区	投票所	投票区の区域	地図情報




お問い合わせ
このページは、選挙管理委員会事務局が担当しています。

市役所田無庁舎　〒188-8666　西東京市南町五丁目6番13号

電話：042-420-2801

ファクス：042-420-2899

お問い合わせフォームを利用する

この情報は皆さまのお役に立ちましたか？
ページ内容の改善の参考とするため、ご意見をお聞かせください。

質問：このページの内容は役に立ちましたか？
役に立った どちらともいえない 役に立たなかった
質問：このページの内容はわかりやすかったですか？
わかりやすかった どちらともいえない わかりにくかった
質問：このページは見つけやすかったですか？
見つけやすかった どちらともいえない 見つけにくかった
本文ここまで
選挙管理委員会
トピックス
投票所の案内
選挙人名簿登録者数（定時登録）
選挙管理委員の構成及び任期
選挙管理委員会会議録
選挙人名簿と選挙権
他の市区町村選挙の不在者投票の受付
西東京市明るい選挙の推進（啓発活動）
検察審査会
直接請求の審査
期日前投票・不在者投票
代理投票・点字投票
国外にいる選挙人の投票方法
過去の選挙の結果
寄附の禁止
選挙管理委員会に関するお問い合わせ
よくある質問
まちづくり
市への意見・要望について
市政情報のよくある質問
よくある質問一覧
こちらもお探しですか
自動体外式除細動器（AED）
西東京市役所
法人番号1000020132292

電話042-464-1311

開庁時間
月曜日～金曜日の午前8時30分から午後5時まで（祝日、年末年始を除く。また、一部の窓口を除く。）

市役所の案内
お問い合わせ
田無庁舎
田無庁舎外観

田無第二庁舎外観

①田無庁舎

②田無第二庁舎

〒188-8666
西東京市南町五丁目6番13号

田無庁舎・田無第二庁舎地図

保谷庁舎
防災センター保谷保健福祉総合センター外観

保谷東分庁舎外観

①防災センター
保谷保健福祉総合センター

〒202-8555
西東京市中町一丁目5番1号

防災センター保谷保健福祉総合センター地図

②保谷東分庁舎

〒202-8555
西東京市中町一丁目6番8号

保谷東分庁舎地図

ようこそ西東京Webへ

西東京市Webについて
個人情報保護方針
© 西東京市
"""

starts_of_ignore_row = []

for line in starts_text_of_ignore_row.split("\n"):
    line = line.strip()
    if line != '':
        starts_of_ignore_row.append(line)


def is_ignore_line(line):
    """この行を無視するか？"""

    # 空行
    if line == '':
        return True

    shall_ignore = False

    for word in starts_of_ignore_row:
        if line.startswith(word):
            #print(f"[ignored] {line}  word:`{word}`")
            shall_ignore = True
            break

    return shall_ignore


# 実施期間 実施時間
patterns_of_time = [
    # 例： 4/17 ～ 4/22 8:30 ～ 20:00
    r'\d+/\d+\s*～\s*\d+/\d+\s+\d+:\d+\s*～\s*\d+:\d+',

    # 例： 4/22   ※改行されて月日だけのケース
    r'\d+/\d+',

    # 例： 4/18 ～ 4/21 10:00 20:00
    r'\d+/\d+\s*～\s*\d+/\d+\s+\d+:\d+\s+\d+:\d+',

    # 例： 6/21～7/6       8:30～20:00
    r'\d+/\d+～\d+/\d+\s+\d+:\d+～\d+:\d+',

    # 例： 10:00～17:00
    r'\d+:\d+～\d+:\d+',
]

def remove_time(line):
    """実施期間 実施時間 の削除"""
    for pattern in patterns_of_time:
        line = re.sub(pattern, '', line)

    return line


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
    town_name = None

    output_table = []

    for line in lines:

        # 前後の空白、改行を除去
        line = line.strip()

        # 除外行
        if is_ignore_line(line):
            continue

        print(f"[read   ] {line}")

        # 町？名か判断
        m = re.match(r'(.+)[\(（]\d+[\)）]', line)
        if m:
            town_name = m.group(1)
            #print(f"[town   ] {town_name}")
            continue

        # 実施期間 実施時間は削除
        line = remove_time(line).strip()

        if line == '':
            continue

        # 最初に出てくるタブまでが建物名と仮定して抽出
        m = re.match(r'(.+)\t(.*)', line)
        if m:
            building = m.group(1).strip()
            address = m.group(2).strip()

            output_table.append(f'''"{town_name}", "{building}", "{address}"''')

        else:
            raise ValueError(f'''[parse error] "{town_name}", "{line}"''')


    # ファイル書出し
    with open(output_file_name, 'w', encoding='utf-8') as f:
        for line in output_table:
            #print(line)
            f.write(f'{line}\n')

    print(f"please read `{output_file_name}` file")
