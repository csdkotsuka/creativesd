import json
import base64
import urllib.request
import urllib.error
import sys

WP_URL = "https://affiliate.creativesd.net"
WP_USER = "creativesd_affiliate"
WP_APP_PASS = "mhJs ti3i ZgRz XVIC LPxb 5Hcf".replace(" ", "")

credentials = f"{WP_USER}:{WP_APP_PASS}"
encoded_creds = base64.b64encode(credentials.encode()).decode("utf-8")

def update_endpoint(path, payload):
    api_url = f"{WP_URL}/wp-json{path}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        api_url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_creds}",
            "User-Agent": "Mozilla/5.0 (compatible; WordPressAPIClient/1.0)",
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"SUCCESS: {path} updated.")
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTPError {e.code} on {path}: {e.reason}", file=sys.stderr)
        print(e.read().decode("utf-8"), file=sys.stderr)
    except Exception as e:
        print(f"Error on {path}: {e}", file=sys.stderr)

# 1. Dynamic Header Component (fetches header.html from creativesd.net in real-time)
HEADER_CONTENT = """<!-- wp:html -->
<div id="csd-header-placeholder"></div>
<script src="https://creativesd.net/js/embed-nav.js?v=20260822" defer></script>
<!-- /wp:html -->"""

# 2. Dynamic Footer Component (fetches footer.html from creativesd.net in real-time)
FOOTER_CONTENT = """<!-- wp:html -->
<div id="csd-footer-placeholder"></div>
<!-- /wp:html -->"""

# 3. Single Post Template
SINGLE_CONTENT = """<!-- wp:template-part {"slug":"header","theme":"twentytwentyfive"} /-->

<!-- wp:group {"tagName":"main","style":{"spacing":{"margin":{"top":"0","bottom":"0"},"padding":{"top":"36px","bottom":"60px","left":"16px","right":"16px"}}},"layout":{"type":"constrained","contentSize":"860px"}} -->
<main class="wp-block-group" style="margin-top:0;margin-bottom:0;padding-top:36px;padding-right:16px;padding-bottom:60px;padding-left:16px;max-width:860px;margin-left:auto;margin-right:auto;">
	<!-- wp:post-title {"level":1,"style":{"typography":{"fontSize":"2rem","lineHeight":"1.4","fontWeight":"700"},"color":{"text":"#0f172a"},"spacing":{"margin":{"bottom":"24px"}}}} /-->
	
	<!-- wp:post-content {"layout":{"type":"constrained"}} /-->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","theme":"twentytwentyfive"} /-->"""

# 4. Home / Index Template
HOME_CONTENT = """<!-- wp:template-part {"slug":"header","theme":"twentytwentyfive"} /-->

<!-- wp:group {"tagName":"main","style":{"spacing":{"padding":{"top":"48px","bottom":"64px","left":"16px","right":"16px"}}},"layout":{"type":"constrained","contentSize":"960px"}} -->
<main class="wp-block-group" style="padding-top:48px;padding-bottom:64px;padding-left:16px;padding-right:16px;max-width:960px;margin-left:auto;margin-right:auto;">
    <div style="text-align:center;margin-bottom:48px;">
        <span style="background:rgba(0,188,212,0.1);color:#0369a1;border:1px solid rgba(0,188,212,0.3);padding:4px 16px;border-radius:9999px;font-size:0.85rem;font-weight:700;display:inline-block;margin-bottom:12px;">CSD EDUCATION COLUMN</span>
        <h1 style="color:#0f172a;font-size:2.2rem;font-weight:700;margin:0 0 12px 0;">教育現場のお役立ちコラム・ICT情報</h1>
        <p style="color:#64748b;font-size:1.05rem;max-width:600px;margin:0 auto;">医療系養成校の教員業務効率化、授業・実習支援、国家試験対策のノウハウをお届けします。</p>
    </div>

	<!-- wp:query {"query":{"perPage":10,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","author":"","search":"","exclude":[],"sticky":"","inherit":true},"layout":{"type":"default"}} -->
	<div class="wp-block-query">
		<!-- wp:post-template {"layout":{"type":"default"}} -->
			<!-- wp:group {"style":{"spacing":{"padding":{"top":"24px","bottom":"24px","left":"24px","right":"24px"},"margin":{"bottom":"20px"}},"border":{"radius":"16px","width":"1px","color":"#e2e8f0"}},"backgroundColor":"white"} -->
			<div class="wp-block-group" style="border:1px solid #e2e8f0;border-radius:16px;padding:24px;margin-bottom:20px;background-color:#ffffff;box-shadow:0 4px 15px -3px rgba(0,0,0,0.04);">
				<!-- wp:post-title {"level":2,"isLink":true,"style":{"typography":{"fontSize":"1.35rem","fontWeight":"700"},"color":{"text":"#004080"}}} /-->
				<!-- wp:post-excerpt {"moreText":"続きを読む →","style":{"typography":{"fontSize":"0.95rem"},"color":{"text":"#475569"}}} /-->
				<!-- wp:post-date {"style":{"typography":{"fontSize":"0.85rem"},"color":{"text":"#94a3b8"}}} /-->
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

def main():
    update_endpoint("/wp/v2/template-parts/twentytwentyfive//header", {"content": HEADER_CONTENT})
    update_endpoint("/wp/v2/template-parts/twentytwentyfive//footer", {"content": FOOTER_CONTENT})
    update_endpoint("/wp/v2/templates/twentytwentyfive//single", {"content": SINGLE_CONTENT})
    update_endpoint("/wp/v2/templates/twentytwentyfive//home", {"content": HOME_CONTENT})
    update_endpoint("/wp/v2/templates/twentytwentyfive//index", {"content": HOME_CONTENT})

if __name__ == "__main__":
    main()
