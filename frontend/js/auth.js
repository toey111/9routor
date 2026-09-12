// Authentication & State Management

const auth = {
    getUser() {
        const userStr = localStorage.getItem("user");
        return userStr ? JSON.parse(userStr) : null;
    },

    getToken() {
        return localStorage.getItem("token");
    },

    getRole() {
        const user = this.getUser();
        return user?.role ? user.role.toUpperCase() : null;
    },

    isAuthenticated() {
        return !!this.getToken();
    },

    setUserSession(tokenData) {
        localStorage.setItem("token", tokenData.access_token);
        localStorage.setItem("user", JSON.stringify({
            id: tokenData.user_id,
            username: tokenData.username,
            role: tokenData.role,
            personnel_id: tokenData.personnel_id,
            full_name: tokenData.full_name
        }));
    },

    logout() {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        window.location.replace("login.html");
    },

    requireAuth(allowedRoles = []) {
        if (!this.isAuthenticated()) {
            window.location.replace("login.html");
            return false;
        }

        if (allowedRoles.length > 0) {
            const currentRole = this.getRole();
            const upperAllowed = allowedRoles.map(r => r.toUpperCase());
            if (!upperAllowed.includes(currentRole)) {
                alert("ท่านไม่มีสิทธิ์ในการเข้าถึงหน้านี้");
                if (currentRole === "STAFF") {
                    const user = this.getUser();
                    window.location.replace(user?.personnel_id ? `personnel-detail.html?id=${user.personnel_id}` : "login.html");
                } else {
                    window.location.replace("dashboard.html");
                }
                return false;
            }
        }
        return true;
    }
};

window.auth = auth;
