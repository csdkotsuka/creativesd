/**
 * Chat Survey Widget for Creative System Design / INTEVE SCHOOL
 * 
 * Provides a floating Messenger-style survey widget connected to Google Forms / Spreadsheet.
 */

(function () {
    'use strict';

    // =========================================================================
    // Configuration
    // Googleフォームの公開エンドポイントまたはGASエンドポイントを設定
    // =========================================================================
    const SURVEY_CONFIG = {
        // Google Formsのエンドポイント
        // 例: https://docs.google.com/forms/d/e/1FAIpQLScXXXXXXXXXXXXX/formResponse
        // または https://docs.google.com/forms/d/1FVg6_D5ngwdzAzM5Ob3I4_MjBs2uP7gIm7gp62GwwBE/formResponse
        formActionUrl: "https://docs.google.com/forms/d/1FVg6_D5ngwdzAzM5Ob3I4_MjBs2uP7gIm7gp62GwwBE/formResponse",

        // または GAS (Google Apps Script) のウェブアプリURLを使用する場合
        gasEndpointUrl: "https://script.google.com/macros/s/AKfycbzq6KlOKz_uTEajQANSlIqYZz7OI-zjLbyxWx_OTMgT6xEe19xJdfwUBUQNa4O0sLuz/exec",
        useGas: true, // Googleフォームが非公開・ログイン制限されている場合はGASモードをデフォルトにして確実にスプレッドシート蓄積可能にする

        // 設問定義（Google Formの各entry.XXXXXX または GAS用のキー）
        fields: {
            organizationType: {
                name: "organization_type",
                entryName: "entry.1000001", // Googleフォームのentry ID
                label: "ご所属・お立場"
            },
            challenges: {
                name: "challenges",
                entryName: "entry.1000002",
                label: "現在の課題・関心事項"
            },
            interestFeature: {
                name: "interest_feature",
                entryName: "entry.1000003",
                label: "特に気になる機能"
            },
            feedback: {
                name: "feedback",
                entryName: "entry.1000004",
                label: "ご意見・ご質問"
            }
        }
    };

    // =========================================================================
    // DOM Template Injection
    // =========================================================================
    function createWidgetDOM() {
        const container = document.createElement('div');
        container.className = 'survey-widget-container';
        container.id = 'survey-widget';

        container.innerHTML = `
            <!-- Callout Tooltip Bubble -->
            <div class="survey-callout" id="survey-callout">
                <span>💬 <strong>30秒で完了</strong> アンケートにご協力ください</span>
                <button class="survey-callout-close" id="survey-callout-close" aria-label="閉じる">
                    <i class="fas fa-times"></i>
                </button>
            </div>

            <!-- Floating Launcher Button -->
            <button class="survey-launcher-btn" id="survey-launcher-btn" aria-label="アンケートを開く">
                <i class="fas fa-comment-dots" id="survey-launcher-icon"></i>
                <span class="survey-badge" id="survey-badge"></span>
            </button>

            <!-- Survey Popup Window -->
            <div class="survey-window" id="survey-window" role="dialog" aria-modal="true" aria-labelledby="survey-window-title">
                <!-- Header -->
                <div class="survey-header">
                    <div class="survey-header-info">
                        <div class="survey-avatar">
                            <i class="fas fa-graduation-cap"></i>
                        </div>
                        <div class="survey-header-text">
                            <h3 id="survey-window-title">INTEVE SCHOOL アンケート</h3>
                            <p>サービス向上のためのご意見募集（約1分）</p>
                        </div>
                    </div>
                    <div class="survey-header-actions">
                        <button class="survey-action-btn" id="survey-close-btn" title="閉じる" aria-label="アンケートを閉じる">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>

                <!-- Body (Form) -->
                <div class="survey-body" id="survey-body-view">
                    <!-- Chat Greeting -->
                    <div class="survey-chat-bubble">
                        こんにちは！INTEVE SCHOOLにご関心をお寄せいただきありがとうございます。
                        教育DXや学事管理に関するご意見をぜひお聞かせください。
                    </div>

                    <form id="survey-inner-form">
                        <!-- Question 1: ご所属 -->
                        <div class="survey-card mb-3">
                            <div class="survey-card-title">
                                <span>Q1. ご所属・お立場</span>
                                <span class="survey-tag-req">必須</span>
                            </div>
                            <div class="survey-options-group">
                                <label class="survey-option-label">
                                    <input type="radio" name="organization_type" value="医療系専門学校（教員・学科長）" required>
                                    <span class="survey-option-text">医療系専門学校（教員・学科長）</span>
                                </label>
                                <label class="survey-option-label">
                                    <input type="radio" name="organization_type" value="大学・短期大学（教員・教授）">
                                    <span class="survey-option-text">大学・短期大学（教員・教授）</span>
                                </label>
                                <label class="survey-option-label">
                                    <input type="radio" name="organization_type" value="学校法人 事務局・IT担当者">
                                    <span class="survey-option-text">学校法人 事務局・IT担当者</span>
                                </label>
                                <label class="survey-option-label">
                                    <input type="radio" name="organization_type" value="その他・一般">
                                    <span class="survey-option-text">その他</span>
                                </label>
                            </div>
                        </div>

                        <!-- Question 2: 課題・関心事（複数選択） -->
                        <div class="survey-card mb-3">
                            <div class="survey-card-title">
                                <span>Q2. 現在お困りの課題（複数選択可）</span>
                                <span class="survey-tag-opt">任意</span>
                            </div>
                            <div class="survey-options-group">
                                <label class="survey-option-label">
                                    <input type="checkbox" name="challenges" value="成績・出欠・学事管理の二重入力や手間">
                                    <span class="survey-option-text">成績・出欠・学事管理の手間</span>
                                </label>
                                <label class="survey-option-label">
                                    <input type="checkbox" name="challenges" value="臨床実習・実習日誌のペーパーレス化・集計">
                                    <span class="survey-option-text">臨床実習・日誌の管理・集計</span>
                                </label>
                                <label class="survey-option-label">
                                    <input type="checkbox" name="challenges" value="国家試験対策・過去問演習の効率化">
                                    <span class="survey-option-text">国家試験対策・過去問演習の効率化</span>
                                </label>
                                <label class="survey-option-label">
                                    <input type="checkbox" name="challenges" value="iPad/Mac/Win等のマルチデバイス対応">
                                    <span class="survey-option-text">マルチデバイス（iPad/Mac等）対応</span>
                                </label>
                            </div>
                        </div>

                        <!-- Question 3: 気になる機能 -->
                        <div class="survey-card mb-3">
                            <div class="survey-card-title">
                                <span>Q3. INTEVE SCHOOLで気になるポイント</span>
                                <span class="survey-tag-opt">任意</span>
                            </div>
                            <div class="survey-options-group">
                                <label class="survey-option-label">
                                    <input type="radio" name="interest_feature" value="Claris FileMakerによる柔軟なカスタマイズ性">
                                    <span class="survey-option-text">FileMakerによる柔軟なカスタマイズ</span>
                                </label>
                                <label class="survey-option-label">
                                    <input type="radio" name="interest_feature" value="学内完結・オンプレミス/LAN導入（高セキュリティ）">
                                    <span class="survey-option-text">セキュアな学内LAN・スタンドアロン導入</span>
                                </label>
                                <label class="survey-option-label">
                                    <input type="radio" name="interest_feature" value="教員の負担を大幅に削減する直感的なUI">
                                    <span class="survey-option-text">直感的で分かりやすい操作画面</span>
                                </label>
                                <label class="survey-option-label">
                                    <input type="radio" name="interest_feature" value="導入費用・デモ体験について">
                                    <span class="survey-option-text">費用感やデモ体験について</span>
                                </label>
                            </div>
                        </div>

                        <!-- Question 4: 自由記述 -->
                        <div class="survey-card mb-3">
                            <div class="survey-card-title">
                                <span>Q4. ご意見・ご要望（自由記述）</span>
                                <span class="survey-tag-opt">任意</span>
                            </div>
                            <textarea 
                                name="feedback" 
                                class="survey-textarea" 
                                placeholder="ご自由に入力してください（例：実際の画面デモを見てみたい、現在のシステムからの移行について等）"
                            ></textarea>
                        </div>
                    </form>
                </div>

                <!-- Footer / Submit Button -->
                <div class="survey-footer" id="survey-footer-view">
                    <button type="button" class="survey-submit-btn" id="survey-submit-btn">
                        <span>アンケートを送信する</span>
                        <i class="fas fa-paper-plane"></i>
                    </button>
                    <div class="survey-privacy-note">
                        ※ 送信いただいたデータはサービスの改善・参考のみに活用いたします。
                    </div>
                </div>

                <!-- Success Screen (Hidden by default) -->
                <div class="survey-success-view" id="survey-success-view">
                    <div class="survey-success-icon">
                        <i class="fas fa-check"></i>
                    </div>
                    <h4 class="survey-success-title">ご協力ありがとうございました！</h4>
                    <p class="survey-success-desc">
                        お送りいただいたご意見は、INTEVE SCHOOLの機能改善・サービス向上の参考にさせていただきます。
                    </p>
                    <button type="button" class="survey-submit-btn" id="survey-done-btn" style="max-width: 200px;">
                        閉じる
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(container);
    }

    // =========================================================================
    // Widget Controller
    // =========================================================================
    function initSurveyWidget() {
        createWidgetDOM();

        const widgetContainer = document.getElementById('survey-widget');
        const launcherBtn = document.getElementById('survey-launcher-btn');
        const launcherIcon = document.getElementById('survey-launcher-icon');
        const callout = document.getElementById('survey-callout');
        const calloutClose = document.getElementById('survey-callout-close');
        const windowEl = document.getElementById('survey-window');
        const closeBtn = document.getElementById('survey-close-btn');
        const submitBtn = document.getElementById('survey-submit-btn');
        const formEl = document.getElementById('survey-inner-form');
        const bodyView = document.getElementById('survey-body-view');
        const footerView = document.getElementById('survey-footer-view');
        const successView = document.getElementById('survey-success-view');
        const doneBtn = document.getElementById('survey-done-btn');
        const badge = document.getElementById('survey-badge');

        let isOpen = false;

        // 一度回答済み、または閉じた履歴をセッション管理
        const isSurveySubmitted = sessionStorage.getItem('inteve_survey_submitted') === 'true';
        if (isSurveySubmitted) {
            if (badge) badge.style.display = 'none';
        }

        // 初期表示から3.5秒後にコールアウト吹き出しを表示
        setTimeout(() => {
            if (!isOpen && !isSurveySubmitted && sessionStorage.getItem('inteve_survey_callout_closed') !== 'true') {
                if (callout) callout.style.display = 'flex';
            }
        }, 3500);

        function toggleWindow(openState) {
            isOpen = typeof openState === 'boolean' ? openState : !isOpen;
            if (isOpen) {
                windowEl.classList.add('is-open');
                launcherIcon.className = 'fas fa-chevron-down';
                if (callout) callout.style.display = 'none';
                if (badge) badge.style.display = 'none';
            } else {
                windowEl.classList.remove('is-open');
                launcherIcon.className = 'fas fa-comment-dots';
            }
        }

        // イベントリスナー登録
        launcherBtn.addEventListener('click', () => toggleWindow());
        if (callout) {
            callout.addEventListener('click', (e) => {
                if (e.target !== calloutClose && !calloutClose.contains(e.target)) {
                    toggleWindow(true);
                }
            });
        }
        if (calloutClose) {
            calloutClose.addEventListener('click', (e) => {
                e.stopPropagation();
                callout.style.display = 'none';
                sessionStorage.setItem('inteve_survey_callout_closed', 'true');
            });
        }
        closeBtn.addEventListener('click', () => toggleWindow(false));
        doneBtn.addEventListener('click', () => toggleWindow(false));

        // 送信処理
        submitBtn.addEventListener('click', async () => {
            // バリデーション
            const requiredSelected = formEl.querySelector('input[name="organization_type"]:checked');
            if (!requiredSelected) {
                alert('「Q1. ご所属・お立場」を選択してください。');
                return;
            }

            const originalBtnContent = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> 送信中...';
            submitBtn.disabled = true;

            try {
                const formData = new FormData(formEl);
                const payload = {
                    form_type: 'survey_widget',
                    organization_type: formData.get('organization_type') || '',
                    challenges: formData.getAll('challenges').join(', ') || '特になし',
                    interest_feature: formData.get('interest_feature') || '特になし',
                    feedback: formData.get('feedback') || '',
                    submitted_at: new Date().toISOString(),
                    page_url: window.location.href
                };

                if (SURVEY_CONFIG.useGas && SURVEY_CONFIG.gasEndpointUrl) {
                    // GAS経由でスプレッドシートへ送信
                    await fetch(SURVEY_CONFIG.gasEndpointUrl, {
                        method: 'POST',
                        mode: 'no-cors',
                        headers: {
                            'Content-Type': 'text/plain',
                        },
                        body: JSON.stringify(payload)
                    });
                } else {
                    // Google Forms 直接送信 (formResponse)
                    const formBody = new URLSearchParams();
                    formBody.append(SURVEY_CONFIG.fields.organizationType.entryName, payload.organization_type);
                    formData.getAll('challenges').forEach(val => {
                        formBody.append(SURVEY_CONFIG.fields.challenges.entryName, val);
                    });
                    formBody.append(SURVEY_CONFIG.fields.interestFeature.entryName, payload.interest_feature);
                    formBody.append(SURVEY_CONFIG.fields.feedback.entryName, payload.feedback);

                    await fetch(SURVEY_CONFIG.formActionUrl, {
                        method: 'POST',
                        mode: 'no-cors',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },
                        body: formBody.toString()
                    });
                }

                // 送信成功時の表示切り替え
                sessionStorage.setItem('inteve_survey_submitted', 'true');
                bodyView.style.display = 'none';
                footerView.style.display = 'none';
                successView.style.display = 'flex';

                // Google Analytics イベントトラッキング (gtagがある場合)
                if (typeof gtag === 'function') {
                    gtag('event', 'survey_submit', {
                        'event_category': 'Engagement',
                        'event_label': 'Floating Survey Widget'
                    });
                }

            } catch (err) {
                console.error('Survey submit error:', err);
                alert('送信中にエラーが発生しました。お手数ですが再度お試しください。');
                submitBtn.innerHTML = originalBtnContent;
                submitBtn.disabled = false;
            }
        });
    }

    // DOMロード時に初期化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSurveyWidget);
    } else {
        initSurveyWidget();
    }
})();
