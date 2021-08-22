import time
from helpers.utils import Setup, WebHandler
from operator import truth
from num2words import num2words
browsers = {1: "brave", 2: "librewolf", 3: "firefox", 4: 'firefox_developer'}
sites = {1: "animekisa", 2: "4anime", 3: "9anime", 4: "yugenanime", 5: "crunchyroll", 6: 'shiro'}
# Browser Tests
brave = Setup(query="hige", browser=browsers[1], website=sites[1], goto_episode="7", dubbed=False, login=False,
              payload=None, debug=True)
firefox_dev = Setup(query="boku", browser=browsers[4], website=sites[1], goto_episode="1", dubbed=False, login=False,
                    payload=None, debug=True)
firefox = Setup(query="erased", browser=browsers[3], website=sites[1], goto_episode="3", dubbed=False,
                login=False, payload=None, debug=True)
librewolf = Setup(query="spice and wolf", browser=browsers[2], website=sites[1], goto_episode="3", dubbed=False,
                  login=False, payload=None, debug=True)

# Query Tests
normal_setup = Setup(query="redo", browser=browsers[1], website=sites[1], goto_episode="4", dubbed=False, login=False,
                     payload=None, debug=True)
# with_login = Setup(query="rising of", browser=browsers[2], website=sites[3], goto_episode="8" ,dubbed=False,
# login=True,payload=["sad","fag"])
with_one_letter = Setup(query="e", browser=browsers[2], website=sites[3], goto_episode="6", dubbed=False, login=False,
                        payload=None, debug=True)
with_big_anime = Setup(query="hunter", browser=browsers[2], website=sites[3], goto_episode="3", dubbed=False,
                       login=False, payload=None, debug=True)
with_multiseries_anime = Setup(query="boku no hero academia", browser=browsers[2], website=sites[3], goto_episode="7",
                               dubbed=False, login=False, payload=None, debug=True)
with_invalid_episode = Setup(query="mugen train", browser=browsers[2], website=sites[3], goto_episode="penis",
                             dubbed=False, login=False, payload=None, debug=True)

# Website Tests
_4anime = Setup(query="boku", browser=browsers[2], website=sites[2], goto_episode="0", dubbed=True, login=False,
                payload=None, debug=True)
_AK = Setup(query="somali", browser=browsers[3], website=sites[1], goto_episode="7", dubbed=True, login=False,
            payload=None, debug=True)
_CR = Setup(query="kemono", browser=browsers[3], website=sites[5], goto_episode="8", dubbed=True, login=False,
            payload=None, debug=True)
_9anime = Setup(query="boku no hero academia 5", browser=browsers[4], website=sites[3], goto_episode="6", dubbed=True,
                login=False, payload=None, debug=True)
_Shiro = Setup(query="saiki", browser=browsers[2], website=sites[6], goto_episode="5", dubbed=True, login=False,
               payload=None, debug=True)
_Yugen = Setup(query="spice and wolf", browser=browsers[3], website=sites[4], goto_episode="2", dubbed=True, login=False,
               payload=None, debug=True)

# Test Collections
browser_tests = (brave, firefox_dev, librewolf)
query_tests = (normal_setup, with_big_anime, with_one_letter, with_multiseries_anime)
site_tests = (_4anime, _AK, _CR, _9anime, _Shiro, _Yugen)
exception = False


class WebTest:
    def __init__(self):
        pass

    def __call__(self, setup):
        try:
            handler = WebHandler()
            funcs = handler(setup)
            for i in range(1,len(funcs)):
                assert(truth(i))
            return funcs
        except AssertionError:
            global exception
            exception = True
            print(f"Crawl test failed at {num2words(i,to='ordinal')} test")
    

def run():
    t1 = time.time()
    test = WebTest()
    lists = test(_Yugen)
    t2 = time.time()
    dt = t2 - t1
    print("---ALL OK---") if not exception else None
    print(f"Completed {len(lists)} "
        f"test(s) in {dt} seconds")
