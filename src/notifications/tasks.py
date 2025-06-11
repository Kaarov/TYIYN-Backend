from celery import shared_task
from django.utils import timezone
from docutils.nodes import description

from budget.models import BudgetModel
from goal.models import GoalModel
from notifications.models import NotificationModel
from notifications.utils import send_push_notification


@shared_task
def check_budget_notifications():
    now = timezone.now()

    for budget in BudgetModel.objects.all():
        if budget.period.year == now.year and budget.period.month == now.month:
            spent_percentage = (budget.spent / budget.limit) * 100 if budget.limit else 0
            category_title = budget.category.get_name(budget.user.language)
            message = ""
            title = ""

            if 29 < spent_percentage < 31:
                title = "Percentage spent for budget"
                message = f"Вы потратили {int(spent_percentage)}% от своего месячного бюджета на '{category_title}'. Попробуйте готовить дома, чтобы сэкономить."
                send_push_notification(budget.user, "Бюджет", message)
            elif 49 < spent_percentage < 51:
                title = "Percentage spent for budget"
                message = f"Половина месячного бюджета на '{category_title}' израсходована ({int(spent_percentage)}%). Будьте внимательны!"
                send_push_notification(budget.user, "Бюджет", message)
            elif 74 < spent_percentage < 76:
                title = "Percentage spent for budget"
                message = f"Вы потратили 75% бюджета на '{category_title}'. Осталось немного!"
                send_push_notification(budget.user, "Бюджет", message)
            elif 89 < spent_percentage < 91:
                title = "Percentage spent for budget"
                message = f"Почти весь бюджет на '{category_title}' израсходован ({int(spent_percentage)}%)."
                send_push_notification(budget.user, "Бюджет", message)

            # Дополнительные проверки с учетом времени и оставшейся суммы
            days_left = (budget.period.replace(day=1, month=budget.period.month + 1) - now.date()).days
            remaining_amount = budget.limit - budget.spent

            if days_left <= 7 and remaining_amount <= 1000 and spent_percentage > 70:
                title = "Remaining spent for budget"
                message = f"Внимание! До конца месяца осталась неделя, а по бюджету '{budget.category}' осталось всего {remaining_amount}C."
                send_push_notification(budget.user, "Бюджет", message)

            if message != "" and title != "":
                NotificationModel.objects.create(
                    title=title,
                    description=message,
                    user=budget.user,
                )


@shared_task
def check_goal_notifications():
    for goal in GoalModel.objects.all():
        progress_percentage = (goal.current / goal.goal) * 100 if goal.goal else 0
        remaining_goal = goal.goal - goal.current
        message = ""
        title = ""

        if 74 < progress_percentage < 76:
            title = "Percentage spent for budget"
            message = f"Уже 75% цели '{goal.title}' достигнуто! Отлично!"
            send_push_notification(goal.user, "Цель", message)
        elif remaining_goal <= 5000 and progress_percentage < 100:
            title = "Percentage spent for budget"
            message = (
                f"Вы почти достигли цели '{goal.title}'. Осталось всего {remaining_goal}C — продолжайте в том же духе!"
            )
            send_push_notification(goal.user, "Цель", message)
        elif progress_percentage >= 99 and progress_percentage < 100:
            title = "Percentage spent for budget"
            message = f"Последний рывок! Цель '{goal.title}' почти достигнута!"
            send_push_notification(goal.user, "Цель", message)

        # Дополнительные проверки с учетом времени
        days_left = (goal.period - timezone.now().date()).days
        if days_left <= 7 and progress_percentage < 90:
            title = "Remaining spent for budget"
            message = f"До конца срока цели '{goal.title}' осталась неделя. Успеете?"
            send_push_notification(goal.user, "Цель", message)

        if message != "" and title != "":
            NotificationModel.objects.create(
                title=title,
                description=message,
                user=goal.user,
            )


@shared_task
def periodic_notifications():
    check_budget_notifications.delay()
    # check_goal_notifications.delay()
