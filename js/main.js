// Global configuration
const currentScript = document.currentScript;
const rootPath = currentScript ? (currentScript.getAttribute('data-root') || './') : './';

document.addEventListener('DOMContentLoaded', () => {
    // 1. 各コンポーネントの読み込み
    Promise.all([
        loadComponent('header-placeholder', 'header.html'),
        loadComponent('footer-placeholder', 'footer.html')
    ]).then(() => {
        // コンポーネント読み込み後に初期化
        initMobileMenu();
        initSearch();
        initActiveNavigation();
        initSuccessModal();
    });

    // スクロール時のヘッダーシャドウ
    window.addEventListener('scroll', () => {
        const header = document.querySelector('header');
        if (header) {
            header.classList.toggle('shadow-lg', window.scrollY > 20);
        }
    });

    // --- お問い合わせフォームの送信処理 ---
    const contactForm = document.getElementById('contact-form');
    const GAS_ENDPOINT = "https://script.google.com/macros/s/AKfycbzq6KlOKz_uTEajQANSlIqYZz7OI-zjLbyxWx_OTMgT6xEe19xJdfwUBUQNa4O0sLuz/exec";

    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // お問い合わせの種類の選択チェック
            const inquiryCheckboxes = contactForm.querySelectorAll('input[name="inquiry_type"]:checked');
            if (inquiryCheckboxes.length === 0) {
                alert("「お問い合わせの種類」を1つ以上選択してください。");
                return;
            }

            const submitBtn = document.getElementById('submit-btn');
            const originalBtnContent = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin mr-2"></i> 送信中...';
            submitBtn.disabled = true;
            submitBtn.classList.add('opacity-70', 'cursor-not-allowed');

            try {
                // フォームデータの収集
                const formData = new FormData(contactForm);
                const payload = {
                    form_source: "contact"
                };

                formData.forEach((value, key) => {
                    if (key === 'interests' || key === 'inquiry_type') {
                        if (!payload[key]) {
                            payload[key] = [];
                        }
                        payload[key].push(value);
                    } else {
                        payload[key] = value;
                    }
                });

                // 配列をカンマ区切り文字列に変換（GASやLark Baseの互換性確保）
                if (Array.isArray(payload.inquiry_type)) {
                    payload.inquiry_type = payload.inquiry_type.join(', ');
                }

                // GASへデータを送信
                await fetch(GAS_ENDPOINT, {
                    method: 'POST',
                    mode: 'no-cors', // GASのCORSエラー回避用
                    headers: {
                        'Content-Type': 'text/plain',
                    },
                    body: JSON.stringify(payload)
                });

                // CONNECTの選択状態を判定してモーダルへ渡す
                const rawInterests = payload.interests || [];
                const hasConnect = Array.isArray(rawInterests)
                    ? rawInterests.includes('CONNECT')
                    : (typeof rawInterests === 'string' && rawInterests.includes('CONNECT'));

                // 成功時の処理
                if (window.showContactSuccessModal) {
                    window.showContactSuccessModal(hasConnect);
                }
                contactForm.reset();

            } catch (error) {
                console.error('Error:', error);
                alert("送信中にエラーが発生しました。もう一度お試しください。");
            } finally {
                submitBtn.innerHTML = originalBtnContent;
                submitBtn.disabled = false;
                submitBtn.classList.remove('opacity-70', 'cursor-not-allowed');
            }
        });
    }

    // --- 資料ダウンロードフォームの送信処理 ---
    const downloadForm = document.getElementById('download-form');
    if (downloadForm) {
        downloadForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // 興味のあるシステムの選択チェック
            const interestCheckboxes = downloadForm.querySelectorAll('input[name="interests"]:checked');
            if (interestCheckboxes.length === 0) {
                alert("「興味のあるシステム」を1つ以上選択してください。");
                return;
            }

            const submitBtn = document.getElementById('dl-submit-btn');
            const originalBtnContent = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin mr-2"></i> 送信中...';
            submitBtn.disabled = true;
            submitBtn.classList.add('opacity-70', 'cursor-not-allowed');

            try {
                // フォームデータの収集
                const formData = new FormData(downloadForm);
                const payload = {
                    form_source: "download",
                    inquiry_type: "資料ダウンロード"
                };

                formData.forEach((value, key) => {
                    if (key === 'interests') {
                        if (!payload[key]) {
                            payload[key] = [];
                        }
                        payload[key].push(value);
                    } else {
                        payload[key] = value;
                    }
                });

                // GASへデータを送信
                await fetch(GAS_ENDPOINT, {
                    method: 'POST',
                    mode: 'no-cors',
                    headers: {
                        'Content-Type': 'text/plain',
                    },
                    body: JSON.stringify(payload)
                });

                // 選択された項目リスト
                const rawInterests = payload.interests || [];
                const interestsList = Array.isArray(rawInterests) ? rawInterests : [rawInterests];

                // 画面上のモーダルにダウンロードボタンが表示されるため、二重ダウンロードを防ぐため自動即時ダウンロードは行わない

                // 成功モーダルの表示（選択項目を渡して動的に資料カードを生成）
                if (window.showDownloadSuccessModal) {
                    window.showDownloadSuccessModal(interestsList);
                }
                downloadForm.reset();

            } catch (error) {
                console.error('Error:', error);
                alert("送信中にエラーが発生しました。もう一度お試しください。");
            } finally {
                submitBtn.innerHTML = originalBtnContent;
                submitBtn.disabled = false;
                submitBtn.classList.remove('opacity-70', 'cursor-not-allowed');
            }
        });
    }

    // --- INTEVE LINK 専用資料ダウンロードフォームの送信処理 ---
    const ilDownloadForm = document.getElementById('inteve-link-download-form');
    if (ilDownloadForm) {
        ilDownloadForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const submitBtn = document.getElementById('il-submit-btn');
            const originalBtnContent = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin mr-2"></i> 送信中...';
            submitBtn.disabled = true;
            submitBtn.classList.add('opacity-70', 'cursor-not-allowed');

            try {
                // フォームデータの収集
                const formData = new FormData(ilDownloadForm);
                const payload = {
                    form_source: "download",
                    inquiry_type: "資料ダウンロード",
                    interests: "INTEVE LINK"
                };

                formData.forEach((value, key) => {
                    payload[key] = value;
                });

                // GASへデータを送信
                await fetch(GAS_ENDPOINT, {
                    method: 'POST',
                    mode: 'no-cors',
                    headers: {
                        'Content-Type': 'text/plain',
                    },
                    body: JSON.stringify(payload)
                });

                // 画面上のモーダルからダウンロード可能

                // 成功モーダルの表示
                if (window.showILDownloadSuccessModal) {
                    window.showILDownloadSuccessModal();
                }
                ilDownloadForm.reset();

            } catch (error) {
                console.error('Error:', error);
                alert("送信中にエラーが発生しました。もう一度お試しください。");
            } finally {
                submitBtn.innerHTML = originalBtnContent;
                submitBtn.disabled = false;
                submitBtn.classList.remove('opacity-70', 'cursor-not-allowed');
            }
        });
    }
});

/**
 * PDFファイルの自動ダウンロードをトリガーする
 */
function triggerPdfDownload(url, filename) {
    try {
        const link = document.createElement('a');
        link.href = url;
        link.download = filename || '';
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        setTimeout(() => {
            document.body.removeChild(link);
        }, 1000);
    } catch (e) {
        console.error('Auto download failed:', e);
    }
}

/**
 * コンポーネント（Header/Footer）を読み込む
 */
async function loadComponent(placeholderId, url) {
    const el = document.getElementById(placeholderId);
    if (!el) return;
    try {
        const cacheBuster = '?v=' + new Date().getTime();
        const response = await fetch(rootPath + url + cacheBuster);
        if (response.ok) {
            let html = await response.text();
            html = html.replace(/\[\[ROOT\]\]/g, rootPath);
            el.outerHTML = html;
        }
    } catch (e) {
        console.error(`Failed to load: ${url}`, e);
    }
}

/**
 * モバイルメニュー初期化
 */
function initMobileMenu() {
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuToggle && mobileMenu) {
        const mobileMenuIcon = mobileMenuToggle.querySelector('i');

        mobileMenuToggle.addEventListener('click', () => {
            const isOpen = mobileMenu.style.maxHeight && mobileMenu.style.maxHeight !== '0px';
            if (isOpen) {
                mobileMenu.style.maxHeight = '0px';
                if (mobileMenuIcon) {
                    mobileMenuIcon.classList.remove('fa-times');
                    mobileMenuIcon.classList.add('fa-bars');
                }
            } else {
                mobileMenu.style.maxHeight = '600px';
                if (mobileMenuIcon) {
                    mobileMenuIcon.classList.remove('fa-bars');
                    mobileMenuIcon.classList.add('fa-times');
                }
            }
        });
    }
}

/**
 * 検索バー初期化（アニメーション維持＋Googleサイト内検索追加）
 */
function initSearch() {
    const searchToggle = document.getElementById('search-toggle');
    const searchBar = document.getElementById('search-bar');
    const searchClose = document.getElementById('search-close');
    const searchInput = document.getElementById('search-input');

    if (!searchToggle || !searchBar) return;

    // 検索アイコンクリック時の表示・非表示トグル（フォーカス連動）
    searchToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        const isHidden = searchBar.classList.contains('hidden');
        if (isHidden) {
            searchBar.classList.remove('hidden');
            searchBar.classList.add('flex');
            setTimeout(() => searchInput && searchInput.focus(), 50);
        } else {
            searchBar.classList.add('hidden');
            searchBar.classList.remove('flex');
        }
    });

    // 「✕」ボタンクリック時
    if (searchClose) {
        searchClose.addEventListener('click', (e) => {
            e.stopPropagation();
            searchBar.classList.add('hidden');
            searchBar.classList.remove('flex');
        });
    }

    // 画面の他領域クリック時に検索バーを閉じる
    document.addEventListener('click', (e) => {
        if (!searchBar.contains(e.target) && e.target !== searchToggle) {
            searchBar.classList.add('hidden');
            searchBar.classList.remove('flex');
        }
    });

    // 検索の実行（Enterキー）
    if (searchInput) {
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const query = searchInput.value.trim();
                if (query) {
                    // Googleサイト内検索（新しいタブ）
                    const site = 'creativesd.net';
                    const url = `https://www.google.com/search?q=site:${site} ${encodeURIComponent(query)}`;
                    window.open(url, '_blank');

                    // 検索後に入力欄をクリアして閉じる
                    searchInput.value = '';
                    searchBar.classList.add('hidden');
                    searchBar.classList.remove('flex');
                }
            }
        });
    }
}

/**
 * アクティブリンクのハイライト
 */
function initActiveNavigation() {
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';

    // Desktop navigation highlight
    const navLinks = document.querySelectorAll('header nav .nav-link');
    navLinks.forEach(link => {
        const targetPath = link.getAttribute('data-path');
        if (targetPath === currentPath) {
            navLinks.forEach(l => l.classList.replace('text-secondary', 'text-slate-200'));
            navLinks.forEach(l => l.classList.replace('border-secondary', 'border-transparent'));

            link.classList.replace('text-slate-200', 'text-secondary');
            link.classList.remove('border-transparent');
            link.classList.add('border-secondary', 'border-b-2');
        }
    });
}

/**
 * 成功モーダル初期化とアニメーション
 */
function initSuccessModal() {
    // お問い合わせ成功モーダル
    const modal = document.getElementById('success-modal');
    if (modal) {
        const closeBtn = document.getElementById('close-success-modal');
        const backdrop = document.getElementById('success-modal-backdrop');

        const closeModal = () => {
            modal.classList.add('opacity-0', 'pointer-events-none');
            const content = document.getElementById('success-modal-content');
            if (content) {
                content.classList.replace('scale-100', 'scale-95');
            }
        };

        if (closeBtn) closeBtn.addEventListener('click', closeModal);
        if (backdrop) backdrop.addEventListener('click', closeModal);
    }

    // 資料ダウンロード成功モーダル
    const dlModal = document.getElementById('dl-success-modal');
    if (dlModal) {
        const dlCloseBtn = document.getElementById('close-dl-success-modal');
        const dlBackdrop = document.getElementById('dl-success-modal-backdrop');

        const closeDlModal = () => {
            dlModal.classList.add('opacity-0', 'pointer-events-none');
            const content = document.getElementById('dl-success-modal-content');
            if (content) {
                content.classList.replace('scale-100', 'scale-95');
            }
        };

        if (dlCloseBtn) dlCloseBtn.addEventListener('click', closeDlModal);
        if (dlBackdrop) dlBackdrop.addEventListener('click', closeDlModal);
    }

    // INTEVE LINK 専用資料ダウンロード成功モーダル
    const ilModal = document.getElementById('il-success-modal');
    if (ilModal) {
        const ilCloseBtn = document.getElementById('close-il-success-modal');
        const ilBackdrop = document.getElementById('il-success-modal-backdrop');

        const closeIlModal = () => {
            ilModal.classList.add('opacity-0', 'pointer-events-none');
            const content = document.getElementById('il-success-modal-content');
            if (content) {
                content.classList.replace('scale-100', 'scale-95');
            }
        };

        if (ilCloseBtn) ilCloseBtn.addEventListener('click', closeIlModal);
        if (ilBackdrop) ilBackdrop.addEventListener('click', closeIlModal);
    }
}

// Make globally accessible functions to show the modal from the form submit handler
window.showContactSuccessModal = function (hasConnect = false) {
    const modal = document.getElementById('success-modal');
    if (modal) {
        const connectCard = document.getElementById('connect-download-card');
        if (connectCard) {
            if (hasConnect) {
                connectCard.classList.remove('hidden');
            } else {
                connectCard.classList.add('hidden');
            }
        }

        modal.classList.remove('opacity-0', 'pointer-events-none');
        const content = document.getElementById('success-modal-content');
        if (content) {
            setTimeout(() => {
                content.classList.replace('scale-95', 'scale-100');
            }, 10);
        }
    }
    trackEvent('form_submission', 'Contact Form Success');
};

window.showDownloadSuccessModal = function (selectedInterests = []) {
    const modal = document.getElementById('dl-success-modal');
    if (modal) {
        const container = document.getElementById('dl-materials-container');
        if (container) {
            container.innerHTML = ''; // クリア

            const interests = Array.isArray(selectedInterests) ? selectedInterests : [selectedInterests];
            let cardsHtml = '';
            let downloadableFiles = [];

            // 1. CONNECT
            if (interests.includes('CONNECT')) {
                downloadableFiles.push({
                    name: 'CONNECT_Leaflet_A4.pdf',
                    path: 'files/CONNECT_Leaflet_A4.pdf'
                });
                cardsHtml += `
                <div class="bg-teal-50/90 border border-teal-200 rounded-2xl p-4 space-y-3">
                    <div class="flex items-start gap-3">
                        <div class="w-10 h-10 rounded-xl bg-teal-100 text-teal-600 flex items-center justify-center text-xl shrink-0">
                            <i class="fas fa-file-pdf"></i>
                        </div>
                        <div class="flex-1">
                            <span class="text-[10px] bg-teal-100 text-teal-800 px-2 py-0.5 rounded font-bold">CONNECT 資料</span>
                            <h4 class="font-bold text-slate-900 text-xs sm:text-sm mt-0.5">CONNECT サービス紹介（A4リーフレット）</h4>
                            <p class="text-[11px] text-slate-500 mt-0.5">AI即レス予約・カレンダー連携の機能概要</p>
                        </div>
                    </div>
                    <a href="files/CONNECT_Leaflet_A4.pdf" download="CONNECT_Leaflet_A4.pdf" target="_blank" class="w-full py-2.5 px-4 bg-teal-600 hover:bg-teal-700 text-white font-bold rounded-xl shadow-sm flex items-center justify-center gap-2 text-xs transition-all transform hover:-translate-y-0.5">
                        <i class="fas fa-download"></i>
                        <span>CONNECT 資料（A4）をダウンロード</span>
                    </a>
                </div>`;
            }

            // 2. 国家試験管理
            if (interests.includes('国家試験管理')) {
                downloadableFiles.push({
                    name: 'EXAM_Leaflet_A4.pdf',
                    path: 'files/EXAM_Leaflet_A4.pdf'
                });
                cardsHtml += `
                <div class="bg-indigo-50/90 border border-indigo-200 rounded-2xl p-4 space-y-3">
                    <div class="flex items-start gap-3">
                        <div class="w-10 h-10 rounded-xl bg-indigo-100 text-indigo-600 flex items-center justify-center text-xl shrink-0">
                            <i class="fas fa-file-pdf"></i>
                        </div>
                        <div class="flex-1">
                            <span class="text-[10px] bg-indigo-100 text-indigo-800 px-2 py-0.5 rounded font-bold">国家試験管理 資料</span>
                            <h4 class="font-bold text-slate-900 text-xs sm:text-sm mt-0.5">国家試験管理システム（A4リーフレット）</h4>
                            <p class="text-[11px] text-slate-500 mt-0.5">国試対策・過去問分析・成績推移機能の詳細</p>
                        </div>
                    </div>
                    <a href="files/EXAM_Leaflet_A4.pdf" download="EXAM_Leaflet_A4.pdf" target="_blank" class="w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow-sm flex items-center justify-center gap-2 text-xs transition-all transform hover:-translate-y-0.5">
                        <i class="fas fa-download"></i>
                        <span>国家試験管理 資料（A4）をダウンロード</span>
                    </a>
                </div>`;
            }

            // 3. 学事（教務マネジメントDX）
            if (interests.includes('学事') || interests.includes('学事・経理') || interests.includes('教務')) {
                downloadableFiles.push({
                    name: 'KYOMU_Leaflet_A4.pdf',
                    path: 'files/KYOMU_Leaflet_A4.pdf'
                });
                cardsHtml += `
                <div class="bg-blue-50/90 border border-blue-200 rounded-2xl p-4 space-y-3">
                    <div class="flex items-start gap-3">
                        <div class="w-10 h-10 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center text-xl shrink-0">
                            <i class="fas fa-file-pdf"></i>
                        </div>
                        <div class="flex-1">
                            <span class="text-[10px] bg-blue-100 text-blue-800 px-2 py-0.5 rounded font-bold">学事システム 資料</span>
                            <h4 class="font-bold text-slate-900 text-xs sm:text-sm mt-0.5">教務・学事マネジメントシステム（A4リーフレット）</h4>
                            <p class="text-[11px] text-slate-500 mt-0.5">カリキュラム設計・履修登録・基本時間割・出欠管理の一元化</p>
                        </div>
                    </div>
                    <a href="files/KYOMU_Leaflet_A4.pdf" download="KYOMU_Leaflet_A4.pdf" target="_blank" class="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-sm flex items-center justify-center gap-2 text-xs transition-all transform hover:-translate-y-0.5">
                        <i class="fas fa-download"></i>
                        <span>学事システム 資料（A4）をダウンロード</span>
                    </a>
                </div>`;
            }

            // 4. マーケティング / 入試・広報
            if (interests.includes('マーケティング') || interests.includes('入試・広報') || interests.includes('入試')) {
                downloadableFiles.push({
                    name: 'NYUSHI_Leaflet_A4.pdf',
                    path: 'files/NYUSHI_Leaflet_A4.pdf'
                });
                cardsHtml += `
                <div class="bg-amber-50/90 border border-amber-200 rounded-2xl p-4 space-y-3">
                    <div class="flex items-start gap-3">
                        <div class="w-10 h-10 rounded-xl bg-amber-100 text-amber-600 flex items-center justify-center text-xl shrink-0">
                            <i class="fas fa-file-pdf"></i>
                        </div>
                        <div class="flex-1">
                            <span class="text-[10px] bg-amber-100 text-amber-800 px-2 py-0.5 rounded font-bold">入試・広報 資料</span>
                            <h4 class="font-bold text-slate-900 text-xs sm:text-sm mt-0.5">入試・広報マネジメントDX（A4リーフレット）</h4>
                            <p class="text-[11px] text-slate-500 mt-0.5">オープンキャンパス受付・志願者追跡・ワンクリックデータ移行</p>
                        </div>
                    </div>
                    <a href="files/NYUSHI_Leaflet_A4.pdf" download="NYUSHI_Leaflet_A4.pdf" target="_blank" class="w-full py-2.5 px-4 bg-amber-600 hover:bg-amber-700 text-white font-bold rounded-xl shadow-sm flex items-center justify-center gap-2 text-xs transition-all transform hover:-translate-y-0.5">
                        <i class="fas fa-download"></i>
                        <span>入試・広報 資料（A4）をダウンロード</span>
                    </a>
                </div>`;
            }

            // 5. INTEVE LINK または 実習管理
            if (interests.includes('INTEVE LINK') || interests.includes('実習管理')) {
                downloadableFiles.push({
                    name: 'INTEVE_LINK_Leaflet_A4.pdf',
                    path: 'files/INTEVE_LINK_Leaflet_A4.pdf'
                });
                cardsHtml += `
                <div class="bg-teal-50/90 border border-teal-200 rounded-2xl p-4 space-y-3">
                    <div class="flex items-start gap-3">
                        <div class="w-10 h-10 rounded-xl bg-teal-100 text-teal-600 flex items-center justify-center text-xl shrink-0">
                            <i class="fas fa-file-pdf"></i>
                        </div>
                        <div class="flex-1">
                            <span class="text-[10px] bg-teal-100 text-teal-800 px-2 py-0.5 rounded font-bold">臨床実習 Webアプリ 資料</span>
                            <h4 class="font-bold text-slate-900 text-xs sm:text-sm mt-0.5">臨床実習管理ポータル INTEVE LINK（A4リーフレット）</h4>
                            <p class="text-[11px] text-slate-500 mt-0.5">実習生・指導者・教員の三者リアルタイム共有（体調・出欠サイン・日誌・チェックリスト）</p>
                        </div>
                    </div>
                    <a href="files/INTEVE_LINK_Leaflet_A4.pdf" download="INTEVE_LINK_Leaflet_A4.pdf" target="_blank" class="w-full py-2.5 px-4 bg-teal-600 hover:bg-teal-700 text-white font-bold rounded-xl shadow-sm flex items-center justify-center gap-2 text-xs transition-all transform hover:-translate-y-0.5">
                        <i class="fas fa-download"></i>
                        <span>INTEVE LINK 資料（A4）をダウンロード</span>
                    </a>
                    <div class="pt-0.5 text-center">
                        <a href="files/INTEVE_LINK_Security.pdf" download="INTEVE_LINK_Security.pdf" target="_blank" class="text-[11px] text-slate-500 hover:text-teal-700 inline-flex items-center gap-1.5 transition-colors">
                            <i class="fas fa-shield-alt text-slate-400"></i>
                            <span>セキュリティ仕様書 (PDF) もあわせてダウンロード</span>
                        </a>
                    </div>
                </div>`;
            }

            // フォールバック（マッチする資料が何もない場合）
            if (downloadableFiles.length === 0) {
                cardsHtml = `
                <div class="bg-cyan-50/90 border border-cyan-200 rounded-2xl p-4 space-y-3">
                    <div class="flex items-start gap-3">
                        <div class="w-10 h-10 rounded-xl bg-cyan-100 text-cyan-600 flex items-center justify-center text-xl shrink-0">
                            <i class="fas fa-file-pdf"></i>
                        </div>
                        <div class="flex-1">
                            <h4 class="font-bold text-slate-900 text-xs sm:text-sm">サービス概要資料</h4>
                            <p class="text-[11px] text-slate-500 mt-0.5">Creative System Design システム概要リーフレット</p>
                        </div>
                    </div>
                    <a href="files/INTEVE_LINK_Leaflet_A4.pdf" download="INTEVE_LINK_Leaflet_A4.pdf" target="_blank" class="w-full py-2.5 px-4 bg-secondary hover:bg-cyan-600 text-white font-bold rounded-xl shadow-sm flex items-center justify-center gap-2 text-xs transition-all transform hover:-translate-y-0.5">
                        <i class="fas fa-download"></i>
                        <span>資料をダウンロード (PDF)</span>
                    </a>
                </div>`;
            }

            // 複数選択されている場合（2つ以上の資料がある場合）、一括ダウンロードボタンを上部に配置
            let batchDownloadHeader = '';
            if (downloadableFiles.length >= 2) {
                batchDownloadHeader = `
                <div class="mb-4">
                    <button type="button" id="btn-download-all-materials" class="w-full py-3 px-4 bg-gradient-to-r from-accent to-orange-600 hover:from-orange-500 hover:to-orange-600 text-white font-bold rounded-xl shadow-md flex items-center justify-center gap-2 text-xs sm:text-sm transition-all transform hover:-translate-y-0.5">
                        <i class="fas fa-file-archive text-base"></i>
                        <span>選択した資料をすべてまとめてダウンロード (${downloadableFiles.length}点)</span>
                    </button>
                    <p class="text-[10px] text-slate-400 text-center mt-1.5">※ 各資料は下の個別ボタンからも個別にダウンロードいただけます</p>
                </div>`;
            }

            container.innerHTML = batchDownloadHeader + cardsHtml;

            // 一括ダウンロードボタンのイベント付与
            const batchBtn = document.getElementById('btn-download-all-materials');
            if (batchBtn) {
                batchBtn.addEventListener('click', () => {
                    downloadableFiles.forEach((file, index) => {
                        setTimeout(() => {
                            const a = document.createElement('a');
                            a.href = file.path;
                            a.download = file.name;
                            a.target = '_blank';
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                        }, index * 300);
                    });
                });
            }

            // 画面上のモーダルからユーザーが明示的にボタンをクリックしてダウンロードする設計のため、
            // 勝手に即時ダウンロードが始まる自動トリガーは行わない
        }

        modal.classList.remove('opacity-0', 'pointer-events-none');
        const content = document.getElementById('dl-success-modal-content');
        if (content) {
            setTimeout(() => {
                content.classList.replace('scale-95', 'scale-100');
            }, 10);
        }
    }
    trackEvent('form_submission', 'Download Form Success');
};

window.showILDownloadSuccessModal = function () {
    const modal = document.getElementById('il-success-modal');
    if (modal) {
        modal.classList.remove('opacity-0', 'pointer-events-none');
        const content = document.getElementById('il-success-modal-content');
        if (content) {
            setTimeout(() => {
                content.classList.replace('scale-95', 'scale-100');
            }, 10);
        }
    }
    trackEvent('form_submission', 'INTEVE LINK Download Form Success');
};

/**
 * Google Analytics Event Tracker
 */
function trackEvent(name, label) {
    if (typeof gtag === 'function') {
        gtag('event', name, {
            'event_category': 'interactive',
            'event_label': label || name
        });
        console.log(`GA Tracked: ${name} - ${label}`);
    }
}

/**
 * Global click listener for [data-ga-click]
 */
document.addEventListener('click', (e) => {
    const target = e.target.closest('[data-ga-click]');
    if (target) {
        const label = target.getAttribute('data-ga-click');
        trackEvent('button_click', label);
    }
});