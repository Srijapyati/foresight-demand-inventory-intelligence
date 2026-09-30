import streamlit as st

def render():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <span style="font-size: 2.2rem; font-weight: 900; color: #ff6b00; letter-spacing: 2px;">⚡ FORESIGHT</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("""
        <div style="padding-right: 30px;">
            <h1 style="font-size: 2.5rem; font-weight: 800; line-height: 1.1; margin-bottom: 16px;">
                Intelligence at scale.
            </h1>
            <p style="font-size: 1.1rem; color: #94a3b8; line-height: 1.6; margin-bottom: 30px;">
                Transform your raw data into actionable supply chain intelligence with the world's most advanced retail analytics platform.
            </p>

            <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 16px 20px; display: inline-flex; align-items: center; gap: 14px; margin-bottom: 40px;">
                <div style="width: 14px; height: 14px; border-radius: 50%; background: #10b981; box-shadow: 0 0 10px #10b981;"></div>
                <div>
                    <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">System Status</div>
                    <div style="font-size: 1.0rem; font-weight: 700; color: #ffffff;">Optimal Performance</div>
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 20px;">
                <div style="display: flex; gap: 14px; align-items: start;">
                    <span style="font-size: 1.4rem;">⚡</span>
                    <div>
                        <div style="font-weight: 700; font-size: 1.0rem;">Real-time Analytics</div>
                        <div style="font-size: 0.88rem; color: #94a3b8;">Process millions of data points instantly with our ultra-fast Edge ML.</div>
                    </div>
                </div>
                <div style="display: flex; gap: 14px; align-items: start;">
                    <span style="font-size: 1.4rem;">🛡️</span>
                    <div>
                        <div style="font-weight: 700; font-size: 1.0rem;">Enterprise Security</div>
                        <div style="font-size: 0.88rem; color: #94a3b8;">Bank-grade encryption and SOC2 compliant infrastructure for your peace of mind.</div>
                    </div>
                </div>
                <div style="display: flex; gap: 14px; align-items: start;">
                    <span style="font-size: 1.4rem;">🔮</span>
                    <div>
                        <div style="font-weight: 700; font-size: 1.0rem;">Predictive Insights</div>
                        <div style="font-size: 0.88rem; color: #94a3b8;">Anticipate supply chain disruptions before they happen using FORESIGHT AI.</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px; padding: 32px; box-shadow: 0 20px 40px rgba(0,0,0,0.4);">
            <h2 style="font-weight: 800; font-size: 1.6rem; margin-bottom: 4px;">Welcome Back</h2>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 24px;">Log in to access your dashboard workspace.</p>
        """, unsafe_allow_html=True)

        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            st.button("🌐 Google SSO", use_container_width=True)
        with btn_c2:
            st.button("🪟 Microsoft SSO", use_container_width=True)

        st.markdown('<div style="text-align: center; color: #64748b; font-size: 0.8rem; margin: 16px 0;">OR CONTINUE WITH EMAIL</div>', unsafe_allow_html=True)

        email = st.text_input("Work Email", value="demo@northbayliving.com")
        password = st.text_input("Password", value="••••••••••••", type="password")

        c_rem, c_forgot = st.columns(2)
        with c_rem:
            st.checkbox("Remember me", value=True)
        with c_forgot:
            st.markdown('<div style="text-align: right;"><a href="#" style="color: #ff6b00; font-size: 0.85rem; text-decoration: none;">Forgot Password?</a></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Sign In to Workspace →", type="primary", use_container_width=True):
            st.session_state["authenticated"] = True
            st.rerun()

        st.markdown("""
            <div style="text-align: center; margin-top: 20px; color: #94a3b8; font-size: 0.85rem;">
                Don't have an account? <a href="#" style="color: #ff6b00; font-weight: 600; text-decoration: none;">Request Access</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
