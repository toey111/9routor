// UI Utilities: Toast, Minimal Modal, Dialogs, Formatters

const ui = {
    showToast(message, type = "success", duration = 3500) {
        let container = document.getElementById("toast-container");
        if (!container) {
            container = document.createElement("div");
            container.id = "toast-container";
            document.body.appendChild(container);
        }

        const isDark = document.body.getAttribute("data-theme") === "dark";

        const typeStyles = {
            success: isDark 
                ? "bg-slate-900/95 border-emerald-500/40 text-emerald-300"
                : "bg-white/95 border-emerald-200 text-emerald-800 shadow-md",
            error: isDark 
                ? "bg-slate-900/95 border-rose-500/40 text-rose-300"
                : "bg-white/95 border-rose-200 text-rose-800 shadow-md",
            warning: isDark 
                ? "bg-slate-900/95 border-amber-500/40 text-amber-300"
                : "bg-white/95 border-amber-200 text-amber-800 shadow-md",
            info: isDark 
                ? "bg-slate-900/95 border-blue-500/40 text-blue-300"
                : "bg-white/95 border-blue-200 text-blue-800 shadow-md"
        };

        const iconColors = {
            success: "text-emerald-500",
            error: "text-rose-500",
            warning: "text-amber-500",
            info: "text-blue-500"
        };

        const icons = {
            success: `<svg class="w-4 h-4 flex-shrink-0 ${iconColors.success}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M5 13l4 4L19 7"/></svg>`,
            error: `<svg class="w-4 h-4 flex-shrink-0 ${iconColors.error}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M6 18L18 6M6 6l12 12"/></svg>`,
            warning: `<svg class="w-4 h-4 flex-shrink-0 ${iconColors.warning}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>`,
            info: `<svg class="w-4 h-4 flex-shrink-0 ${iconColors.info}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`
        };

        const toast = document.createElement("div");
        toast.className = `toast border ${typeStyles[type] || typeStyles.info}`;
        toast.innerHTML = `
            ${icons[type] || icons.info}
            <span class="flex-1 text-xs font-medium">${message}</span>
            <button onclick="this.parentElement.remove()" class="opacity-50 hover:opacity-100 transition-opacity p-0.5">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
        `;

        container.appendChild(toast);

        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.opacity = "0";
                toast.style.transform = "translateY(-10px) scale(0.95)";
                toast.style.transition = "all 0.25s ease";
                setTimeout(() => toast.remove(), 250);
            }
        }, duration);
    },

    confirmModal({ title, message, confirmText = "ยืนยันการลบ", confirmColor = "bg-rose-600 hover:bg-rose-700", onConfirm }) {
        const modal = document.createElement("div");
        modal.className = "fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4";
        modal.innerHTML = `
            <div class="bg-white dark:bg-slate-900 rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-200 dark:border-slate-800 scale-100 transition-all">
                <div class="flex items-start gap-3.5 mb-4">
                    <div class="w-10 h-10 rounded-xl bg-rose-50 dark:bg-rose-950/50 text-rose-600 dark:text-rose-400 flex items-center justify-center flex-shrink-0 border border-rose-100 dark:border-rose-900/50">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                    </div>
                    <div class="flex-1">
                        <h3 class="text-base font-bold text-slate-800 dark:text-slate-100 leading-tight">${title}</h3>
                        <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 leading-relaxed">${message}</p>
                    </div>
                </div>
                <div class="flex items-center justify-end gap-2.5 mt-6 pt-3 border-t border-slate-100 dark:border-slate-800">
                    <button id="cancel-btn" class="px-4 py-2 text-xs font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl transition-colors">ยกเลิก</button>
                    <button id="confirm-btn" class="px-4 py-2 text-xs font-semibold text-white ${confirmColor} rounded-xl shadow-sm transition-all">${confirmText}</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        modal.querySelector("#cancel-btn").onclick = () => modal.remove();
        modal.querySelector("#confirm-btn").onclick = () => {
            modal.remove();
            if (typeof onConfirm === "function") onConfirm();
        };
    },

    formatDateThai(dateString) {
        if (!dateString) return "-";
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return dateString;
        const months = [
            "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
            "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."
        ];
        const day = date.getDate();
        const month = months[date.getMonth()];
        let year = date.getFullYear();
        if (year < 2400) {
            year += 543;
        }
        return `${day} ${month} ${year}`;
    },

    highlightError(elementId, message = "") {
        const el = typeof elementId === "string" ? document.getElementById(elementId) : elementId;
        if (!el) return;
        el.classList.add("input-error", "shake-anim");
        el.focus();
        if (message) {
            this.showToast(message, "warning");
        }
        const removeError = () => {
            el.classList.remove("input-error", "shake-anim");
            el.removeEventListener("input", removeError);
            el.removeEventListener("change", removeError);
        };
        el.addEventListener("input", removeError);
        el.addEventListener("change", removeError);
    }
};

window.ui = ui;
