from crawler import bojcrawler

USER_AGENT = {
    "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/76.0.3809.132 Safari/537.36"
}

page_max = bojcrawler.get_rank_list_page_max(USER_AGENT)

for page in range(1, page_max + 1 ):
    for uid in bojcrawler.get_user_list_by_page(page, USER_AGENT):
        bojcrawler.get_accept_list_by_user(uid, USER_AGENT)
