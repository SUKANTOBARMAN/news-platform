def test_otp_request_and_verify(client, db_session):
    # প্রথমে phone দিয়ে একজন ইউজার বানাও (OTP verify-এর পর তাকেই খুঁজে বের করা হবে)
    from app.core.security import hash_password
    from app.models.user import User

    user = User(
        first_name="Otp",
        last_name="User",
        phone="+8801700000000",
        password_hash=hash_password("irrelevant"),
    )
    db_session.add(user)
    db_session.commit()

    request_resp = client.post(
        "/api/v1/auth/otp/request",
        json={"phone_or_email": "+8801700000000", "purpose": "login"},
    )
    assert request_resp.status_code == 204

    # ডেভ-মোডে OTP কনসোলে প্রিন্ট হয় -- টেস্টে সরাসরি DB থেকে পড়ে নিচ্ছি
    from app.core.security import verify_password
    from app.models.user import Otp
    from sqlalchemy import select

    otp = db_session.scalar(
        select(Otp).where(Otp.phone_or_email == "+8801700000000").order_by(Otp.id.desc())
    )
    # রিয়েল কোডটা হ্যাশড, তাই টেস্টে সরাসরি জানা সম্ভব না -- এই টেস্ট শুধু
    # request endpoint কাজ করছে কিনা যাচাই করে; verify করতে হলে otp_code_hash
    # বাইপাস করে একটা নতুন known OTP বসিয়ে verify করা যায়:
    otp.otp_code_hash = hash_password("123456")
    db_session.commit()

    verify_resp = client.post(
        "/api/v1/auth/otp/verify",
        json={"phone_or_email": "+8801700000000", "otp_code": "123456", "purpose": "login"},
    )
    assert verify_resp.status_code == 200
    assert "access_token" in verify_resp.json()


def test_otp_verify_wrong_code(client):
    client.post(
        "/api/v1/auth/otp/request",
        json={"phone_or_email": "+8801700000001", "purpose": "login"},
    )
    response = client.post(
        "/api/v1/auth/otp/verify",
        json={"phone_or_email": "+8801700000001", "otp_code": "000000", "purpose": "login"},
    )
    assert response.status_code in (400, 404)