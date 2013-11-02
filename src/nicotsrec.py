# -*- coding: utf-8 -*-

import re
import sys
import requests
import subprocess
from pit import Pit
from xml.etree import ElementTree


class NicoVideoSession(object):
    def __init__(self, mailaddr, password):
        self.session = requests.session()
        self.login(mailaddr, password)

    def login(self, mailaddr, password):
        login_url = 'https://secure.nicovideo.jp/secure/login?site=niconico'

        r = self.session.post(login_url, {'mail_tel': mailaddr, 'password': password})
        if r.headers['x-niconico-authflag'] != '0' and r.headers['x-niconico-id']:
            return True
        else:
            raise RuntimeError("Login failed")

    def get_player_status(self, video_id):
        url = 'http://watch.live.nicovideo.jp/api/getplayerstatus?v=' + video_id
        r = self.session.get(url)
        assert r.status_code == 200
        return ElementTree.fromstring(r.text.encode('utf-8'))


def main(args=sys.argv[1:]):
    if len(args) != 1:
        print "Usage: nicotsrec [nicolive_url]"
        sys.exit(-1)

    video_id = re.sub('^.*/(lv\d+).*$', '\\1', args[0])

    identifier = Pit.get('nicovideo',
                         {'require': {'mail': 'input your mail address',
                                      'password': 'your password'}})
    session = NicoVideoSession(identifier['mail'], identifier['password'])
    status = session.get_player_status(video_id)

    title = status.find('./stream/title').text
    rtmp_url = status.find('./rtmp/url').text
    ticket = status.find('./rtmp/ticket').text

    quesheet = status.findall('.//quesheet/que')
    publish_ques = [que.text for que in quesheet if que.text.startswith('/publish')]
    que_urls = [re.sub('^.*(rtmp://\S+).*$', '\\1', que) for que in publish_ques]

    for i, que_url in enumerate(que_urls):
        filename = "%s_%02d.flv" % (title, i)
        cmd = ['rtmpdump', '-o', filename, '-r', rtmp_url,
               '-C', 'S:"%s"' % ticket, '-N', que_url, '-v']
        print('Execute: %s' % cmd)
        subprocess.call(cmd)
