import unittest
from urllib import parse

import urltrim


class UrlTrimTests(unittest.TestCase):
    def test_strip_www(self):
        url = "https://www.something.com/a/b?c=d"
        expected = "https://something.com/a/b?c=d"

        parsed = parse.urlparse(url)
        stripped = urltrim.strip_www(parsed).geturl()
        self.assertEqual(stripped, expected)

        parsed = parse.urlparse(stripped)
        stripped = urltrim.strip_www(parsed).geturl()
        self.assertEqual(stripped, expected)

    def test_strip_query(self):
        url = "http://www.something.com/a/b?c=d"
        expected = "http://www.something.com/a/b"

        parsed = parse.urlparse(url)
        stripped = urltrim.strip_query(parsed).geturl()
        self.assertEqual(stripped, expected)

        parsed = parse.urlparse(url)
        stripped = urltrim.strip_query(parsed).geturl()
        self.assertEqual(stripped, expected)

    def test_force_https(self):
        url = "http://www.something.com/a/b?c=d"
        expected = "https://www.something.com/a/b?c=d"

        parsed = parse.urlparse(url)
        forced = urltrim.force_https(parsed).geturl()
        self.assertEqual(forced, expected)

        parsed = parse.urlparse(url)
        forced = urltrim.force_https(parsed).geturl()
        self.assertEqual(forced, expected)

    def test_youtube(self):
        vid = "raZkWL2mndY"
        urls = [
            "http://www.youtube.com/watch?v=%s&feature=youtu.be&t=4" % vid,
            "http://youtube.com/watch?v=%s&feature=youtu.be&t=4" % vid,
            "http://youtu.be/%s?t=4" % vid,
            "http://www.youtu.be/%s?t=4" % vid]
        expected = "https://youtube.com/watch?v=%s" % vid

        for url in urls:
            self.assertEqual(urltrim.trim_url(url), expected)

    def test_reddit(self):
        urls = [
            "https://www.reddit.com/r/soccer/comments/4iriov/postmatch_thread_west_ham_united_3_2_manchester/d30hlop?context=10000",
            "https://www.reddit.com/r/soccer/comments/4iriov/postmatch_thread_west_ham_united_3_2_manchester/d30hlop",
            "http://www.reddit.com/r/soccer/comments/4iriov/postmatch_thread_west_ham_united_3_2_manchester/d30hlop?context=10000",
            "http://www.reddit.com/r/soccer/comments/4iriov/postmatch_thread_west_ham_united_3_2_manchester/d30hlop",
            "https://reddit.com/r/soccer/comments/4iriov/postmatch_thread_west_ham_united_3_2_manchester/d30hlop?context=10000",
            "https://reddit.com/r/soccer/comments/4iriov/postmatch_thread_west_ham_united_3_2_manchester/d30hlop",
            "http://reddit.com/r/soccer/comments/4iriov/postmatch_thread_west_ham_united_3_2_manchester/d30hlop?context=10000",
            "http://reddit.com/r/soccer/comments/4iriov/postmatch_thread_west_ham_united_3_2_manchester/d30hlop",
        ]
        expected = "https://reddit.com/r/soccer/comments/4iriov/postmatch_thread_west_ham_united_3_2_manchester/d30hlop"

        for url in urls:
            self.assertEqual(urltrim.trim_url(url), expected)

    def test_aftonbladet(self):
        url = "http://www.aftonbladet.se/nyheter/article12345.ab?asdfasdf=asdf"
        expected = "http://www.aftonbladet.se/nyheter/article12345.ab"
        self.assertEqual(urltrim.trim_url(url), expected)

    def test_twitter(self):
        url = "http://twitter.com/CIA/status/726824007220125696?a=b"
        expected = "https://twitter.com/CIA/status/726824007220125696"
        self.assertEqual(urltrim.trim_url(url), expected)

    def test_i_imgur(self):
        urls = [
            "http://i.imgur.com/53gPJHj.png",
            "http://i.imgur.com/53gPJHj.png?a=b",
            "https://i.imgur.com/53gPJHj.png",
            "https://i.imgur.com/53gPJHj.jpg",
            "https://i.imgur.com/53gPJHj.gif",
        ]
        expected = "http://imgur.com/53gPJHj"

        for url in urls:
            self.assertEqual(urltrim.trim_url(url), expected)

    def test_imgur(self):
        url = "http://www.imgur.com/abc123?a=b"
        expected = "http://imgur.com/abc123"
        self.assertEqual(urltrim.trim_url(url), expected)

if __name__ == '__main__':
    unittest.main()
