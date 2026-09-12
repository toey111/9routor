/* global auth, lucide */
// Dynamic Components: Minimalist Sidebar & Header with Morning/Dark (Light/Dark) Theme Support

function getStoredTheme() {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark" || savedTheme === "light") {
        return savedTheme;
    }
    // Default to light (โหมดสว่าง) or detect system preference
    if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
        return "dark";
    }
    return "light";
}

function applyTheme(theme) {
    const normalizedTheme = theme === "dark" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", normalizedTheme);
    document.body.setAttribute("data-theme", normalizedTheme);
    localStorage.setItem("theme", normalizedTheme);

    // Update main header theme toggle
    const toggleButtons = document.querySelectorAll(".theme-toggle-btn, #theme-toggle, #login-theme-toggle");
    toggleButtons.forEach(btn => {
        btn.classList.toggle("is-dark", normalizedTheme === "dark");
        btn.setAttribute("aria-label", normalizedTheme === "dark" ? "สลับเป็นโหมดสว่าง" : "สลับเป็นโหมดมืด");

        const label = btn.querySelector(".theme-toggle-label");
        if (label) {
            label.textContent = normalizedTheme === "dark" ? "โหมดมืด" : "โหมดสว่าง";
        }
    });

    // Notify listeners (such as Chart.js instances) about the theme change
    window.dispatchEvent(new CustomEvent("themeChanged", { detail: { theme: normalizedTheme } }));

    if (typeof lucide !== "undefined" && window.lucide && window.lucide.createIcons) {
        window.lucide.createIcons();
    }
}

function renderLayout(activePage = "dashboard") {
    const user = typeof auth !== "undefined" ? auth.getUser() : null;
    const role = (typeof auth !== "undefined" ? auth.getRole() : null) || "STAFF";

    const sidebarContainer = document.getElementById("sidebar");
    const headerContainer = document.getElementById("header");

    if (sidebarContainer) {
        let menuItems = [];

        if (role === "ADMIN") {
            menuItems = [
                { id: "dashboard", label: "ภาพรวมสถิติ", icon: "layout-dashboard", href: "dashboard.html" },
                { id: "personnel", label: "จัดการบุคลากร", icon: "users", href: "personnel-list.html" },
                { id: "personnel-add", label: "เพิ่มข้อมูลบุคลากร", icon: "user-plus", href: "personnel-form.html" },
                { id: "master-data", label: "ข้อมูลสาขา/ตำแหน่ง", icon: "database", href: "master-data.html" },
                { id: "audit-logs", label: "ประวัติการทำงาน (Audit Log)", icon: "shield-check", href: "audit-logs.html" }
            ];
        } else if (role === "EXECUTIVE") {
            menuItems = [
                { id: "dashboard", label: "ภาพรวมสถิติ", icon: "layout-dashboard", href: "dashboard.html" },
                { id: "personnel", label: "รายชื่อและรายงานบุคลากร", icon: "users", href: "personnel-list.html" }
            ];
        } else { // STAFF
            menuItems = [
                { id: "my-profile", label: "ข้อมูลประวัติของฉัน", icon: "user", href: user?.personnel_id ? `personnel-detail.html?id=${user.personnel_id}` : "#" },
                { id: "edit-profile", label: "แก้ไขข้อมูลส่วนตัว", icon: "edit-3", href: user?.personnel_id ? `personnel-form.html?id=${user.personnel_id}` : "#" }
            ];
        }

        const navHtml = menuItems.map(item => {
            const isActive = activePage === item.id;
            return `
                <a href="${item.href}" class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-medium transition-all text-xs ${
                    isActive 
                        ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/30 font-semibold' 
                        : 'text-slate-400 hover:bg-slate-800/80 hover:text-slate-200'
                }">
                    <i data-lucide="${item.icon}" class="w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}"></i>
                    <span>${item.label}</span>
                </a>
            `;
        }).join("");

        sidebarContainer.innerHTML = `
            <div class="h-full flex flex-col justify-between p-4 bg-[#090d16] text-white">
                <div>
                    <!-- Brand / Logo Minimalist -->
                    <a href="dashboard.html" class="flex items-center gap-3 px-2 py-3 mb-5 border-b border-white/10 group">
                        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white font-bold text-sm shadow-md">
                            IT
                        </div>
                        <div>
                            <h1 class="font-bold text-xs tracking-tight text-white leading-tight">คณะเทคโนโลยีสารสนเทศ</h1>
                            <p class="text-[11px] text-blue-400 font-medium">มรภ.ร้อยเอ็ด (RERU)</p>
                        </div>
                    </a>

                    <!-- Section Label -->
                    <p class="px-2 mb-2 text-[10px] font-semibold text-slate-500 uppercase tracking-wider">เมนูหลัก</p>

                    <!-- Menu List -->
                    <nav class="space-y-1">
                        ${navHtml}
                    </nav>
                </div>

                <!-- Footer User Info & Logout -->
                <div class="pt-3 border-t border-white/10 space-y-2">
                    <div class="flex items-center gap-3 px-2.5 py-2 rounded-xl bg-white/5 border border-white/5">
                        <div class="w-8 h-8 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-xs">
                            ${(user?.username || 'U')[0].toUpperCase()}
                        </div>
                        <div class="flex-1 min-w-0">
                            <p class="text-xs font-semibold text-slate-200 truncate leading-tight">${user?.full_name || user?.username || 'ผู้ใช้งาน'}</p>
                            <span class="inline-block text-[10px] font-medium text-slate-400">${role}</span>
                        </div>
                    </div>
                    <button type="button" onclick="auth.logout()" class="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-xl text-xs font-medium text-rose-400 hover:bg-rose-500/10 transition-colors">
                        <i data-lucide="log-out" class="w-3.5 h-3.5"></i>
                        <span>ออกจากระบบ</span>
                    </button>
                </div>
            </div>
        `;
    }

    if (headerContainer) {
        headerContainer.innerHTML = `
            <div class="flex items-center justify-between px-6 py-3.5 backdrop-blur-md sticky top-0 z-30">
                <div class="flex items-center gap-3">
                    <button id="mobile-menu-btn" type="button" class="lg:hidden p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors" aria-label="เปิดเมนูหลัก">
                        <i data-lucide="menu" class="w-5 h-5"></i>
                    </button>
                    <div>
                        <h2 class="text-sm font-bold text-slate-800 dark:text-slate-100 leading-tight">ระบบจัดเก็บและบริหารข้อมูลบุคลากร</h2>
                        <p class="text-[11px] text-slate-500 dark:text-slate-400 font-medium">Faculty Personnel Information System</p>
                    </div>
                </div>

                <div class="flex items-center gap-3">
                    <!-- Morning / Dark Mode Minimalist Switch -->
                    <button id="theme-toggle" type="button" class="theme-toggle-btn" aria-label="สลับโหมดสว่าง/โหมดมืด">
                        <span class="theme-state-icon theme-icon-light"><i data-lucide="sun" class="w-4 h-4"></i></span>
                        <span class="theme-state-icon theme-icon-dark"><i data-lucide="moon" class="w-4 h-4"></i></span>
                        <span class="theme-toggle-label">โหมดสว่าง</span>
                    </button>

                    <!-- User Quick Badge -->
                    <div class="flex items-center gap-2.5 pl-3 border-l border-slate-200 dark:border-slate-800">
                        <div class="text-right hidden sm:block">
                            <p class="text-xs font-semibold text-slate-800 dark:text-slate-200 leading-tight">${user?.full_name || user?.username}</p>
                            <p class="text-[10px] text-emerald-500 font-medium flex items-center justify-end gap-1">
                                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block animate-pulse"></span>
                                ออนไลน์
                            </p>
                        </div>
                        <div class="w-8 h-8 rounded-xl bg-blue-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-center text-blue-600 dark:text-blue-400 font-bold text-xs">
                            ${(user?.username || 'U')[0].toUpperCase()}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Apply saved theme
    applyTheme(getStoredTheme());

    // Setup theme toggle listener
    const themeToggleBtn = document.getElementById("theme-toggle");
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", () => {
            const currentTheme = document.body.getAttribute("data-theme") || "light";
            const nextTheme = currentTheme === "dark" ? "light" : "dark";
            applyTheme(nextTheme);
        });
    }

    // Setup Mobile Menu Drawer & Overlay
    const mobileBtn = document.getElementById("mobile-menu-btn");
    let backdrop = document.getElementById("sidebar-backdrop");
    if (!backdrop) {
        backdrop = document.createElement("div");
        backdrop.id = "sidebar-backdrop";
        backdrop.className = "fixed inset-0 bg-slate-900/60 backdrop-blur-xs z-35 hidden lg:hidden transition-opacity";
        document.body.appendChild(backdrop);
    }

    const closeMobileSidebar = () => {
        if (sidebarContainer) sidebarContainer.classList.add("hidden");
        if (backdrop) backdrop.classList.add("hidden");
    };

    if (mobileBtn && sidebarContainer) {
        mobileBtn.onclick = () => {
            const isHidden = sidebarContainer.classList.contains("hidden");
            if (isHidden) {
                sidebarContainer.classList.remove("hidden");
                sidebarContainer.classList.add("shadow-2xl");
                if (backdrop) backdrop.classList.remove("hidden");
            } else {
                closeMobileSidebar();
            }
        };
    }

    if (backdrop) {
        backdrop.onclick = closeMobileSidebar;
    }

    // Initialize Lucide icons
    if (typeof lucide !== "undefined" && window.lucide && window.lucide.createIcons) {
        window.lucide.createIcons();
    }
}

window.getStoredTheme = getStoredTheme;
window.applyTheme = applyTheme;
window.renderLayout = renderLayout;

