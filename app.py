import streamlit as st
import boto3, json, time, random

#cloudwatch config, communicating with cloudwatch logs

client = boto3.client('logs', region_name='us-east-1') 
LOG_GROUP = '/project/app-logs'
LOG_STREAM = 'ecommerce-frontend'

# initializing log stream on application startup, 
# checking if the stream already exists from a previous session.
try:
    client.create_log_stream(logGroupName=LOG_GROUP, logStreamName=LOG_STREAM)
except client.exceptions.ResourceAlreadyExistsException:
    pass
except Exception as e:
    st.error(f"AWS Connection Error: {e}")

# log ingeston function

def send_log(event_type, code, latency, user_id):
    log_data = {"user_id": user_id, "event": event_type, "code": code, "latency": latency}
   
# push the event to cloudwatch
    try:
        
        client.put_log_events(
            logGroupName=LOG_GROUP,
            logStreamName=LOG_STREAM,
            logEvents=[{'timestamp': int(round(time.time() * 1000)), 'message': json.dumps(log_data)}]
        )
        return log_data
    except Exception as e:
        #captures IAM permission errors of region mismatches to display on the UI
        st.error(f"AWS Error: {e}")
        return None

# notifications
@st.dialog("🚨 CRITICAL INCIDENT TRIGGERED")
def show_critical_popup(code, message):
    st.error(f"**Status Code: {code}**")
    st.write(f"**Details:** {message}")
    st.write("AWS Lambda has detected this outage and is dispatching an emergency Incident Report to the Operations team.")
    #the acknowledgment button forces a page rerun for reseting the state
    if st.button("Acknowledge & Close"):
        st.rerun()

# UI part
st.set_page_config(page_title="Chaos Simulator", layout="wide")
st.title("🛒 Chaos Simulator - testing environment")
st.markdown("Inject synthetic traffic, security threats, and system faults into the AWS CloudWatch pipeline.")
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🟢 Operations & Performance")
    if st.button("✅ Normal User Checkout", use_container_width=True):
        send_log("checkout_success", 200, random.randint(100, 300), f"u_{random.randint(100,999)}")
       
        st.toast("200 OK: Normal traffic logged to AWS.", icon="✅")
       
    if st.button("🐌 Slow Checkout (Performance)", use_container_width=True):
        send_log("checkout_slow", 200, random.randint(4000, 8000), f"u_{random.randint(100,999)}")
        st.toast("200 OK: Succeeded, but high latency recorded.", icon="🐌")

with col2:
    st.subheader("🟡 Client & Security Threats")
    if st.button("🔍 404 (Missing Image/Page)", use_container_width=True):
        send_log("404_error", 404, 50, f"u_{random.randint(100,999)}")
        st.toast("404 Warning: Page not found logged.", icon="🔍")
       
    if st.button("🛑 403 (Unauthorized Admin Login)", use_container_width=True):
        send_log("admin_access_denied", 403, 40, f"u_{random.randint(100,999)}")
        st.toast("403 Security Threat: Blocked admin access logged.", icon="🛑")

    if st.button("🤖 429 (DDoS / Bot Spike)", use_container_width=True):
        send_log("rate_limit_exceeded", 429, 20, f"u_{random.randint(100,999)}")
        st.toast("429 Rate Limit: Bot traffic spike logged.", icon="🤖")

with col3:
    st.subheader("🔴 Critical Outages (Triggers Email)")
    if st.button("🔥 500 (Database Timeout)", type="primary", use_container_width=True):
        send_log("db_timeout", 500, 5000, f"u_{random.randint(100,999)}")
        
        show_critical_popup(500, "Database connection lost!")
       
    if st.button("💳 502 (Stripe/PayPal Gateway Down)", type="primary", use_container_width=True):
        send_log("payment_gateway_fail", 502, 300, f"u_{random.randint(100,999)}")
       
        show_critical_popup(502, "Third-party API failure!")