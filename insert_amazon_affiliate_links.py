import json
import base64
import urllib.request
import urllib.parse
import ssl
import time
import sys
import re

WP_URL = "https://affiliate.creativesd.net"
WP_USER = "creativesd_affiliate"
WP_APP_PASS = "mhJs ti3i ZgRz XVIC LPxb 5Hcf".replace(" ", "")
TRACKING_ID = "csdaffiliate-22"

credentials = f"{WP_USER}:{WP_APP_PASS}"
encoded_creds = base64.b64encode(credentials.encode()).decode("utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "Authorization": f"Basic {encoded_creds}",
    "User-Agent": "WordPress/6.0; https://creativesd.net",
    "Content-Type": "application/json"
}

def generate_amazon_url(keyword):
    encoded_kw = urllib.parse.quote_plus(keyword)
    return f"https://www.amazon.co.jp/s?k={encoded_kw}&tag={TRACKING_ID}"

def generate_amazon_btn_html(keyword, label="Amazonで詳細・価格を見る"):
    url = generate_amazon_url(keyword)
    return (
        f'<div class="csd-amazon-wrapper">\n'
        f'  <a href="{url}" target="_blank" rel="nofollow noopener noreferrer" class="csd-amazon-btn">\n'
        f'    <i class="fab fa-amazon"></i> {label} →\n'
        f'  </a>\n'
        f'</div>\n'
    )

AMAZON_KEYWORDS = {
    "Meta Quest": "Meta Quest 3",
    "書画カメラ": "書画カメラ 4K IPEVO",
    "iPad": "iPad Air Apple Pencil",
    "ScanSnap": "ScanSnap iX1600",
    "ポケットエコー": "ポータブル 超音波 エコー プローブ",
    "ワイヤレスピンマイク": "DJI Mic 2",
    "生成AI": "Elgato Stream Deck MK.2",
    "モバイルモニター": "モバイルモニター 15.6インチ",
    "電子黒板": "BenQ 電子黒板 インタラクティブ",
    "左手デバイス": "TourBox Elite",
    "ウェアラブルカメラ": "Insta360 GO 3S",
    "デジタル採点": "高速 ドキュメントスキャナー fi",
    "ノイズキャンセリング": "Sony WH-1000XM5",
    "BYOD": "Wi-Fi 6 無線LAN ルーター",
    "3Dプリンター": "3Dプリンター Bambu Lab",
    "クリッカー": "大型 モバイルモニター タブレット",
    "エルゴノミクス": "Logicool MX Master 3S",
    "CBT": "タブレット端末 Android 10インチ",
    "音声認識": "PLAUD NOTE AI ボイスレコーダー",
    "プロジェクター": "Anker Nebula Capsule 3",
    "液晶ペンタブレット": "Wacom One 液晶ペンタブレット",
    "OSCE": "iPad 10.2インチ タブレット",
    "急速充電器": "Anker 65W GaN 急速充電器",
    "Kahoot": "iPad タブレット スタンド",
    "360度Web": "Meeting Owl 3",
    "動作分析": "ソニー mocopi モーションキャプチャー",
    "ポータブルSSD": "SanDisk Extreme ポータブルSSD",
    "VRトリアージ": "Meta Quest 3 VRヘッドセット",
    "シミュレーション": "医療 シミュレーター 模型",
    "AIプロクタリング": "Webカメラ 4K 高画質",
    "タイムライン": "iPad Pro 11インチ",
    "多職種連携": "Jabra 会議用 マイクスピーカー",
    "Anki": "8BitDo Zero 2 コントローラー",
    "電動昇降デスク": "FlexiSpot 電動昇降デスク",
    "ペーパーレス": "ScanSnap iX1300 スキャナー",
    "メッシュWi-Fi": "メッシュWi-Fi 6 ルーター",
    "ミニ動画": "ロジクール Webカメラ C920n",
    "健康管理": "オムロン 上腕式血圧計 Bluetooth",
    "ポートフォリオ": "iPad Air キーボードケース",
    "INTEVE LINK": "iPad セルラーモデル 10.2インチ"
}

def update_post_6_with_amazon():
    req = urllib.request.Request(f"{WP_URL}/wp-json/wp/v2/posts/6", headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            post = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Error reading post 6: {e}")
        return

    content = post["content"]["rendered"]

    if "csdaffiliate-22" not in content:
        boxes = content.split('<div class="csd-gadget-box">')
        new_boxes = [boxes[0]]
        
        gadget_keywords = [
            "iPad Air Apple Pencil",
            "書画カメラ 4K IPEVO",
            "ワイヤレスプレゼンター 空中マウス",
            "モバイルモニター 15.6インチ",
            "DJI Mic 2 ワイヤレスピンマイク"
        ]

        for i, box in enumerate(boxes[1:]):
            kw = gadget_keywords[i] if i < len(gadget_keywords) else "医療教育 ICTガジェット"
            btn_html = generate_amazon_btn_html(kw)
            last_div_idx = box.rfind('</div>')
            if last_div_idx != -1:
                box = box[:last_div_idx] + btn_html + box[last_div_idx:]
            new_boxes.append(box)
        
        content = '<div class="csd-gadget-box">'.join(new_boxes)

        payload = {
            "content": content,
            "date": post["date"],
            "status": "publish"
        }

        req_update = urllib.request.Request(
            f"{WP_URL}/wp-json/wp/v2/posts/6",
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        try:
            with urllib.request.urlopen(req_update, context=ctx) as r:
                print("SUCCESS: Post 6 updated with Amazon Affiliate links.")
        except Exception as e:
            print(f"Error updating post 6: {e}")
    else:
        print("Post 6 already has Amazon links.")

def update_all_posts_with_amazon():
    req = urllib.request.Request(f"{WP_URL}/wp-json/wp/v2/posts?per_page=100&status=publish", headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            posts = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return

    print(f"Fetched {len(posts)} published posts. Processing Amazon affiliate links...")

    updated_count = 0
    for post in posts:
        post_id = post["id"]
        title = post["title"]["rendered"]
        content = post["content"]["rendered"]
        post_date = post["date"]

        if post_id == 6:
            continue

        matched_kw = "医療教育 ICT ガジェット"
        for key, kw in AMAZON_KEYWORDS.items():
            if key in title or key in content:
                matched_kw = kw
                break

        if "csd-gadget-box" in content and "csdaffiliate-22" not in content:
            btn_html = generate_amazon_btn_html(matched_kw)
            pattern = r'(<div class="csd-gadget-box">[\s\S]*?)(</div>)'
            match = re.search(pattern, content)
            if match:
                content = content[:match.start(2)] + btn_html + content[match.start(2):]
                
                payload = {
                    "content": content,
                    "date": post_date,
                    "status": "publish"
                }

                req_update = urllib.request.Request(
                    f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
                    data=json.dumps(payload).encode('utf-8'),
                    headers=headers,
                    method='POST'
                )

                for attempt in range(3):
                    try:
                        with urllib.request.urlopen(req_update, context=ctx) as r:
                            updated_count += 1
                            print(f"[{updated_count}] Updated ID {post_id} with Amazon link ({matched_kw})")
                            break
                    except Exception as e:
                        print(f"Retry {attempt+1} on ID {post_id}: {e}")
                        time.sleep(1)

                time.sleep(0.3)
        else:
            print(f"Skipping ID {post_id} (already has affiliate link or no gadget box)")

    print(f"\n==========================================")
    print(f"Complete: Successfully inserted Amazon affiliate links into {updated_count+1} posts.")
    print(f"==========================================")

if __name__ == "__main__":
    print("1. Updating Post 6 with Amazon links...")
    update_post_6_with_amazon()
    print("2. Updating all other posts with Amazon links...")
    update_all_posts_with_amazon()
