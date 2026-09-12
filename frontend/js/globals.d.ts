declare const auth: {
    getToken(): string | null;
    getUser(): any;
    getRole(): string | null;
    isAuthenticated(): boolean;
    setUserSession(data: any): void;
    requireAuth(allowedRoles?: string[]): boolean;
    logout(): void;
};

declare const apiClient: {
    request(endpoint: string, options?: any): Promise<any>;
    get(endpoint: string, params?: any): Promise<any>;
    post(endpoint: string, body?: any): Promise<any>;
    put(endpoint: string, body?: any): Promise<any>;
    delete(endpoint: string): Promise<any>;
    uploadFile(endpoint: string, formData: FormData): Promise<any>;
    downloadFile(endpoint: string, params?: any, defaultFilename?: string): Promise<void>;
};

declare const ui: {
    showToast(message: string, type?: string, duration?: number): void;
    confirmModal(options: { title: string; message: string; confirmText?: string; confirmColor?: string; onConfirm?: () => void }): void;
    formatDateThai(dateString: string | null | undefined): string;
    highlightError(elementId: string | HTMLElement, message?: string): void;
};

declare const lucide: {
    createIcons(): void;
};

declare const Chart: any;

declare const tailwind: {
    config: any;
};

declare function renderLayout(activePage?: string): void;
declare function getStoredTheme(): string;
declare function applyTheme(theme: string): void;
declare function applyLoginTheme(theme: string): void;
declare function resetLoginButtonState(): void;
declare function fillDemo(user: string, pass: string): void;
declare function loadPersonnel(page?: number): Promise<void>;
declare function loadAuditLogs(page?: number): Promise<void>;
declare function confirmDelete(id: number, name: string): void;
declare function exportData(format: string): void;

