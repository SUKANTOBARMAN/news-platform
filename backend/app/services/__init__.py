"""
Service লেয়ার -- জটিল বিজনেস লজিক (badge calculation, PDF generation, paywall
rules evaluation ইত্যাদি) এখানে রাখা হবে, route ফাইলে না।

নিয়ম (ORM Maintenance Guide, Part ৯): service ফাংশন নিজে কখনো SessionLocal()
কল করে নতুন session বানাবে না -- route থেকে যে session (db) ইতিমধ্যে তৈরি হয়েছে,
সেটাই প্যারামিটার হিসেবে পাস করতে হবে, যাতে একই request-এর সব DB অপারেশন একই
transaction-এর অংশ থাকে।

উদাহরণ:
    def check_and_award_badges(db: Session, volunteer: User) -> None:
        ...
"""
