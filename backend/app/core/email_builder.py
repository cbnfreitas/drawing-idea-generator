from ..core import route_paths, s
from ..core.jinja_env import jinja_env
from ..models import UserModel
from ..services import sendgrid_service


def send_reset_password_email(
        user: UserModel, token: str
) -> None:

    link = f"{s.SERVER_HOST}{route_paths.ROUTE_AUTH_PASSWORD_RESET}?token={token}"

    subject = f"{s.PROJECT_NAME} - Recupere a sua senha"
    html_template = jinja_env.get_template('reset_password.html')
    html = html_template.render(project_name=s.PROJECT_NAME,
                                email=user.email,
                                link=link)

    sendgrid_service.send_email(
        to=user.email, subject=subject, html=html)


def send_activation_email(
        user: UserModel, token: str
) -> None:

    link = f"{s.SERVER_HOST}{route_paths.FRONT_AUTH_ACTIVATION}/{token}"

    if s.SEND_GRID_API_KEY:
        subject = f"{s.PROJECT_NAME} - Ative a sua conta"
        html_template = jinja_env.get_template('user_activation.html')
        html = html_template.render(project_name=s.PROJECT_NAME,
                                    email=user.email,
                                    full_name=user.full_name,
                                    link=link)
        sendgrid_service.send_email(
            to=user.email, subject=subject, html=html)
    else:
        print(link)
