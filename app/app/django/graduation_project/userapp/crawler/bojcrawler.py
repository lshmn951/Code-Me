from typing import Dict, List, Set, Union, Optional
from . import basecrawler

USER_AGENT = {
    "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/76.0.3809.132 Safari/537.36"
}
URL_BASE = "https://www.acmicpc.net"
URL_RANKLIST_PREFIX = URL_BASE + "/ranklist/"
URL_USER_PREFIX = URL_BASE + "/user/"
URL_PROBLEM_PREFIX = URL_BASE + "/problem/"
URL_PROBLEM_STATUS_PREFIX = URL_PROBLEM_PREFIX + "status/"
URL_ALGORITHM_TAG_PREFIX = URL_PROBLEM_PREFIX + "tag/"
URL_ALGORITHM_TAG_LIST = URL_PROBLEM_PREFIX + "tags"
KEY_NAME = {
    "제출": "submit",
    "제출한 사람": "submit_people",
    "맞은 사람": "accept_people",
    "평균 시도": "average_attempt",
    "맞았습니다": "accept",
    "틀렸습니다": "wrong",
    "시간 초과": "time_over",
    "메모리 초과": "memory_over",
    "출력 초과": "output_over",
    "출력 형식": "output_type_error",
    "런타임 에러": "runtime_error",
    "컴파일 에러": "compile_error",
    "정답 비율": "accept_proportion",
    "정답자 비율": "accept_people_proportion",
}


def get_rank_list_page_max(rheader: Optional[Dict[str, str]] = None) -> int:
    rheader = rheader or USER_AGENT
    bs = basecrawler.get_bs_from_url(URL_RANKLIST_PREFIX + "1", rheader)
    return int(bs.select(".pagination a")[-1]["href"][10:])


def get_user_list(rheader: Optional[Dict[str, str]] = None) -> Set[str]:
    """
    함수 이름은 list이지만 크롤링과 실제 데이터의 중복 제거를 고려해 set 구조
    """
    rheader = rheader or USER_AGENT
    user_set = set()

    for i in range(1, get_rank_list_page_max(rheader) + 1):
        user_set |= set(get_user_list_by_page(i, rheader))

    return user_set


def get_user_list_by_page(pagenum: int, rheader: Optional[Dict[str, str]] = None) -> List[str]:
    rheader = rheader or USER_AGENT
    bs = basecrawler.get_bs_from_url(URL_RANKLIST_PREFIX + str(pagenum), rheader)
    return [tr.select_one("a").text for tr in bs.select("#ranklist > tbody > tr")]


def get_solved_list_by_user(uid: str, rheader: Optional[Dict[str, str]] = None) -> List[int]:
    rheader = rheader or USER_AGENT
    bs = basecrawler.get_bs_from_url(URL_USER_PREFIX + uid, rheader)

    if bs is not None:
        solved_list = bs.select(".panel-body")[0].select(".problem_number")
        return [int(solve.text) for solve in solved_list]
    else:
        return None


def get_failed_list_by_user(uid: str, rheader: Optional[Dict[str, str]] = None) -> List[int]:
    rheader = rheader or USER_AGENT
    bs = basecrawler.get_bs_from_url(URL_USER_PREFIX + uid, rheader)

    if bs is not None:
        failed_list = bs.select(".panel-body")[1].select(".problem_number")
        return [int(fail.text) for fail in failed_list]
    else:
        return None


def get_algorithm_tag_list(rheader: Optional[Dict[str, str]] = None) -> List[str]:
    rheader = rheader or USER_AGENT
    bs = basecrawler.get_bs_from_url(URL_ALGORITHM_TAG_LIST, rheader)
    tr_list = bs.select("tbody > tr")
    return [tr.select_one("td").text for tr in tr_list]


def get_problem_statics(pid: int, eng: bool = True, rheader: Optional[Dict[str, str]] = None) -> Dict[
    str, Union[int, float]]:
    rheader = rheader or USER_AGENT
    bs_pr = basecrawler.get_bs_from_url(URL_PROBLEM_PREFIX + str(pid), rheader)
    problem = {
        "number" if eng else "문제 번호": pid,
        "name" if eng else "문제 이름": bs_pr.select_one("#problem_title").text,
    }

    bs_st = basecrawler.get_bs_from_url(URL_PROBLEM_STATUS_PREFIX + str(pid), rheader)
    col_list = bs_st.select("#statics > tbody > tr")

    for col in col_list:
        key = col.select_one("th").text

        if key == "채점 불가":
            break

        value = col.select_one("td").text

        problem[KEY_NAME[key] if eng else key] = \
            float(value[:-1]) if key == "정답 비율" \
                else (
                float(value) if key in ("평균 시도", "정답자 비율")
                else int(value)
            )

    for keyname in KEY_NAME:
        pkey = KEY_NAME[keyname] if eng else keyname

        if pkey not in problem:
            problem[pkey] = 0

    apkey = KEY_NAME["정답자 비율"] if eng else "정답자 비율"

    problem[apkey] = \
        0.0 if problem[apkey] == 0 else \
        problem[KEY_NAME["맞은 사람"] if eng else "맞은 사람"] / \
        problem[KEY_NAME["제출한 사람"] if eng else "제출한 사람"]

    problem["algorithm_id_id"] = 1

    return problem
