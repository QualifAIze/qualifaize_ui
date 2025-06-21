not_logged_dashboard_style = """<style>
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
