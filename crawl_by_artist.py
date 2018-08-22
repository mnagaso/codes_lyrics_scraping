import os


#init_urls = ["http://gakufu.gakki.me/search/?mode=list&word=AT:%88%E4%8F%E3%97z%90%85"] # 井上陽水
init_urls = ["http://gakufu.gakki.me/search/?mode=list&word=AT:aiko",
            "http://gakufu.gakki.me/search/?mode=list&word=AT:%8F%BC%93c%90%B9%8Eq",
            "http://gakufu.gakki.me/search/?mode=list&word=AT:%89%AA%91%BA%96%F5%8DK",
            "http://gakufu.gakki.me/search/?mode=list&word=AT:%92%C5%96%BC%97%D1%8C%E7",
            "http://gakufu.gakki.me/search/?mode=list&word=AT:Mr.Children"]
out_fnames = ["aiko","seiko_matsuda","yasuyuki_okamura","ringo_shina","mr_children"]

for i, a_url in enumerate(init_urls):
    json_fname = '{}.json'.format(out_fnames[i])
    cmdstr = "scrapy crawl get_codes_lyrics -a init_url=\"" + str(a_url) + "\" -o " + json_fname
    os.system(cmdstr)

