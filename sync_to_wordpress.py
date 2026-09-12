import json
import base64
import urllib.request
import urllib.error
import os
import re
import sys

WP_URL = "https://affiliate.creativesd.net"
WP_USER = "creativesd_affiliate"
WP_APP_PASS = "mhJs ti3i ZgRz XVIC LPxb 5Hcf".replace(" ", "")

MAIN_SITE_URL = "https://creativesd.net/"

credentials = f"{WP_USER}:{WP_APP_PASS}"
encoded_creds = base64.b64encode(credentials.encode()).decode("utf-8")

def update_global_styles_css():
    api_url = f"{WP_URL}/wp-json/wp/v2/global-styles/8"
    
    # Import CSS and fonts directly from CDN and main site + enforce dark theme (#0f172a)
    css_imports = """
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css");
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap");
@import url("https://creativesd.net/css/style.css");
@import url("https://creativesd.net/css/wp-header-footer.css");
"""
    payload = {
        "styles": {
            "css": css_imports,
            "color": {
                "text": "#e2e8f0",
                "background": "#0f172a"
            },
            "elements": {
                "heading": {
                    "color": {
                        "text": "#ffffff"
                    }
                },
                "link": {
                    "color": {
                        "text": "#00BCD4"
                    }
                }
            }
        }
    }
    req = urllib.request.Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_creds}",
            "User-Agent": "Mozilla/5.0 (compatible; WordPressAPIClient/1.0)",
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print("SUCCESS: Updated WordPress <head> CSS & Dark Theme Global Styles.")
            return True
    except Exception as e:
        print(f"Error on Global Styles CSS: {e}", file=sys.stderr)
        return False

def update_template_part(slug, content):
    api_url = f"{WP_URL}/wp-json/wp/v2/template-parts/twentytwentyfive//{slug}"
    payload = {
        "content": content
    }
    req = urllib.request.Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_creds}",
            "User-Agent": "Mozilla/5.0 (compatible; WordPressAPIClient/1.0)",
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"SUCCESS: Synced template-part [{slug}] to WordPress.")
            return True
    except urllib.error.HTTPError as e:
        print(f"HTTPError {e.code} on [{slug}]: {e.reason}", file=sys.stderr)
        print(e.read().decode("utf-8"), file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error on [{slug}]: {e}", file=sys.stderr)
        return False

def update_templates():
    # 1. Single Post Template
    single_content = """<!-- wp:template-part {"slug":"header","theme":"twentytwentyfive"} /-->

<!-- wp:group {"tagName":"main","style":{"spacing":{"margin":{"top":"0","bottom":"0"},"padding":{"top":"40px","bottom":"80px","left":"20px","right":"20px"}}},"layout":{"type":"constrained","contentSize":"900px"}} -->
<main class="wp-block-group" style="margin-top:0;margin-bottom:0;padding-top:40px;padding-right:20px;padding-bottom:80px;padding-left:20px;max-width:900px;margin-left:auto;margin-right:auto;color:#e2e8f0;">
	<!-- wp:post-title {"level":1,"style":{"typography":{"fontSize":"2.2rem","lineHeight":"1.4","fontWeight":"700"},"color":{"text":"#ffffff"},"spacing":{"margin":{"bottom":"32px"}}}} /-->
	
	<!-- wp:post-content {"layout":{"type":"constrained"}} /-->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","theme":"twentytwentyfive"} /-->"""

    # 2. Home / Index Template
    home_content = """<!-- wp:template-part {"slug":"header","theme":"twentytwentyfive"} /-->

<!-- wp:group {"tagName":"main","style":{"spacing":{"padding":{"top":"56px","bottom":"80px","left":"20px","right":"20px"}}},"layout":{"type":"constrained","contentSize":"1000px"}} -->
<main class="wp-block-group" style="padding-top:56px;padding-bottom:80px;padding-left:20px;padding-right:20px;max-width:1000px;margin-left:auto;margin-right:auto;color:#e2e8f0;">
    <div style="text-align:center;margin-bottom:56px;">
        <span style="background:rgba(0,188,212,0.15);color:#38bdf8;border:1px solid rgba(0,188,212,0.4);padding:6px 18px;border-radius:9999px;font-size:0.85rem;font-weight:700;display:inline-block;margin-bottom:16px;">CSD EDUCATION COLUMN</span>
        <h1 style="color:#ffffff;font-size:2.4rem;font-weight:800;margin:0 0 16px 0;letter-spacing:-0.02em;">教育現場のお役立ちコラム・ICT情報</h1>
        <p style="color:#94a3b8;font-size:1.1rem;max-width:640px;margin:0 auto;line-height:1.7;">医療系養成校の教員業務効率化、授業・実習支援、国家試験対策のノウハウをお届けします。</p>
    </div>

	<!-- wp:query {"query":{"perPage":10,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","author":"","search":"","exclude":[],"sticky":"","inherit":true},"layout":{"type":"default"}} -->
	<div class="wp-block-query">
		<!-- wp:post-template {"layout":{"type":"default"}} -->
			<!-- wp:group {"style":{"spacing":{"padding":{"top":"28px","bottom":"28px","left":"28px","right":"28px"},"margin":{"bottom":"24px"}},"border":{"radius":"20px","width":"1px","color":"rgba(255,255,255,0.1)"}},"backgroundColor":"transparent"} -->
			<div class="wp-block-group" style="border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:28px;margin-bottom:24px;background-color:#1e293b;box-shadow:0 10px 25px -5px rgba(0,0,0,0.3);">
				<!-- wp:post-title {"level":2,"isLink":true,"style":{"typography":{"fontSize":"1.4rem","fontWeight":"700"},"color":{"text":"#ffffff"}}} /-->
				<!-- wp:post-excerpt {"moreText":"続きを読む →","style":{"typography":{"fontSize":"0.95rem"},"color":{"text":"#94a3b8"}}} /-->
				<!-- wp:post-date {"style":{"typography":{"fontSize":"0.85rem"},"color":{"text":"#64748b"}}} /-->
			</div>
			<!-- /wp:group -->
		<!-- /wp:post-template -->

		<!-- wp:query-pagination {"layout":{"type":"flex","justifyContent":"center"}} -->
			<!-- wp:query-pagination-previous /-->
			<!-- wp:query-pagination-numbers /-->
			<!-- wp:query-pagination-next /-->
		<!-- /wp:query-pagination -->
	</div>
	<!-- /wp:query -->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","theme":"twentytwentyfive"} /-->"""

    for slug, content in [("single", single_content), ("home", home_content), ("index", home_content)]:
        api_url = f"{WP_URL}/wp-json/wp/v2/templates/twentytwentyfive//{slug}"
        req = urllib.request.Request(
            api_url,
            data=json.dumps({"content": content}).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": f"Basic {encoded_creds}"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req) as resp:
                print(f"SUCCESS: Synced template [{slug}] to WordPress.")
        except Exception as e:
            print(f"Error on template [{slug}]: {e}", file=sys.stderr)

def sync_header_and_footer():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    header_path = os.path.join(base_dir, "header.html")
    footer_path = os.path.join(base_dir, "footer.html")

    if not os.path.exists(header_path) or not os.path.exists(footer_path):
        print("Error: header.html or footer.html not found.", file=sys.stderr)
        return

    # 1. Sync CSS & Webfont Imports to WordPress <head>
    update_global_styles_css()

    # 2. Sync Templates (single, home, index)
    update_templates()

    # 3. Process Header from master header.html
    with open(header_path, "r", encoding="utf-8") as f:
        header_html = f.read()

    header_html = header_html.replace("[[ROOT]]", MAIN_SITE_URL)
    header_html = header_html.replace('src="assets/', f'src="{MAIN_SITE_URL}assets/')
    header_html = header_html.replace('src="images/', f'src="{MAIN_SITE_URL}images/')
    header_html = re.sub(r'<script.*?</script>', '', header_html, flags=re.DOTALL)

    # 4. Process Footer from master footer.html
    with open(footer_path, "r", encoding="utf-8") as f:
        footer_html = f.read()

    footer_html = re.sub(r'href="([^":/]+\.html)"', lambda m: f'href="{MAIN_SITE_URL}{m.group(1)}"', footer_html)

    header_block = f"<!-- wp:html -->\n{header_html}\n<!-- /wp:html -->"
    footer_block = f"<!-- wp:html -->\n{footer_html}\n<!-- /wp:html -->"

    print("Syncing header.html to WordPress...")
    update_template_part("header", header_block)

    print("Syncing footer.html to WordPress...")
    update_template_part("footer", footer_block)

if __name__ == "__main__":
    sync_header_and_footer()
