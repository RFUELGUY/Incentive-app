from sqlalchemy.orm import Session
from models.sale import Sale
from models.salesman import Salesman
from sqlalchemy import func
from datetime import date, timedelta
from models.streak import Streak

def get_leaderboard(db: Session, scope: str):
    today = date.today()

    if scope == "day":
        start_date = today
    elif scope == "week":
        start_date = today - timedelta(days=7)
    else:  # month
        start_date = today.replace(day=1)

    results = (
        db.query(Salesman.name, func.sum(Sale.amount).label("total_sales"))
        .join(Sale, Salesman.id == Sale.salesman_id)
        .filter(Sale.date >= start_date)
        .group_by(Salesman.id)
        .order_by(func.sum(Sale.amount).desc())
        .limit(10)
        .all()
    )

    return [{"name": r.name, "sales": r.total_sales} for r in results]

def update_user_streak(db: Session, salesman_id: int, date_str: str):
    # Placeholder until we add a streak model/table
    return {"message": f"✅ Streak updated for salesman {salesman_id} on {date_str}"}





def get_streak_leaderboard(db: Session):
    results = (
        db.query(
            Salesman.name,
            Salesman.mobile,
            Salesman.outlet,
            func.max(Streak.day_streak_count).label("total_streak")
        )
        .join(Streak, Salesman.id == Streak.salesman_id)
        .filter(Streak.continued == True)
        .group_by(Salesman.id)
        .order_by(func.max(Streak.day_streak_count).desc())
        .limit(10)
        .all()
    )

    return [
        {
            "name": r.name,
            "mobile": r.mobile,
            "outlet": r.outlet,
            "total_sales": r.total_streak  # shown as 'total_sales' in frontend
        }
        for r in results
    ]

