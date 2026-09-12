// API Client for Personnel Management System

const API_BASE = window.location.port === "3000" 
    ? "http://localhost:8000/api/v1" 
    : "/api/v1";

const apiClient = {
    async request(endpoint, options = {}) {
        const token = localStorage.getItem("token");
        const headers = { ...options.headers };

        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        if (!(options.body instanceof FormData) && !headers["Content-Type"]) {
            headers["Content-Type"] = "application/json";
        }

        const url = `${API_BASE}${endpoint.startsWith('/') ? endpoint : '/' + endpoint}`;

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            if (response.status === 401) {
                localStorage.removeItem("token");
                localStorage.removeItem("user");
                if (!window.location.pathname.endsWith("login.html")) {
                    window.location.href = "login.html?expired=1";
                }
                throw new Error("เซสชันหมดอายุ กรุณาเข้าสู่ระบบใหม่");
            }

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: "เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์" }));
                const message = errorData.detail || "เกิดข้อผิดพลาดในการประมวลผล";
                throw new Error(typeof message === "string" ? message : JSON.stringify(message));
            }

            // Return blob/stream for file downloads
            const contentType = response.headers.get("content-type");
            if (contentType && (contentType.includes("text/csv") || contentType.includes("application/pdf") || contentType.includes("spreadsheetml"))) {
                return response.blob();
            }

            return await response.json();
        } catch (err) {
            console.error("API Error:", err);
            throw err;
        }
    },

    get(endpoint, params = {}) {
        const queryString = new URLSearchParams(
            Object.entries(params).filter(([_, v]) => v !== undefined && v !== null && v !== "")
        ).toString();
        const url = queryString ? `${endpoint}?${queryString}` : endpoint;
        return this.request(url, { method: "GET" });
    },

    post(endpoint, body) {
        return this.request(endpoint, {
            method: "POST",
            body: body instanceof FormData ? body : JSON.stringify(body)
        });
    },

    put(endpoint, body) {
        return this.request(endpoint, {
            method: "PUT",
            body: body instanceof FormData ? body : JSON.stringify(body)
        });
    },

    delete(endpoint) {
        return this.request(endpoint, { method: "DELETE" });
    },

    uploadFile(endpoint, formData) {
        return this.request(endpoint, {
            method: "POST",
            body: formData
        });
    },

    async downloadFile(endpoint, params = {}, defaultFilename = "download") {
        const blob = await this.get(endpoint, params);
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = defaultFilename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    }
};

window.apiClient = apiClient;
