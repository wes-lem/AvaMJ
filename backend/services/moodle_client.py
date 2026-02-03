"""
Funções que falam com a API do Moodle (cursos, usuários, notas).
Usa a mesma lógica do backend/teste_moodle.py.
"""
import logging
from typing import Any

import requests

from backend.config import settings

logger = logging.getLogger(__name__)

_BASE = f"{settings.MOODLE_URL}/webservice/rest/server.php"


def _chamar(funcao: str, params: dict[str, Any] | None = None) -> Any:
    """Chama uma função da API REST do Moodle."""
    if params is None:
        params = {}
    payload = {
        "wstoken": settings.MOODLE_TOKEN,
        "wsfunction": funcao,
        "moodlewsrestformat": "json",
    }
    payload.update(params)
    try:
        r = requests.post(_BASE, data=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, dict) and "exception" in data:
            logger.warning("Moodle API exception: %s", data.get("message"))
            return None
        return data
    except requests.RequestException as e:
        logger.exception("Erro ao chamar Moodle: %s", e)
        return None


def get_site_info() -> dict | None:
    """Informações do site (teste de conexão)."""
    return _chamar("core_webservice_get_site_info")


def get_courses() -> list[dict]:
    """Lista todos os cursos (exclui o curso 'Site' id 1)."""
    data = _chamar("core_course_get_courses")
    if not isinstance(data, list):
        return []
    return [c for c in data if c.get("id") != 1]


def get_course_users(course_id: int) -> list[dict]:
    """Lista usuários inscritos em um curso (alunos, professores, etc.)."""
    data = _chamar("core_enrol_get_enrolled_users", {"courseid": course_id})
    if not isinstance(data, list):
        return []
    return data


def get_grades(course_id: int, user_ids: list[int] | None = None) -> dict | None:
    """
    Notas de um curso. Se user_ids for passado, restringe a esses usuários.
    Retorno: estrutura do Moodle (grades -> items -> grades por usuário).
    """
    params: dict[str, Any] = {"courseid": course_id}
    if user_ids:
        for i, uid in enumerate(user_ids):
            params[f"userids[{i}]"] = uid
    return _chamar("core_grades_get_grades", params)


def get_grades_flat(course_id: int, user_ids: list[int] | None = None) -> list[dict]:
    """
    Retorna lista simples de notas: [{"user_id": moodle_id, "itemname": str, "grade": float, "grademax": float}, ...].
    user_id aqui é o ID do Moodle (para cruzar com User.moodle_id depois).
    """
    raw = get_grades(course_id, user_ids)
    if not raw or "grades" not in raw:
        return []

    out = []
    for item in raw.get("grades", []):
        itemname = item.get("itemname") or item.get("itemtype", "")
        for grade_info in item.get("grades", []):
            userid = grade_info.get("userid")
            if userid is None:
                continue
            grade = grade_info.get("grade")
            grademax = grade_info.get("grademax") or 100
            if grade is None:
                continue
            try:
                grade_f = float(grade)
            except (TypeError, ValueError):
                continue
            out.append({
                "user_id": userid,
                "itemname": itemname,
                "grade": grade_f,
                "grademax": float(grademax),
            })
    return out


def sync_grades_from_moodle() -> None:
    """
    Sincroniza usuários e notas do Moodle para o banco local.
    - Cria/atualiza User a partir dos inscritos nos cursos.
    - Insere notas em GradeHistory (por curso e item de nota).
    """
    from backend.database import SessionLocal
    from backend.models.user import User
    from backend.models.analytics import GradeHistory

    db = SessionLocal()
    try:
        courses = get_courses()
        for course in courses:
            cid = course.get("id")
            cname = course.get("fullname", "")
            if not cid:
                continue
            users = get_course_users(cid)
            moodle_user_ids = []
            for u in users:
                moodle_id = u.get("id")
                if not moodle_id:
                    continue
                moodle_user_ids.append(moodle_id)
                # Cria ou atualiza usuário local
                local = db.query(User).filter(User.moodle_id == moodle_id).first()
                if not local:
                    local = User(
                        moodle_id=moodle_id,
                        email=u.get("email") or f"moodle_{moodle_id}@local",
                        full_name=u.get("fullname") or f"User {moodle_id}",
                    )
                    db.add(local)
                    db.flush()
                # nada a atualizar por enquanto (nome/email podem ser atualizados se quiser)

            if not moodle_user_ids:
                continue

            grades_flat = get_grades_flat(cid, moodle_user_ids)
            for g in grades_flat:
                moodle_uid = g["user_id"]
                local_user = db.query(User).filter(User.moodle_id == moodle_uid).first()
                if not local_user:
                    continue
                # Evita duplicata: mesmo user, course, activity e valor (ou usa recorded_at mais recente)
                existing = (
                    db.query(GradeHistory)
                    .filter(
                        GradeHistory.user_id == local_user.id,
                        GradeHistory.course_id == cid,
                        GradeHistory.activity_name == g["itemname"],
                    )
                    .order_by(GradeHistory.recorded_at.desc())
                    .first()
                )
                if existing and existing.grade == g["grade"]:
                    continue
                db.add(
                    GradeHistory(
                        user_id=local_user.id,
                        course_id=cid,
                        activity_name=g["itemname"],
                        grade=g["grade"],
                        max_grade=g["grademax"],
                    )
                )
        db.commit()
        logger.info("Sincronização Moodle concluída: %s cursos", len(courses))
    except Exception as e:
        db.rollback()
        logger.exception("Erro na sincronização Moodle: %s", e)
    finally:
        db.close()
