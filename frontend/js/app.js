document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const targetBtns = document.querySelectorAll(".target-btn");
    const inputText = document.getElementById("inputText");
    const outputText = document.getElementById("outputText");
    const charCount = document.getElementById("charCount");
    const convertBtn = document.getElementById("convertBtn");
    const btnSpinner = document.getElementById("btnSpinner");
    const copyBtn = document.getElementById("copyBtn");
    const copyBtnText = document.getElementById("copyBtnText");
    const loadingOverlay = document.getElementById("loadingOverlay");
    const toast = document.getElementById("toast");

    const API_BASE = window.location.origin;

    // Tailwind Active Classes
    const activeClasses = ["ring-2", "ring-indigo-500", "bg-indigo-500/10", "border-indigo-500/50", "active"];

    // 1. Target Audience Button Selection (Single Active Toggle)
    targetBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            targetBtns.forEach(b => {
                b.classList.remove(...activeClasses);
            });
            btn.classList.add(...activeClasses);
        });
    });

    // 2. Character Counter
    inputText.addEventListener("input", () => {
        charCount.textContent = inputText.value.length;
    });

    // 3. Convert Tone API Call
    async function convertTone() {
        const text = inputText.value.trim();
        const activeBtn = document.querySelector(".target-btn.active");
        const targetAudience = activeBtn ? activeBtn.dataset.target : null;

        if (!text) {
            showToast("⚠️ 변환할 원문 내용을 입력해주세요.");
            inputText.focus();
            return;
        }

        if (!targetAudience) {
            showToast("⚠️ 수신 대상을 선택해주세요.");
            return;
        }

        setLoadingState(true);

        try {
            const response = await fetch(`${API_BASE}/api/convert`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: text,
                    target_audience: targetAudience
                })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || "말투 변환 중 오류가 발생했습니다.");
            }

            const data = await response.json();
            
            outputText.value = data.converted_text;
            copyBtn.disabled = false;
            showToast("✨ 비즈니스 말투 변환이 완료되었습니다!");

        } catch (error) {
            console.error("Convert Error:", error);
            showToast(`❌ ${error.message}`);
        } finally {
            setLoadingState(false);
        }
    }

    // 4. Loading State Toggle
    function setLoadingState(isLoading) {
        if (isLoading) {
            convertBtn.disabled = true;
            btnSpinner.classList.remove("hidden");
            loadingOverlay.classList.remove("hidden");
        } else {
            convertBtn.disabled = false;
            btnSpinner.classList.add("hidden");
            loadingOverlay.classList.add("hidden");
        }
    }

    // 5. Copy to Clipboard
    async function copyToClipboard() {
        const textToCopy = outputText.value;
        if (!textToCopy) return;

        try {
            await navigator.clipboard.writeText(textToCopy);
            copyBtnText.textContent = "✅ 복사 완료!";
            showToast("📋 클립보드에 복사되었습니다!");
            
            setTimeout(() => {
                copyBtnText.textContent = "📋 복사하기";
            }, 2000);
        } catch (err) {
            outputText.select();
            document.execCommand("copy");
            showToast("📋 클립보드에 복사되었습니다!");
        }
    }

    // 6. Toast Notification Helper
    let toastTimeout;
    function showToast(message) {
        toast.textContent = message;
        toast.classList.remove("hidden");

        clearTimeout(toastTimeout);
        toastTimeout = setTimeout(() => {
            toast.classList.add("hidden");
        }, 3000);
    }

    // Event Listeners
    convertBtn.addEventListener("click", convertTone);
    copyBtn.addEventListener("click", copyToClipboard);
});
