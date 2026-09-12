import json
import base64
import urllib.request
import urllib.error
import sys
import time
from update_all_posts_rich_style import articles_data, CAT_MAP

WP_URL = "https://affiliate.creativesd.net"
WP_USER = "creativesd_affiliate"
WP_APP_PASS = "mhJs ti3i ZgRz XVIC LPxb 5Hcf".replace(" ", "")

credentials = f"{WP_USER}:{WP_APP_PASS}"
encoded_creds = base64.b64encode(credentials.encode()).decode("utf-8")

def build_clean_post_content(art):
    benefits_html = "".join([f"<li><strong>{b}</strong></li>\n" for b in art['benefits']])
    sources_html = "".join([
        f'<li><a href="{s["url"]}" target="_blank" rel="noopener noreferrer">{s["text"]} <i class="fas fa-external-link-alt"></i></a></li>\n'
        for s in art['sources']
    ])

    return f"""<p><a href="https://creativesd.net/column.html" class="csd-back-link">← 教育現場のお役立ちコラム・ICT情報一覧へ戻る</a></p>

<div class="csd-lead-box">
<p>{art['lead']}</p>
</div>

<h2 class="wp-block-heading">1. 国内外における最新動向・教育現場のトレンド</h2>
<p>{art['trend']}</p>

<h2 class="wp-block-heading">2. 現場への導入メリットと教育効果</h2>
<ul class="wp-block-list">
{benefits_html}</ul>

<h2 class="wp-block-heading">3. 現場教員におすすめする関連ICT機器・ガジェット</h2>
<div class="csd-gadget-box">
<span class="csd-gadget-badge"><i class="fas fa-microchip"></i> おすすめガジェット</span>
<h3>{art['gadget_name']}</h3>
<p class="csd-gadget-role">【想定用途】{art['gadget_role']}</p>
<p class="csd-gadget-desc">{art['gadget_points']}</p>
</div>

<h2 class="wp-block-heading">4. まとめ：無理のないICT導入で教育の質を高める</h2>
<p>教育DXやICT機器の導入は、必ずしも学校全体のシステムを一度に刷新する必要はありません。まずは教員個人のデスクワーク効率化や、特定の実習科目の手技指導など、効果を実感しやすいスモールスタートから始めることが成功の秘訣です。</p>
<p>Creative System Designでは、医療系養成校に特化した臨床実習ポータル「INTEVE LINK」をはじめ、教員の皆様の現場知に寄り添ったDXソリューションをご提案しています。日々の校務や実習指導でお困りの際はお気軽にご相談ください。</p>

<div class="csd-source-box">
<p class="csd-source-title"><i class="fas fa-link"></i> 【参照・情報ソース（公式リンク・ガイドライン）】</p>
<ul>
{sources_html}</ul>
</div>

<hr class="wp-block-separator has-alpha-channel-opacity"/>

<p class="csd-cta-wrapper"><a href="https://creativesd.net/contact.html" class="csd-cta-button">システム・ICT導入についてのお問い合わせはこちら →</a></p>
"""

def update_post_6():
    sources = [
        {"text": "文部科学省: 高等教育機関におけるICTを活用した教育指導の高度化事例集", "url": "https://www.mext.go.jp/"},
        {"text": "厚生労働省: 情報機器作業における労働衛生管理のためのガイドライン（VDT作業基準）", "url": "https://www.mhlw.go.jp/"},
        {"text": "大学ICT推進協議会 (AXIES): 高等教育における教育・学習支援システム（LMS）活用白書", "url": "https://axies.jp/"},
        {"text": "日本医学教育学会: 医学教育におけるICT機器・デジタルツールの活用ガイドライン", "url": "https://jsme-net.org/"},
        {"text": "日本看護学教育学会: 看護技術演習における視覚提示メディアの有効性と教育評価", "url": "https://www.janet.org/"}
    ]
    sources_html = "".join([
        f'<li><a href="{s["url"]}" target="_blank" rel="noopener noreferrer">{s["text"]} <i class="fas fa-external-link-alt"></i></a></li>\n'
        for s in sources
    ])

    content_6 = f"""<p><a href="https://creativesd.net/column.html" class="csd-back-link">← 教育現場のお役立ちコラム・ICT情報一覧へ戻る</a></p>

<div class="csd-lead-box">
<p>日々の講義スライド作成やシラバス改訂、定期試験・模擬試験の作問と採点、さらには臨床実習指導やOSCE（客観的臨床能力試験）の運営、国家試験対策指導まで――。<br>医療系養成校の教員が担う業務は多岐にわたり、学生指導にかける時間を確保するために残業や持ち帰り仕事が常態化しやすい現状があります。本記事では、多忙を極める医療系養成校の先生方に向けて、教育の質を保ちながら講義・実習・校務の負担を客観的に軽減するための「ICT機器・ガジェット」を、具体的な現場の使用シーンと併せてご紹介します。</p>
</div>

<h2 class="wp-block-heading">1. 医療系教育現場が抱える3大負荷とICT活用の意義</h2>
<p>医療系専門職の育成現場では、一般的な講義科目に加えて実技指導や実習記録の点検が日常的に発生します。特に教員の負担となりやすいのは以下の3点です。</p>

<figure class="wp-block-table"><table><thead><tr><th>教育・校務領域</th><th>具体的な課題・現場の負担</th></tr></thead><tbody><tr><td><strong>講義・国試対策</strong></td><td>解剖図・生理機能図の板書やスライド解説に手間がかかる。過去問解説や記述式課題の添削・採点に膨大な時間を要する。</td></tr><tr><td><strong>実技・実習指導</strong></td><td>細かい手技（採血、縫合、触診、機器操作など）を手本で見せる際、大人数の学生に手元が見えにくい。ベッドサイド指導時の資料携行が重い。</td></tr><tr><td><strong>校務・教材研究</strong></td><td>参考図書、シラバス、試験過去問、論文など複数資料を照合しながらの作問・スライド作成作業が非効率になりやすい。</td></tr></tbody></table></figure>

<p>これらの課題は、機器のスペックそのものではなく「教員の動線や作業手順」に適合したガジェットを導入することで、着実に作業工程を短縮できます。</p>

<h2 class="wp-block-heading">2. 現場の課題を解決するICT機器・ガジェット5選</h2>

<div class="csd-gadget-box">
<span class="csd-gadget-badge">① 講義・採点・実習巡回</span>
<h3>スタイラスペン対応タブレット（iPad / Apple Pencil 等）</h3>
<p class="csd-gadget-role">【想定シーン】講義時のリアルタイム描画、PDF課題・レポートのペーパーレス添削</p>
<ul class="wp-block-list">
<li><strong>プロジェクター投影時のリアルタイム解説：</strong>スライドや解剖図上に直接走行ラインや病変部を書き込みながら説明でき、板書の手間と時間を削減。</li>
<li><strong>ペーパーレス添削：</strong>学生から提出されたPDFレポートやOSCE評価シートに直接手書きでコメント・丸付けを行い、そのままクラウド返却。</li>
<li><strong>実習室での身軽な巡回：</strong>学内Wi-Fiと連携し、実習室内を巡回しながら手元のタブレットで資料や評価表を閲覧・入力。</li>
</ul>
</div>

<div class="csd-gadget-box">
<span class="csd-gadget-badge">② 実技・手技指導・テスト解説</span>
<h3>可動式高解像度書画カメラ（ドキュメントカメラ）</h3>
<p class="csd-gadget-role">【想定シーン】手技実習の手元拡大投影、記述式テスト・模型の全体共有</p>
<ul class="wp-block-list">
<li><strong>微細手技のライブ投影：</strong>教卓や実習ベッド脇にアーム式書画カメラを固定し、教員の手元手技を高精細にモニター・プロジェクターへライブ投影。</li>
<li><strong>模範解答・誤答例の即時共有：</strong>学生の記述解答用紙やレントゲン・心電図の実物資料をそのまま投影し、クラス全体で即時共有・ディスカッション。</li>
</ul>
</div>

<div class="csd-gadget-box">
<span class="csd-gadget-badge">③ 大講義室・アクティブラーニング</span>
<h3>ジャイロセンサー搭載ワイヤレスプレゼンター（空中マウス機能付）</h3>
<p class="csd-gadget-role">【想定シーン】大講義室でのアクティブラーニング、学生巡回型の講義運営</p>
<ul class="wp-block-list">
<li><strong>教卓からの解放：</strong>広い階段教室や実習室で、学生の表情・理解度を確認しながら前後のスライド送りや動画再生を行う。</li>
<li><strong>画面上デジタルポインター：</strong>空中ポインター機能により、大型液晶モニター投影時でもレーザー光が見えにくくなる問題を解決。</li>
</ul>
</div>

<div class="csd-gadget-box">
<span class="csd-gadget-badge">④ 作問・教材研究・校務効率化</span>
<h3>軽量モバイルデュアルディスプレイ（14〜15.6インチ）</h3>
<p class="csd-gadget-role">【想定シーン】研究室外・非常勤先での作問作業、複数資料の照合作業</p>
<ul class="wp-block-list">
<li><strong>2画面での効率的な作問・教材研究：</strong>メイン画面で講義スライドや試験問題を編集しつつ、サブ画面で国家試験過去問データベースや医学教科書・ガイドライン（PDF）を表示。</li>
<li><strong>持ち運び可能なデュアル環境：</strong>教員室・実習準備室・非常勤先など、作業場所が変わる環境でもUSB Type-Cケーブル1本でデュアルモニター環境を構築。</li>
</ul>
</div>

<div class="csd-gadget-box">
<span class="csd-gadget-badge">⑤ 大講義・喉の保護・動画収録</span>
<h3>ノイズリダクション機能付きピンマイク（ワイヤレス型）</h3>
<p class="csd-gadget-role">【想定シーン】マスク着用下の大講義・実習室での発声負担軽減、オンデマンド補講収録</p>
<ul class="wp-block-list">
<li><strong>喉の負担軽減と明瞭な拡声：</strong>胸元に小型トランスミッターを装着し、広い実習室や大講義室でも声を張らずに明瞭な音声をスピーカーへ伝達。</li>
<li><strong>オンデマンド教材のクリアな収録：</strong>国家試験対策のオンデマンド補講や欠席者向け講義録画の際、周囲の雑音（空調音・プロジェクターファン音）を抑えたクリアな音声を収録。</li>
</ul>
</div>

<h2 class="wp-block-heading">3. 導入・運用のポイントと注意点</h2>
<ol class="wp-block-list">
<li><strong>学内ネットワーク・セキュリティポリシーの確認：</strong>クラウドストレージの利用可否や個人所有デバイス（BYOD）の校内ネットワーク接続ルールを事前に確認してください。</li>
<li><strong>個人情報・患者情報の取り扱い：</strong>実習病院等の患者情報・臨床データを含むスライドや資料を扱う場合、ローカル保存や画面共有の範囲に十分留意します。</li>
<li><strong>スモールステップでの導入：</strong>いきなりすべての業務をデジタル化するのではなく、「まずは添削のみタブレットで行う」「実技デモのみ書画カメラを使う」といった単一の用途から試すことが定着への近道です。</li>
</ol>

<h2 class="wp-block-heading">4. まとめ：教員のゆとりが質の高い学生指導を生む</h2>
<p>医療系養成校の教員業務は、医療の進歩や国家試験の出題基準改定に伴い、年々高度化・過密化しています。<br>ICT機器の導入は、単なる「作業の短縮」にとどまらず、反復的な準備作業や採点の手間を削減し、<strong>「個々の学生と向き合う時間」や「臨床実習・国試対策のきめ細やかな指導」に注力するための環境づくり</strong>です。<br>ご自身の担当科目や日々の業務負担に合わせて、導入しやすいツールから段階的に取り入れてみてはいかがでしょうか。</p>

<div class="csd-source-box">
<p class="csd-source-title"><i class="fas fa-link"></i> 【参照・情報ソース（公式リンク・ガイドライン）】</p>
<ul>
{sources_html}</ul>
</div>

<hr class="wp-block-separator has-alpha-channel-opacity"/>

<p class="csd-cta-wrapper"><a href="https://creativesd.net/contact.html" class="csd-cta-button">システム・ICT導入についてのお問い合わせはこちら →</a></p>
"""

    payload = {
        "content": content_6,
        "categories": [6, 7],
        "date": "2026-08-22T23:11:13",
        "status": "publish"
    }

    req = urllib.request.Request(
        f"{WP_URL}/wp-json/wp/v2/posts/6",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_creds}",
            "User-Agent": "WordPress/6.0; https://creativesd.net"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            print("SUCCESS: Post 6 updated perfectly.")
    except Exception as e:
        print(f"Error updating post 6: {e}", file=sys.stderr)

def update_all_drafts():
    api_url = f"{WP_URL}/wp-json/wp/v2/posts?status=draft&per_page=100"
    req = urllib.request.Request(api_url, headers={"Authorization": f"Basic {encoded_creds}"})
    try:
        with urllib.request.urlopen(req) as resp:
            drafts = json.loads(resp.read().decode())
    except Exception as e:
        print(f"Error fetching drafts: {e}", file=sys.stderr)
        return

    print(f"Fetched {len(drafts)} draft posts. Updating...")

    updated = 0
    for post in drafts:
        post_id = post["id"]
        post_title = post["title"]["rendered"]

        matched = None
        for art in articles_data:
            if art["title"].strip() == post_title.strip() or art["title"][:20] in post_title:
                matched = art
                break

        if not matched:
            print(f"No match for post {post_id}: {post_title[:25]}...")
            continue

        cat_id = CAT_MAP.get(matched["category_name"], 5)
        new_content = build_clean_post_content(matched)

        payload = {
            "content": new_content,
            "categories": [cat_id]
        }

        req_update = urllib.request.Request(
            f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {encoded_creds}",
                "User-Agent": "WordPress/6.0; https://creativesd.net"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req_update) as resp:
                print(f"SUCCESS: Post {post_id} updated ({post_title[:30]}...)")
                updated += 1
        except Exception as e:
            print(f"Error on post {post_id}: {e}", file=sys.stderr)

        time.sleep(0.3)

    print(f"\n==========================================")
    print(f"Completed updating {updated}/{len(drafts)} draft posts.")
    print(f"==========================================")

if __name__ == "__main__":
    print("1. Updating Post 6...")
    update_post_6()
    print("2. Updating all draft posts...")
    update_all_drafts()
