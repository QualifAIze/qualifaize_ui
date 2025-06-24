dashboard_styles = """<style>
.feature-card {
    /* Enhanced glassmorphism background with gradient */
    background: linear-gradient(
        135deg,
        rgba(92, 95, 102, 0.5) 0%,
        rgba(92, 95, 102, 0.7) 100%
    );

    /* Enhanced border with subtle gradient */
    border-image: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.4), 
        rgba(255, 255, 255, 0.15)
    ) 1;

    border-radius: 16px;
    padding: 28px 20px 20px 20px;
    margin-bottom: 20px;
    min-height: 210px;

    /* Advanced glass effects */
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);

    /* Enhanced shadow with multiple layers */
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.15),
        0 2px 8px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.15);

    /* Typography with enhanced contrast */
    color: #ffffff !important;
    font-size: 18px;
    font-family: 'Segoe UI', 'Roboto', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    line-height: 1.6;

    /* Smooth transitions */
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    transform: translateZ(0);

    /* Subtle animation on hover */
    position: relative;
    overflow: hidden;
}

/* Animated background overlay */
.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
        45deg,
        rgba(255, 255, 255, 0.05) 0%,
        transparent 50%,
        rgba(255, 255, 255, 0.05) 100%
    );
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
    border-radius: 16px;
}

.feature-card:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 
        0 20px 40px rgba(0, 0, 0, 0.15),
        0 8px 16px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.feature-card:hover::before {
    opacity: 1;
}

.feature-title {
    font-weight: 700;
    font-size: 22px;
    margin-bottom: 16px;
    color: #FF4B4B;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
    letter-spacing: -0.02em;
    transition: color 0.3s ease;
}

.feature-card:hover .feature-title {
    color: #FF6B6B;
    text-shadow: 0 4px 8px rgba(255, 75, 75, 0.4);
}

/* Responsive design */
@media (max-width: 768px) {
    .feature-card {
        padding: 24px 16px 16px 16px;
        margin-bottom: 16px;
    }

    .feature-title {
        font-size: 20px;
        margin-bottom: 12px;
    }
}

/* Light theme adaptations */
@media (prefers-color-scheme: light) {
    .feature-card {
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.8) 0%,
            rgba(240, 242, 247, 0.9) 100%
        );
        color: #1a202c !important;
        border-image: linear-gradient(135deg, 
            rgba(0, 0, 0, 0.15), 
            rgba(0, 0, 0, 0.08)
        ) 1;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.1),
            0 2px 8px rgba(0, 0, 0, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }

    .feature-card::before {
        background: linear-gradient(
            45deg,
            rgba(0, 0, 0, 0.03) 0%,
            transparent 50%,
            rgba(0, 0, 0, 0.03) 100%
        );
    }

    .feature-card:hover {
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.15),
            0 8px 16px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.95);
    }

    .feature-title {
        color: #CC3333;
        text-shadow: 0 2px 4px rgba(204, 51, 51, 0.3);
    }

    .feature-card:hover .feature-title {
        color: #AA2222;
        text-shadow: 0 4px 8px rgba(204, 51, 51, 0.4);
    }
}

/* Dark theme optimizations */
@media (prefers-color-scheme: dark) {
    .feature-card {
        background: linear-gradient(
            135deg,
            rgba(45, 55, 72, 0.6) 0%,
            rgba(74, 85, 104, 0.4) 100%
        );
    }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
    .feature-card {
        border: 2px solid currentColor;
        backdrop-filter: none;
        -webkit-backdrop-filter: none;
    }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
    .feature-card,
    .feature-card::before,
    .feature-title {
        transition: none;
    }

    .feature-card:hover {
        transform: none;
    }
}

/* Enhanced focus styles for accessibility */
.feature-card:focus-within {
    outline: 2px solid #4299e1;
    outline-offset: 2px;
}

.step-number {
    background: #FF4B4B;
    color: white;
    display: inline-block;
    border-radius: 50%;
    width: 32px;
    height: 32px;
    text-align: center;
    font-size: 18px;
    font-weight: 700;
    line-height: 32px;
    margin-right: 12px;
}
</style>
"""


auth_styles = """
<style>
.login-title {
    font-weight: 700;
    font-size: 2.2rem;
    text-align: center;
    margin-bottom: 20px;
    color: #FF4B4B;
    letter-spacing: -0.02em;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    transition: color 0.3s;
}
</style>
"""


account_details_styles = """
<style>
:root {
    --account-bg: rgba(31, 41, 55, 0.8);
    --account-border: #374151;
    --section-border: #60a5fa;
    --text-primary: #f9fafb;
    --text-secondary: #d1d5db;
    --info-bg: rgba(55, 65, 81, 0.8);
    --status-bg: #dcfce7;
    --status-text: #166534;
    --status-border: #bbf7d0;
}


.info-field {
    background: var(--info-bg);
    border: 1px solid var(--account-border);
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
}

.info-label {
    font-weight: 600;
    color: var(--text-secondary);
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}

.info-value {
    color: var(--text-primary);
    font-size: 16px;
    font-weight: 500;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}


.account-type-badge {
    background: var(--status-bg);
    color: var(--status-text);
    padding: 6px 16px;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 600;
    border: 1px solid var(--status-border);
    display: inline-block;
}

.status-badge {
    background: var(--status-bg);
    color: var(--status-text);
    padding: 6px 16px;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 600;
    border: 1px solid var(--status-border);
}
</style>
"""


user_management_styles = """
<style>
.user-title {
    font-weight: 600;
    color: #111827;
    margin: 0 0 8px 0;
    font-size: 16px;
    line-height: 1.3;
}

[data-theme="dark"] .user-title {
    color: #f9fafb;
}

.user-title:hover {
    color: #1e40af;
}

[data-theme="dark"] .user-title:hover {
    color: #93c5fd;
}

.user-meta {
    font-size: 14px;
    color: #6b7280;
    margin: 3px 0;
    line-height: 1.2;
}

[data-theme="dark"] .user-meta {
    color: #9ca3af;
}

.role-badge {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 13px;
    font-weight: 500;
    border: 1px solid;
    display: inline-block;
    margin: 6px 0 8px 0;
    width: fit-content;
}

.delete-confirmation {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 4px;
    padding: 8px;
    margin: 8px 0 4px 0;
}

.section-header {
    background: rgba(59, 130, 246, 0.08);
    border-left: 3px solid #3b82f6;
    border-radius: 0 4px 4px 0;
    padding: 10px 12px;
    margin: 8px 0;
}

[data-theme="dark"] .section-header {
    background: rgba(59, 130, 246, 0.15);
    border-left-color: #60a5fa;
}

.empty-state {
    text-align: center;
    padding: 40px 20px;
    background: rgba(59, 130, 246, 0.05);
    border-radius: 6px;
    border: 2px dashed rgba(59, 130, 246, 0.3);
}

[data-theme="dark"] .empty-state {
    background: rgba(59, 130, 246, 0.1);
}
</style>
"""


document_management_styles = """
<style>
.doc-title {
    font-weight: 600;
    color: #111827;
    margin: 0 0 8px 0;
    font-size: 16px;
    line-height: 1.3;
}

[data-theme="dark"] .doc-title {
    color: #f9fafb;
}

.doc-title:hover {
    color: #1e40af;
}

[data-theme="dark"] .doc-title:hover {
    color: #93c5fd;
}

.doc-meta {
    font-size: 14px;
    color: #6b7280;
    margin: 3px 0;
    line-height: 1.2;
}

[data-theme="dark"] .doc-meta {
    color: #9ca3af;
}

.uploader-badge {
    background: rgba(59, 130, 246, 0.1);
    color: #1e40af;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 13px;
    font-weight: 500;
    border: 1px solid rgba(59, 130, 246, 0.3);
    display: inline-block;
    margin: 6px 0 8px 0;
    width: fit-content;
}

[data-theme="dark"] .uploader-badge {
    background: rgba(59, 130, 246, 0.2);
    color: #93c5fd;
}

.delete-confirmation {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 4px;
    padding: 8px;
    margin: 8px 0 4px 0;
}

.section-header {
    background: rgba(59, 130, 246, 0.08);
    border-left: 3px solid #3b82f6;
    border-radius: 0 4px 4px 0;
    padding: 10px 12px;
    margin: 8px 0;
}

[data-theme="dark"] .section-header {
    background: rgba(59, 130, 246, 0.15);
    border-left-color: #60a5fa;
}

.empty-state {
    text-align: center;
    padding: 40px 20px;
    background: rgba(59, 130, 246, 0.05);
    border-radius: 6px;
    border: 2px dashed rgba(59, 130, 246, 0.3);
}

[data-theme="dark"] .empty-state {
    background: rgba(59, 130, 246, 0.1);
}
</style>
"""


interview_page_styles = """
    <style>
    .interview-container {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(139, 69, 19, 0.05) 100%);
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }

    [data-theme="dark"] .interview-container {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 69, 19, 0.1) 100%);
        border-color: rgba(59, 130, 246, 0.3);
    }

    .question-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    [data-theme="dark"] .question-card {
        background: rgba(55, 65, 81, 0.95);
        border-left-color: #60a5fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        color: #f9fafb;
    }

    .question-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }

    .feedback-correct {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(34, 197, 94, 0.05) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
        color: #065f46;
    }

    [data-theme="dark"] .feedback-correct {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(34, 197, 94, 0.1) 100%);
        color: #a7f3d0;
    }

    .feedback-incorrect {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
        color: #991b1b;
    }

    [data-theme="dark"] .feedback-incorrect {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.1) 100%);
        color: #fca5a5;
    }

    .interview-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .question-counter {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 8px;
        padding: 8px 16px;
        display: inline-block;
        font-weight: 500;
        color: #1e40af;
        margin-bottom: 16px;
    }

    [data-theme="dark"] .question-counter {
        background: rgba(59, 130, 246, 0.2);
        color: #93c5fd;
    }

    .status-badge {
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 500;
        text-align: center;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }

    .question-history-sidebar {
        background: rgba(248, 250, 252, 0.8);
        border-radius: 8px;
        padding: 16px;
        margin-top: 20px;
        border: 1px solid rgba(203, 213, 225, 0.5);
        max-height: 80vh;
        overflow-y: auto;
    }

    [data-theme="dark"] .question-history-sidebar {
        background: rgba(30, 41, 59, 0.8);
        border-color: rgba(71, 85, 105, 0.5);
    }

    .history-question-item {
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 6px;
        border-left: 3px solid;
        font-size: 14px;
    }

    .history-correct {
        border-left-color: #10b981;
        background: rgba(16, 185, 129, 0.1);
    }

    .history-incorrect {
        border-left-color: #ef4444;
        background: rgba(239, 68, 68, 0.1);
    }

    @media (max-width: 768px) {
        .interview-container {
            padding: 16px;
            margin: 8px 0;
        }
        
        .question-card {
            padding: 16px;
            margin: 12px 0;
        }
        
        .interview-header {
            padding: 16px;
        }
        
        .question-history-sidebar {
            margin-top: 16px;
            max-height: 60vh;
        }
    }
    </style>
    """
