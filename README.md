#  Enterprise Chaos Simulator & Serverless Observability

A cloud-native log generation and intelligent alerting system built with **Python, Streamlit, and AWS Serverless (CloudWatch, Lambda, SNS)**.

This project solves the "Alert Fatigue" problem by using event-driven architecture to filter out standard application noise and only triggering email notifications for critical system outages (HTTP 5xx errors).

##  Features
* **Synthetic Traffic Generator:** A local Streamlit UI to simulate normal transactions, security threats, and database timeouts.
* **Direct AWS Integration:** Boto3 integration to push structured JSON logs directly to Amazon CloudWatch.
* **Serverless Processing:** AWS Lambda function triggered by CloudWatch Subscription Filters to decode and evaluate log severity in milliseconds.
* **Zero-Spam Alerting:** Amazon SNS integration that strictly emails the operations team only when `status_code >= 500`.

##  Prerequisites
* Python 3.10+
* AWS CLI configured with `us-east-1` region
* IAM permissions (`CloudWatchLogsFullAccess`)

##  Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/bobokhidze/Chaos-Application.git](https://github.com/bobokhidze/Chaos-Application.git)
   cd Chaos-Application
